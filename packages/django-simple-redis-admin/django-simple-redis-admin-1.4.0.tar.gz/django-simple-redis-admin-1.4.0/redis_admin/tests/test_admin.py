from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import override_settings, TestCase


@override_settings(ROOT_URLCONF='redis_admin.tests.test_urls')
class RedisAdminSanityTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('test', 'test@test.com', 'password')
        self.client.login(username=self.user.username, password='password')

    def test_admin_accessible(self):
        response = self.client.get('/admin/')
        self.assertEqual(200, response.status_code)


@override_settings(ROOT_URLCONF='redis_admin.tests.test_urls')
class RedisAdminViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('test', 'test@test.com', 'password')
        self.client.login(username=self.user.username, password='password')

        cache.master_client.set('test-redis-admin', 'test')

    def test_index(self):
        response = self.client.get('/admin/redis_admin/manage/')
        self.assertEqual(200, response.status_code)

    def test_key(self):
        response = self.client.get('/admin/redis_admin/manage/test-redis-admin/')
        self.assertEqual(200, response.status_code)

    def test_delete_key_confirmation(self):
        response = self.client.get('/admin/redis_admin/manage/test-redis-admin/delete/')
        self.assertEqual(200, response.status_code)

    def test_delete_key_action(self):
        response = self.client.post('/admin/redis_admin/manage/test-redis-admin/delete/', {'post': 'yes'})
        self.assertEqual(302, response.status_code)

    def tearDown(self):
        cache.master_client.delete('test-redis-admin')
