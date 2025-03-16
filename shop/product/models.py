from django.db import models


class Category(models.Model):
    """
    Represents a category in the system.

    Each category can have a parent category, allowing for hierarchical structures.
    If a parent category is deleted, the parent field of its children will be set to NULL.
    """
    title = models.CharField(max_length=20, verbose_name='Category Title', help_text='Enter the title of the category.')
    parent = models.ForeignKey('self',
                                  on_delete=models.SET_NULL,
                                    blank=True,
                                    null=True,
                                     verbose_name='Parent Category',
                                     help_text='Select a parent category (optional).'
                                     
                                      )    
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"





