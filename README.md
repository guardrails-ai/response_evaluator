## Overview

| Developed by | Guardrails AI |
| --- | --- |
| Date of development | Feb 15, 2024 |
| Validator type | Format |
| Blog |  |
| License | Apache 2 |
| Input/Output | Output |

## Description

This validator validates an LLM response based on a question provided by the user.

## Requirements
- Dependencies:
    - LiteLLM

## Installation

```bash
$ guardrails hub install hub://guardrails/response_evaluator
```

## Usage Examples

### Validating string output via Python

In this example, we use the `response_evaluator` validator on any LLM generated text.

```python
# Import Guard and Validator
from guardrails.hub import ResponseEvaluator
from guardrails import Guard

# Initialize Validator
val = ResponseEvaluator(llm_callable="gpt-3.5-turbo")

# Setup Guard
guard = Guard.from_string(
    validators=[val, ...],
)

# Pass LLM output through guard
guard.parse(
    "The capital of France is Paris", 
    metadata={
        "validation_question": "Is Paris the capital of France?", 
        "pass_on_unsure"=True
    }
)  # Pass

guard.parse(
    "The capital of France is London", 
    metadata={
        "validation_question": "Is Paris the capital of France?", 
    }
)  # Fail

```

## API Reference

**`__init__(self, llm_callable="gpt-3.5-turbo", on_fail="noop")`**
<ul>

Initializes a new instance of the Validator class.

**Parameters:**

- **`llm_callable`** *(str):* The string name for the model used with LiteLLM. More info about available options [here](https://docs.litellm.ai/docs/completion/input)
- **`on_fail`** *(str, Callable):* The policy to enact when a validator fails. If `str`, must be one of `reask`, `fix`, `filter`, `refrain`, `noop`, `exception` or `fix_reask`. Otherwise, must be a function that is called when the validator fails.

</ul>

<br>

**`__call__(self, value, metadata={}) → ValidationOutcome`**

<ul>

Validates the given `value` using the rules defined in this validator, relying on the `metadata` provided to customize the validation process. This method is automatically invoked by `guard.parse(...)`, ensuring the validation logic is applied to the input data.

Note:

1. This method should not be called directly by the user. Instead, invoke `guard.parse(...)` where this method will be called internally for each associated Validator.
2. When invoking `guard.parse(...)`, ensure to pass the appropriate `metadata` dictionary that includes keys and values required by this validator. If `guard` is associated with multiple validators, combine all necessary metadata into a single dictionary.

**Parameters:**

- **`value`** *(Any):* The input value to validate.
- **`metadata`** *(dict):* A dictionary containing metadata required for validation. Keys and values must match the expectations of this validator.
    
    
    | Key | Type | Description | Default | Required |
    | --- | --- | --- | --- | --- |
    | `validation_question` | String | The question to ask the LLM | N/A | Yes |

</ul>
