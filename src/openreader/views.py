from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

reader_login_required = login_required(login_url='/reader/')

def index(request):
    if (request.user.is_authenticated()):
        return redirect(reverse("reader:reader"))
    return render_to_response("index.html")

def default_render_failure(request, message, status=403,
                           template_name='',
                           exception=None):
    """Render an error page to the user."""
    return redirect("/loginfailed/")

@reader_login_required
def reader(request):
    return render_to_response("reader.html")

@reader_login_required
def reader_content(request):
    return render_to_response("readercontent.html")
