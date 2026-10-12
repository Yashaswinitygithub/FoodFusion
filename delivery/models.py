from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Restaurant(models.Model):
    name = models.CharField(max_length=100)

    picture = models.URLField(
        max_length=500,
        default='https://cdn-icons-png.flaticon.com/256/6643/6643359.png'
    )

    cuisine = models.CharField(max_length=200)

    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Item(models.Model):

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='items'
    )

    name = models.CharField(max_length=100)

    description = models.CharField(max_length=300)

    price = models.FloatField()

    vegeterian = models.BooleanField(default=False)

    picture = models.URLField(
        max_length=500,
        default='https://www.indiafilings.com/learn/wp-content/uploads/2024/08/How-to-Start-Food-Business.jpg'
    )

    def __str__(self):
        return self.name


class Cart(models.Model):

    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    def total_price(self):
        return sum(
            cart_item.item.price * cart_item.quantity
            for cart_item in self.cart_items.select_related('item')
        )

    def __str__(self):
        return self.customer.username + "'s Cart"


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'item')

    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"