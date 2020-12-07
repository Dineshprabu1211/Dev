from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your views here.
def register(request):
    if request.method == 'POST':
        # Get Form Values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password2 = request.POST['password2']
        password = request.POST['password']

        # Check Password Matches
        if password == password2:
            # Check Username is not same with already taken Username
            if User.objects.filter(username=username).exists():
                messages.error(request, "User name already exists!!")
                return redirect('register')
            else:
                # Check Email is not same with already taken email
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists!!")
                    return redirect('register')
                else:
                    # Good to go
                    user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
                    user.save()
                    messages.success(request, "You have Registered and now you can Login!!")
                    return redirect('login')
        else:
            messages.error(request, "Passwords don't match")
            return redirect('register')

    else:
        return render(request, "accounts/register.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are Logged in!!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('login')

    else:
        return render(request, "accounts/login.html")

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now Logged out!!')
        return redirect("index")

def dashboard(request):
    user_contact = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contact
    }
    return render(request, "accounts/dashboard.html", context)
