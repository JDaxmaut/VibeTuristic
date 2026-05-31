from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def docs_view(request):
    return render(request, "tours/admin_docs.html")
