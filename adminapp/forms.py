from authapp.models import ShopUser
from authapp.forms import ShopUserEditForm
from django import forms
from mainapp.models import ProductCategory, Product


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')

    def __init__(self, *args, **kwargs):
        super(ProductCategoryEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.fields.BooleanField):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'
            field.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.fields.BooleanField):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'
            field.help_text = ''
