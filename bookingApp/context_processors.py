from .models import Category



def categories_processor(request):
    list_category = Category.objects.all()

    return {'list_category':list_category}