import csv

from decimal import Decimal as D

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Sum, Max

from .models import *
from .forms import CommentForm, ShopCartForm
from .business_logic import (
    get_client_ip,
    get_page_load_stats,
    check_shop_cart_for_user_or_ip_exists
)



class CategoryListView(View):
    """ List of categories and populars by number of likes"""
    def get(self, request):
        category = Category.objects.all()
        popular = Product.objects.all(
        ).annotate(popular=Sum('likes')
                   ).order_by('likes')[:10]
        page_slug = ''
        get_page_load_stats(request, PageLoadStats, page_slug)
        shop_cart = check_shop_cart_for_user_or_ip_exists(request, ShopCart)
        product = Product.objects.order_by('category', '-post_date').distinct('category')
        return render(request, 'main.html', {
            "category_list": category,
            "popular_list": popular,
            "new_arrivals": product,
            "shop_cart": shop_cart
        })


class ProductListView(View):
    """ List of products by category """
    def get(self, request, slug):
        queryset = Product.objects.filter(category__slug=slug)
        shop_cart = check_shop_cart_for_user_or_ip_exists(request, ShopCart)
        get_page_load_stats(request, PageLoadStats, slug)
        product = Product.objects.order_by('category', '-post_date').distinct('category')

        paginator = Paginator(queryset, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'category_product.html', {
            "product_list": page_obj,
            "new_arrivals": product,
            "shop_cart": shop_cart
        })


class ProductDetailView(View):
    """ Product details"""
    def get(self, request, slug):
        queryset = Product.objects.get(slug=slug)
        shop_cart = check_shop_cart_for_user_or_ip_exists(request, ShopCart)
        get_page_load_stats(request, PageLoadStats, slug)
        product = Product.objects.order_by('category', '-post_date').distinct('category')
        return render(request, 'product_details.html', {
            "product_detail": queryset,
            "new_arrivals": product,
            "shop_cart": shop_cart
        })


class AddCommentView(View):
    """ Add comment by auth user or by ip for unauth user """
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if request.user.is_authenticated:
                form.product_id = pk
                form.user_id = request.user.id
                form.save()
            else:
                form.product_id = pk
                form.ip = get_client_ip(request)
                form.save()
        return redirect(f'/product/{form.product.slug}/')


class AddLikeView(View):
    """ Add comment by auth user or by ip for unauth user """
    def post(self, request, pk):
        model = Like()
        if request.user.is_authenticated:
            if Product.objects.get(id=pk).likes.filter(user_id=request.user.id).exists():
                return HttpResponse("404")
            else:
                model.product_id = pk
                model.user_id = request.user.id
                model.save()
        else:
            if Product.objects.get(id=pk).likes.filter(ip=get_client_ip(request)).exists():
                return HttpResponse("404")
            else:
                model.product_id = pk
                model.ip = get_client_ip(request)
                model.save()
        return redirect(f'/product/{model.product.slug}/')


class ShopCartAddView(View):
    """ Add product to ShopCart """
    def post(self, request, pk):
        form = ShopCartForm(request.POST)
        product = Product.objects.get(id=pk)
        if request.user.is_authenticated:
            if form.is_valid():
                form = form.save(commit=False)
                form.product = product
                form.user_id = request.user.id
                form.save()
        else:
            if form.is_valid():
                form = form.save(commit=False)
                form.product = product
                form.ip = get_client_ip(request)
                form.save()
        return redirect(f'/product/{form.product.slug}/')


class ShopCartDetailView(View):
    """ Shop cart details """
    def get(self, request):
        shop_cart = check_shop_cart_for_user_or_ip_exists(request, ShopCart)
        return render(request, 'shop_cart.html', {"shop_cart": shop_cart})


class FilterCategoryCostView(ListView):
    """ Costs filter for category page by min/max """
    def get_queryset(self):
        price_min = D(self.request.GET.get("min_price"))
        price_max = D(self.request.GET.get("max_price"))

        if not price_max:
            price_max = Product.objects.aggregate(Max('price'))['price__max']

        product_list = Product.objects.filter(price__range(price_min, price_max))
        return product_list


def export_csv_file():
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Number of Comments', 'Number of Likes'])

    for product in Product.objects.all().values_list('id', 'name', 'comments.count', 'likes.count'):
        writer.writerow(product)

    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    return response
