from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Using named URLs instead of hardcoded paths is much safer!
    if request.user.is_contractor:
        return redirect('contractor_dashboard')
    return redirect('worker_feed')