import os
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import Game
from .forms import GameUploadForm, UserUpdateForm, ProfilisUpdateForm, CommentForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import FormMixin


# Create your views here.


from django.http import HttpResponse
class SuccessView(TemplateView):
    template_name = 'file_upload_success.html'

def flappygame(request):
    return render(request, 'flappy_game.html')

def welcome(request):
    return render(request, 'welcome.html')

def tutorial(request):
    return render(request, 'tutorial.html')

def about(request):
    num_users = User.objects.all().count()
    num_games = Game.objects.all().count()

    context = {
        'num_games': num_games,
        'num_users': num_users,
    }
    return render(request, 'about.html', context=context)

def games(request):
    paginator = Paginator(Game.objects.all(), 2)
    page_number = request.GET.get('page')
    zaidimai = paginator.get_page(page_number)
    context = {
        'zaidimai': zaidimai
    }
    return render(request, 'games.html', context=context)

class GameDetailView(FormMixin, DetailView):
    model = Game
    #template_name = 'game_detail.html'
    form_class = CommentForm
    context_object_name = 'game'
    def get_template_names(self):
        game = self.get_object()
        if game.template_name:
            return [game.template_name]

    def get_success_url(self):
        return reverse('game_detail', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.game = self.object
        form.instance.commenter = self.request.user
        form.save()
        return super(GameDetailView, self).form_valid(form)

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render(request, f"games/{slug}.html", {'game': game})

class FileUploadView(CreateView):
    model = Game
    form_class = GameUploadForm
    template_name = 'upload_file.html'
    success_url = reverse_lazy('file_upload_success')

    def form_valid(self, form):
        response = super().form_valid(form)
        game = form.instance
        self.create_game_template(game)
        return response

    def create_game_template(self, game):
        template_path = os.path.join(settings.TEMPLATES[0]['DIRS'][0], f"{game.slug}.html")

        content = """
{% extends 'base.html' %}
{% block content %}
{% load static %}
<div class="iframe-container">
<iframe src='{{ MEDIA_URL }}web/{{ game.slug }}/index.html' style='width:864px; height:827px; border:none;'></iframe>
</div>
<h4>Reviews:</h4>
{% if game.comment_set.all %}
{% for review in game.comment_set.all %}
 <hr>
<strong>{{ review.commenter }}</strong>, <em>{{ review.date_created}}</em>
<p>{{ review.content }}</p>
{% endfor %}
{% else %}
<p>Game doesn't have any reviews</p>
{% endif %}

{% if user.is_authenticated %}

<div class='fieldWrapper'>
    <hr><br/>
    <h4>Leave a review:</h4>
    <form action='' method='POST'>{% csrf_token %}
        {{ form.as_p }}
        <input type='submit' value='Save'>
    </form>
</div>
{% endif %}
{% endblock %}
        """

        with open(template_path, 'w') as file:
            file.write(content)


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile was updated!')
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username %s already exists!' % username)
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email %s already exists!' % email)
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, 'User %s was created!' % username)
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'register.html')



