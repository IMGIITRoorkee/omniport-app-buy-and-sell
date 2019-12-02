import swapper

from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo


class Picture(Model):
    """
    This model stores one image of a product
    """

    product = models.ForeignKey(
        to='SaleProduct',
        on_delete=models.CASCADE,
    )

    picture = models.ImageField(
        upload_to=UploadTo('buy_and_sell', 'product_pictures'),
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        name = self.picture.name
        product = self.product

        return f'{name}: {product}'
