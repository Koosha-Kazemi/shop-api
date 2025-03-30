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


class OptionGroup(models.Model):
    """
    Represents a group of options that can be associated with products or other entities.
    
    Attributes:
        title (str): The title of the option group (e.g., "Color", "Size").
    """
    
    title = models.CharField(max_length=40,
                             verbose_name='Option group title',
                             help_text='Select the option values for this group.',
                             unique=True)
    
    def __str__(self):
        return self.title
    

    class Meat:
        verbose_name = 'Option group'
        verbose_name_plural = 'Option groups' 


class OptionValue(models.Model):
    """
    Represents a specific value within an option group.

    This model is used to store individual values that belong to an option group.
    For example, if the option group is "Color", the values could be "Red", "Blue", etc.

    Attributes:
        value (str): The specific value of the option (e.g., "Red", "Large").
        option_group (OptionGroup): The group to which this value belongs.
    """
    
    value = models.CharField(
        max_length=30,  
        verbose_name='Option Value',  
        help_text='Enter the specific value for this option (e.g., "Red", "Large").', 
    )
        
    option_group = models.ForeignKey(
        OptionGroup,  
        related_name='option_values',  
        on_delete=models.CASCADE, 
        verbose_name='Option Group', 
        help_text='Select the option group to which this value belongs.',  
    )

    def __str__(self):

        return f"{self.value} ({self.option_group.title})"
    

class ProductAttribute(models.Model):
    """
    Represents an attribute option association between a Product and an OptionGroup.
    
    This model links products to their configurable option groups (like color, size etc.),
    establishing a many-to-one relationship between products and available options.
    
    Attributes:
        product (ForeignKey): Reference to the Product this attribute belongs to.
                             Related name 'product_attributes' allows accessing all
                             attributes of a product through reverse relation.
        option_group (ForeignObject): Reference to the OptionGroup that defines the
                                    available choices for this attribute. Related name
                                    'option_group' allows reverse lookup from OptionGroup.""
    """
    
    proudct = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attributes')
    option_group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE, related_name='option_group_attribiute')

    def __str__(self):
        return f'{self.proudct.name}'


def product_image_path(instance, filename):
    return f'products/{instance.product.id}/images/{filename}'


class ProductImage(models.Model):
    """
    Represents an image associated with a product in the e-commerce system.
    
    Stores product images with metadata and provides organization through:
    - Automatic path-based storage
    - Timestamp tracking
    - Activation control
    - Display ordering

    Attributes:
        product (ForeignKey): The product this image belongs to
        image (ImageField): The image file with dynamic path generation
        created_at (DateTimeField): Date/time when the image was first uploaded
        updated_at (DateTimeField): Date/time when the image was last modified
        is_active (BooleanField): Controls whether the image is visible in storefront
        index (PositiveIntegerField): Determines display order in product galleries
    """
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_images', 
        verbose_name='Product'
    )
    image = models.ImageField(
        upload_to=product_image_path,
        verbose_name='Image File'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Updated'
    )
    index = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order',
        help_text='Determines sorting order in image galleries (lower numbers show first)'
    )

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ('index',)

    def __str__(self):
        return f"Image {self.id} for {self.product.name} ({'active' if self.is_active else 'inactive'})"


