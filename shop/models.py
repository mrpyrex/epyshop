from django.db import models
from django.utils import timezone
from django.urls import reverse
from PIL import Image
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        unique_together = ('slug', 'parent',)

    def __str__(self):
        return self.name


    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.name]                  # post.  use __unicode__ in place of
                                                 # __str__ if you are using python 2
        k = self.parent

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(db_index=True)
    image = models.ImageField(upload_to='products/', blank=True)
    image_1 = models.ImageField(blank=True, null=True, upload_to='products/')
    image_2 = models.ImageField(blank=True, null=True, upload_to='products/')
    image_3 = models.ImageField(blank=True, null=True, upload_to='products/')
    image_4 = models.ImageField(blank=True, null=True, upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_cat_list(self):           #for now ignore this instance method,
        k = self.category
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent

        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
