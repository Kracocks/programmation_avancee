from django.shortcuts import render
from django.http import HttpResponse

def home(request, param="World"):
    return HttpResponse(f"""<h1>Hello {param}!</h1>""")

def contact_us(request):
    return HttpResponse("""<h1>Contact Us</h1>
                            <p>contact us</p>""")

def about_us(request):
    return HttpResponse("""<h1>About Us</h1>
                            <p>about us</p>""")

# Create your views here.
