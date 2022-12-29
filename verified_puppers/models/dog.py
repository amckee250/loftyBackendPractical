import json
import requests
from PIL import Image
from PIL.ExifTags import TAGS
from django.db import models

from lofty_backend_practical_proj.constants import DOG_IMG_API_ENDPOINT, TEMP_IMG_NAME


class Dog(models.Model):
    """
    Model used for DB and business logic encapsulation of
    object used in dog service and modification endpoints
    """
    # Unique to ensure no duplicates
    original_img = models.URLField(unique=True)
    modified_img = models.URLField(null=True)

    # Meta and Exif data
    img_width = models.IntegerField(null=True)
    img_height = models.IntegerField(null=True)
    img_aspect_ratio = models.FloatField(null=True)
    img_format = models.CharField(max_length=10, null=True)
    img_mode = models.CharField(max_length=10, null=True)
    is_img_animated = models.BooleanField(null=True)
    frames_in_img = models.IntegerField(null=True)
    img_exifdata = models.JSONField(null=True)

    @classmethod
    def fetch_original_images(cls, count):
        """
        Class Method for returning original_image from random dog image URL from Dog.ceo
        """

        response = requests.get(f'{DOG_IMG_API_ENDPOINT}{count}')

        if response.status_code != 200:
            raise ConnectionError

        data = json.loads(response.text)
        return data['message']

    def extract_image_metadata(self):
        """
        Method for extracting and returning meta and exif data from original_image
        """

        # Download from path for further processing
        with open(TEMP_IMG_NAME, 'wb') as f:
            f.write(requests.get(self.original_img).content)
        image = Image.open(TEMP_IMG_NAME)

        # Assign basic metadata
        self.img_width = image.width
        self.img_height = image.height
        self.img_aspect_ratio = max(image.width, image.height) / min(image.width, image.height)
        self.img_format = image.format
        self.img_mode = image.mode
        self.is_img_animated = getattr(image, "is_animated", False)
        self.frames_in_img = getattr(image, "n_frames", 1)

        # Assign exif data
        exifdata = image.getexif()
        exifdata_tagged = {}

        # Iterate over all EXIF data fields and assign human-readable tags
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            # Decode bytes
            if isinstance(data, bytes):
                data = data.decode()
            exifdata_tagged[tag] = data

        self.img_exifdata = exifdata_tagged
        self.save()

    def __str__(self):
        return f'Dog: {self.id}'
