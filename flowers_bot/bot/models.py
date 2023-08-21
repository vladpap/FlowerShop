from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers
from django.contrib.auth.models import User
from PIL import Image, ImageOps, ImageDraw, ImageFont


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
    
    
    def get_event(id):
        definite_event = Event.objects.get(id=id)
        event = f'{definite_event.title}'

        return event
        


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
        return f'{self.title},{self.description},{self.composition},{self.price} р.'
    

    def make_images_3x3_grid(imgs, id_imgs, border=0):
        cols = 3
        rows = len(imgs) // 3
        w, h = 900, 300 * rows
        grid = Image.new('RGB',
            size=(w + border * 2 ,  h + border * (rows - 1)),
            color=(200,200,200))
    
        if sys.platform == 'linux':
            font_name = 'arial.ttf'
        else:
            font_name = 'Helvetica'

        for i, img in enumerate(imgs):
            img_tmp = ImageOps.fit(img, size=(300, 300))
            draw_img = ImageDraw.Draw(img_tmp)
            draw_img.rectangle([0, 0, 60, 35], fill=(200,200,200))
            draw_img.text(
                        (10, 5),  # Coordinates
                        str(id_imgs[i]),  # Text
                        (0, 0, 0),  # Color
                        font=ImageFont.truetype(font=font_name, size=30))

            grid.paste(img_tmp,
                box=(i%cols*300 + (i%cols*border), i//cols*300 + (i//cols*border)))

        return grid


    def make_catalog(imgs, id_imgs):
        assert len(imgs) == len(id_imgs)

        catalog = []
    
        imgs_divide = divide(imgs, 9)
        id_imgs_divide = divide(id_imgs, 9)

        for index, imgs_element in enumerate(imgs_divide):
            catalog.append(
                {'img' : make_images_3x3_grid(imgs_element,
                                          id_imgs_divide[index],
                                          border=20),
                'id_imgs': id_imgs_divide[index]})

        return catalog


    def divide(lst: list, n: int):
        divide_list = []
        for i in range(0, len(lst), n):
            divide_list.append(lst[i:i+n])

        return divide_list


    def get_catalog():
        #catalog_base = Catalog.objects.all()
        #for image in catalog_base:
        #    images = image.photo
        images, id_list = Catalog.objects.values('photo', 'id')
        # id_list = Catalog.objects.values('id')
        catalog = make_catalog(images, id_list)

        return catalog
    

    def get_bouquet(id):
        bouquet = Catalog.objects.get(id=id)
        image = bouquet.photo
        description = f'<b>{bouquet.title}<b>\n' \
            f'{bouquet.description}\n' \
            f'{bouquet.composition}\n' \
            f'Цена: {bouquet.price} руб.'
        return {'image': image,
                'text': description}
    

    #def get_custom_bouquet(event):
    #    if chosen_price = #не важно
    #        bouquets=Catalog.objects.filter(event=event, price__gte=3000)
    #    elif chosen_price = #до 500
    #        bouquets=Catalog.objects.filter(event=event, price__lte=500)
    #    elif chosen_price = #до 100
    #        bouquets=Catalog.objects.filter(event=event, price__gte=500, price__lte=1000)
    
        
            
    

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
        null=True,
        blank= True,
        verbose_name='Курьер',
        related_name='courier_order_set')

    class Meta:
        verbose_name='Заказ'
        verbose_name_plural='Заказы'

    def __str__(self):
        return f'{self.client}, {self.delivery_date} {self.delivery_time}{self.courier}'
    

    def save_order(telegram_msg):
        if len(telegram_msg['name'].split()) > 1:
            first_name = telegram_msg['name'].split()[0]
            last_name = telegram_msg['name'].split()[1]
        else:
            first_name = telegram_msg['name']
            last_name = ''

        client = Client.objects.filter(telegram_id=telegram_msg['telegram_id']).first()

        if not client:
            user = User.objects.create(
                username=f'{first_name} {last_name}',
                first_name=first_name,
                last_name=last_name)

            client = Client.objects.create(
                user=user,
                telegram_id=telegram_msg['telegram_id'],
                phone=telegram_msg['phone'],
                adress=telegram_msg['address'])
            

        order = Order.objects.create(
            client=client,
            adress=telegram_msg['adress'],
            bouquet=telegram_msg['bouquet'],
            delivery_date=telegram_msg['delivery_date'],
            delivery_time=telegram_msg['delivery_time'])
        
        



            


