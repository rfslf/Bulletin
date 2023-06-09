from django.contrib import admin

# Register your models here.
from .models import Bulletin, Category, Reply


class BulletinAdmin(admin.ModelAdmin):
    # list_display - это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('id', 'header', 'body', 'author', 'category_name')
    list_filter = ('category_name', 'author')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('header',)  # тут всё очень похоже на фильтры из запросов в базу

admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Reply)
admin.site.register(Category)