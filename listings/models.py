from django.db import models
from django.utils.timezone import now


class Listing(models.Model):
    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale'
        FOR_RENT = 'For Rent'

    class HomeType(models.TextChoices):
        HOUSE = 'House'
        CONDO = 'Condo'
        TOWNHOUSE = 'Townhouse'


    realtor = models.EmailField(max_length=100)
    title = models.CharField(max_length=255)
    slug = models.SlugField( unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField()

    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    bedrooms = models.IntegerField()

    sale_type = models.CharField(max_length=20, choices=SaleType.choices, default=SaleType.FOR_SALE)
    home_type = models.CharField(max_length=20, choices=HomeType.choices, default=HomeType.HOUSE)

    main_photo = models.ImageField(upload_to='listings/')
    photo_1 = models.ImageField(upload_to='listings/')
    photo_2 = models.ImageField(upload_to='listings/')
    photo_3 = models.ImageField(upload_to='listings/')

    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)


    def delete(self):
        self.main_photo.storage.delete(self.main_photo.name)
        self.photo_1.storage.delete(self.photo_1.name)
        self.photo_2.storage.delete(self.photo_2.name)
        self.photo_3.storage.delete(self.photo_3.name)
        super().delete()
        
    def __str__(self):
        return self.title