from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib.auth.hashers import make_password

# 認証設定を上書き
class UserManager(UserManager):  # BaseUserManagerをUserManagerに変更
    # use_in_migrations = True 削除
    # ユーザーネームに関する処理を削除してメールアドレスで認証するように変更
    def _create_user(self, email, password, **extra_fields): # usernameを削除
        # """                                                                   ここから
        # Create and save a user with the given username, email, and password.    ⇩
        # """                                                                     ⇩
        # if not username:                                                        ⇩
        #     raise ValueError('The given username must be set')               ここまで削除
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        # username = GlobalUserModel.normalize_username(username)  削除
        user = self.model(email=email, **extra_fields)  # username=usernameを削除
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):  # username,emailのNoneを削除
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)  # usernameを削除

    def create_superuser(self, email, password=None, **extra_fields): # username,emailのNoneを削除
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields)  # usernameを削除
    

class CustomUser(AbstractBaseUser, PermissionsMixin):  # AbstractUserをCustomUserに変更
    # """                                                                   ここから
    # An abstract base class implementing a fully featured User model with     ⇩
    # admin-compliant permissions.                                             ⇩
    #                                                                          ⇩
    # Username and password are required. Other fields are optional.           ⇩
    # """                                                                  ここまで削除
    # username_validator = UnicodeUsernameValidator()  削除

    # usernameの変数を削除
    # username = models.CharField(
    #     _('username'),
    #     max_length=150,
    #     unique=True,
    #     help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    #     validators=[username_validator],
    #     error_messages={
    #         'unique': _("A user with that username already exists."),
    #     },
    # )
    
    # ここにprofile情報に必要なデータベースを作成
    email = models.EmailField('メールアドレス', unique=True)
    first_name = models.CharField('姓', max_length=30) # firstnameを姓に変更,blankは削除,max_lengthは30に変更
    last_name = models.CharField('名', max_length=150, blank=True) # lastnameを名に変更,blankは削除,max_lengthは30に変更
    # email = models.EmailField(_('email address'), blank=True)  emailは追加したので削除
    department = models.CharField('所属', max_length=30, blank=True) # 追加
    # DateTimeField: Djangoのモデルに日付と時刻を記録することが出来る
    created = models.DateTimeField('入会日', default=timezone.now)
    # BooleanField: モデルに真偽値を使ったフィールド、つまりFalseかTrueを持つフィールドを定義することが出来る
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    # date_joined = models.DateTimeField(_('date joined'), default=timezone.now)  削除

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email' # usernameをemailに変更
    REQUIRED_FIELDS = []  # emailを空のリストに変更

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # abstract = True 削除

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)