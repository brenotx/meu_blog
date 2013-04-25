from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required

from .models import Article
from forms import RegisterForm, ContactForm


def article(request, slugs):
    article = get_object_or_404(Article, slugs=slugs)
    return render_to_response('blog/article.html',
                              locals(),
                              context_instance=RequestContext(request))


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            success_msg = 'Contato enviado!'
    else:
        form = ContactForm()

    return render_to_response('blog/contact.html',
                              locals(),
                              context_instance=RequestContext(request))


def register(request):
    """Sign up an user"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()
    return render_to_response('blog/register.html',
                              locals(),
                              context_instance=RequestContext(request))


@permission_required('show_all_users')
def all_users(request):
    users = User.objects.all()
    return render_to_response('all_users.html',
                              locals(),
                              context_instance=RequestContext(request))
