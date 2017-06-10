from django import forms
from product.models import Product

class ProductModelForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name','categories','description', 'quantity', 'price','discount','photo',)
        widgets = {
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'}),
        }
