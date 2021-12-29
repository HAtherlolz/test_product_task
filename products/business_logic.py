
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_page_load_stats(request, model, slug):
    if request.user.is_authenticated:
        model.objects.create(
            page_url=slug,
            user=request.user
        )
    else:
        model.objects.create(
            page_url=slug,
            ip=get_client_ip(request)
        )


def check_shop_cart_for_user_or_ip_exists(request, model):
    if request.user.is_authenticated:
        if model.objects.filter(user=request.user).exists():
            return model.objects.filter(user=request.user)
    else:
        if model.objects.filter(ip=get_client_ip(request)):
            return model.objects.filter(ip=get_client_ip(request))
