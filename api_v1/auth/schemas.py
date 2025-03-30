from pydantic import BaseModel


class TokenSchemas(BaseModel):
    """Schema for representing a token response."""

    token: str
    token_type: str
