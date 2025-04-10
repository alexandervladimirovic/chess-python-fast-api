from pydantic import BaseModel, ConfigDict


class ChessBaseSchema(BaseModel):
    """Basic data schema for models.

    Inherits from Pydantic BaseModel and provides
    settings for data serialization and validation, as well config for working with
    types.

    Config:
        - `arbitrary_types_allowed': Allows use arbitrary data types in models.
        - `hide_input_in_errors': Hides input values in error messages.
        - `strict`: Enables strict typing.
        - `str_strip_whitespace': Removes spaces at begin and end string.
        - `validate_assignment': Enables data validation when changing model fields.
        - `validate_default': enables validation of default values during model
        initialization.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        hide_input_in_errors=True,
        strict=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        validate_default=True,
    )
