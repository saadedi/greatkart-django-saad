from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.
class Product(models.Model):
    product_name   = models.CharField(max_length=200, unique=True)
    slug           = models.SlugField(max_length=200, unique=True)
    description    = models.TextField(max_length=500, blank=True)
    price          = models.IntegerField()
    images         = models.ImageField(upload_to='photos/products')
    stock          = models.IntegerField()
    is_available   = models.BooleanField(default=True)
    category       = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    created_date   = models.DateTimeField(auto_now_add=True)
    modified_date  = models.DateTimeField(auto_now=True)
    
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name

class VariationManger(models.Manager): # this is used to filter the color and size
    def colors(self):
        return super(VariationManger, self).filter(variation_category='color', is_active=True) # this is used to filter the color
    
    def sizes(self):
        return super(VariationManger, self).filter(variation_category='size', is_active=True) # this is used to filter the size

variation_category_choice =(  # this is used to select the variation category 
    ('color', 'color'),
    ('size', 'size'),
)
    
class Variation(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)# product is the parent
    variation_category  = models.CharField(max_length=100, choices=variation_category_choice) # color or size
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now_add=True)
    
    
    objects = VariationManger() # this is used to filter the color and size
    
    def __str__(self): # this is used to display the variation value in the admin panel
        return self.variation_value
    
    
    