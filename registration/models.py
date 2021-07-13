from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.

class Prefecture(models.Model):
    prefecture = models.CharField(verbose_name='都道府県', max_length=3)

    class Meta:
        verbose_name_plural = '都道府県'

    def __str__(self):
        return self.prefecture


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth
        )

    def create_superuser(self, email, date_of_birth, password=None):
        user = self.create_user(email, password=password, date_of_birth=date_of_birth)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
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


# サービス
class Service(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=50)
    description = models.CharField(verbose_name='説明', max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='サービス'

    def __str__(self):
        return self.title


# 買い手
class Buyer(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '購入者'

    def __str__(self):
        return self.buyer


# 売り手
class Seller(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "出品者"

    def __str__(self):
        return self.seller


# メッセージ
class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    Buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    text = models.CharField(verbose_name='テキスト', max_length=250)
    published_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "チャット"

    def __str__(self):
        return self.text


class MessageRoom(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    Seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    Buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    purchase_review = models.IntegerField(verbose_name='購入実績', default=0, null=True, blank=True)
    exhibit_review = models.IntegerField(verbose_name='販売実績', default=0, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'チャットルーム'
