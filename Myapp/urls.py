from django.urls import path
from Myapp import views


urlpatterns = [
    path('',views.homepage,name='home'),
    path('adminindex/',views.adminindex,name='adminindex'),
    path('additem/',views.adminadditem,name='adminadditem'),
    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('admincatalog/',views.admincatalog,name='admincatalog'),
    path('admincatalog_delete/<id>',views.admincatalog_delete,name='admincatalog_delete'),
    path('admincomments/',views.admincomments,name='admincomments'),
    path('admincomments_delete/<id>',views.admincomments_delete,name='admincomments_delete'),
    path('adminreviews/',views.adminreviews,name='adminreviews'),
    path('adminreview_delete/<id>',views.adminreview_delete,name='adminreview_delete'),
    path('adminusers/',views.adminusers,name='adminusers'),
    path('usernavandfoot/',views.usernavandfoot,name='usernavandfoot'),
    path('movie_list/<genre>',views.movie_list,name='movie_list'),
    path('search/',views.search,name='search'),
    path('filter/',views.filter,name='filter'),
    path('about/',views.about,name='about'),
    path('contacts/',views.contacts,name='contacts'),
    path('productdetails/<id>',views.productdetails,name='productdetails'),
    path('FaQ/',views.FaQ,name='FaQ'),
    path('forgot/',views.forgot,name='forgot'),
    path('privacy/',views.privacy,name='privacy'),
    path('profile/',views.profile,name='profile'),
    path('login/',views.user_login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('watch_later_add/<int:id>',views.watch_later_add,name='watch_later_add'),
    path('watch_later_delete/<int:id>',views.watch_later_delete,name='watch_later_delete'),
    path('watch_later/',views.watch_later,name='watch_later'),


]