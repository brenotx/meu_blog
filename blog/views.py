from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import send_mail
from django import forms

from blog.models import Article


def article(request, slugs):
	article = get_object_or_404(Article, slugs=slugs)
	return render_to_response('blog/article.html', locals(),
		context_instance=RequestContext(request))

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.send_email()
			success_msg = 'Contato enviado!'
	else:
		form = ContactForm()

	return render_to_response('blog/contact.html', locals(),
		context_instance=RequestContext(request))

class ContactForm(forms.Form):
	name = forms.CharField(max_length=100)
	sender = forms.EmailField(required=False)
	subject = forms.CharField(max_length=100)
	message = forms.Field(widget=forms.Textarea)

	def send_email(self):
		subject = self.cleaned_data['subject']
		from_email = self.cleaned_data['sender']
		message = """
			Nome: %(name)s
			E-mail: %(sender)s
			Mensagem: %(message)s
		""" % self.cleaned_data

		send_mail(subject, message, from_email, ['brenotx@gmail.com'],)
