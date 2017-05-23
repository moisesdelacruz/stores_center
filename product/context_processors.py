from django.core.urlresolvers import reverse
from product.models import Category

def menu(request):
    menu = {'menu': [
        {'name': 'Home', 'url': reverse('product:list')},
        {'name': 'New', 'url': '#'},
        {'name': 'Offerts', 'url': '#'},
        {'name': 'Categories', 'url': '#'},
    ]}

    for item in menu['menu']:
        if item['url'] == request.path:
            item['active'] = True
    return menu


def categories(request):
    object = Category.objects.all()
    categories = {'categories': []}
    for cat in object:
        if request.path == cat.slug:
            categories['categories'].append({'name': cat.title, 'url': '/category/'+cat.slug, 'active': True})
        else:
            categories['categories'].append({'name': cat.title, 'url': '/category/'+cat.slug, 'active': False})
    return categories
