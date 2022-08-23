import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', 'jpeg', '.tiff', '.tif', 'gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Only images allowed: {valid_extensions}')