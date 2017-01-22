from django.shortcuts import render
from users.models import UserImage
# Create your views here.


def main_gallery_view(request):
    context = dict()
    context['image_list'] = UserImage.objects.filter(public=True).order_by('-creation_date')
    return render(request, 'main.html', context)
