from enum import Enum


class GeminiModels(str, Enum):
    FLASH_25 = "gemini-2.5-flash-image"
    PRO_3 = "gemini-3-pro-image"
    FLASH_31 = "gemini-3.1-flash-image"


DEFAULT_GEMINI_MODEL = GeminiModels.FLASH_31


MODELS_WITH_IMAGE_CONFIG: set[GeminiModels] = {
    GeminiModels.PRO_3,
    GeminiModels.FLASH_31,
}


def supports_image_config(model: GeminiModels) -> bool:
    return model in MODELS_WITH_IMAGE_CONFIG