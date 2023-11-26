from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete = models.PROTECT, null = True)
    address = models.CharField(max_length = 200, null = True)
    phone = models.CharField(max_length = 200)
    image = models.ImageField(
        default = 'profile_images/default/default-avatar.png', 
        upload_to = 'profile_images',
        help_text='Maximum file size: 5 MB. Allowed extensions: .png or .jpeg',
    )

    create_date = models.DateTimeField(blank = True, null = True)
    update_date = models.DateTimeField(blank = True, null = True)

    allowed_extensions = ['png', 'jpeg']

    def __str__(self):
        return f"{self.staff.username.upper()}'s Profile"

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.localtime(timezone.now())

        self.update_date = timezone.localtime(timezone.now())
        
        super(Profile, self).save(*args, **kwargs)

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)