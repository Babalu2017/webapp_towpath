from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extentions = ['.png', '.jpg', '.jpeg', '.webp']
    if not ext.lower() in valid_extentions:
        raise ValidationError('Unsupported file extension. Allowed extensions: ' +str(valid_extentions))
