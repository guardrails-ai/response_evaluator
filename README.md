## Overview

| Developed by | Guardrails AI |
| --- | --- |
| Date of development | Feb 15, 2024 |
| Validator type | Format |
| Blog |  |
| License | Apache 2 |
| Input/Output | Output |

## Description

This validator evaluates an LLM-generated text by prompting another LLM.

## Installation

```bash
$ guardrails hub install hub://guardrails/response-evaluator
```

## Usage Examples

### Validating string output via Python

In this example, we use the `response-evaluator` validator on any LLM generated text.

```python
# Import Guard and Validator
from guardrails.hub import ResponseEvaluator
from guardrails import Guard

# Initialize Validator
val = ResponseEvaluator()

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
### Validating JSON output via Python

In this example, we use the `response-evaluator` validator on a pet description string.

```python
# Import Guard and Validator
from pydantic import BaseModel
from guardrails.hub import ResponseEvaluator
from guardrails import Guard

val = ResponseEvaluator()

# Create Pydantic BaseModel
class PetInfo(BaseModel):
    pet_description: str = Field(validators=[val])

# Create a Guard to check for valid Pydantic output
guard = Guard.from_pydantic(output_class=PetInfo)

# Run LLM output generating JSON through guard
guard.parse(
    """
    {
        "pet_description": "Caesar is a great dog",
    }
    """,
    metadata={
        "validation_question": "Is Caesar a great dog?",
    }
)  # Pass

guard.parse(
    """
    {
        "pet_description": "Caesar is a great cat",
    }
    """,
    metadata={
        "validation_question": "Is Caesar a great dog?",
    }
)  # Fail
```


## API Reference

`__init__`

- `on_fail`: The policy to enact when a validator fails.
