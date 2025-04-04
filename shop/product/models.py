from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Category(models.Model):
    """
    Represents a category in the system.

    Each category can have a parent category, allowing for hierarchical structures.
    If a parent category is deleted, the parent field of its children will be set to NULL.
    """
    title = models.CharField(
        max_length=50, 
        verbose_name='Category Title', 
        help_text='Enter the title of the category.',
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,
        help_text='URL-friendly version of the title'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Parent Category',
        help_text='Select a parent category (optional).',
        related_name='children'
    )
    description = models.TextField(
        blank=True,
        help_text='Brief description of the category'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Controls whether the category is visible in the storefront'
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent']),
        ]


class Product(models.Model):
    """
    Represents a product in the system.

    Attributes:
        title (CharField): The title of the product.
        slug (SlugField): URL-friendly version of the title.
        category (ManyToManyField): The categories this product belongs to.
        price (DecimalField): The base price of the product.
        price_discount (DecimalField): The discount percentage applied to the product's price.
        final_price_value (DecimalField): The final price after applying the discount.
        stock (PositiveIntegerField): The number of items available in stock.
        description (TextField): Detailed description of the product.
        is_active (BooleanField): Controls product visibility.
        created_at (DateTimeField): Creation timestamp.
        updated_at (DateTimeField): Last update timestamp.
    """
    
    title = models.CharField(
        max_length=100, 
        verbose_name='Product Title', 
        help_text='Enter the title of Product'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        help_text='URL-friendly version of the title'
    )
    category = models.ManyToManyField(
        Category, 
        verbose_name='Product Category',
        help_text='Select categories for product',
        related_name='products'
    )
    description = models.TextField(
        blank=True,
        help_text='Detailed description of the product'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Product Price',
        help_text='Enter the price of product',
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    
    price_discount = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name='Discount Percentage',
        help_text='Enter the discount percentage of product\'s price',
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    final_price_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Final Price',
        help_text='The final price after applying the discount.',
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    
    stock = models.PositiveIntegerField(
        verbose_name='Product Stock', 
        help_text='Enter the number of items in stock.', 
        default=0
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text='Controls whether the product is visible in the storefront'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
    
    @property
    def _final_price(self):
        """Calculate the final price after applying the discount."""
        if self.price_discount:
            return self.price - (self.price * self.price_discount/100)
        return self.price

    @property
    def has_stock(self):
        """Check if product has stock available."""
        return self.stock > 0

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.final_price_value = self._final_price
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]


class OptionGroup(models.Model):
    """
    Represents a group of options that can be associated with products or other entities.
    
    Attributes:
        title (str): The title of the option group (e.g., "Color", "Size").
        description (str): Optional description of the option group.
        is_active (bool): Controls whether the option group is available.
    """
    
    title = models.CharField(
        max_length=40,
        verbose_name='Option group title',
        help_text='Select the option values for this group.',
        unique=True
    )
    description = models.TextField(
        blank=True,
        help_text='Optional description of the option group'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Controls whether the option group is available'
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Option group'
        verbose_name_plural = 'Option groups'
        ordering = ['title']
        indexes = [
            models.Index(fields=['is_active']),
        ]


class OptionAttribute(models.Model):
    """
    Represents an option attribute that belongs to an option group.
    Attributes:
        title (CharField): The title of the option attribute, with a maximum length of 50 characters.
            - verbose_name: 'Option Attribute Title'
            - help_text: 'Enter the title of the option attribute.'
        option_group (ForeignKey): A foreign key relationship to the OptionGroup model.
    """
   
    title = models.CharField(
        max_length=50,
        verbose_name='Option Attribute Title',
        help_text='Enter the title of the option attribute.'
    )
    option_group = models.ForeignKey(
        OptionGroup,
        on_delete=models.CASCADE,
        verbose_name='Option Group',
        help_text='Select the option group this attribute belongs to.'
    )


class OptionValue(models.Model):
    """
    Represents a specific value within an option group.

    This model is used to store individual values that belong to an option group.
    For example, if the option group is "Color", the values could be "Red", "Blue", etc.

    Attributes:
        value (str): The specific value of the option (e.g., "Red", "Large").
        option_group (OptionGroup): The group to which this value belongs.
        is_active (bool): Controls whether the option value is available.
    """
    
    value = models.CharField(
        max_length=30,  
        verbose_name='Option Value',  
        help_text='Enter the specific value for this option (e.g., "Red", "Large").'
    )
    option_group = models.ForeignKey(
        OptionGroup,  
        related_name='option_values',  
        on_delete=models.CASCADE, 
        verbose_name='Option Group', 
        help_text='Select the option group to which this value belongs.'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Controls whether the option value is available'
    )

    def __str__(self):
        return f"{self.value} ({self.option_group.title})"
    
    class Meta:
        verbose_name = 'Option Value'
        verbose_name_plural = 'Option Values'
        unique_together = ['value', 'option_group']
        ordering = ['value']
        indexes = [
            models.Index(fields=['is_active']),
        ]


class ProductOptionGroup(models.Model):
    """
    Represents an attribute option association between a Product and an OptionGroup.
    
    This model links products to their configurable option groups (like color, size etc.),
    establishing a many-to-one relationship between products and available options.
    
    Attributes:
        product (ForeignKey): Reference to the Product this attribute belongs to.
        option_group (ForeignKey): Reference to the OptionGroup that defines the available choices.
        is_active (bool): Controls whether the attribute is available for the product.
    """
    
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='product_attributes'
    )
    option_group = models.ForeignKey(
        OptionGroup, 
        on_delete=models.CASCADE, 
        related_name='option_group_attribute'
    )
   

    def __str__(self):
        return f'{self.product.title} - {self.option_group.title}'
    
    class Meta:
        verbose_name = 'Product Attribute'
        verbose_name_plural = 'Product Attributes'
        unique_together = ['product', 'option_group']
        indexes = [
            models.Index(fields=['is_active']),
        ]


class ProductAttributeValue(models.Model):
    """
    Represents a value for a specific product attribute.
    Attributes:
        product (ForeignKey): A reference to the associated product. When the product is deleted, 
            all related ProductAttributeValue instances are also deleted. 
            Accessible via the `product_attribute_values` related name.
        option_value (ForeignKey): A reference to the selected option value for the product attribute. 
            When the option value is deleted, all related ProductAttributeValue instances are also deleted. 
            Accessible via the `option_value` related name. Displayed as 'Option Value' in the admin interface.
    """
    
    product = models.ForeignKey(Product, 
                                on_delete=models.CASCADE,
                                 related_name='product_attribute_values') 
    
    option_value = models.ForeignKey(OptionValue,
                                on_delete=models.CASCADE,
                                related_name='option_value',
                                verbose_name='Option Value',
    )


def product_image_path(instance, filename):
    """Generate a path for storing product images."""
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
        alt_text (CharField): Alternative text for accessibility
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
    alt_text = models.CharField(
        max_length=100,
        blank=True,
        help_text='Alternative text for accessibility'
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
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active Status',
        help_text='Controls whether the image is visible in storefront'
    )

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ('index',)
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['index']),
        ]

    def __str__(self):
        return f"Image {self.id} for {self.product.title} ({'active' if self.is_active else 'inactive'})"

