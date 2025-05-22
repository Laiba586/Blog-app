from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Post,BlogComment
from django.contrib.auth import authenticate, login, logout         

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        desc =request.POST['desc']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(desc)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")

def about(request):
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = POST.objects.none()
    else:
        allpostsTitle = POST.objects.filter(title__icontains=query)
        allpostauthor = POST.objects.filter(author__icontains=query)
        allpostsContent = POST.objects.filter(content__icontains=query)
        allposts = allpostsTitle.union(allpostsContent, allpostauthor)
    if allposts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    else:
        messages.success(request, "The results found form this query")
    params = {'allposts': allposts, 'query': query}
    return render(request, 'home/search.html', params)

def handlesignup(request):
    if request.method == "POST":
        # Get the post parameters
        name = request.POST['name']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        Password1 = request.POST['Password1']
        Password2 = request.POST['Password2']

        # check for errorneous input
        if len(name) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('/')
        if not name.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('/')
        if Password1 != Password2:
            messages.error(request, "Passwords do not match")
            return redirect('/')
        # create the user
        myuser = User.objects.create_user(name, email, Password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created")
        return redirect('/')
    
    else:
        return HttpResponse("404 page not found")
    
def handlelogin(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        Password = request.POST['Password']

        user = authenticate(username=username, password=Password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('/')
    
    return HttpResponse("404 page not found")

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')    


 




    
