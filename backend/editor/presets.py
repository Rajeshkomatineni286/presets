from PIL import ImageEnhance, ImageFilter, ImageOps


def vintage(image):
    toned = ImageOps.colorize(ImageOps.grayscale(image), black='#2f1b0c', white='#f2d8b0')
    return ImageEnhance.Contrast(toned).enhance(1.15)


def vivid(image):
    saturated = ImageEnhance.Color(image).enhance(1.7)
    return ImageEnhance.Sharpness(saturated).enhance(1.2)


def noir(image):
    gray = ImageOps.grayscale(image)
    high_contrast = ImageEnhance.Contrast(gray).enhance(1.6)
    return high_contrast.filter(ImageFilter.DETAIL)


PRESETS = {
    'vintage': vintage,
    'vivid': vivid,
    'noir': noir,
}
