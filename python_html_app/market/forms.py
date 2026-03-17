from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Address, Category, Complaint, NotificationSetting, Product, UserProfile


def apply_form_classes(form):
    for field in form.fields.values():
        widget = field.widget
        existing = widget.attrs.get("class", "")
        widget.attrs["class"] = f"{existing} form-input".strip()
    return form


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=120, label="Ism")
    last_name = forms.CharField(max_length=120, required=False, label="Familiya")
    email = forms.EmailField(required=False, label="Email")
    phone = forms.CharField(max_length=30, required=False, label="Telefon")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Login")
    password = forms.CharField(widget=forms.PasswordInput, label="Parol")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=120, label="Ism")
    last_name = forms.CharField(max_length=120, required=False, label="Familiya")
    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = UserProfile
        fields = ("phone", "city", "district")
        labels = {"phone": "Telefon", "city": "Shahar", "district": "Tuman"}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["first_name"].initial = self.user.first_name
        self.fields["last_name"].initial = self.user.last_name
        self.fields["email"].initial = self.user.email
        apply_form_classes(self)

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]
        if commit:
            self.user.save()
            profile.user = self.user
            profile.save()
        return profile


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("title", "full_name", "phone", "region", "city", "street", "landmark", "is_default")
        widgets = {"street": forms.Textarea(attrs={"rows": 2})}
        labels = {
            "title": "Manzil nomi",
            "full_name": "Qabul qiluvchi",
            "phone": "Telefon",
            "region": "Viloyat",
            "city": "Shahar",
            "street": "Ko'cha / manzil",
            "landmark": "Mo'ljal",
            "is_default": "Asosiy manzil",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ("subject", "message")
        widgets = {"message": forms.Textarea(attrs={"rows": 4})}
        labels = {"subject": "Mavzu", "message": "Xabar"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)


class NotificationSettingForm(forms.ModelForm):
    class Meta:
        model = NotificationSetting
        fields = ("order_updates", "promo_news", "system_alerts")
        labels = {
            "order_updates": "Buyurtma yangilanishlari",
            "promo_news": "Aksiya va yangiliklar",
            "system_alerts": "Muhim tizim xabarlari",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "toggle-input"


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120, label="F.I.SH")
    phone = forms.CharField(max_length=30, label="Telefon")
    address = forms.ModelChoiceField(queryset=Address.objects.none(), required=False, label="Saqlangan manzil")
    address_text = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label="Yetkazish manzili")
    delivery_type = forms.ChoiceField(
        choices=[("oddiy", "Oddiy yetkazish"), ("tezkor", "Tezkor yetkazish"), ("olib_ketish", "Olib ketish")],
        label="Yetkazish turi",
    )
    note = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False, label="Izoh")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields["address"].queryset = user.addresses.all()
        else:
            self.fields["address"].widget = forms.HiddenInput()
        apply_form_classes(self)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "category",
            "brand",
            "description_short",
            "description_full",
            "technical_specs",
            "price",
            "unit",
            "stock_quantity",
            "sku",
            "image",
            "is_featured",
        )
        widgets = {
            "description_full": forms.Textarea(attrs={"rows": 5}),
            "technical_specs": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "slug", "icon", "description")
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_form_classes(self)
