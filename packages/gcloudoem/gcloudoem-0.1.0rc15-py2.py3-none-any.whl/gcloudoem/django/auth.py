# Copyright (c) 2012-2015 Kapiche Ltd.
# Author: Ryan Stuart<ryan@kapiche.com>
from __future__ import absolute_import, division, print_function, unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import _user_has_perm, _user_get_all_permissions, _user_has_module_perms
from django.contrib.contenttypes.models import ContentTypeManager
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str

from .. import Entity, TextProperty, ListProperty, BooleanProperty, DateTimeProperty, ReferenceProperty, EmailProperty
from .utils import datetime_now

REDIRECT_FIELD_NAME = 'next'

try:
    from django.contrib.auth.hashers import check_password, make_password
except ImportError:
    """Handle older versions of Django"""
    from django.utils.hashcompat import md5_constructor, sha_constructor

    def get_hexdigest(algorithm, salt, raw_password):
        raw_password, salt = smart_str(raw_password), smart_str(salt)
        if algorithm == 'md5':
            return md5_constructor(salt + raw_password).hexdigest()
        elif algorithm == 'sha1':
            return sha_constructor(salt + raw_password).hexdigest()
        raise ValueError('Got unknown password algorithm type in password')

    def check_password(raw_password, password):
        algo, salt, hash = password.split('$')
        return hash == get_hexdigest(algo, salt, raw_password)

    def make_password(raw_password):
        from random import random
        algo = 'sha1'
        salt = get_hexdigest(algo, str(random()), str(random()))[:5]
        hash = get_hexdigest(algo, salt, raw_password)
        return '%s$%s$%s' % (algo, salt, hash)


class ContentType(Entity):
    name = TextProperty(max_length=100)
    app_label = TextProperty(max_length=100)
    model = TextProperty(max_length=100, verbose_name=_('python model class name'))
    objects = ContentTypeManager()

    class Meta:
        verbose_name = _('content type')
        verbose_name_plural = _('content types')
        kind = 'django_content_type'
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def model_class(self):
        """Returns the Python model class for this type of content."""
        from django.db import models
        return models.get_model(self.app_label, self.model)
    entity_class = model_class

    def get_object_for_this_type(self, **kwargs):
        """
        Returns an object of this type for the keyword arguments given. Basically, this is a proxy around this
        object_type's get_object() model method. The ObjectNotExist exception, if thrown, will not be caught, so code
        that calls this method should catch it.
        """
        return self.entity_class().object.get(**kwargs)

    def natural_key(self):
        return (self.app_label, self.model)


class SiteProfileNotAvailable(Exception):
    pass


class PermissionManager(models.Manager):
    def get_by_natural_key(self, codename, app_label, model):
        return self.get(
            codename=codename,
            content_type=ContentType.objects.get_by_natural_key(app_label, model)
        )


class Permission(Entity):
    """
    The permissions system provides a way to assign permissions to specific users and groups of users.

    The permission system is used by the Django admin site, but may also be useful in your own code. The Django admin
    site uses permissions as follows:

        - The "add" permission limits the user's ability to view the "add"
          form and add an object.
        - The "change" permission limits a user's ability to view the change
          list, view the "change" form and change an object.
        - The "delete" permission limits the ability to delete an object.

    Permissions are set globally per type of object, not per specific object instance. It is possible to say "Mary may
    change news stories," but it's not currently possible to say "Mary may change news stories, but only the ones she
    created herself" or "Mary may only change news stories that have a certain status or publication date."

    Three basic permissions -- add, change and delete -- are automatically created for each Django model.
    """
    name = TextProperty(max_length=50, verbose_name=_('username'))
    # content_type = ReferenceField(ContentType)
    codename = TextProperty(max_length=100, verbose_name=_('codename'))
    # FIXME: don't access field of the other class
    # unique_with=['content_type__app_label', 'content_type__model'])

    objects = PermissionManager()

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')

    def __unicode__(self):
        return u"%s | %s | %s" % (str(self.content_type.app_label), str(self.content_type), str(self.name))

    def natural_key(self):
        return (self.codename,) + self.content_type.natural_key()
    natural_key.dependencies = ['contenttypes.contenttype']


class Group(Entity):
    """
    Groups are a generic way of categorizing users to apply permissions, or some other label, to those users. A user
    can belong to any number of groups.

    A user in a group automatically has all the permissions granted to that group. For example, if the group Site
    editors has the permission can_edit_home_page, any user in that group will have that permission.

    Beyond permissions, groups are a convenient way to categorize users to apply some label, or extended functionality,
    to them. For example, you could create a group 'Special users', and you could write code that would do special
    things to those users -- such as giving them access to a members-only portion of your site, or sending them
    members-only e-mail messages.
    """
    # name = TextProperty(max_length=80, unique=True, verbose_name=_('name'))
    name = TextProperty(max_length=80, verbose_name=_('name'))
    permissions = ListProperty(ReferenceProperty(Permission, verbose_name=_('permissions'), required=False))

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __unicode__(self):
        return self.name


