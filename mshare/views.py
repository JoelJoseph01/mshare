from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login as dj_login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import ShareForm, Searching
from .models import Share, Friends
from django.utils import timezone
from .forms import SignUp
# Create your itemss here.
def home(request):
    return render(request,'mshare/home.html')

def signupuser(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'GET':
        return render(request,'mshare/signupuser.html',{'form':SignUp()})
    if request.POST['password1'] == request.POST['password2']:
            try:
                form=SignUp(request.POST)
                email=request.POST['email']
                if User.objects.filter(email=email):
                    return render(request,'mshare/signupuser.html',{'form':SignUp(), 'error':'Email is already taken'})
                user = User.objects.create_user(request.POST['username'],email=request.POST['email'],password=request.POST['password1'])
                user.save()
                dj_login(request,user)
                return redirect('profile')
            except IntegrityError:
                return render(request, 'mshare/signupuser.html', {'form':SignUp(), 'error':'That username has already been taken. Please choose a new username'})
    else:
            return render(request, 'mshare/signupuser.html', {'form':SignUp(), 'error':'Passwords did not match'})
def login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'GET':
            return render(request, 'mshare/loginuser.html', {'form':AuthenticationForm()})
    else:   
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'mshare/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
            else:
                dj_login(request, user)
                return redirect('profile')

@login_required
def logoutuser(request):
        logout(request)
        return render(request,'mshare/home.html')

@login_required
def profile(request, pk=None):   
        if pk:
                users=User.objects.get(pk=pk)
                return render(request,'mshare/friendspro.html',{'users':users})
        else:
                users=request.user
                return render(request,'mshare/profile.html',{'users': users})

@login_required
def changepassword(request):
    if request.method == 'POST':
         form=PasswordChangeForm(request.user,request.POST)
         if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            return redirect('change_done')
         else:
            print(form.errors)
    else:
        form=PasswordChangeForm(request.user)
    return render(request, 'mshare/changepassword.html',{'form':form})

@login_required
def change_done(request):
    return render(request,'mshare/change_done.html')


@login_required
def add(request):
    if request.method == 'GET':
        return render(request,'mshare/add.html',{'form':ShareForm()})
    else:
        form = ShareForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.date=timezone.now()
            post.save()
            return redirect('items')
        else:
         return render(request, 'mshare/add.html', {'form':ShareForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def detail(request,pk):
    obj=get_object_or_404(Share,pk=pk)
    return render(request,'mshare/detail.html',{'obj':obj})

# @login_required
# def delete(request,pk):
#     data = get_object_or_404(Share, pk=pk, author=request.user)
#     if request.method == 'GET':
#         data.delete()
#         return render(request,'mshare/view.html',{'data':data})

@login_required  
def items(request):
    item=Share.objects.order_by('-date').filter(author=request.user)
    try:
        friend = Friends.objects.get(current_user=request.user)
        friends = friend.users.all()
        for f in friends:
                obj=Share.objects.filter(author=f.username)
                item = item | obj
    except Friends.DoesNotExist:
        friends=None
    return render(request,'mshare/items.html',{'item':item})

# @login_required
# def view(request,pk):
#     data = get_object_or_404(Share, pk=pk, author=request.user)
#     if request.method == 'GET':
#         form = ShareForm(instance=data)
#         return render(request, 'mshare/view.html', {'data':data, 'form':form})
#     else:
#         try:
#             form = ShareForm(request.POST, instance=data)
#             form.save()
#             return redirect('items')
#         except ValueError:
#             return render(request, 'mshare/view.html', {'data':data, 'form':form, 'error':'Bad info'})

def change_friends(request,operation,pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'make':
        Friends.add_friend(request.user,new_friend)
        return redirect('others')
    elif operation == 'lose':      
        Friends.lose_friend(request.user,new_friend)
        return redirect('friends')
    return redirect('home')

@login_required
def others(request):
    users = User.objects.exclude(id=request.user.id)
    new_friend = User.objects.get(pk=request.user.pk)
    Friends.add_friend(request.user,request.user)
    try: 
        friend = Friends.objects.get(current_user=request.user)
        friends = friend.users.all() 
    except Friends.DoesNotExist:
        friends=None                       
    return render(request,'mshare/others.html',{'users':users,'friends':friends})

@login_required
def friends(request):
        try:    
            friend = Friends.objects.get(current_user=request.user)
            friends = friend.users.all()
        except Friends.DoesNotExist:
                friends=None
        f = {'friends':friends}
        return render(request,'mshare/friends.html',f)

def search(request):
    check ='found'
    if request.method == 'POST':
        form = Searching(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            obj=Share.objects.order_by('-date').filter(title=post.title)
            if len(obj) == 0:
                check = 'notfound'
            form = Searching()
            return render(request,'mshare/search.html',{'form':form,'obj':obj,'check':check})        
    else:
        form = Searching()
        return render(request,'mshare/search.html',{'form':form,'check':check})
