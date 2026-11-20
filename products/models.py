from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=120)
    description = models.TextField(blank=True)
    image_url = models.CharField(max_length=500, blank=True)
    icon = models.CharField(max_length=50, blank=True, default='fa-gem')
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    how_to_use = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    main_image = models.CharField(max_length=500)
    hover_image = models.CharField(max_length=500, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    review_count = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=50)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    badge_text = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int(round(((self.original_price - self.price) / self.original_price) * 100))
        return 0

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def star_full_count(self):
        return int(round(float(self.rating)))


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.product.title}"


class ProductShade(models.Model):
    product = models.ForeignKey(Product, related_name='shades', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color_hex = models.CharField(max_length=20, default="#B76E79")
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.title} - {self.name}"


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='product_reviews', null=True, blank=True, on_delete=models.SET_NULL)
    author_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.author_name} for {self.product.title}"
