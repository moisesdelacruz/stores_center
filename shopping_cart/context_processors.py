from shopping_cart.models import CartProduct

def cart_products(request):
    if request.user.is_authenticated():
        product = CartProduct.objects.filter(user=request.user).values_list('product__id', flat=True)
        return {'shopping_cart': product}
    return {'shopping_cart': []}
