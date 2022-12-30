from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from verified_puppers.models import Dog

fake = Faker()

ITERATIONS = 100


class DogTests(APITestCase):
    """
    Test cases for testing all Dog related endpoints
    """

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test', first_name='test',
            last_name='test', email='test@gmail.com', password='Test1234'
        )

        # Utilize and test Django custom command for Dog model DB population
        call_command('populate_db_dog_obj')
        self.assertEqual(
            Dog.objects.count(), 24
        )

    def test_dog_detail(self):
        """
        Test querying Dog object detail
        """
        url = reverse('dog-detail', kwargs={'pk': fake.random_int(min=1, max=24, step=1)})
        for _ in range(ITERATIONS):
            response = self.client.get(url, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_200_OK
            )
