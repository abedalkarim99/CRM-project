from django.db import models


class Customer(models.Model) :
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model) :
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),

    )
    name = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.CharField(max_length=100 , choices=CATEGORY)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name



class Order(models.Model) :
    STATUS = (
        ('Pending' , 'Pending'),
        ('Out for delivary' , 'Out for delivary'),
        ('Delivered' , 'Delivered'),

    )
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL ,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date_created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100,choices=STATUS)
    note = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.customer.name

