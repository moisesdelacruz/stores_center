from django import forms

from shop.models import Shop

class ShopModelForm(forms.ModelForm):
    # description = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}))

    class Meta:
        model = Shop
        fields = ('name', 'description', 'logo', 'cover_image',)
        widgets = {
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
