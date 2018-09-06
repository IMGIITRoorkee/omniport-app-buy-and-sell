import swapper

from django.db import models

from kernel.models.root import Model

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel, Model):
    """
    Model for listing the categories and subcategories of the products
    """

    name = models.CharField(
        max_length=127,
        unique=True
    )

    users = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Person'),
        blank=True,
    ) 

    parent_category = TreeForeignKey(
        to='self', 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategory'
    )

    class Meta:
        """
        Meta class for Category
        """

        verbose_name_plural = 'categories'
    
    class MPTTMeta:
        parent_attr = 'parent_category'

    def __str__(self):
        """
        Return the name of the category or subcategory
        """

        return f'{self.name}'
