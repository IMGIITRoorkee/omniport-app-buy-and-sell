import datetime
import swapper

from django.db import models

from kernel.models.root import Model
from kernel.mixins.period_mixin import PeriodMixin

class AbstractProduct(PeriodMixin, Model):
    """
    Abstract model that includes all the basic information neded for a product
    """
    
    person = models.ForeignKey(
        to=swapper.get_model_name('kernel', 'Person'),
        on_delete=models.CASCADE,
    )
    
    name = models.CharField(
        max_length=127,
    )

    cost = models.IntegerField()

    category = models.ForeignKey(
        to='categories.Category',
        on_delete=models.SET_NULL,
        null=True,
    )

    is_phone_visible = models.BooleanField(
        default=False,
    )

    class Meta:
        """
        Meta class for AbstractProduct
        """
        
        abstract = True

    def save(self, *args, **kwargs):
        """
        Set the start date and defer to the save() of the superclass
        """

        self.start_date = datetime.datetime.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        name = self.name
        person = self.person
        
        return f'{name}: {person}'

    
class SaleProduct(AbstractProduct):
    """
    This model stores the products for sale
    """
    
    details = models.TextField(
        blank=True,
    )
    
    warranty_detail = models.TextField(
        blank=True,
    )

    payment_modes = models.ManyToManyField(
        to='PaymentMode',
    )


class RequestProduct(AbstractProduct):
    """
    This model stores the products requested
    """

    pass
