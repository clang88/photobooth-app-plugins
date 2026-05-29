from enum import Enum


class GeminiModels(str, Enum):
    FLASH_25 = "gemini-2.5-flash-image"
    PRO_3 = "gemini-3-pro-image"
    FLASH_31 = "gemini-3.1-flash-image"


DEFAULT_GEMINI_MODEL = GeminiModels.FLASH_31


COMMON_ASPECT_RATIOS: tuple[str, ...] = (
    "1:1",
    "2:3",
    "3:2",
    "3:4",
    "4:3",
    "4:5",
    "5:4",
    "9:16",
    "16:9",
    "21:9",
)


MODEL_IMAGE_SIZES: dict[GeminiModels, tuple[str, ...]] = {
    GeminiModels.FLASH_25: (),
    GeminiModels.PRO_3: ("1K", "2K", "4K"),
    GeminiModels.FLASH_31: ("1K", "2K", "4K"),
}


def get_allowed_aspect_ratios(model: GeminiModels) -> tuple[str, ...]:
    _ = model
    return COMMON_ASPECT_RATIOS


def get_allowed_image_sizes(model: GeminiModels) -> tuple[str, ...]:
    return MODEL_IMAGE_SIZES[model]


def supports_image_size(model: GeminiModels) -> bool:
    return bool(get_allowed_image_sizes(model))