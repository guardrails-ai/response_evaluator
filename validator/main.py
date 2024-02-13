from typing import Any, Callable, Dict, Optional
from warnings import warn

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)
from litellm import completion


@register_validator(name="guardrails/self_reflect_validator", data_type="string")
class SelfReflectValidator(Validator):
    """Validates an LLM-generated output by re-prompting an LLM to self-reflect.

    **Key Properties**

    | Property                      | Description                          |
    | ----------------------------- | ------------------------------------ |
    | Name for `format` attribute   | `guardrails/self_reflect_validator`  |
    | Supported data types          | `string`                             |
    | Programmatic fix              | N/A                                  |

    Args:
        on_fail (Callable, optional): A function to call when validation fails.
            Defaults to None.
    """

    def __init__(
        self,
        llm_callable: str = "gpt-3.5-turbo",  # str for litellm model name
        on_fail: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(on_fail, llm_callable=llm_callable, **kwargs)
        self.llm_callable = llm_callable

    def get_validation_prompt(self, value: str, question: str) -> str:
        """Generates the prompt to send to the LLM.

        Args:
            value (str): The value to validate.
            question (str): The question to ask the LLM.

        Returns:
            prompt (str): The prompt to send to the LLM.
        """
        prompt = f"""
        As an oracle of truth and logic, your task is to evaluate an LLM-generated response by answering a simple rhetorical question based on the context of that response.
        You have been provided with the 'LLM Response' and a 'Question', and you need to generate 'Your Answer'.
        Please answer the question with just a 'Yes' or a 'No'. If you're unsure, say 'Unsure'. Any other text is forbidden.
        You'll be evaluated based on how well you understand the question and how well you follow the instructions to answer the question.

        LLM Response:
        {value}

        Question:
        {question}

        Your Answer:

        """
        return prompt

    def get_llm_response(self, prompt: str) -> str:
        """Gets the response from the LLM.

        Args:
            prompt (str): The prompt to send to the LLM.

        Returns:
            str: The response from the LLM.
        """
        # 0. Create messages
        messages = [{"content": prompt, "role": "user"}]

        # 1. Get LLM response
        try:
            response = completion(model=self.llm_callable, messages=messages)
            response = response.choices[0].message.content  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Error getting response from the LLM: {e}") from e

        # 2. Strip the response of any leading/trailing whitespaces
        # and convert to lowercase
        response = response.strip().lower()
        # 3. Return the response
        return response

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        """Validation method for the SelfReflectValidator.


        Args:
            value (Any): The value to validate.
            metadata (Dict): The metadata for the validation.

        Returns:
            ValidationResult: The result of the validation.
        """
        # 1. Get the question and arg from the metadata
        validation_question = metadata.get("validation_question")
        if validation_question is None:
            raise RuntimeError(
                "'validation_question' missing from metadata. "
                "Please provide a question to prompt the LLM."
            )

        pass_on_unsure = metadata.get(
            "pass_on_unsure", False
        )  # Default behavior: Fail on 'Unsure'

        # 2. Setup the prompt
        prompt = self.get_validation_prompt(value, validation_question)

        # 3. Get the LLM response
        llm_response = self.get_llm_response(prompt)

        if llm_response == "no":
            return FailResult(error_message="The LLM says 'No'. The validation failed.")

        if llm_response == "yes":
            return PassResult()

        if llm_response == "unsure":
            if pass_on_unsure:
                warn("The LLM is unsure about the answer. Passing the validation...")
                return PassResult()

            warn("The LLM is unsure about the answer. Failing the validation...")
            return FailResult(error_message="The LLM is unsure about the answer.")

        # Else
        warn("The LLM generated an invalid response. Passing the validation...")
        return PassResult()
