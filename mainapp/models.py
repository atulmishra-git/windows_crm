import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db.models.aggregates import Sum, Count
from django.db.models.functions import Extract
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from mainapp.fields import ContentTypeRestrictedFileField
from mainapp.view.constants import CALL_NOTE_PRIORITY
from .usermanager import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("First Name"), max_length=255)
    surname = models.CharField(_("Surname"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=20, unique=True)
    username = models.CharField(_("Username"), max_length=255, unique=True)
    email = models.EmailField(_("Email"), max_length=255, unique=True)
    is_active = models.BooleanField(_("Active"), default=True)
    is_deleted = models.BooleanField(_('Deleted'), default=False)
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
    ('Male', _('Male')),
    ('Female', _('Female'))
)
PURPOSE_CHOICES = (
    ('Comapny', _('Company')),
    ('individual', _('individual')),
    ('Family', _('Family'))
)
OFFER_CHOICES = (
    ('Email', _('Via Email')),
    ('Letter', _('Via Letter')),
)
ATTACHMENT_TYPE_CHOICES = (
    ('offer', _('offer')),
    ('offer confirmation', _('offer confirmation')),
    ('install', _('install')),
    ('invoice', _('invoice'))
)
CALL_NOTE_PRIORITY_CHOICES = (
    (CALL_NOTE_PRIORITY.high, _('high')),
    (CALL_NOTE_PRIORITY.medium, _('medium')),
    (CALL_NOTE_PRIORITY.low, _('low')),
)


