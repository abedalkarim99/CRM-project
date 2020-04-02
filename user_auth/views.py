from django.shortcuts import render ,redirect , get_object_or_404
from django.contrib.auth import login , authenticate ,logout ,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# imports for generate_password function
import random



def home(request) :
    context = {
        'title' : 'Home'

    }
    return render(request,'user_auth/home.html',context)


def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, 'u are aready loged in')
        return redirect('home')
    else :
        if request.method == "GET":
            context = {
                'title': 'Login'
            }
            return render(request, 'user_auth/login.html',context)

        elif request.method == "POST":
            user_username = request.POST['username']
            user_password = request.POST['password']
            user = authenticate(request, username=user_username, password=user_password)
            if user is not None:
                login(request, user)
                return redirect('user_home')
            else:
                messages.info(request, "your username or password is incorrect , please try again")
                return redirect("login_user")

@login_required(login_url='login_user')
def logout_user(request) :
    if request.method == "POST" :
        logout(request)
        return redirect('user_home')

def sign_up_user(request) :
    if request.user.is_authenticated:
        messages.info(request,'u are aready Register')
        return redirect('home')
    else :
        if request.method == "GET" :
            context = {
                'title': 'Sign Up'
            }
            return render(request, 'user_auth/sign_up.html',context)
        elif request.method == "POST" :
            user_first_name = request.POST['first_name']
            user_last_name = request.POST['last_name']
            user_username = request.POST['username']
            user_email = request.POST['email']
            user_password1 = request.POST['password1']
            user_password2 = request.POST['password2']

            if User.objects.filter(username=user_username).exists():
                messages.info(request, 'username is taken, try another one')
                return redirect('sign_up_user')



            elif User.objects.filter(email= user_email).exists() :
                messages.info(request, 'email is taken, try another one')
                return redirect('sign_up_user')

            elif user_password1 != user_password2 :
                messages.info(request, 'password not matching')
                return redirect('sign_up_user')


            else :
                user = User.objects.create_user(first_name = user_first_name,
                                                last_name = user_last_name,
                                                username = user_username,
                                                email = user_email,
                                                password = user_password1
                                                )
                user.save()
                login(request,user)
                return redirect("user_home")


@login_required(login_url='login_user')
def delete_account(request,user_id) :
    user = get_object_or_404(User , pk=user_id)
    if request.method == "POST" :
        user.delete()
        messages.info(request,"Your account was deleted sucssfully")
        return redirect('user_home')

@login_required(login_url='login_user')
def change_password(request) :
    if request.method == "GET" :
        return render(request,'user_auth/change_password.html')
    if request.method == "POST" :
        user = get_object_or_404(User, pk=request.user.id)
        user_old_password = request.POST['old_password']
        user_new_password = request.POST['new_password']
        user_new_password2 = request.POST['new_password2']

        if not user.check_password(user_old_password):
            messages.info(request, 'the password(current) You entered is incorrect')
            return redirect('change_password')
        elif user_new_password != user_new_password2 :
            messages.info(request, 'the new password did not matching')
            return redirect('change_password')
        else :
            user.set_password(user_new_password)
            user.save()
            # update_session_auth_hash(request, user)
            messages.info(request, "Your password was changed sucssfully , please login again")
            return redirect('user_home')




# generate_password function view
def generate_password(request) :
    if request.method == "GET" :
        context = {
            'title' : 'Password Generator' ,
            'range' : range(7,31) ,

        }
        return render(request,'user_auth/generate_password_function/generate_password.html', context)
    elif request.method == "POST" :
        characters = list('abcdefghijklmnopqrstuvwxyz')

        if request.POST.get('uppercase'):
            characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        if request.POST.get('special_characters'):
            characters.extend(list('!@#$%^&*()<>?;.'))
        if request.POST.get('numbers'):
            characters.extend(list('0123456789'))
        if request.POST.get('arabic_letters'):
            characters.extend(list('ابتثجحخدذرزسشصضطظعغفقكلمنهوي'))

        length = int(request.POST.get('length', 12))

        password_generated = ''
        for i in range(length):
            password_generated += random.choice(characters)
        context =  {
            'title' : 'the result' ,
            'password': password_generated
        }

        return render(request,
                      'user_auth/generate_password_function/generate_password_result.html',
                      context)


#error views
def error_404(request,exception) :
    context = {

    }
    return render(request,'user_auth/errors/error_404.html',context)