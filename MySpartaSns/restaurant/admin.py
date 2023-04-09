from django.contrib import admin
from .models import MyTopping, MyPizza

# Register your models here.
admin.site.register(MyTopping)
admin.site.register(MyPizza)  # 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다
