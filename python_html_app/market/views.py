from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    AddressForm,
    CategoryForm,
    CheckoutForm,
    ComplaintForm,
    NotificationSettingForm,
    ProductForm,
    ProfileForm,
    RegisterForm,
)
from .models import (
    Cart,
    CartItem,
    Category,
    Complaint,
    CompareItem,
    Favorite,
    NotificationSetting,
    Order,
    OrderItem,
    Product,
    RecentlyViewed,
    UserProfile,
)


def ensure_session_key(request: HttpRequest) -> str:
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key or ""


def session_queryset(model, request: HttpRequest):
    key = ensure_session_key(request)
    if request.user.is_authenticated:
        return model.objects.filter(Q(user=request.user) | Q(session_key=key))
    return model.objects.filter(session_key=key)


def get_cart(request: HttpRequest) -> Cart:
    key = ensure_session_key(request)
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, defaults={"session_key": key})
        Cart.objects.filter(session_key=key, user__isnull=True).exclude(pk=cart.pk).update(user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(session_key=key, user__isnull=True)
    request.cart_instance = cart
    return cart


def stock_badge(status: str):
    if status == "yoq":
        return ("yo'q", "badge-danger")
    if status == "kam":
        return ("tugab bormoqda", "badge-warning")
    return ("mavjud", "badge-success")


def base_catalog_queryset():
    return Product.objects.select_related("category").all()


def catalog_filters(request: HttpRequest, queryset):
    q = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    availability = request.GET.get("availability", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    sort = request.GET.get("sort", "new")

    if q:
        queryset = queryset.filter(
            Q(name__icontains=q)
            | Q(category__name__icontains=q)
            | Q(brand__icontains=q)
            | Q(description_short__icontains=q)
        )
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    if availability == "in_stock":
        queryset = queryset.filter(stock_quantity__gt=0)
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    sort_map = {
        "price_asc": "price",
        "price_desc": "-price",
        "popular": "-is_featured",
        "new": "-created_at",
    }
    queryset = queryset.order_by(sort_map.get(sort, "-created_at"))
    return queryset, q, sort


def home(request: HttpRequest) -> HttpResponse:
    get_cart(request)
    featured = Product.objects.filter(is_featured=True)[:8]
    recommended = Product.objects.filter(is_available=True).exclude(pk__in=featured.values_list("pk", flat=True))[:8]
    recent_ids = list(session_queryset(RecentlyViewed, request).values_list("product_id", flat=True)[:8])
    recent_products = Product.objects.filter(id__in=recent_ids)
    return render(
        request,
        "market/home.html",
        {
            "categories": Category.objects.all()[:10],
            "featured_products": featured,
            "recommended_products": recommended,
            "recent_products": recent_products,
        },
    )


def catalog(request: HttpRequest) -> HttpResponse:
    get_cart(request)
    queryset, search_query, current_sort = catalog_filters(request, base_catalog_queryset())
    paginator = Paginator(queryset, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "market/catalog.html",
        {
            "page_obj": page_obj,
            "categories": Category.objects.all(),
            "search_query": search_query,
            "current_sort": current_sort,
            "current_category": request.GET.get("category", ""),
            "current_availability": request.GET.get("availability", ""),
            "min_price": request.GET.get("min_price", ""),
            "max_price": request.GET.get("max_price", ""),
        },
    )


def category_detail(request: HttpRequest, slug: str) -> HttpResponse:
    category = get_object_or_404(Category, slug=slug)
    queryset, search_query, current_sort = catalog_filters(request, base_catalog_queryset().filter(category=category))
    paginator = Paginator(queryset, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "market/category_detail.html",
        {
            "category": category,
            "page_obj": page_obj,
            "categories": Category.objects.all(),
            "search_query": search_query,
            "current_sort": current_sort,
            "current_availability": request.GET.get("availability", ""),
            "min_price": request.GET.get("min_price", ""),
            "max_price": request.GET.get("max_price", ""),
        },
    )


def product_detail(request: HttpRequest, slug: str) -> HttpResponse:
    get_cart(request)
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    key = ensure_session_key(request)
    RecentlyViewed.objects.filter(product=product, session_key=key).delete()
    RecentlyViewed.objects.create(product=product, user=request.user if request.user.is_authenticated else None, session_key=key)
    similar = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    recent_ids = list(
        session_queryset(RecentlyViewed, request).exclude(product=product).values_list("product_id", flat=True)[:4]
    )
    recent_products = Product.objects.filter(id__in=recent_ids)
    favorite_ids = set(session_queryset(Favorite, request).values_list("product_id", flat=True))
    compare_ids = set(session_queryset(CompareItem, request).values_list("product_id", flat=True))
    return render(
        request,
        "market/product_detail.html",
        {
            "product": product,
            "similar_products": similar,
            "recent_products": recent_products,
            "favorite_ids": favorite_ids,
            "compare_ids": compare_ids,
            "stock_badge_data": stock_badge(product.stock_status),
        },
    )


def about_page(request):
    get_cart(request)
    return render(request, "market/about.html")


def contact_page(request):
    get_cart(request)
    return render(request, "market/contact.html")


def help_page(request):
    get_cart(request)
    return render(request, "market/help.html")


def favorites_page(request):
    get_cart(request)
    items = session_queryset(Favorite, request).select_related("product", "product__category")
    return render(request, "market/favorites.html", {"favorites": items})


@require_POST
def toggle_favorite(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    key = ensure_session_key(request)
    filters = {"product": product}
    if request.user.is_authenticated:
        filters["user"] = request.user
    else:
        filters["session_key"] = key
    item = Favorite.objects.filter(**filters).first()
    if item:
        item.delete()
        messages.info(request, "Saqlanganlar ro'yxatidan olib tashlandi.")
    else:
        Favorite.objects.create(product=product, user=request.user if request.user.is_authenticated else None, session_key=key)
        messages.success(request, "Mahsulot saqlandi.")
    return redirect(request.META.get("HTTP_REFERER", "favorites"))


def compare_page(request):
    get_cart(request)
    items = session_queryset(CompareItem, request).select_related("product", "product__category")[:4]
    return render(request, "market/compare.html", {"compare_items": items})


@require_POST
def toggle_compare(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    key = ensure_session_key(request)
    filters = {"product": product}
    if request.user.is_authenticated:
        filters["user"] = request.user
    else:
        filters["session_key"] = key
    item = CompareItem.objects.filter(**filters).first()
    if item:
        item.delete()
        messages.info(request, "Taqqoslashdan olib tashlandi.")
    else:
        if session_queryset(CompareItem, request).count() >= 4:
            messages.warning(request, "Bir vaqtda 4 tagacha mahsulot taqqoslash mumkin.")
        else:
            CompareItem.objects.create(product=product, user=request.user if request.user.is_authenticated else None, session_key=key)
            messages.success(request, "Mahsulot taqqoslashga qo'shildi.")
    return redirect(request.META.get("HTTP_REFERER", "compare"))


@require_POST
def remove_compare_item(request, item_id: int):
    item = get_object_or_404(session_queryset(CompareItem, request), pk=item_id)
    item.delete()
    messages.info(request, "Taqqoslash ro'yxati yangilandi.")
    return redirect("compare")


def cart_page(request):
    return render(request, "market/cart.html", {"cart": get_cart(request)})


@require_POST
def add_to_cart(request, product_id: int):
    cart = get_cart(request)
    product = get_object_or_404(Product, pk=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": 1})
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, "Mahsulot savatga qo'shildi.")
    return redirect(request.META.get("HTTP_REFERER", "cart"))


@require_POST
def update_cart_item(request, item_id: int):
    item = get_object_or_404(get_cart(request).items.select_related("product"), pk=item_id)
    item.quantity = max(1, int(request.POST.get("quantity", 1)))
    item.save()
    messages.success(request, "Savat yangilandi.")
    return redirect("cart")


@require_POST
def delete_cart_item(request, item_id: int):
    item = get_object_or_404(get_cart(request).items, pk=item_id)
    item.delete()
    messages.info(request, "Mahsulot savatdan o'chirildi.")
    return redirect("cart")


@require_POST
def buy_now(request, product_id: int):
    cart = get_cart(request)
    cart.items.all().delete()
    product = get_object_or_404(Product, pk=product_id)
    CartItem.objects.create(cart=cart, product=product, quantity=1)
    return redirect("checkout")


def checkout_page(request):
    cart = get_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Savat hozircha bo'sh.")
        return redirect("cart")

    initial = {}
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        initial = {"full_name": request.user.get_full_name() or request.user.username, "phone": profile.phone}

    if request.method == "POST":
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            selected_address = form.cleaned_data.get("address")
            address_text = selected_address.full_address() if selected_address else form.cleaned_data["address_text"]
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=form.cleaned_data["full_name"],
                phone=form.cleaned_data["phone"],
                address=selected_address,
                address_text=address_text,
                delivery_type=form.cleaned_data["delivery_type"],
                note=form.cleaned_data["note"],
                total_price=cart.subtotal,
            )
            total = Decimal("0")
            for item in cart.items.select_related("product"):
                line_total = item.product.price * item.quantity
                total += line_total
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    unit=item.product.unit,
                    price=item.product.price,
                    quantity=item.quantity,
                    line_total=line_total,
                )
            order.total_price = total
            order.save(update_fields=["total_price"])
            cart.items.all().delete()
            messages.success(request, "Buyurtma muvaffaqiyatli yaratildi.")
            return redirect("profile_orders" if request.user.is_authenticated else "home")
    else:
        form = CheckoutForm(user=request.user, initial=initial)
    return render(request, "market/checkout.html", {"cart": cart, "form": form})


def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, phone=form.cleaned_data.get("phone", ""), city="Qarshi")
            NotificationSetting.objects.create(user=user)
            login(request, user)
            messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile_dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(
        request,
        "market/profile_dashboard.html",
        {
            "profile": profile,
            "orders_count": request.user.orders.count(),
            "complaints_count": request.user.complaints.count(),
            "addresses_count": request.user.addresses.count(),
        },
    )


@login_required
def profile_edit(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi.")
            return redirect("profile_dashboard")
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, "market/profile_edit.html", {"form": form})


@login_required
def profile_orders(request):
    return render(request, "market/profile_orders.html", {"orders": request.user.orders.prefetch_related("items")})


@login_required
def profile_complaints(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Shikoyat yuborildi.")
            return redirect("profile_complaints")
    else:
        form = ComplaintForm()
    return render(request, "market/profile_complaints.html", {"form": form, "complaints": request.user.complaints.all()})


@login_required
def profile_addresses(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if address.is_default:
                request.user.addresses.update(is_default=False)
            address.save()
            messages.success(request, "Manzil saqlandi.")
            return redirect("profile_addresses")
    else:
        form = AddressForm()
    return render(request, "market/profile_addresses.html", {"form": form, "addresses": request.user.addresses.all()})


@login_required
@require_POST
def delete_address(request, address_id: int):
    address = get_object_or_404(request.user.addresses, pk=address_id)
    address.delete()
    messages.info(request, "Manzil o'chirildi.")
    return redirect("profile_addresses")


@login_required
def profile_notifications(request):
    settings_obj, _ = NotificationSetting.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = NotificationSettingForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Bildirishnoma sozlamalari saqlandi.")
            return redirect("profile_notifications")
    else:
        form = NotificationSettingForm(instance=settings_obj)
    return render(request, "market/profile_notifications.html", {"form": form})


def staff_required(view):
    return login_required(user_passes_test(lambda u: u.is_staff)(view))


@staff_required
def admin_dashboard(request):
    return render(
        request,
        "market/admin/dashboard.html",
        {
            "product_count": Product.objects.count(),
            "order_count": Order.objects.count(),
            "complaint_count": Complaint.objects.count(),
            "category_count": Category.objects.count(),
        },
    )


@staff_required
def admin_products(request):
    return render(request, "market/admin/products.html", {"products": Product.objects.select_related("category")})


@staff_required
def admin_product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mahsulot yaratildi.")
            return redirect("admin_products")
    else:
        form = ProductForm()
    return render(request, "market/admin/product_form.html", {"form": form, "title": "Mahsulot qo'shish"})


@staff_required
def admin_product_edit(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Mahsulot yangilandi.")
            return redirect("admin_products")
    else:
        form = ProductForm(instance=product)
    return render(request, "market/admin/product_form.html", {"form": form, "title": "Mahsulotni tahrirlash"})


@staff_required
@require_POST
def admin_product_delete(request, product_id: int):
    get_object_or_404(Product, pk=product_id).delete()
    messages.info(request, "Mahsulot o'chirildi.")
    return redirect("admin_products")


@staff_required
def admin_categories(request):
    return render(request, "market/admin/categories.html", {"categories": Category.objects.all()})


@staff_required
def admin_category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya yaratildi.")
            return redirect("admin_categories")
    else:
        form = CategoryForm()
    return render(request, "market/admin/category_form.html", {"form": form, "title": "Kategoriya qo'shish"})


@staff_required
def admin_category_edit(request, category_id: int):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya yangilandi.")
            return redirect("admin_categories")
    else:
        form = CategoryForm(instance=category)
    return render(request, "market/admin/category_form.html", {"form": form, "title": "Kategoriyani tahrirlash"})


@staff_required
def admin_orders(request):
    return render(request, "market/admin/orders.html", {"orders": Order.objects.prefetch_related("items")})


@staff_required
def admin_complaints(request):
    return render(request, "market/admin/complaints.html", {"complaints": Complaint.objects.select_related("user")})
