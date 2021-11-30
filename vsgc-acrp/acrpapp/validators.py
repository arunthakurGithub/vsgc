from django.core.exceptions import ValidationError
from django.conf import settings

def validate_file_size(value):
    filesize= value.size 
    if filesize > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
        print("valid")
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return value
