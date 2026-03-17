from .models import Cart, Category


def marketplace_context(request):
    cart = getattr(request, "cart_instance", None)
    cart_count = 0
    if cart:
        cart_count = sum(item.quantity for item in cart.items.all())
    else:
        session_key = request.session.session_key
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        elif session_key:
            cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
        else:
            cart = None
        if cart:
            cart_count = sum(item.quantity for item in cart.items.all())

    return {
        "nav_categories": Category.objects.order_by("name")[:8],
        "location_label": "Qarshi",
        "cart_count": cart_count,
    }