class Customer(models.Model):
    first_name = models.CharField(_("first name"), max_length=255)
    offer_id = models.CharField(_("offer id"), max_length=255, blank=True,
                                null=True)
    invoice_id = models.CharField(_("Invoice ID"), max_length=255, blank=True,
                                  null=True)
    street = models.CharField(_("street"), max_length=500)
    postcode = models.CharField(_("postcode"), max_length=255)
    place = models.CharField(_("place"), max_length=255)
    surname = models.CharField(_("surname"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=20, unique=True,
                             default='N.A')
    mobile = models.CharField(_("Mobile"), max_length=20, null=True, blank=True,
                              default='N.A')
    email = models.CharField(_("Email"), max_length=120, null=True, blank=True,
                             default='N.A')
    birthday = models.DateField(_("Birthday"), null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_deleted = models.BooleanField(_('deleted'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(_("gender"), max_length=100, choices=GENDER_CHOICES, null=True, blank=True)
    purpose = models.CharField(_("purpose"), max_length=100, choices=PURPOSE_CHOICES, null=True, blank=True)

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
        return self.first_name + " " + self.surname


class CallNotes(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='call_notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='call_notes')
    notes = models.CharField(_("notes"), max_length=1000)
    status = models.PositiveSmallIntegerField(choices=CALL_NOTE_PRIORITY_CHOICES,
                                              default=CALL_NOTE_PRIORITY.medium)
    created = models.DateTimeField(null=True)

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
    customer = models.OneToOneField(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE,
                                    related_name='purchase_record')
    module_manufacturer = models.CharField(_("manufacturer"), max_length=255, null=True)
    watt = models.PositiveIntegerField(_("watt"), null=True, default=0)
    module_count = models.PositiveIntegerField(_("module count"), null=True, default=0)

    with_battery = models.BooleanField(_("with battery"), blank=True, default=False, null=True)
    manufacturer = models.CharField(_("manufacturer"), max_length=255, null=True, blank=True)
    kwh = models.CharField(_("Kw/H"), max_length=255, blank=True, null=True)
    manufacturer2 = models.CharField(_('Manufacturer'), max_length=255, blank=True, null=True)
    kwh2 = models.CharField(_('Kw/H'), max_length=255, blank=True, null=True)

    price_without_tax = models.FloatField(_("price without tax"), help_text=_("Price in Euro (€)"), null=True,
                                          validators=[MinValueValidator(0, _("Should be above 0"))],
                                          default=0)

    offer_by = models.CharField(_("offer by"), choices=OFFER_CHOICES, max_length=16, null=True)
    # OFFER INFORMATION
    offer_date = models.DateField(_("offer date"), blank=True, null=True)
    reseller_name = models.CharField(_("reseller name"), max_length=255, null=True, blank=True)
    declined = models.BooleanField(_("declined"), default=False, null=True, blank=True)
    # TECHNICAL DETAILS
    date_sent = models.DateField(_('date sent'), null=True, blank=True)
    project_planning_created = models.BooleanField(_('project planning created'),
                                                   blank=False, default=False)
    dc_term = models.DateField(_('DC Term'), blank=True, null=True)
    dc_mechanic = models.CharField(_('DC mechanic'), max_length=255, blank=True, null=True)
    ac_term = models.DateField(_('AC Term'), blank=True, null=True)
    ac_mechanic = models.CharField(_('AC mechanic'), max_length=255, blank=True, null=True)
    # INFORMATION FOR THE ROOF
    roof_type = models.CharField(_("roof type"), max_length=255, null=True, blank=True)
    roof_tilt = models.FloatField(_("roof tilt"), help_text=_("in Degrees"), null=True, blank=True)
    alignment = models.CharField(_("alignment"), max_length=64, null=True, blank=True)
    module_area = models.FloatField(_("module area"), help_text=_("Area in meter squared (m2)"), null=True, blank=True,
                                    validators=[MinValueValidator(0, _("Should be above 0"))],
                                    default=0)

    extra_details = models.TextField(_("extra details"), blank=True, null=True)

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

    @classmethod
    def purchases_last_seven_days(cls):
        return cls.objects.filter(
            created_at__gte=datetime.datetime.now() - datetime.timedelta(days=7)
        ).values('watt').annotate(total=Sum('price_without_tax')).values('watt', 'total')

    @classmethod
    def installations_last_six_months(cls):
        month_counts = cls.objects.filter(
            created_at__gte=datetime.datetime.now() - datetime.timedelta(days=6*30)
        ).annotate(month=Extract('ac_term', 'month')).values('month').annotate(
            count=Count('month')
        )
        month_mapping = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'Mäi',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Okt',
            11: 'Nov',
            12: 'Dez',
        }
        curr_month = datetime.datetime.now().month
        result = {}
        for i in range(6):
            month = curr_month - i
            if month < 1:
                month += 12
            if month_counts.filter(month=month).exists():
                count = month_counts.get(month=month)['count']
            else:
                count = 0
            result[month_mapping[month]] = count
        return result

    @property
    def tax(self):
        return round(float("%.2f" % (getattr(self, 'price_without_tax', 0) * 0.19)))

    @property
    def price_with_tax(self):
        return round(float("%.2f" % (getattr(self, 'price_without_tax', 0) * 1.19)))

    @property
    def kwp(self):
        return round(float("%.2f" % (getattr(self, 'module_count', 0) * getattr(self, 'watt', 0) / 1000.0)))

    @property
    def manufacturer_display(self):
        if self.with_battery:
            return self.manufacturer
        return self.manufacturer2

    @property
    def kwh_display(self):
        if self.with_battery:
            return self.kwh
        return self.kwh2

    @property
    def total_area(self):
        return round(float("%.2f" % (self.module_count * self.module_area)))

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
                                                 photo_counter_cabinet=photo_counter_cabinet,
                                                 video_counter=video_counter,
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
    file_name = models.CharField(_("File Name"), max_length=255)
    kind = models.CharField(_('kind'), max_length=16,
                            default='custom')
    upload = ContentTypeRestrictedFileField(_("Upload"), upload_to='uploads/', null=True,
                                            content_types=['application/pdf', 'image/jpg', 'image/png', 'image/gif',
                                                           'image/jpeg', 'image/bmp', 'text/plain', 'text/csv',
                                                           'image/vnd.microsoft.icon', 'image/png',
                                                           'application/msword', 'application/vnd.ms-excel',
                                                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                                           'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                                           'video/x-msvideo', 'video/mpeg', 'video/webm', 'video/mp4'],
                                            max_upload_size=5242880)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)

    @property
    def file_type(self):
        return self.upload.name.split('.')[-1]

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


class AttachmentTemplate(models.Model):
    kind = models.CharField(_('type'), max_length=32,
                            choices=ATTACHMENT_TYPE_CHOICES,
                            unique=True)
    subject = models.CharField(_('subject'), max_length=256)
    body = models.TextField()


class Tasks(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    message = models.TextField(_("message"), blank=False)
    todo_date = models.DateField(_('Complete Before'), null=True)
    todo_time = models.TimeField('', default=datetime.time(16, 0))
    completed = models.BooleanField(_('completed'), default=False)

    creator = models.ForeignKey('User', on_delete=models.SET_NULL,
                                null=True, related_name='created_tasks')
    created = models.DateField(null=True)

    private = models.BooleanField(_('private'), default=False)

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
