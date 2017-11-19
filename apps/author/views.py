from django.shortcuts import render

from django.views.generic.base import View
from .models import Author
# Create your views here.

class UserListView(View):
    def get(self,request):

        return render(request, 'users-list.html', {})