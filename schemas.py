from pydantic import BaseModel, ConfigDict


class ChessBaseSchema(BaseModel):
    """Basic data schema for models.

    Inherits from Pydantic BaseModel and provides
    settings for data serialization and validation, as well config for working with
    types.

    Config:
        - `str_strip_whitespace': Removes spaces at begin and end string.
        - `validate_assignment': Enables data validation when changing model fields.
        - `arbitrary_types_allowed': Allows use arbitrary data types in models.
        - `validate_default': enables validation of default values during model
        initialization.
        - `hide_input_in_errors': Hides input values in error messages.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        validate_default=True,
        hide_input_in_errors=True,
    )
