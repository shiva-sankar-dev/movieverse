from datetime import date
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres import *
from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, HttpResponseRedirect




def adminindex(request):
    return render(request,"admin-index.html")

def adminadditem(request):
    if 'publish' in request.POST:
        cover=request.FILES['form__img-upload']
        title=request.POST['title']
        Description=request.POST['Description']
        Releaseyear=request.POST['Releaseyear']
        time=request.POST['time']
        age=request.POST['age']
        country=request.POST['country']
        genre=request.POST['genre']
        cast=request.POST['cast']
        director=request.POST['director']
        video=request.FILES['video']
        trailer=request.FILES['trailer']
        cdate=date.today()

        moviename=Addproduct.objects.filter(movie_title=title)
        if moviename:
            print("already exist")
            return HttpResponseRedirect(reverse("adminadditem"))
            

        else:
            Addproduct.objects.create(movie_cover=cover,movie_title=title,movie_desc=Description,movie_video=video,movie_age=age,movie_year=Releaseyear,movie_time=time,movie_country=country,movie_genre=genre,movie_trailer=trailer,movie_director=director,movie_cast=cast,date=cdate)

        return HttpResponseRedirect(reverse("adminadditem"))
            


        
    return render(request,"admin-add-item.html")



def admindashboard(request):
    movies=Addproduct.objects.all().order_by('-id')[:5]
    review=rating.objects.all().order_by('-id')[:5]
    users=user_reg.objects.all().order_by('-id')[:5]
    
    context={
        "movies":movies,
        "reviews":review,
        "users":users,
    }
    return render(request,"admin-dashboard.html",context)

def admincatalog(request):
    catalog=Addproduct.objects.all().order_by('-id')
    total_count=Addproduct.objects.all().count()


        
    context={
        "catalog":catalog,
        "total_count":total_count,
    }
    
    return render(request,"admin-catalog.html",context)

def admincatalog_delete(request,id):
    Addproduct.objects.filter(id=id).delete()
    
    return redirect('admincatalog')

def admincomments(request):
    comment=comments.objects.all().order_by('-id')
    total_comment=comments.objects.all().count()
    context={
        "comment":comment,
        "total_comment":total_comment,
    }
    return render(request,"admin-comments.html",context)

def admincomments_delete(request,id):
    comments.objects.filter(id=id).delete()
    return redirect("admincomments")

def adminreview_delete(request,id):
    rating.objects.filter(id=id).delete()
    return redirect("adminreviews")

def adminreviews(request):
    review=rating.objects.all().order_by('-id')
    total_review=rating.objects.all().count()
    context={
        "review":review,
        "total_review":total_review,

    }
    return render(request,"admin-reviews.html",context)

def adminusers(request):
    users=user_reg.objects.all().order_by('-id')
    total_users=user_reg.objects.all().count()

    context={
        "users":users,
        "total_users":total_users,

    }
    return render(request,"admin-users.html",context)