class UserManager(models.Manager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given username, e-mail and password.
        """
        now = datetime_now()

        # Normalize the address by lowercasing the domain part of the email
        # address.
        try:
            email_name, domain_part = email.strip().split('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])

        user = self.model(username=username, email=email, is_staff=False, is_active=True,
                          is_superuser=False, last_login=now, date_joined=now)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        u = self.create_user(username, email, password)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save()
        return u

    def make_random_password(self, length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
        """Generates a random password with the given length and given allowed_chars."""
        # Note that default value of allowed_chars does not have "I" or letters
        # that look like it -- just to avoid confusion.
        from random import choice
        return ''.join([choice(allowed_chars) for _ in range(length)])


class User(Entity):
    """
    A User entity that aims to mirror most of the API specified by Django at
    http://docs.djangoproject.com/en/dev/topics/auth/#users
    """
    username = TextProperty(
        max_length=30,
        required=True,
        verbose_name=_('username'),
        help_text=_("Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters")
    )
    first_name = TextProperty(
        max_length=30,
        verbose_name=_('first name')
    )
    last_name = TextProperty(max_length=30, verbose_name=_('last name'))
    email = EmailProperty(verbose_name=_('e-mail address'))
    password = TextProperty(
        max_length=128,
        verbose_name=_('password'),
        help_text=_(
            "Use '[algo]$[iterations]$[salt]$[hexdigest]' or use the <a href=\"password/\">change password form</a>."
        )
    )
    is_staff = BooleanProperty(
        default=False,
        verbose_name=_('staff status'),
        help_text=_("Designates whether the user can log into this admin site.")
    )
    is_active = BooleanProperty(
        default=True,
        verbose_name=_('active'),
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        )
    )
    is_superuser = BooleanProperty(
        default=False,
        verbose_name=_('superuser status'),
        help_text=_("Designates that this user has all permissions without explicitly assigning them.")
    )
    last_login = DateTimeProperty(default=datetime_now, verbose_name=_('last login'))
    date_joined = DateTimeProperty(default=datetime_now, verbose_name=_('date joined'))
    user_permissions = ListProperty(
        ReferenceProperty(Permission),
        verbose_name=_('user permissions'),
        help_text=_('Permissions for the user.')
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        """Returns the users first and last names, separated by a space.
        """
        full_name = u'%s %s' % (self.first_name or '', self.last_name or '')
        return full_name.strip()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        """
        Sets the user's password - always use this rather than directly assigning to
        :attr:`~gcloudoem.django.auth.User.password` as the password is hashed before storage.
        """
        self.password = make_password(raw_password)
        self.save()
        return self

    def check_password(self, raw_password):
        """
        Checks the user's password against a provided password - always use this rather than directly comparing to
        :attr:`~mongoengine.django.auth.User.password` as the password is hashed before storage.
        """
        return check_password(raw_password, self.password)

    @classmethod
    def create_user(cls, username, password, email=None):
        """Create (and save) a new user with the given username, password and email address."""
        now = datetime_now()

        # Normalize the address by lowercasing the domain part of the email address.
        if email is not None:
            try:
                email_name, domain_part = email.strip().split('@', 1)
            except ValueError:
                pass
            else:
                email = '@'.join([email_name, domain_part.lower()])

        user = cls(username=username, email=email, date_joined=now)
        user.set_password(password)
        user.save()
        return user

    def get_group_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through his/her groups. This method queries all
        available auth backends. If an object is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method queries all available auth backends, but
        returns immediately if any backend returns True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, permissions for this specific object are
        checked.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label. Uses pretty much the same logic as
        has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def email_user(self, subject, message, from_email=None):
        """Sends an e-mail to this User."""
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises SiteProfileNotAvailable if this site does not allow
        profiles.
        """
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable('You need to set AUTH_PROFILE_MODULE in your project settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in the AUTH_PROFILE_MODULE setting'
                )

            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check AUTH_PROFILE_MODULE in your project settings'
                    )
                self._profile_cache = model.objects.get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache


class GCloudDatastoreBackend(object):
    """Authenticate using Google Datastore and gcloudoem.django.auth.User."""

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False
    _user_entity = False

    def authenticate(self, username=None, password=None):
        user = self.user_entity.objects(username=username).first()
        if user:
            if password and user.check_password(password):
                backend = auth.get_backends()[0]
                user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
                return user
        return None

    def get_user(self, user_id):
        return self.user_entity.objects.with_id(user_id)

    @property
    def user_entity(self):
        if self._user_entity is False:
            from .gcloud_auth.models import get_user_entity
            self._user_entity = get_user_entity()
        return self._user_entity


def get_user(userid):
    """
    Returns a User object from an id (User.id). Django's equivalent takes request, but taking an id instead leaves it
    up to the developer to store the id in any way they want (session, signed cookie, etc.)
    """
    if not userid:
        return AnonymousUser()
    return GCloudDatastoreBackend().get_user(userid) or AnonymousUser()
