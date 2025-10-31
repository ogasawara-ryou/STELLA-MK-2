from django.db import models
from django.urls import reverse
from .account_models import User
from .utils import create_id, upload_image_to


class Tag(models.Model):
    slug = models.CharField(max_length=32, primary_key=True) #要らない
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Category(models.Model):
    slug = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Item(models.Model):
    id = models.CharField(default=create_id, primary_key=True,
                          max_length=22, editable=False)
    name = models.CharField(default='題名　(作成者名)', max_length=50)
    description = models.TextField(default='説明文', blank=False) #true→false
    is_published = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latest_author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(
        default="", blank=True, upload_to=upload_image_to)


    def __str__(self):
        return self.name
    
    # 新規作成・編集完了時のリダイレクト先
    def get_absolute_url(self):
        return reverse('list')
    
class Bookmark(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, related_name='bookmarked_users', null=True, blank=True)
    item=models.ForeignKey(Item,on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "ブックマーク"
        verbose_name_plural = "ブックマーク一覧"

    def __str__(self):
        return f"{self.user.username} / {self.item.name}" 
        



    


