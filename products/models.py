from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Name', max_length=200)
    slug = models.SlugField('Slug', unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Name', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    price = models.DecimalField('Price', decimal_places=2, max_digits=9)
    description = models.TextField('Description', blank=True)
    image = models.ImageField('Image', upload_to='products')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True, db_index=True)
    GRADE = (
        ('Base', 'Base'),
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
    )
    product_grade = models.CharField(max_length=50, choices=GRADE, default="Standard")

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ('-post_date', )

    def __str__(self):
        return self.name


class Like(models.Model):
    product = models.ForeignKey(Product, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True, related_name='likes', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '{} from {}'.format(self.product, self.user or self.ip)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True, related_name='comments', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(blank=True, null=True)
    text = models.TextField('Comment', max_length=500)
    post_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return 'comment from {}'.format(self.user or self.ip)


class PageLoadStats(models.Model):
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    page_url = models.SlugField('Slug')
    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True, related_name='stats', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f'date: {self.date}, from {self.user or self.ip}'


class ShopCart(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True, related_name='cart', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(blank=True, null=True)
    product = models.ForeignKey(Product, related_name='cart_product', on_delete=models.CASCADE)
    amount = models.SmallIntegerField()

    def __str__(self):
        return f'customer: {self.user or self.ip}, product: {self.product}'
