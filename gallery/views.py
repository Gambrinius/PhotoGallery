from django.shortcuts import render
from users.models import UserImage
# Create your views here.


def main_gallery_view(request):
    context = dict()
    context['image_list'] = UserImage.objects.all()
    return render(request, 'main.html', context)
