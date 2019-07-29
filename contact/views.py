from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic import CreateView
from .models import Enquiry
from .forms import ContactForm


class ContactView(CreateView):
    def get(self, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(self.request, 'contact/contact_us.html', context)
        
    def post(self, *args, **kwargs):
        form = ContactForm(self.request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            
            """Save the enquiry"""
            enquiry = Enquiry()
            enquiry.name = name
            enquiry.email = email
            enquiry.subject = subject
            enquiry.message = message
            enquiry.save()
            messages.success(self.request, "Your enquiry was submitted successfully! Please check your email for confirmation!")
            
            """Send confirmation email"""
            send_mail(
                'Enquiry Wedding Planner',
                'We have successfully received your enquiry',
                'weddingplanner@email.com',
                [self.request.user.email],
                fail_silently=False,
                )
            return redirect('/')
        else:
            messages.warning(self.request, "The data entered is invalid!")
            return redirect('contact')

