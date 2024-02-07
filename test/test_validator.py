from guardrails import Guard
from pydantic import BaseModel, Field
from validator import GenericPromptValidator
import pytest


# Create a pydantic model with a field that uses the custom validator
class ValidatorTestObject(BaseModel):
    text: str = Field(validators=[GenericPromptValidator(on_fail="exception")])


# Test happy path
@pytest.mark.parametrize(
    "value, metadata",
    [
        (
            """
            {
                "text": "The capital of France is Paris."
            }
            """,
            {
                "validation_question": "Is Paris the capital of France?",
                "pass_on_unsure": "True",
            },
        ),
        (
            """
            {
                "text": "Greg scored 12 points in the basketball game."
            }
            """,
            {
                "validation_question": "Did Greg score 12 points in the basketball game?",
                "pass_on_unsure": "True",
            },
        ),
    ],
)
def test_happy_path(value, metadata):
    """Test happy path."""
    guard = Guard.from_pydantic(output_class=ValidatorTestObject)
    response = guard.parse(value, metadata=metadata)
    print("Happy path response", response)
    assert response.validation_passed is True


# Test fail path
@pytest.mark.parametrize(
    "value, metadata",
    [
        (
            """
            {
                "text": "The capital of France is Berlin."
            }
            """,
            {
                "validation_question": "Is Paris the capital of France?",
            },
        ),
        (
            """
            {
                "text": "Greg scored 12 points in the basketball game."
            }
            """,
            "Did Greg score 100 points in the basketball game?",
        ),
    ],
)
def test_fail_path(value, metadata):
    """Test fail path."""
    guard = Guard.from_pydantic(output_class=ValidatorTestObject)
    with pytest.raises(Exception):
        response = guard.parse(
            value,
            metadata=metadata,
        )
        print("Fail path response", response)
