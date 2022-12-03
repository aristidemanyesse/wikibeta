from django.shortcuts import render

# Create your views here.

###################################################################################################

def handler404(request, exception):
    return render(request, 'auth/404.html')


def handler400(request, exception):
    return render(request, 'auth/400.html')


def handler500(request):
    return render(request, 'auth/500.html')