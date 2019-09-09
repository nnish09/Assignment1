from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from .validators import validate_file_extension
# from pyuploadcare.dj import ImageField


# def minimum_size(width=None, height=None):
#     def validator(image):
#         if not image.is_image():
#             raise ValidationError('File should be image.')

#         errors, image_info = [], image.info()['image_info']
#         if width is not None and image_info['width'] < width:
#             errors.append('Width should be > {} px.'.format(width))
#         if height is not None and image_info['height'] < height:
#             errors.append('Height should be > {} px.'.format(height))
#         raise ValidationError(errors)
#     return validator





class User(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be upto 10 digits")
    phone_no = models.CharField(validators=[phone_regex], max_length=10, blank=True) 
    profimg = models.ImageField(upload_to='images/',default='images/about.jpg',validators=[validate_file_extension])
    organization = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username