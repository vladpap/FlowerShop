from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers


class Client(models.Model):
    first_name = models.CharField(
        'Имя',
        max_length=50,
        db_index=True)
    
    last_name = models.CharField(
        'Фамилия',
        max_length=50,
        db_index=True)
        
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
    
    is_florist = models.BooleanField(
        'Флорист',
        default=None,
        null=True,
        blank=True
    )

    is_courier = models.BooleanField(
        'Курьер',
        default=None,
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name='Пользователь'
        verbose_name_plural='Пользователи'


    def __str__(self):
        return f'{self.first_name} {self.last_name}{self.phone}{self.adress}'


    def get_client(tg_id):
        client = Client.objects.filter(telegram_id=tg_id).first()
        if client:
            return {
                'name': client.first_name,
                'phone': phonenumbers.format_number(
                         client.phone,
                         phonenumbers.PhoneNumberFormat.E164),
                'adress': client.adress}
        else:
            return None


