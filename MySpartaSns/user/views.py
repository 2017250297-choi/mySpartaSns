from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model  # 사용자가 데이터베이스에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        pw1 = request.POST.get('password', '')
        pw2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')
        if pw1 != pw2:
            return render(request, 'user/signup.html', {'error': '패스워드 확인해주세요'})
        if not (username or pw1):
            return render(request, 'user/signup.html', {'error': '이름과 비밀번호입력해주세요'})

        exsisting_user = get_user_model().objects.filter(username=username)
        if exsisting_user:
            return render(request, 'user/signup.html', {'error': '이미 존재하는 사용자입니다'})
        # new_user = UserModel()
        # new_user.username = username
        # new_user.password = pw1
        # new_user.bio = bio
        # new_user.save()
        UserModel.objects.create_user(username=username, password=pw1, bio=bio)
        return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        return render(request, 'user/signin.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        pw = request.POST.get('password', '')
        if not (username and pw):
            return render(request, 'user/signin.html', {'error': 'input ID and PW'})
        me = auth.authenticate(request, username=username, password=pw)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return redirect('/sign-in/')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
# user/views.py


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')
