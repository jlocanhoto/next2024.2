"""Define the JSON Schema for API objects."""

import pydantic
import pydantic.alias_generators


class JsonSchema(pydantic.BaseModel):
    """Setup a Pydantic BaseModel to automatically format Python objects into JSON format."""

    model_config = pydantic.ConfigDict(
        alias_generator=pydantic.alias_generators.to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
