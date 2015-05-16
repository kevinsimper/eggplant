# -*- coding: utf-8 -*-
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from foodnet.common.utils import absolute_url_reverse


class UserProfile(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    SEX_CHOICES = (
        (FEMALE, 'female'),
        (MALE, 'male')
    )

    user = models.OneToOneField(User, editable=False)
    middle_name = models.CharField(max_length=30, null=True)

    # old system: adr1, adr2, streetno, floor, door
    address = models.TextField(max_length=255)
    postcode = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    tel = models.CharField(max_length=15)
    tel2 = models.CharField(max_length=15)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    dob = models.DateField(null=True)  # old system: birthday
    privacy = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    changed = models.DateTimeField(auto_now=True, editable=False)

    @property
    def full_name(self):
        "Returns member's full name."
        if self.middlename:
            return '{0} {1} {2}'.format(self.user.firstname, self.middlename,
                                    self.user.lastname)
        return '{0} {2}'.format(self.user.firstname, self.user.lastname)

    def is_complete(self):
        if self.address and self.postcode and self.city and\
                self.sex and self.tel and self.dob and self.privacy:
            return True
        return False

    @classmethod
    def get_for_user(cls, user):
        return cls.objects.get(user_id=user.id)


class MemberCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return u'{0}'.format(self.name)


class Member(models.Model):
    number = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User)
    category = models.ForeignKey(MemberCategory)


class Division(models.Model):
    shortname = models.CharField(max_length=4)
    name = models.CharField(max_length=255)

    # old system: type
    category = models.CharField(max_length=255)

    # old system: webmembers
    allow_webmembers = models.BooleanField()
    contact = models.CharField(max_length=255)

    # FIXME: should we move it out to model manager with
    # other bits from old models?
    # members = models.ManyToManyField('membership.Member',
    #                                 through='membership.DivisionMember')

    def __str__(self):
        return u'{0}'.format(self.name)


class DivisionMember(models.Model):
    member = models.ForeignKey(Member)
    division = models.ForeignKey(Division)
    start = models.DateTimeField(auto_now_add=True)
    exit = models.DateTimeField()
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('member', 'division'),)


class Invitation(models.Model):
    email = models.EmailField(null=False, blank=False, unique=True)
    accepted = models.BooleanField(default=False)
    accepted_dt = models.DateTimeField(null=True)
    verification_key = models.UUIDField(default=uuid.uuid4, editable=False,
                                        null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(User)
    division = models.ForeignKey(Division)
    member_category = models.ForeignKey(MemberCategory)

    def __str__(self):
        if self.accepted:
            acp = 'accepted'
        else:
            acp = 'NOT accepted'
        return '{} {}>'.format(self.email, acp)


@receiver(post_save, sender=User, dispatch_uid='membership-user-profile')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Invitation,
          dispatch_uid='membership-invitation-send_email_invitation')
def send_email_invitation(sender, instance, created, **kwargs):
    if created:
        from django.core.mail import send_mail
        subject = 'You have been invitate to FoodNet!'
        to_addrs = [instance.email, ]
        invite_url = absolute_url_reverse('accept_invitation', kwargs=dict(
                                 verification_key=
                                 instance.verification_key.hex))
        body = """
            Please click the following link to confirm:
            {invite_url}

        """.format(invite_url=invite_url)
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, to_addrs,
                  fail_silently=False)
