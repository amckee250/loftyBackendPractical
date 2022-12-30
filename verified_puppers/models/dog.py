from io import BytesIO
import json
import requests
import tempfile
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
from django.core.files import File
from django.db import models

from lofty_backend_practical_proj.constants import DOG_IMG_API_ENDPOINT, \
    BASE_IMG_NAME, BASE_IMG_MODIFIED_NAME


class Dog(models.Model):
    """
    Model used for DB and business logic encapsulation of
    object used in dog service and modification endpoints
    """
    # Unique to ensure no duplicates
    original_img_url = models.URLField()
    original_img = models.ImageField(null=True, upload_to='media/verified_puppers/images')
    modified_img = models.ImageField(null=True, upload_to='media/verified_puppers/images')

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
        Void method for extracting and assigning meta and exif data from original_image
        """

        # Download from path for further processing
        response = requests.get(self.original_img_url, stream=True)

        # Temp file for saving to model
        temp_img = tempfile.NamedTemporaryFile()

        # Read the streamed image in sections
        for block in response.iter_content(1024 * 8):
            # If no more file, stop
            if not block:
                break
            # Write image block to temporary file
            temp_img.write(block)

        self.original_img.save(f'{BASE_IMG_NAME}{self.id}.jpg', File(temp_img))

        image = Image.open(self.original_img)

        # Assign basic metadata
        self.img_width = image.width
        self.img_height = image.height
        self.img_aspect_ratio = image.width / image.height
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

    def generate_modified_image(self):
        """
        Void method that takes temp image, updates the image with a
        human-readable and logo graphic
        """
        # Open image and set watermark properties
        image = Image.open(self.original_img)
        # image = Image.open(self.original_image_path)
        draw = ImageDraw.Draw(image)
        text = f"Verified by a Human"
        font = ImageFont.truetype(
            font='lofty_backend_practical_proj/fonts/Kanit-SemiBold.ttf',
            size=round(image.width / 12)
        )
        text_width, text_height = draw.textsize(text, font)

        # Assign font to lower right corner of image
        text_pos_x = image.width - text_width - (image.width * 0.05)
        text_pos_y = image.height - text_height - (image.height * 0.05)

        # Draw and save using BytesIO
        draw.text((text_pos_x, text_pos_y), text, font=font, fill=(255, 0, 0))
        blob = BytesIO()
        image.save(blob, 'JPEG')
        self.modified_img.save(f'{BASE_IMG_MODIFIED_NAME}{self.id}.jpg', File(blob))

    def __str__(self):
        return f'Dog: {self.id}'
