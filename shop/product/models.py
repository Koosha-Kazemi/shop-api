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








class Product(models.Model):
    """
    Represents a product in the system.

    Attributes:
        title (CharField): The title of the product.
        category (ForeignKey): The category of the product.
        price (DecimalField): The price of the product.
        price_discount (DecimalField): The discount percentage applied to the product's price.
        final_price_value (DecimalField): The final price after applying the discount.
        stock (PositiveIntegerField): The number of items available in stock.
        created_at (DateField): The date when the product was created.
        updated_at (DateField): The date when the product was last updated.
     """
    
    title = models.CharField(max_length=20, verbose_name='product Title', help_text='Enter the title of Product')
    category = models.ManyToManyField(Category, 
                                  verbose_name='Product Category',
                                  help_text='Select a category for product')
    

    price = models.DecimalField(max_digits=4,
                                 decimal_places=2,
                                 verbose_name= 'Product',
                                 help_text='Enter the price of product',
                                 default=0.00
                                 )
    
    price_discount = models.DecimalField(max_digits=4,
                                          decimal_places=2,
                                          verbose_name='discount of product\'s price',
                                          help_text='Enter the dicsount of product\'s price',
                                          default=0.00
                                          )
    
    final_price_value = models.DecimalField(
                                            max_digits=5,
                                            decimal_places=2,
                                            verbose_name='Final Price',
                                            help_text='The final price after applying the discount.',
                                            default=0.00
                                                      )
    
    stock = models.PositiveIntegerField(verbose_name='product\'s stock', 
                                        help_text='Enter the number of items in stock.', 
                                        default=0)
    
    created_at = models.DateTimeField(auto_now_add=True,
                                 verbose_name = 'Create at',
                                    )
    updated_at = models.DateTimeField(auto_now=True,
                                 verbose_name= 'Upadate at'
                                )
    
    @property
    def _final_price(self):
        """
          Calculate the final price after applying the discount.
        
        """

        if self.price_discount:
            return self.price - (self.price * self.price_discount/100)
        return self.price


    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        self.final_price_value = self._final_price
        return super().save(*args, **kwargs)
    

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products' 
