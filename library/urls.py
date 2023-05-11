from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from myApp import views
from django.contrib.auth.views import LoginView,LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls') ),
    path('', views.home_view),

#after clicking button for admin/student
    path('adminclick', views.adminclick_view),
    path('studentclick', views.studentclick_view),
#signup page
    path('adminsignup', views.adminsignup_view),
    path('studentsignup', views.studentsignup_view),
#login page
    path('adminlogin', LoginView.as_view(template_name='adminlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='studentlogin.html')),
    path('logout', LogoutView.as_view(template_name='index.html')),
#dashboard display
    path('afterlogin', views.afterlogin_view),

#adding and viewing book
    path('addbook', views.addbook_view),
    path('viewbook', views.viewbook_view),

#issuing and view issued book by admin
    path('issuebook', views.issuebook_view),
    path('viewissuedbook', views.viewissuedbook_view),
#student viewing books borrowed by them
    path('viewissuedbookbystudent', views.viewissuedbookbystudent),

#studet viewing available books
   path('studentviewbook', views.studentviewbook_view),
#admin view students in system
   path('viewstudent', views.viewstudent_view),
]

