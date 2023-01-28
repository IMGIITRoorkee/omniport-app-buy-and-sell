import datetime
import swapper

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from kernel.managers.get_role import get_role

from formula_one.models.base import Model
from formula_one.mixins.period_mixin import PeriodMixin
from formula_one.mixins.report_mixin import ReportMixin
from buy_and_sell import constants




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

    # For rental, this field will store renting rate (per day)
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

    is_rental = models.BooleanField(
        default=False,
    )

    periodicity = models.CharField(
        max_length=10,
        choices=constants.PERIODICITY,
        default=constants.LIFESPAN,
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

    # If the product is for rent, this field will store maximum renting period, 
    # else, stores warranty detail.
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

    # If the product is for rent, stores the security deposit, 
    # else stores default value (i.e. 0)
    security_deposit = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000000)
        ]
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

    def has_reported(self, person):
        """
        Return whether the person has reported the object or not
        :param person: the person whose report status is being checked
        :return: True if the person has reported the object, False otherwise
        """

        if person in self.reporters.all():
            return True
        return False

    def toggle_report(self, person):
        """
        Toggle the report status of the given object for the given person
        :param person: the person toggling his report against the object
        """

        reported = False
        if person in self.reporters.all():
            self.reporters.remove(person)
        else:
            reported = True
            self.reporters.add(person)
        self.save()
        if reported:
            if get_role(person, "Maintainer", silent=True):
                self.delete()

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

    def has_reported(self, person):
        """
        Return whether the person has reported the object or not
        :param person: the person whose report status is being checked
        :return: True if the person has reported the object, False otherwise
        """

        if person in self.reporters.all():
            return True
        return False

    def toggle_report(self, person):
        """
        Toggle the report status of the given object for the given person
        :param person: the person toggling his report against the object
        """

        reported = False
        if person in self.reporters.all():
            self.reporters.remove(person)
        else:
            reported = True
            self.reporters.add(person)
        self.save()
        if reported:
            if get_role(person, "Maintainer", silent=True):
                self.delete()

