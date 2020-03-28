import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .usermanager import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField("First Name", max_length=255)
    surname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_deleted = models.BooleanField(_('deleted'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'first_name', 'email']

    def __str__(self):
        return self.first_name + " " + self.surname

    @classmethod
    def fetch(cls, username=None, user_id=None, is_superuser=False):
        try:
            if is_superuser is not None:
                user = cls.objects.filter(is_superuser=is_superuser)
            else:
                user = cls.objects.all()

            if username:
                user = user.filter(username=username).first()
            elif user_id:
                user = user.filter(id=user_id).first()

            return user
        except Exception as e:
            print("Exception occurs while fetching User: Error: {}".format(str(e)))
            return None


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female')
)
PURPOSE_CHOICES = (
    ('Comapny', 'Company'),
    ('individual', 'individual'),
    ('Family', 'Family')
)
OFFER_CHOICES = (
    ('Email', 'Via Email'),
    ('Letter', 'Via Letter'),
)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    offer_id = models.CharField(max_length=255, blank=True,
                                null=True)
    invoice_id = models.CharField(max_length=255, blank=True,
                                  null=True)
    street = models.CharField(max_length=500)
    postcode = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    mobile = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_deleted = models.BooleanField(_('deleted'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, null=True, blank=True)
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES, null=True, blank=True)

    @classmethod
    def create(cls, first_name, street, postcode, place, surname, phone, mobile, gender, purpose):
        try:
            customer = cls.objects.create(first_name=first_name, street=street, postcode=postcode, place=place,
                                          surname=surname, phone=phone, mobile=mobile, gender=gender, purpose=purpose)
            return customer
        except Exception as e:
            print("Exception occurs while creating Customer. Error: {}".format(str(e)))
            return None

    @classmethod
    def fetch(cls, customer_id=None, name=None):
        try:
            customer = cls.objects.all()
            if customer_id:
                customer = customer.filter(id=customer_id).last()

            if name:
                customer = customer.filter(first_name__contains=name)

            return customer
        except Exception as e:
            print("Exception occurs while fetching Customer. Error: {}".format(str(e)))
            return None

    def __str__(self):
        return self.first_name


