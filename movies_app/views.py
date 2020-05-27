from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *

from .forms import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView

from django.shortcuts import get_object_or_404

from django.contrib.auth import login, logout, authenticate

from django.contrib import messages

from django.forms import inlineformset_factory

from django.http import HttpResponse, HttpResponseRedirect

from django.db import transaction

from cloudinary.forms import cl_init_js_callbacks

import cloudinary

import cloudinary.uploader

import cloudinary.api


# Create your views here.

class FilmListView(ListView):
    template_name = 'movies_app/film_list.html'
    context_object_name='all_movies'
    model=Film

    def get_queryset(self):
        return Film.objects.all()


class FilmDetailView(FormMixin, DetailView):
    template_name='movies_app/film_detail.html'
    model = Film
    form_class = CommentForm

    def get_success_url(self):
        return reverse('film_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(FilmDetailView, self).get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.all().filter(film_comment=self.kwargs['pk'])
        return context

    def post(self, request, **kwargs):
        content=request.POST.get('content')
        self.object = self.get_object()
        cc = Comment.objects.create( film_comment_id=self.kwargs['pk'], user=request.user, content=content)
        context = super(FilmDetailView, self).get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.all().filter(film_comment=self.kwargs['pk'])
        return self.render_to_response(context=context)


class FilmCreateView(CreateView):
    template_name = 'movies_app/film_form.html'
    form_class = FilmForm
    model=Film

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        photo_form = PhotoFormSet()
        return self.render_to_response(self.get_context_data(form=form, photo_form=photo_form))
        print(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        f =Film.objects.create(film_title=self.request.POST['film_title'], year=self.request.POST['year'], genre=self.request.POST['genre'], summary=self.request.POST['summary'])
        f.save()
        if form.is_valid():
            temp_image = request.FILES['images-0-image']
            cloudinary_response = cloudinary.uploader.upload(temp_image.file.read())
            image_url = cloudinary_response['url']
            pf=Photo.objects.create(image_u=image_url, photo_film_id=f.id)
            pf.save()
            return redirect(reverse('film_detail', kwargs={'pk': f.id}))
        else:
            return redirect(reverse('film_detail', kwargs={'pk': f.id}))

    def form_valid(self, form, photo_form):
        self.object = form.save()
        photo_form.instance = self.object
        photo_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, photo_form):
        return self.render_to_response(self.get_context_data(form=form, photo_form=photo_form))



class FilmUpdateView(UpdateView):
    model=Film
    fields=['film_title', 'year', 'genre', 'summary']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        photo_form = PhotoFormSet(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, photo_form=photo_form, ))

    def post(self, request, *args, **kwargs):
# load film
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
# update film
        form.save()
# looking into dictionary (by using .get, n.b. this get is different to the queryset .get) with key 'images-0-image' and seeing associated value (ie user uploaded image). if there is no value, pass none.
        if request.FILES != None:
            temp_image = request.FILES.get('images-0-image', None)
# update image if present
        if temp_image != None:
            cloudinary_response = cloudinary.uploader.upload(temp_image.file.read())
            image_url = cloudinary_response['url']
            pf=Photo.objects.filter(photo_film_id=self.kwargs['pk']).update(image_u=image_url)
# redirect to film_detail page
            return redirect(reverse('film_list'))
        else:
            return redirect(reverse('film_list'))

    def form_valid(self, form, photo_form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        photo_form.instance = self.object
        photo_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, photo_form):
        return self.render_to_response(self.get_context_data(form=form, photo_form=photo_form))


class FilmDeleteView(DeleteView):
    model= Film
    success_url = reverse_lazy('film_list')


class CommentDeleteView(DeleteView):
    model=Comment
    template_name = 'movies_app/comment_confirm_delete.html'
    pk_url_kwarg = "comment_id"

    def delete(self, request, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        film_id = kwargs["pk"]
        return redirect(reverse('film_detail', kwargs={'pk': film_id}))


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'movies_app/register.html'
