from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from photobooth import CONFIG_PATH
from photobooth.services.config.baseconfig import BaseConfig

from .models import StylePrompt


class ConnectionSettings(BaseModel):
    gemini_api_key: str = Field(
        default="",
        description="Google Gemini API key for AI image processing. Obtain from https://aistudio.google.com/app/apikey",
    )

    default_model: Literal["gemini-2.5-flash-image", "gemini-3-pro-image-preview", "gemini-3.1-flash-image-preview"] = Field(
        default="gemini-2.5-flash-image",
        description="Default Google Gemini model to use for image generation when no model is specified in style prompts. gemini-2.5-flash-image for speed, gemini-3-pro-image-preview for quality.",
    )

    timeout_seconds: int = Field(
        default=120,
        ge=5,
        le=300,
        description="Timeout for AI API calls in seconds.",
    )


class ImageGenerationSettings(BaseModel):
    input_image_format: Literal["jpeg", "png", "webp"] = Field(
        default="jpeg",
        description="Format to convert input images to before sending to Gemini API.",
    )

    aspect_ratio: Literal["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"] = Field(
        default="1:1",
        description="Aspect ratio for generated images.",
    )

    image_size: Literal["1K", "2K", "4K"] = Field(
        default="1K",
        description="Resolution for generated images. Only available for gemini-3-pro-image-preview model.",
    )

    response_modalities: list[Literal["TEXT", "IMAGE"]] = Field(
        default=["IMAGE"],
        description="Response modalities - can include TEXT and/or IMAGE.",
    )

    max_input_image_size: int = Field(
        default=1024,
        ge=256,
        le=2048,
        description="Maximum dimension (width or height) for images sent to the API.",
    )


class PluginBehaviorSettings(BaseModel):
    add_userselectable_filter: bool = Field(
        default=True,
        description="Add userselectable AI filters to the list the user can choose from. When enabled, all enabled style_prompts will be available for user selection.",
    )

    enable_fallback_on_error: bool = Field(
        default=True,
        description="If AI generation fails, return the original image instead of an error.",
    )

    cache_results: bool = Field(
        default=True,
        description="Cache AI-generated results to avoid regenerating the same image multiple times.",
    )


class FilterNanobananaConfig(BaseConfig):
    model_config = SettingsConfigDict(
        title="Nano Banana Filter Plugin Config",
        json_file=f"{CONFIG_PATH}plugin_filter_nanobanana.json",
        env_prefix="filter-nanobanana-",
    )

    connection: ConnectionSettings = ConnectionSettings()
    image_generation: ImageGenerationSettings = ImageGenerationSettings()
    plugin_behavior: PluginBehaviorSettings = PluginBehaviorSettings()

    # Style prompts for different filter types
    style_prompts: list[StylePrompt] = Field(
        default=[
            StylePrompt(style_name="jojo", prompt="Redraw this portrait in the style of Jojo's Bizarre Adventure, exaggerated poses and vibrant colors with thick lines."),
            StylePrompt(style_name="anime", prompt="Redraw this portrait in an anime style similar to Howl's Moving Castle by Studio Ghibli."),
            StylePrompt(style_name="cartoon", prompt="Transform this portrait into a cartoon style, animated, colorful, disney-like illustration"),
            StylePrompt(style_name="sketch", prompt="Convert this portrait to a pencil sketch, black and white drawing, artistic sketch"),
            StylePrompt(style_name="watercolor", prompt="Transform this portrait into a watercolor painting, soft brush strokes, artistic"),
            StylePrompt(style_name="oil_painting", prompt="Convert this portrait to an oil painting, classical art style, rich textures"),
            StylePrompt(style_name="vintage", prompt="Transform this portrait to vintage photography style, sepia tones, retro aesthetic"),
            StylePrompt(style_name="cyberpunk", prompt="Redraw this portrait in cyberpunk style, neon lights, futuristic, sci-fi aesthetic"),
            StylePrompt(style_name="fantasy", prompt="Transform this portrait into fantasy art, magical, ethereal, mystical atmosphere"),
            StylePrompt(style_name="pixar", prompt="Redraw this portrait in Pixar animation style, 3D rendered appearance, colorful and friendly"),
            StylePrompt(style_name="custom", prompt="This prompt is read from a the 'prompt.txt' file in the {CONFIG_PATH}/photobooth-data/prompts/ folder. Do not modify!")
        ],
        description="Prompt templates for different AI filter styles. These guide the AI generation process.",
    )