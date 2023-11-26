from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

class FileValidatorMixin:
    def validate_file_size(self, value, field_name):
        
        max_size = getattr(self, 'max_file_size', 5 * 1024 * 1024)  # Default: 5 MB

        if value.size > max_size:
            self.add_error(field_name, f"File size must be no more than {max_size / 1000000} megabytes.")

    def validate_file_extension(self, value, field_name):
        allowed_extensions = getattr(self, 'allowed_extensions', None)

        if not allowed_extensions:
            raise ValidationError("Allowed extensions are not specified.")

        extension = value.name.split('.')[-1].lower()

        if extension not in allowed_extensions:
            self.add_error(field_name, f"Invalid file extension. Allowed extensions are: {', '.join(allowed_extensions)}")