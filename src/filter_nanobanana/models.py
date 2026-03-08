from typing import Literal, Optional

from pydantic import BaseModel, Field


class StylePrompt(BaseModel):
    style_name: str = Field(
        description="The name for this AI filter style.",
    )
    prompt: str = Field(
        description="Prompt template to guide the AI generation process for this style.",
    )
    enabled: bool = Field(
        description="Enable this style prompt.",
        default=True,
    )
    model: Optional[Literal[None, "gemini-2.5-flash-image", "gemini-3-pro-image-preview", "gemini-3.1-flash-image-preview"]] = Field(
        default=None,
        description="Google Gemini model to use for this specific style. If not set, will use the default model from connection settings.",
    )