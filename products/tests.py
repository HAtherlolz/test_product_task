from django.test import TestCase

from .models import Product, Like, Comment, Category


class ViewsTestCase(TestCase):
    def test_view_main_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('category/mainboards/')
        self.assertEqual(response.status_code, 201)


class DbTestCase(TestCase):

    def test_db(self):
        queryset = Product.objects.get(id=1)
        self.assertEqual(queryset.id, 1)

    def test_db_create_like(self):
        like = Like.objects.create(
            product=1,
            ip="127.0.0.1",
        )
        self.assertEqual(like.ip, "127.0.0.1")

    def test_db_create_comment(self):
        comment = Comment.objects.create(
            product=1,
            user_id=1,
        )
        self.assertEqual(comment.user_id, 1)

    def test_db_product_filter(self):
        product = Product.objects.filter(product_grade="Base")
        self.assertEqual(product.product_grade, "Base")

    def test_db_category(self):
        category = Category.objects.create(name="name_test", slug="slug_test")
        self.assertEqual(category.slug, "slug_test")

