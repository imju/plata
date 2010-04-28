from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext


class BillingShippingAddress(models.Model):
    ADDRESS_FIELDS = ['company', 'first_name', 'last_name', 'address',
        'zip_code', 'city', 'country']

    billing_company = models.CharField(_('company'), max_length=100, blank=True)
    billing_first_name = models.CharField(_('first name'), max_length=100, blank=True)
    billing_last_name = models.CharField(_('last name'), max_length=100, blank=True)
    billing_address = models.TextField(_('address'), blank=True)
    billing_zip_code = models.CharField(_('ZIP code'), max_length=50, blank=True)
    billing_city = models.CharField(_('city'), max_length=100, blank=True)
    billing_country = models.CharField(_('country'), max_length=2, blank=True,
        help_text=_('ISO2 code'))

    shipping_company = models.CharField(_('company'), max_length=100, blank=True)
    shipping_first_name = models.CharField(_('first name'), max_length=100, blank=True)
    shipping_last_name = models.CharField(_('last name'), max_length=100, blank=True)
    shipping_address = models.TextField(_('address'), blank=True)
    shipping_zip_code = models.CharField(_('ZIP code'), max_length=50, blank=True)
    shipping_city = models.CharField(_('city'), max_length=100, blank=True)
    shipping_country = models.CharField(_('country'), max_length=2, blank=True,
        help_text=_('ISO2 code'))

    class Meta:
        abstract = True

    def copy_address(self, contact=None):
        contact = contact or self.contact

        shipping_prefix = contact.shipping_same_as_billing and 'billing' or 'shipping'

        for field in self.ADDRESS_FIELDS:
            setattr(self, 'billing_%s' % field,
                getattr(contact, 'billing_%s' % field))
            setattr(self, 'shipping_%s' % field,
                getattr(contact, '%s_%s' % (shipping_prefix, field)))


class Contact(BillingShippingAddress):
    user = models.ForeignKey(User, verbose_name=_('user'), blank=True, null=True)
    email = models.EmailField(_('e-mail address'), unique=True)
    created = models.DateTimeField(_('created'), default=datetime.now)

    shipping_same_as_billing = models.BooleanField(_('shipping address equals billing address'),
        default=True)

    currency = models.CharField(_('currency'), max_length=10,
        help_text=_('Preferred currency.'))
    notes = models.TextField(_('notes'), blank=True)

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    def __unicode__(self):
        return u'%s %s' % (self.billing_first_name, self.billing_last_name)