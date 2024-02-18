from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import UserAccount
from .form import UserAccountForm
from django.contrib.auth import logout
#from .DB import DbConnection

#dbobj=DbConnection(host="localhost",user="root",passwd="",database="secure_data_cloud",port=3306)
def signup(request):
    return render(request,'signup.html')

def signupaction(request):
    username=request.POST['txtusername']
    password=request.POST['txtpassword']
    firstname=request.POST['txtfirstname']
    lastname=request.POST['txtlastname']
    address=request.POST['txtaddress']
    mobile=request.POST['txtmobile']
    email2=request.POST['txtemail']
    status=0
    role='user'
    useraccount=UserAccount.objects.create(username=username,password=password,role=role,firstname=firstname,lastname=lastname,address=address,mobile=mobile,email=email2,status=status)
    try:
        useraccount.save()
        return redirect(login)
    except:
        errmsg='User Registration Failed'
        return render(request,'signup.html',{'errmsg':errmsg})
    
def home(request):
    role=request.session['role']
    if role=='admin':
        return render(request,'adminhome.html')
    else:
        return render(request,'userhome.html')
    
def login(request):
    form=UserAccountForm()
    return render(request,'login.html',{'form':form})

def loginaction(request):
    username=request.POST["username"]
    password=request.POST["password"]
    record=UserAccount.objects.filter(username=username,password=password,status=1)
    if record.count()>0:
        record=UserAccount.objects.get(username=username,password=password)
        request.session['username'] = record.username
        request.session['role']=record.role
        if record.role=="admin":
            return render(request,'adminhome.html')
        else:
            return render(request,'userhome.html')
    else:
        form=UserAccountForm()
        return render(request,'login.html',{'errmsg':'Invlid username or password, or your account is not apporved by the admin','form':form})

def editlogin(request,username):
    login = UserAccount.objects.get(username=username)
    return render(request,'editlogin.html', {'login':login})

def updatelogin(request, id):
    login = UserAccount.objects.get(userid=id)
    form = UserAccountForm(request.POST, instance = login)
    if form.is_valid():
        form.save()
        return render(request,'editusers.html')
    else:
        login = UserAccount.objects.get(userid=id)
        return render(request,'editlogin.html', {'login':login})

def deletelogin(request, id):
    login = UserAccount.objects.get(userid=id)
    login.delete()
    logins=UserAccount.objects.all()
    return render(request,'adminhome.html',{'logins':logins})

def editprofile(request):
    username=request.session['username']
    login = UserAccount.objects.get(username=username)
    return render(request,'editprofile.html', {'login':login})

def updateprofile(request):
    username=request.session['username']
    firstname=request.POST['txtfirstname']
    lastname=request.POST['txtlastname']
    address=request.POST['txtaddress']
    mobile=request.POST['txtmobile']
    email=request.POST['txtemail']
    login=UserAccount.objects.get(username=username)
    try:
        login.firstname=firstname
        login.lastname=lastname
        login.address=address
        login.mobile=mobile
        login.email=email
        login.save()
        return redirect(home)
    except:
        errmsg='Update Failed.....'
        username=request.session['username']
        login = UserAccount.objects.get(username=username)
        return render(request,'editprofile.html', {'login':login,'errmsg':errmsg})
        
def custom_logout(request):
    logout(request)
    return redirect('login')

def changepassword(request):
    return render(request,'changepassword.html')

def updatepassword(request):
    password=request.POST['password']
    newpassword=request.POST['newpassword']
    confirmpassword=request.POST['confirmpassword']
    username=request.session['username']
    login=UserAccount.objects.get(username=username)
    p=login.password
    if p==password:
        if newpassword==confirmpassword:
            login.password=newpassword
            login.save()
            errmsg='Password changed successfully'
            return render(request,'changepassword.html',{'errmsg':errmsg})
        else:
            errmsg='New Password and Confirm Password must be the same'
            return render(request,'changepassword.html',{'errmsg':errmsg})
    else:
        errmsg='Invalid Current Password'
        return render(request,'changepassword.html',{'errmsg':errmsg})
    

def validateuser(request):
    logins=UserAccount.objects.filter(status=0)
    return render(request,'validateuser.html',{'logins':logins})

def approveuser(request,username):
    login=UserAccount.objects.get(username=username)
    login.status=1
    login.save()
    return redirect (validateuser)

def rejectuser(request,username):
    login=UserAccount.objects.get(username=username)
    login.delete()
    return redirect (validateuser)

def editusers(request):
    logins=UserAccount.objects.all()
    return render(request,'editusers.html',{'logins':logins})

from django.shortcuts import render
from .models import UserAccount
from django.utils import timezone




def profilebase(request):
    # Retrieve all user accounts from the UserAccount model ordered alphabetically
    user_accounts = UserAccount.objects.order_by('username')

    # Render the template with the user accounts passed as context data
    return render(request, "profilebase.html", {'user_accounts': user_accounts})



        
        
        
