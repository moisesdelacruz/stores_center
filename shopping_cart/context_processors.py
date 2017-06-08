from shopping_cart.models import CartProduct

def cart_products(request):
    if request.user.is_authenticated():
        product = CartProduct.objects.filter(user=request.user)
        return {'count_product_cart': product.count()}
    return {'count_product_cart': 0}
