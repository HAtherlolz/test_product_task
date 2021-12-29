from django.contrib import admin
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    fields = [
        'name',
        'slug',
        'price',
        'description',
        'image',
        'category',
        'product_grade',
        'post_date'
    ]
    readonly_fields = ["post_date"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    fields = ['product', 'user', 'ip', 'post_date']
    readonly_fields = ["post_date"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ['product', 'user', 'ip', 'text', 'post_date']
    readonly_fields = ["post_date"]


@admin.register(PageLoadStats)
class PageLoadStatsAdmin(admin.ModelAdmin):
    fields = ['date', 'user', 'ip', 'page_url']
    readonly_fields = ["date"]


@admin.register(ShopCart)
class ShopCartStatsAdmin(admin.ModelAdmin):
    fields = ['created_date', 'user', 'ip', 'product', 'amount']
    readonly_fields = ["created_date"]
