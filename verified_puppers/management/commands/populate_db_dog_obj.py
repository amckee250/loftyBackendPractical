from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from verified_puppers.models import Dog


class Command(BaseCommand):
    help = 'Populates the database with two dozen images of dogs and any corresponding metadata' \
           'from the images. Use "--fresh_db true" flag to remove existing Dog objects/files and replace with new set'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fresh_db',
            help='Remove existing Dog objects/files and replace with new',
        )

    def handle(self, *args, **options):
        """
        Future Development: A more scalable solution would be to use a cloud service (AWS S3) to store these files
        """
        if options['fresh_db']:
            dogs = Dog.objects.all()
            for dog in dogs:
                dog.original_img.delete()
                dog.modified_img.delete()
            # :'( - Just bring them to a shelter instead!
            dogs.delete()

        # Create 24 non-conflicting Dog objects with processed metadata and image modifications
        try:
            # Create all or none if error
            with transaction.atomic():
                original_images = Dog.fetch_original_images(24)
                dogs = Dog.objects.bulk_create(
                    [Dog(original_img_url=img) for img in original_images]
                )

                # Extract data and create modifications
                for dog in dogs:
                    dog.extract_image_metadata()
                    dog.generate_modified_image()

                # Successfully created
                self.stdout.write(self.style.SUCCESS('Woof!\n24 Dog objects were successfully created'))

        except ConnectionError:
            self.stdout.write(self.style.SUCCESS('Connection Error: No dogs created'))
        except IntegrityError:
            self.stdout.write(self.style.SUCCESS('Duplicate Dog(s) fetched from API: No dogs created'))
