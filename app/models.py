from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    # slug: 文字、ハイフン、数字、アンダースコアだけを含んだ文字列でURLの一部に使用
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    
    def __str__(self):
        return self.title