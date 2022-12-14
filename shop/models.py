from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields


# Create your models here.


class Category(TranslatableModel):

    # make another table for these fields
    # and have multiple value for each field
    # depend on the language
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=AutoSlugField(unique=True)
    )

    class Meta:
        # can't order translations fields
        # You can filter by translated fields in queries
        # ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(TranslatableModel):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=AutoSlugField(db_index=True, max_length=200),
        description=models.TextField(blank=True)
    )

    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # can't order translations fields
    # You can filter by translated fields in queries
    # also does not provide support
    # to validate index_together
    # class Meta:
    #   ordering = ('name',)
    #   index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
