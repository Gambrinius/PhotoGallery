import os

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http.response import Http404
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist

from PhotoGallery.settings import MAX_UPLOAD_SIZE
from users.models import UserProfile, UserImage
from users.forms import UserRegistrationForm, LoginForm, ProfileForm, UserImageForm

from PIL import Image


def registration_view(request):
    context = dict()
    context['registration_form'] = UserRegistrationForm()
    context.update(csrf(request))
    if request.POST:
        form = UserRegistrationForm(request.POST)
        context['registration_form'] = form
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/')
        else:
            context['registration_form'] = form
    return render(request, "registration.html", context)


def login_view(request):
    context = dict()
    context['login_form'] = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled!")
            else:
                context['login_error'] = "User not found or incorrect input."
                return render(request, "login.html", context)
    else:
        return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def profile_view(request):
    try:
        context = dict()
        user_profile, created = UserProfile.objects.get_or_create(user_id=request.user.id)
        user_profile.save()

        context['profile'] = user_profile
        context['user'] = request.user
        context['image_list'] = UserImage.objects.filter(user=request.user)

    except ObjectDoesNotExist:
        raise Http404

    return render(request, "profile.html", context)


def edit_view(request):
    context = dict()
    context['user'] = request.user
    context['edit_form'] = ProfileForm(instance=UserProfile.objects.get(user=request.user))
    context.update(csrf(request))
    if request.POST:
        form = ProfileForm(request.POST, request.FILES)
        context['edit_form'] = form
        if form.is_valid():
            user_profile = UserProfile.objects.get(user=request.user)

            user_profile.first_name = form.cleaned_data['first_name']
            user_profile.last_name = form.cleaned_data['last_name']
            user_profile.birthday = form.cleaned_data['birthday']
            user_profile.about_user = form.cleaned_data['about_user']
            user_profile.url_height = 200
            user_profile.url_width = 200

            if request.POST.get('avatar', True):
                user_profile.avatar = request.FILES['avatar']

            user_profile.save()

            return redirect('profile')
        else:
            context['form'] = form
    return render(request, "edit_profile.html", context)


def upload_view(request):
    context = dict()
    image_formats = ['.JPG', '.jpg', '.JPEG', '.jpeg', '.PNG', '.png', '.GIF', '.gif', '.BMP', '.bmp']
    context['upload_form'] = UserImageForm()
    if request.method == 'POST':
        uploaded_file = request.FILES['image']  # object UploadedFile
        filename, context['file_format'] = os.path.splitext(uploaded_file.name)
        context['file_size'] = uploaded_file.size

        if context['file_format'] in image_formats:
            if uploaded_file.size <= int(MAX_UPLOAD_SIZE):

                form = UserImageForm(request.POST, request.FILES)
                if form.is_valid():
                    img = Image.open(uploaded_file)
                    (width, height) = img.size
                    user_image = UserImage.objects.create(user=request.user)
                    user_image.image_height = height
                    user_image.image_width = width
                    user_image.public = form.cleaned_data['public']
                    user_image.image = request.FILES['image']
                    user_image.save()
                    context['successful_upload'] = 'Image file %s successful uploaded.' % uploaded_file.name
                    return render(request, 'upload_image.html', context)

            context['upload_error'] = "'Please keep file size under %s bytes. Current file size %s bytes'" \
                                      % (MAX_UPLOAD_SIZE, uploaded_file.size)
        else:
            context['upload_error'] = "You try upload image/file not allowed format! \n " \
                                      "Please, try to upload files with '.jpg', '.png', '.gif', '.bmp' formats."

    return render(request, 'upload_image.html', context)


def delete_image_view(request):
    if request.method == 'POST':
        image = UserImage.objects.get(id=request.POST['image_id'])
        image.delete()

    return redirect('profile')
