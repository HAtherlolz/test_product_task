from django.urls import path, include

from .views import *


urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('price-range-filter/', FilterCategoryCostView.as_view(), name="price_range_filter"),
    path('category/<slug:slug>/', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/comment/<int:pk>/', AddCommentView.as_view(), name='add_comment'),
    path('product/like/<int:pk>/', AddLikeView.as_view(), name='add_like'),
    path('product/shop-cart/<int:pk>/', ShopCartAddView.as_view(), name='add_to_cart'),
    path('shop-cart/', ShopCartDetailView.as_view(), name='shop_cart'),
    path('category/products-to-csv/', export_csv_file, name='products_to_csv')
]
