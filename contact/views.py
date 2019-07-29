from django.shortcuts import render
from django.views.generic import View


class ContactView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'contact/contact_us.html')

