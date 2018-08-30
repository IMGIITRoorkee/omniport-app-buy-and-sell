import swapper

from django.db import models

from kernel.models.root import Model
from buy_and_sell.constants import *


class Photo(Model):
    """
    Model for Storing the images of Products
    """
        
    product_id = models.ForeignKey(
        SaleProduct,
        on_delete=models.CASCADE,
    )
    
    picture = models.ImageField(
        upload_to = self.photo_directory_path,
    )

    def photo_directory_path(instance, filename):
    
        ext = filename.split('.')[-1]
        
        return (f'BuyAndSellPhoto/{instance.product_id}\
        _{instance.image_id}.{ext}')
        
    def __str__(self):
        """
        Return the name of the product image
        """
        
        return f'{self.picture.name}'


class AbstractProduct(PeriodMixin, Model):
    """
    Abstract model that includes all the basic
    information neded for a product
    """
    
    person = models.ForeignKey(
        to = swapper.get_model_name('kernel', 'Person'),
    )
    
    name = models.CharField(
        max_length = char_max_length,
    )

    cost = models.IntegerField()

    category = models.ForeignKey(
        to = Category,
    )

    sub_category = models.ForeignKey(
        to = SubCategory,
        blank = True,
    )

    add_phone = models.BooleanField(
        default = 0,
    )
    
    def __str__(self):
        """
        Return the name of the Product
        """
        
        return f'{self.name}'

    class Meta:
        """
        Meta class for AbstractProduct
        """
        
        abstract = True

    
class SaleProduct(AbstractProduct):
    """
    Model for storing the products for sale
    """
    
    details = models.TextField()
    
    warranty_detail = models.TextField(
        blank = True,        
    )
    
    payment_modes = models.ManyToManyField(
        to = BuyAndSellPayment,
        blank = True,
    )
    

class RequestProduct(AbstractProduct):
    """
    Model for storing the products requested
    """
    
    def __str__(self):
        """
        Return the name of the SaleProduct
        """
        
        return f'{self.name}'

class BuyAndSellPayment(Model):
    """
    Model for listing the payment methods available
    """
    
    name = model.CharField(
        max_length = char_max_length,
        required = True,
    )
    
    def __str__(self):
        """
        Return the name of the payment mode
        """
        return f'{self.name}'

class Category(Model):
    """
    Model for listing the categories of the products
    """
    
    name = models.CharField(
        max_length = char_max_length,
    )

    users = models.ManyToManyField(
        to = swapper.get_model_name('kernel', 'Person'),
        blank=True,
    )    
    
    def __str__(self):
        """
        Return the name of the Category
        """
        
        return f'{self.name}'
        

class SubCategory(Model):
    """
    Model for listing the categories of the products
    """
    
    name = models.CharField(
        max_length = char_max_length,
    )
            
    main_category = models.ForeignKey(
        to = Category,
        on_delete = CASCADE,        
    )    

    users = models.ManyToManyField(
        to = swapper.get_model_name('kernel', 'Person'),
        blank=True,
    )
y