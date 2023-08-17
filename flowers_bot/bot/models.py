from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь')
        
    telegram_id = models.CharField(
        'Telegram id',
        max_length=50,
        db_index=True)

    phone = PhoneNumberField(
        'Номер телефона',
        null=True,
        blank=True)
    
    adress = models.CharField(
        'Адрес',
        max_length=50,
        null=True,
        blank=True)
    
    
    class Meta:
        verbose_name='Пользователя'
        verbose_name_plural='Пользователи'


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}{self.phone}{self.adress}'


    def get_client(tg_id):
        client = Client.objects.filter(telegram_id=tg_id).first()
        if client:
            return {
                'name': client.user.first_name,
                'phone': phonenumbers.format_number(
                         client.phone,
                         phonenumbers.PhoneNumberFormat.E164),
                'adress': client.adress}
        else:
            return None


class Event(models.Model):
    title = models.CharField(
        'Событие',
        max_length=25)
    
    class Meta:
        verbose_name='Событие'
        verbose_name_plural='События'
       
    def __str__(self):
        return f'{self.title}'


class Catalog(models.Model):
    title = models.CharField(
        'Букет',
        max_length=25,
        db_index=True)
    
    description = models.TextField('Описание')

    composition = models.TextField('Состав букета',)

    photo = models.ImageField(
        'Изображение',
        upload_to='flowers_img')
    
    price = models.DecimalField(
        'Цена',
        max_digits=7,
        decimal_places=2)
    
    event = models.ManyToManyField(Event)

    class Meta:
        verbose_name='Букет'
        verbose_name_plural='Букеты' 


    def __str__(self):
        return f'{self.title},{self.price} р.'
    

class Consultation(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Клиент',
        related_name='client_consultation_set')
    
    florist = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Флорист',
        related_name='florist_consultation_set')
    
    class Meta:
        verbose_name='Консультацию'
        verbose_name_plural='Консультации'

    def __str__(self):
        return f'{self.client}, {self.florist}'
    

class Order(models.Model):
    bouquet = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Букет',
        related_name='orders',
        blank=True)
    
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Клиент',
        related_name='client_order_set')
    
    delivery_date = models.DateField(verbose_name='Дата доставки')

    CHOICE = (
        ('AM', '11:00 - 15:00'),
        ('PM', '15:00 - 20:00'),
    )

    delivery_time = models.CharField(
        verbose_name='Время доставки',
        max_length=20,
        choices=CHOICE,
        default='PM')
    
    courier = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Курьер',
        related_name='courier_order_set')

    class Meta:
        verbose_name='Заказ'
        verbose_name_plural='Заказы'

    def __str__(self):
        return f'{self.client}, {self.delivery_date} {self.delivery_time}{self.courier}'