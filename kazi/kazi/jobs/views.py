from django.shortcuts import render,redirect
from django.db.models import Q
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login ,logout
from grpc import Status
from matplotlib.style import context
from .models import jobCategory,User_profile,Jobs
from django.contrib.auth.models import User
from django.contrib import messages
from .decorators import un_authenticated
from .forms import SignUpForm,CreateJob

@un_authenticated
def LoginPage(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try: 
            user = User_profile.objects.get(email=email)

        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'User or password is incorrect')

    context = {'page': page}

    return render(request, 'login_register.html', context)
def LogoutUser(request):

    logout(request)
    return redirect('home')



#@allowed_users(allowed_allowed_roles=['donor'])
@un_authenticated
def RegisterUser(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, " Error ") 

    return render(request, 'login_register.html',{'form': form})



@login_required(login_url= 'login')
def updateShop(request,pk):
    shop = Jobs.objects.get(id=pk)
    form = CreateJob(instance = shop)

    if request.user != shop.owner:
        return HttpResponse(' Invalid request')

    if request.method == 'POST':
        form = CreateJob(request.POST, instance = shop)
        if form.is_valid():
            form.save()

            return redirect('shops')

    context = {'form': form}
    return render(request, 'jobadd.html', context)
# delete a shop
@login_required(login_url= 'login')
def deleteShop(request, pk): 
    shop = Jobs.objects.get(id=pk)

    if request.user != shop.owner:
        return HttpResponse(' Invalid request')

    if request.method == 'POST':
        shop.delete()
        return redirect('shops')
    return render(request, 'delete.html', {'obj': shop} )


def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ""
    status = True
    jobs = Jobs.objects.filter(
        Q(poster__First_name__icontains = q) |
        Q(poster__Last_name__icontains = q) |
        Q(Job_Title__icontains = q) |
        Q(Company_name__icontains = q) |
        Q(Job_category__name__icontains = q)|
        Q(short_description__icontains = q) |
        Q(job_description__icontains = q) |
        Q(date_added__icontains = q) |
        Q(is_active__icontains = q) 

        
        )
    categories = jobCategory.objects.all()
    jobs_count =  jobs.count()

    context = {'jobs':  jobs, 'categories': categories, 'jobs_count':jobs_count,"status":status}
    return render(request, 'home.html',context)

@login_required(login_url= 'login')
def addJob(request):
    categories = jobCategory.objects.all()
    if request.method == 'POST':
        job_data = request.POST     
        name_check = 'none'
        if job_data['product_category'] != name_check:
            name = jobCategory.objects.get(id=job_data['product_category'])
        elif job_data['product_category_new'] != '':
            name,created = jobCategory.objects.get_or_create(
                name = job_data['product_category_new']
            )
        else:
            name=None
        job = Jobs.objects.create(
                poster = request.user,
                Job_Title=job_data['job_title'],
                Company_name = job_data['company_hiring_name'],
                Job_category = name,
                short_description = job_data['short'],
                job_description = job_data['job_description'],
                
            )

        return redirect('home')
    context = {'categories': categories}
    return render(request, 'jobadd.html', context )


def ViewJob(request,pk):
    job = Jobs.objects.get(id = pk)
    context = {'job':job}
    return render(request, 'job.html', context)

def userProfile(request):
    return render(request, 'userprofile.html')

def viewWall(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ""
    categories = jobCategory.objects.all()
    kazi_users = User_profile.objects.filter(
        Q(username__icontains = q) |
        Q(email__icontains = q) |
        Q(First_name__icontains = q) |
        Q(Last_name__icontains = q) |
        Q(date_joined__icontains = q)|
        Q(is_active__icontains = q) 
    )

    
    kazi_users_count = kazi_users.count()

    context = {"kazi_users": kazi_users, "categories":categories,"kazi users count":kazi_users_count}

    return render(request, 'wall.html', context)