def signup(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        cdate=date.today()
        if Login.objects.filter(username=email).exists():
            messages.error(request,"E-mail already exist")
            return redirect("signup")
        else:
            log=Login.objects.create_user(username=email,password=password,userType='Customer',viewpassword=password)
            log.save()
            obj=user_reg.objects.create(user=log,user_full_name=name,user_email=email,user_password=password,date=cdate)
            obj.save()
            return redirect('login')
        

    return render(request,"signup.html")

def user_login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        customer=authenticate(username=email,password=password)
        if customer:
            login(request,customer)
            request.session["userID"]=customer.id
            # print(customer.id)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request,"signin.html")

def user_logout(request):
    logout(request)
    return redirect('home')

def homepage(request):

    latest_movie = Addproduct.objects.order_by('-id')
    comedymovies=Addproduct.objects.filter(movie_genre='Comedy').order_by('-id')[:10]
    romanticmovies=Addproduct.objects.filter(movie_genre='Romance').order_by('-id')[:10]
    animationmovies=Addproduct.objects.filter(movie_genre='Animation').order_by('-id')[:10]
    science_fictionymovies=Addproduct.objects.filter(movie_genre='Science-fiction').order_by('-id')[:10]

    all_products = Addproduct.objects.all()

    # Number of items per page
    items_per_page = 12

    # Get the current page number from the request
    page_number = request.GET.get('page', 1)

    # Create a Paginator instance with the queryset and items per page
    paginator = Paginator(all_products, items_per_page)

    try:
        # Get the page object for the requested page number
        allmovie = paginator.page(page_number)
    except EmptyPage:
        # If the requested page number is out of range, return the last page
        allmovie = paginator.page(paginator.num_pages)

    # Generate the range of page numbers for the paginator
    num_pages = paginator.num_pages
    if num_pages <= 5:
        # If there are 5 or fewer pages, display all page numbers
        page_range = range(1, num_pages + 1)
    else:
        # Otherwise, display a subset of page numbers around the current page
        if allmovie.number <= 3:
            page_range = range(1, 6)
        elif allmovie.number >= num_pages - 2:
            page_range = range(num_pages - 4, num_pages + 1)
        else:
            page_range = range(allmovie.number - 2, allmovie.number + 3)


        
    context={
        "allmovie":allmovie,
        "latest_movie":latest_movie,
        "comedymovies":comedymovies,
        "romanticmovies":romanticmovies,
        "animationmovies":animationmovies,
        "science_fictionymovies":science_fictionymovies,
        'allmovie': allmovie,
        'page_range': page_range,
    }
    return render(request,"user-index.html",context)

def movie_list(request,genre):
    movie=None
    if genre=="Comedy":
        movie=Addproduct.objects.filter(movie_genre="Comedy").order_by('-id')
    elif genre == "Romantic":
        movie=Addproduct.objects.filter(movie_genre="Romantic").order_by('-id')
    elif genre == "Animation":
        movie=Addproduct.objects.filter(movie_genre="Animation").order_by('-id')
    elif genre == "Science-fiction":
        movie=Addproduct.objects.filter(movie_genre="Science-fiction").order_by('-id')

    
    
    context={
        "genre":genre,
        "movie":movie,

    }
    return render(request,"movie-list.html",context)

def search(request):
    result=""
    if 'search' in request.GET:
        searchtxt=request.GET['tosearch']
        result=Addproduct.objects.filter(movie_title__contains=searchtxt).order_by('-id')
    context={

        "result":result,
        "searchtxt":searchtxt,

    } 
    return render(request,"search.html",context)

def filter(request):

    if "genre" in request.GET:
        genre=request.GET['genre']          
        filter_apply=Addproduct.objects.filter(movie_genre=genre)
        filter_apply_count=Addproduct.objects.filter(movie_genre=genre).count()
    else:
        message_success="Please select a filter first"
        messages.error(request,message_success)
        return redirect("home")
            

    context={
        "filter_apply":filter_apply,
        "filter_apply_count":filter_apply_count,
        }
    return render(request,"filter.html",context)

def usernavandfoot(request):
    return render(request,"header-footer.html")

def about(request):
    return render(request,"about.html")

import requests

def contacts(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        cdate=date.today()
        obj=contact.objects.create(fullname=name,mail=email,subject=subject,message=message,date=cdate)
        obj.save()
        data={
            "access_key": "0fe05a4e-e52d-4253-ac6e-34e6034c1b7d", 
            "name": name,
            "email": email,
            "subject of message": subject,
            "message": message
        }
        response = requests.post("https://api.web3forms.com/submit",json=data)
        result = response.json()
        if result.get("success"):
            messages.success(request, "Message sent successfully!")
        else:
            messages.error(request, "Message failed to send.")
        return redirect("contacts")
            
    return render(request,"contacts.html")

def productdetails(request,id):
    user = ""
    if "userID" in request.session:
        uid=request.session["userID"]
        user=user_reg.objects.get(user__id=uid)
    movie=Addproduct.objects.get(id=id)
    cmt=comments.objects.filter(product_id=id).order_by('-id')
    reviews=rating.objects.filter(product_id=id).order_by('-id')
    # if 'userID' in request.session:
       
    total_rate=rating.objects.filter(product_id=id)
    total_rate_count=rating.objects.filter(product_id=id).count()
    if total_rate_count==0:
        total_rate_count=1
    total=0
    for i in total_rate:
        total+=i.star_rating
    average_rating=total/total_rate_count
    rating_for_movie=round((average_rating/5)*5,1)
    check=""
    if user:
        check = watchlater.objects.filter(product_id=id, user_id=user).count()
        
    
    
        

    if 'cmtbtn' in request.POST:
        if not request.POST['addcomment']:
            return redirect("productdetails" ,id)
        else:
            addcomment=request.POST['addcomment']
            cdate=date.today()
            comments.objects.create(user_id=user,comment=addcomment,cdate=cdate,product_id=movie)
        return redirect("productdetails" ,id)
        
    if 'reviewbtn' in request.POST:
        title=request.POST['reviewtitle']
        review_instance =request.POST['review']
        ratings = request.POST.get('rating', 0) 
        cdate=date.today()
        rating.objects.create(user_id=user,product_id=movie,reviewtitle=title,review=review_instance,date=cdate,star_rating=ratings)
        return redirect("productdetails", id)

    context={
        "movie":movie,
        "cmt":cmt,
        "reviews":reviews,
        "custom_user":user,
        "rating_for_movie":rating_for_movie,
        "check":check,

    }
    return render(request,"details.html",context)

@login_required(login_url="login")
def watch_later(request):
    uid=request.session["userID"]
    user=user_reg.objects.get(user__id=uid)
    my_list=watchlater.objects.filter(user_id_id=user.id)
    my_list_count=watchlater.objects.filter(user_id_id=user.id).count()

    context={
        "my_list":my_list,
        "my_list_count":my_list_count,
    }
        
    return render(request,"watch-later.html",context)

def watch_later_add(request,id):
    uid=request.session["userID"]
    user=user_reg.objects.get(user__id=uid)
    check=watchlater.objects.filter(product_id=id,user_id=user)
    if not check:
        obj=watchlater.objects.create(product_id_id=id,user_id=user)
        obj.save()
    return redirect("productdetails" ,id)

def watch_later_delete(request,id):
    uid=request.session["userID"]
    user=user_reg.objects.get(user__id=uid)
    watchlater.objects.filter(product_id=id,user_id=user).delete()
    return redirect("productdetails",id)

def FaQ(request):
    return render(request,"faq.html")

def forgot(request):
    return render(request,"forgot.html")

def privacy(request):
    return render(request,"privacy.html")

@login_required(login_url="login")
def profile(request):
    # uid=""
    # user=""
    # cmtcount=""
    # reviewcount=""
    # reviews=""
    if request.session["userID"]:
        uid=request.session["userID"]
        user=user_reg.objects.get(user__id=uid)
        cmtcount=comments.objects.filter(user_id_id=user).count()
        reviewcount=rating.objects.filter(user_id_id=user).count()
        reviews=rating.objects.filter(user_id_id=user)
    

    if 'profileupdate' in request.POST:
        username=request.POST['username']
        update=user_reg.objects.get(user__id=uid)

        if username:
            update.user_full_name=username
            update.save()
        if 'image' in request.FILES: 
            image = request.FILES['image']
            update.img = image
            update.save()
            
        return HttpResponseRedirect(reverse("profile"))



    context={
        "custom_user":user,
        "cmtcount":cmtcount,
        "reviewcount":reviewcount,
        "reviews":reviews
    }
        
        
    
    return render(request,"profile.html",context)





