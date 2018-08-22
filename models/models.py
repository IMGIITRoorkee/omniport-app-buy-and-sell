import swapper

from django.db import models

from kernel.models.root import Model

class Photo(Model):
        
    product_id = models.ForeignKey(
        SaleItems,
        on_delete=models.CASCADE,
    )
    
    picture = models.ImageField(
        upload_to = self.photo_directory_path,
    )

    def photo_directory_path(instance, filename):
    
        ext = filename.split('.')[-1]
        
        return (f'BuyAndSellPhoto/{instance.product_id}_
            {instance.image_id}.{ext}')
        
    def __str__(self):
        """
        Return the name of the product image
        """
        
        return f'{self.picture.name}'


class Product(Model):
    
    user = models.ForeignKey(
        to = swapper.get_model_name('kernel', 'Student'),
    )
    
    name = models.CharField(
        max_length = 127,
    )
    
    cost = models.IntegerField()
    
    detail = models.TextField()

    contact = models.CharField(
        max_length = 127,
    )
    
    post_date = models.DateField()

    expiry_date = models.DateField()
    
    email = models.EmailField()
    
    category = models.ForeignKey(
        to = Category
    )
    
    warranty_detail = models.TextField(
        blank = True,        
    )
    
    payment_modes = models.ManyToManyField(
        to = BuyAndSellPayment,
        blank = True,
    )
    
    is_active = models.BooleanField(
        default = True
    )
    
    def __str__(self):
        """
        Return the name of the product
        """
        
        return f'{self.name}'


class BuyAndSellPayment(Model):
    
    name = model.CharField(
        max_length = 127,
        required = True,
    )
    
    def __str__(self):
        """
        Return the name of the payment mode
        """
        return f'{self.name}'

class Category(Model):
    
    users = models.ManyToManyField(
        to = swapper.get_model_name('kernel', 'Student'),
        blank=True,
    )
        
    main_category = models.CharField(
        max_length=127,
    )

    name = models.CharField(
        max_length=127,
    )
        
    code = models.CharField(
        max_length=127,
        unique=True,
    )
    
    def __str__(self):
        """
        Return the name of the Category
        """
        
        return f'{self.name}'