class CallNotes(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='call_notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='call_notes')
    notes = models.CharField(max_length=1000)
    created = models.DateField(null=True)

    def save(self, *args, **kwargs):
        self.created = datetime.datetime.now()
        return super(CallNotes, self).save(*args, **kwargs)

    @classmethod
    def create(cls, customer_id, user_id, notes):
        try:
            call_notes = cls.objects.create(customer_id=customer_id, user_id=user_id, notes=notes)
            return call_notes

        except Exception as e:
            print("Exception occurs while creating Call Notes. Error: {}".format(str(e)))
            return None

    @classmethod
    def fetch(cls, customer_id):
        try:
            call_notes = cls.objects.filter(customer_id=customer_id)
            return call_notes

        except Exception as e:
            print("Exception occues while fetching Call Notes. Error: {}".format(str(e)))
            return None


class PurchaseRecord(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='purchase_records')
    watt = models.PositiveIntegerField(null=True, default=0)
    module_count = models.PositiveIntegerField(null=True, default=0)

    with_battery = models.BooleanField(blank=True, default=False, null=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    kwh = models.CharField(max_length=255, blank=True, null=True)
    manufacturer2 = models.CharField('Manufacturer', max_length=255, blank=True, null=True)
    kwh2 = models.CharField('Kw/H', max_length=255, blank=True, null=True)

    price_without_tax = models.FloatField(help_text="Price in Euro (€)", null=True,
                                          validators=[MinValueValidator(0, "Should be above 0")],
                                          default=0)

    offer_by = models.CharField(choices=OFFER_CHOICES, max_length=16, null=True)
    # OFFER INFORMATION
    offer_date = models.DateField(blank=True, null=True)
    reseller_name = models.CharField(max_length=255, null=True, blank=True)
    declined = models.BooleanField(default=False, null=True, blank=True)
    # TECHNICAL DETAILS
    date_sent = models.DateField('AG geschickt/AG Sent', null=True, blank=True)
    project_planning_created = models.BooleanField('Projektierung Erstellt',
                                                   blank=True, default=True)
    dc_term = models.DateField('DC Termin', blank=True, null=True)
    dc_mechanic = models.CharField(max_length=255, blank=True, null=True)
    ac_term = models.DateField('AC Termin', blank=True, null=True)
    ac_mechanic = models.CharField(max_length=255, blank=True, null=True)
    # INFORMATION FOR THE ROOF
    roof_type = models.CharField(max_length=255, null=True, blank=True)
    roof_tilt = models.FloatField(help_text="in Degrees", null=True, blank=True)
    alignment = models.CharField(max_length=64, null=True, blank=True)
    module_area = models.FloatField(help_text="Area in meter squared (m2)", null=True, blank=True,
                                    validators=[MinValueValidator(0, "Should be above 0")],
                                    default=0)

    extra_details = models.TextField(blank=True, null=True)

    # module_type = models.CharField(max_length=255)
    # memory_type = models.CharField(max_length=255)
    #
    # installation_date = models.DateTimeField()
    # cancellation = models.BooleanField(blank=True, default=True)
    # photo_roof_access = models.BooleanField(blank=True, default=True)
    # photo_counter_cabinet = models.BooleanField(blank=True, default=True)
    # video_counter = models.BooleanField(blank=True, default=True)
    # photo_of_counter = models.BooleanField(blank=True, default=True)
    # power_of_attorney = models.BooleanField(blank=True, default=True)
    # data_collection = models.BooleanField(blank=True, default=True)
    # order_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)

    @property
    def price_with_tax(self):
        return "%.2f" % (getattr(self, 'price_without_tax', 0) * 1.19)

    @property
    def kwp(self):
        return "%.4f" % (getattr(self, 'module_count', 0) * getattr(self, 'watt', 0) / 1000.0)

    @property
    def total_area(self):
        return "%.2f m^2" % self.price_without_tax * 1.19

    @classmethod
    def create(cls, customer_id, reseller_name, module_count, module_type, kwp, price_without_tax, price_with_tax,
               offer_created, cancellation, project_planning_created, installation_date, ac_date, photo_roof_area,
               photo_counter_cabinet, video_counter, photo_of_counter, power_of_attorney, data_collection,
               order_date, memory_type, with_battery):
        try:
            if not installation_date:
                installation_date = timezone.now()
                ac_date = timezone.now()
                order_date = timezone.now()
            purchase_record = cls.objects.create(customer_id=customer_id, reseller_name=reseller_name,
                                                 module_count=module_count, module_type=module_type, kwp=kwp,
                                                 price_without_tax=price_without_tax, price_with_tax=price_with_tax,
                                                 offer_created=offer_created, cancellation=cancellation,
                                                 project_planning_created=project_planning_created,
                                                 installation_date=installation_date, ac_date=ac_date,
                                                 photo_roof_access=photo_roof_area,
                                                 photo_counter_cabinet=photo_counter_cabinet, video_counter=video_counter,
                                                 photo_of_counter=photo_of_counter, power_of_attorney=power_of_attorney,
                                                 data_collection=data_collection, order_date=order_date,
                                                 memory_type=memory_type, with_battery=with_battery)
            return purchase_record
        except Exception as e:
            print("Exception occurs while creating Purchase Record. Error: {}".format(str(e)))
            return None

    @classmethod
    def fetch(cls, customer_id):
        try:
            purchases = cls.objects.filter(customer_id=customer_id)
            return purchases
        except Exception as e:
            print("Exception occurs while fetching Purchases. Error: {}".format(str(e)))
            return None

    @classmethod
    def fetch_by_id(cls, purchase_id):
        try:
            purchase = cls.objects.filter(id=purchase_id).first()
            return purchase
        except Exception as e:
            print("Exception occurs while fetching Purchase by ID. Error: {}".format(str(e)))
            return None


class Attachments(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='attachments')
    file_type = models.CharField(max_length=255)
    file_link = models.CharField(max_length=1000)
    upload = models.FileField(upload_to='uploads/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)

    @classmethod
    def create(cls, customer_id, file_type, file_link):
        try:
            attachment = cls.objects.create(customer_id=customer_id, file_type=file_type, file_link=file_link)
            return attachment
        except Exception as e:
            print("Exception occurs while creating Attachments. Error: {}".format(str(e)))
            return None

    @classmethod
    def fetch(cls, customer_id):
        try:
            attachments = cls.objects.filter(customer_id=customer_id)
            return attachments
        except Exception as e:
            print("Exception occurs while creating Attachments. Error: {}".format(str(e)))
            return None

    @classmethod
    def create_attachment(cls, customer_id, file_type, upload):
        try:
            attachment = cls.objects.create(customer_id=customer_id, file_type=file_type, upload=upload)
            return attachment
        except Exception as e:
            print("Exception occurs while creating Attachments. Error: {}".format(str(e)))
            return None


class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    message = models.TextField(blank=False)
    todo_date = models.DateField('Complete Before', blank=True, null=True)
    todo_time = models.TimeField('', blank=True, default=datetime.time(16, 0))
    completed = models.BooleanField(default=False)

    creator = models.ForeignKey('User', on_delete=models.SET_NULL,
                                null=True, related_name='created_tasks')
    created = models.DateField(null=True)

    @property
    def complete_before(self):
        return datetime.datetime.combine(self.todo_date, self.todo_time)

    def save(self, *args, **kwargs):
        self.created = timezone.now().date()
        super().save(*args, **kwargs)

    @classmethod
    def create(cls, user_id, message):
        try:
            task = cls.objects.create(user_id=user_id, message=message)
            return task
        except Exception as e:
            print("Exception occurs while creating task. Error: {}".format(str(e)))
            return None

    @classmethod
    def fetch(cls, user_id=None):
        try:
            task = cls.objects.all()
            if user_id:
                task = task.filter(user_id=user_id)

            return task
        except Exception as e:
            print("Exception occurs while creating task. Error: {}".format(str(e)))
            return None
