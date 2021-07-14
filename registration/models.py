import uuid as uuid_lib

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Prefecture(models.Model):
    prefecture = models.CharField(verbose_name='都道府県', max_length=3)

    class Meta:
        verbose_name_plural = '都道府県'

    def __str__(self):
        return self.prefecture


class CustomUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid_lib.uuid4, primary_key=True, editable=False)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )
    full_name = models.CharField(_('氏名'),max_length=150,blank=True)
    email = models.EmailField(_('email address'),blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
        )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active.'
            'Unselect this instead of deleting accounts accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'),default=timezone.now)

    male = '男'
    female = '女'
    gender_choice = [
        (male, '男'),
        (female, '女')
    ]
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    gender = models.CharField(verbose_name='性別', max_length=2, choices=gender_choice, null=False, blank=False)
    purpose = models.CharField(verbose_name='ご登録目的', max_length=2, null=False, blank=False)
    scene = models.CharField(verbose_name='ご利用シーン', max_length=6, null=False, blank=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    class Meta:
        verbose_name_plural = 'ユーザー'

    def clean(self):
        super(CustomUser, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self,subject,message,form_email=None,**kwargs):
        send_mail(subject,message,form_email,[self.email],**kwargs)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name


# サービス
class Service(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=50)
    description = models.CharField(verbose_name='説明', max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'サービス'

    def __str__(self):
        return self.title


# 買い手

# 売り手


# メッセージ
class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    message = models.CharField(verbose_name='テキスト', max_length=250)
    published_at = models.DateTimeField(auto_now=True)

    # ファイルの送信の仕方がわかりません

    class Meta:
        verbose_name_plural = "チャット"

    def __str__(self):
        return self.message


class MessageRoom(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    Seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_people')
    Buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer_people')
    fixed_phrase = models.CharField(verbose_name='定型文', max_length=250, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'チャットルーム'


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purchase_review = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='purchase_review_group',
                                        verbose_name='購入評価')
    exhibit_review = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='exhibit_review_group',
                                       verbose_name='出品評価')

    class Meta:
        verbose_name_plural = 'レビュー'
