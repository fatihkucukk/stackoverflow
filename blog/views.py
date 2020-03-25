from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView, View
from django.views.generic import RedirectView
from django.views.generic.edit import FormView, CreateView
from requests import request

from blog.models import Post, Cevap
from .forms import SoruSorForm, CevapForm
from django.shortcuts import render, get_object_or_404


class HomePageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Post.objects.all()
        context['questions'] = questions
        return context


class SoruSorFormView(FormView):
    template_name = 'Ask_Question.html'
    form_class = SoruSorForm

    def form_valid(self, form):
        form.instance.author = User.objects.first()
        form.save()
        return redirect(reverse('homepage'))

    def form_invalid(self, form):
        return redirect(reverse('homepage'))


class SoruCevapView(TemplateView):
    template_name = 'soru_cevap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = Post.objects.get(id=kwargs['id'])
        context['question'] = question
        return context


class CevapFormView(FormView):
    template_name = 'soru_cevap.html'
    form_class = CevapForm

    def get_soru(self):
        return Post.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.instance.kullanici = User.objects.first()
        form.instance.soru = self.get_soru()
        form.save()
        return redirect(reverse('homepage'))

    def form_invalid(self, form):
        return redirect(reverse('homepage'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# Oy verme de istek atılıp redirect edilecegi için ve herhangi
# bir template ihtiyaç duyulmadıgından redirectview dan extend ediyoruz.
class SoruOyView(RedirectView):

    def get_soru(self):
        return Post.objects.get(id=self.kwargs.get('id'))

    def get(self, request, *args, **kwargs):
        soru = self.get_soru()
        soru.oy_ver(voter_user=request.user)
        return redirect(reverse('soru_detay', kwargs={'id': soru.id}))

class CevapOyView(RedirectView):

    def get_cevap(self):
        return Cevap.objects.get(id=self.kwargs.get('id'))

    def get(self, request, *args, **kwargs):
        cevap = self.get_cevap()
        cevap.oy_ver(voter_user=request.user)
        return redirect(reverse('cevap_detay', kwargs={'id': cevap.id}))