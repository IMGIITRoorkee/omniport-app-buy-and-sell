from django.db import models

from formula_one.models.base import Model


class PaymentMode(Model):
    """
    Model for listing the payment methods available
    """

    name = models.CharField(
        max_length=127,
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        name = self.name

        return f'{name}'
