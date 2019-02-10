import datetime
import swapper

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from kernel.models.root import Model
from kernel.mixins.period_mixin import PeriodMixin
from kernel.mixins.report_mixin import ReportMixin


class AbstractProduct(PeriodMixin, ReportMixin, Model):
    """
    Abstract model that includes all the basic information needed for a product
    """

    person = models.ForeignKey(
        to=swapper.get_model_name('kernel', 'Person'),
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=127,
    )

    cost = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000000)
        ]
    )

    category = models.ForeignKey(
        to='categories.Category',
        on_delete=models.SET_NULL,
        null=True,
    )

    is_phone_visible = models.BooleanField(
        default=False,
    )

    @property
    def feed_person(self):
        """
        Return the person behind this entry to be displayed on the feed item
        :return: the person behind this entry to be displayed on the feed item
        """

        return self.person

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

    reporters = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Person'),
        related_name='reported_sale_products',
        blank=True,
    )

    @property
    def feed_text(self):
        """
        Return the display text for the attached feed item
        :return: the display text for the attached feed item
        """

        return f'Added {self.name} for sale.'

    @property
    def feed_url(self):
        """
        Return the URL to which the attached feed item should point
        :return: the URL to which the attached feed item should point
        """

        return f'/buy_and_sell/buy/{self.id}'

    @property
    def feed_image(self):
        """
        Return the display image for the attached feed item
        :return: the display image for the attached feed item
        """

        picture_url = '/static/buy_and_sell/assets/default-image.svg'
        picture = self.picture_set.all()
        if picture:
            picture_url = picture[0].picture.url
        return picture_url


class RequestProduct(AbstractProduct):
    """
    This model stores the products requested
    """

    reporters = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Person'),
        related_name='reported_request_products',
        blank=True,
    )

    @property
    def feed_text(self):
        """
        Return the display text for the attached feed item
        :return: the display text for the attached feed item
        """

        return f'Requested for {self.name}.'

    @property
    def feed_url(self):
        """
        Return the URL to which the attached feed item should point
        :return: the URL to which the attached feed item should point
        """

        return f'/buy_and_sell/request/{self.id}'

    @property
    def feed_image(self):
        """
        Return the display image for the attached feed item
        :return: the display image for the attached feed item
        """

        return None
