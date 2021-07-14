from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models


# Create your models here.

class Prefecture(models.Model):
    prefecture_choice = models.CharField(verbose_name='都道府県', max_length=3)

    class Meta:
        verbose_name_plural = '都道府県'

    def __str__(self):
        return self.prefecture_choice


class CustomUser(AbstractUser):
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
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name_plural = 'ユーザー'


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
