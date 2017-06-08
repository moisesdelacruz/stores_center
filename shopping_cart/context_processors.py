from shopping_cart.models import CartProduct

def cart_products(request):
    product = CartProduct.objects.filter(user=request.user)
    return {'count_product_cart': product.count()}
