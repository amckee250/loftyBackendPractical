from django.contrib.auth.models import User
from faker import Faker
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from key_lookup.models import ItemModel

fake = Faker()

ITERATIONS = 100


class ItemModelTests(APITestCase):
    """
    Test cases for testing all ItemModel related endpoints
    """

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test', first_name='test',
            last_name='test', email='test@gmail.com', password='Test1234'
        )

    def test_create_itemmodel(self):
        """
        Test creating a new ItemModel.
        """
        self.client.force_authenticate(user=self.user)

        url = reverse('create-item-or-list')
        for _ in range(ITERATIONS):
            data = {
                'item_key': fake.random_number(digits=5)
            }

            response = self.client.post(url, data, format='json')
            self.assertTrue(
                response.status_code == status.HTTP_201_CREATED
                or response.data['item_key'] == ["item model with this item key already exists."]
            )

        self.client.logout()

    def test_create_itemmodel_without_login(self):
        """
        Test creating a new ItemModel without being logged in
        """
        url = reverse('create-item-or-list')
        for _ in range(ITERATIONS):
            data = {
                'item_key': fake.random_number(digits=5)
            }

            response = self.client.post(url, data, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_403_FORBIDDEN
            )

        self.client.logout()

    def test_itemmodel_list(self):
        """
        Test fetching a list of ItemModel objects
        """
        url = reverse('create-item-or-list')
        for _ in range(ITERATIONS):
            response = self.client.get(url, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_200_OK
            )

    def test_itemmodel_increment(self):
        """
        Test incrementing an ItemModel.
        """
        self.client.force_authenticate(user=self.user)

        random_key = fake.random_number(digits=5)

        ItemModel.objects.create(item_key=random_key)

        url = reverse('item-increment', kwargs={'item_key': random_key})
        for _ in range(ITERATIONS):
            data = {
                'increment_amount': fake.random_number(digits=5)
            }

            response = self.client.patch(url, data, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_200_OK
            )

        self.client.logout()

    def test_itemmodel_increment_without_login(self):
        """
        Test incrementing ItemModel without being logged in
        """
        url = reverse('item-increment', kwargs={'item_key': '1'})
        for _ in range(ITERATIONS):
            data = {
                'increment_amount': fake.random_number(digits=5)
            }

            response = self.client.patch(url, data, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_403_FORBIDDEN
            )