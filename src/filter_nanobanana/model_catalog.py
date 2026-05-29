from enum import Enum


class GeminiModel(str, Enum):
    FLASH_25 = "gemini-2.5-flash-image"
    PRO_3 = "gemini-3-pro-image"
    FLASH_31 = "gemini-3.1-flash-image"


DEFAULT_GEMINI_MODEL = GeminiModel.FLASH_25


MODELS_WITH_IMAGE_CONFIG: set[GeminiModel] = {
    GeminiModel.PRO_3,
    GeminiModel.FLASH_31,
}


def supports_image_config(model: GeminiModel) -> bool:
    return model in MODELS_WITH_IMAGE_CONFIG