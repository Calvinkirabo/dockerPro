from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms,models
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import date

#landing page
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'index.html')

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'studentclick.html')

#for showing signup/login button for librarian
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'adminclick.html')

#admin_signup
def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'adminsignup.html',{'form':form})
#student_signup
def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'studentsignup.html',context=mydict)

#dashboards
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'adminafterlogin.html')
    else:
        return render(request,'studentafterlogin.html')

#admin adding a new book
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)

def addbook_view(request):
    #now it is empty book form for sending to html
    form=forms.BookForm()
    if request.method=='POST':
        #now this form has data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'bookadded.html')
    return render(request,'addbook.html',{'form':form})

#admin view available books
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books=models.Book.objects.all()
    return render(request,'viewbook.html',{'books':books})


#issuing a book
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'bookissued.html')
    return render(request,'issuebook.html',{'form':form})

#borrowed books
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.expirydate)
        print(date.today())
        d=days.days
        fine=0
        if d ==3:
            fine=5000
        elif d == 10:
            fine=15000
        elif d <= 0:
            fine=0
        else:
            fine=d*1500

        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'viewissuedbook.html',{'li':li})


#student view borrowed books
@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1=[]
    li2=[]

    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,book.name,book.author)
            li1.append(t)

        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        
        #fine calculation

        days=(date.today()-ib.expirydate)
        print(date.today())
        d=days.days
        fine=0
        if d ==3:
            fine=5000
        elif d == 10:
            fine=15000
        elif d <= 0:
            fine=0
        else:
            fine=d*1500
        t = (issdate,expdate,fine)
        li2.append(t)
    return render(request,'viewissuedbookbystudent.html',{'li1':li1,'li2':li2})

#student view available books in library

@login_required(login_url='studentlogin')
def studentviewbook_view(request):
    books=models.Book.objects.all()
    return render(request,'studentviewbook.html',{'books':books})

#seeing available students in system
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'viewstudent.html',{'students':students})
