from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.user.is_contractor:
        return redirect('/contractor/dashboard/')
    return redirect('/worker/feed/')
