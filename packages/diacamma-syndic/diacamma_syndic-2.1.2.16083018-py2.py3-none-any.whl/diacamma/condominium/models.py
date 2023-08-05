# -*- coding: utf-8 -*-
'''
diacamma.condominium models package

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2015 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import unicode_literals
from datetime import date

from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Sum, Max
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.utils import six, formats

from lucterios.framework.models import LucteriosModel, get_value_converted
from lucterios.framework.error import LucteriosException, IMPORTANT, GRAVE
from lucterios.framework.tools import convert_date
from lucterios.framework.signal_and_lock import Signal
from lucterios.CORE.models import Parameter

from diacamma.accounting.models import CostAccounting, EntryAccount, Journal,\
    ChartsAccount, EntryLineAccount, FiscalYear
from diacamma.accounting.tools import format_devise, currency_round,\
    current_system_account, get_amount_sum, correct_accounting_code
from diacamma.payoff.models import Supporting
from django_fsm import FSMIntegerField, transition


class Set(LucteriosModel):
    name = models.CharField(_('name'), max_length=100)
    budget = models.DecimalField(_('budget'), max_digits=10, decimal_places=3, default=0.0, validators=[
        MinValueValidator(0.0), MaxValueValidator(9999999.999)])
    revenue_account = models.CharField(_('revenue account'), max_length=50)
    cost_accounting = models.ForeignKey(
        CostAccounting, verbose_name=_('cost accounting'), null=True, default=None, db_index=True, on_delete=models.PROTECT)
    is_link_to_lots = models.BooleanField(_('is link to lots'), default=False)
    type_load = models.IntegerField(verbose_name=_('type of load'),
                                    choices=((0, _('current')), (1, _('exceptional'))), null=False, default=0, db_index=True)
    is_active = models.BooleanField(_('is active'), default=True)
    set_of_lots = models.ManyToManyField('PropertyLot', verbose_name=_('set of lots'), blank=True)

    def __init__(self, *args, **kwargs):
        LucteriosModel.__init__(self, *args, **kwargs)
        self.date_begin = None
        self.date_end = None

    def set_dates(self, begin_date=None, end_date=None):
        if begin_date is None:
            self.date_begin = six.text_type(FiscalYear.get_current().begin)
        else:
            self.date_begin = begin_date
        if end_date is None:
            self.date_end = six.text_type(FiscalYear.get_current().end)
        else:
            self.date_end = end_date
        if self.date_end < self.date_begin:
            self.date_end = self.date_begin

    def set_context(self, xfer):
        if xfer is not None:
            self.set_dates(convert_date(xfer.getparam("begin_date")), convert_date(
                xfer.getparam("end_date")))

    def __str__(self):
        return self.name

    @classmethod
    def get_default_fields(cls):
        return ["name", 'type_load', 'partition_set', (_('budget'), "budget_txt"), (_('expense'), 'sumexpense_txt')]

    @classmethod
    def get_edit_fields(cls):
        return ["name", "budget", "type_load", 'is_link_to_lots', "revenue_account", 'cost_accounting']

    @classmethod
    def get_show_fields(cls):
        return [("name", ), ("revenue_account", 'cost_accounting'), ("type_load", 'is_active'), ('is_link_to_lots', (_('partition sum'), 'total_part')), 'partition_set', ((_('budget'), "budget_txt"), (_('expense'), 'sumexpense_txt'),)]

    def _do_insert(self, manager, using, fields, update_pk, raw):
        new_id = LucteriosModel._do_insert(
            self, manager, using, fields, update_pk, raw)
        for owner in Owner.objects.all():
            Partition.objects.create(set_id=new_id, owner=owner)
        return new_id

    @property
    def budget_txt(self):
        return format_devise(self.budget, 5)

    @property
    def total_part(self):
        total = self.partition_set.all().aggregate(sum=Sum('value'))
        if 'sum' in total.keys():
            return total['sum']
        else:
            return 0

    def get_expenselist(self):
        if self.date_begin is None:
            self.set_dates()
        return self.expensedetail_set.filter(expense__date__gte=self.date_begin, expense__date__lte=self.date_end)

    def get_sumexpense(self):
        total = self.get_expenselist().aggregate(sum=Sum('price'))
        if 'sum' in total.keys():
            return total['sum']
        else:
            return 0

    @property
    def sumexpense_txt(self):
        return format_devise(self.get_sumexpense(), 5)

    def refresh_ratio_link_lots(self):
        if self.is_link_to_lots:
            for part in self.partition_set.all():
                value = 0
                for lot in self.set_of_lots.filter(owner=part.owner):
                    value += lot.value
                part.value = value
                part.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.revenue_account = correct_accounting_code(self.revenue_account)
        self.refresh_ratio_link_lots()
        return LucteriosModel.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta(object):
        verbose_name = _('class load')
        verbose_name_plural = _('class loads')


class Owner(Supporting):

    information = models.CharField(
        _('information'), max_length=200, null=True, default='')

    def __init__(self, *args, **kwargs):
        Supporting.__init__(self, *args, **kwargs)
        self.date_begin = None
        self.date_end = None

    def set_dates(self, begin_date=None, end_date=None):
        if begin_date is None:
            self.date_begin = six.text_type(FiscalYear.get_current().begin)
        else:
            self.date_begin = begin_date
        if end_date is None:
            self.date_end = six.text_type(FiscalYear.get_current().end)
        else:
            self.date_end = end_date
        if self.date_end < self.date_begin:
            self.date_end = self.date_begin
        if isinstance(self.date_begin, six.text_type):
            self.date_begin = convert_date(self.date_begin)
        if isinstance(self.date_end, six.text_type):
            self.date_end = convert_date(self.date_end)

    def set_context(self, xfer):
        if xfer is not None:
            self.set_dates(convert_date(xfer.getparam("begin_date")), convert_date(
                xfer.getparam("end_date")))

    def get_third_mask(self):
        return current_system_account().get_societary_mask()

    def default_date(self):
        if self.date_begin is None:
            self.set_dates()
        ret_date = date.today()
        if ret_date < self.date_begin:
            ret_date = self.date_begin
        if ret_date > self.date_end:
            ret_date = self.date_end
        return ret_date

    @property
    def date_current(self):
        if self.date_begin is None:
            self.set_dates()
        if isinstance(self.date_end, six.text_type):
            self.date_end = convert_date(self.date_end)
        return formats.date_format(self.date_end, "DATE_FORMAT")

    def __str__(self):
        return six.text_type(self.third)

    @classmethod
    def get_default_fields(cls):
        return ["third", (_('property part'), 'property_part'), (_('initial state'), 'total_initial'), (_('total call for funds'), 'total_call'), (_('total payoff'), 'total_payed'), (_('total estimate'), 'total_estimate'), (_('total ventilated'), 'total_ventilated'), (_('total real'), 'total_real')]

    @classmethod
    def get_edit_fields(cls):
        return ["third", "information"]

    @classmethod
    def get_show_fields(cls):
        # return ["third", "information", 'callfunds_set', ((_('total call for
        # funds'), 'total_call'), (_('total estimate'), 'total_estimate')),
        # 'partition_set', ((_('initial state'), 'total_initial'), (_('total
        # ventilated'), 'total_ventilated')), ((_('total real'), 'total_real'),)]
        return {"": ["third", "information"],
                _("001@Owning"): ['propertylot_set', 'partition_set'],
                _("002@callfunds"): ['callfunds_set'],
                _("003@Situation"): [('payoff_set',),
                                     ((_('initial state'), 'total_initial'), (_('total real'), 'total_real')),
                                     ((_('total call for funds'), 'total_call'), (_('total payed'), 'total_payed')),
                                     ((_('total estimate'), 'total_estimate'), (_('total ventilated'), 'total_ventilated')), ]}

    @classmethod
    def get_print_fields(cls):
        fields = ["third"]
        fields.extend(["callfunds_set.num", "callfunds_set.date",
                       "callfunds_set.comment", (_('total'), 'callfunds_set.total')])
        fields.extend(["partition_set.set.str", "partition_set.set.budget", (_('expense'), 'partition_set.set.sumexpense_txt'),
                       "partition_set.value", (_("ratio"), 'partition_set.ratio'), (_('ventilated'), 'partition_set.ventilated_txt')])
        fields.extend(['propertylot_set.num', 'propertylot_set.value', 'propertylot_set.ratio', 'propertylot_set.description'])
        fields.extend(['payoff_set'])
        fields.extend([(_('total call for funds'), 'total_call'), (_('total estimate'), 'total_estimate'), (_('initial state'), 'total_initial'), (_(
            'total ventilated'), 'total_ventilated'), (_('total payed'), 'total_payed'), (_('total real'), 'total_real')])
        return fields

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_new = self.id is None
        Supporting.save(self, force_insert=force_insert,
                        force_update=force_update, using=using, update_fields=update_fields)
        if is_new:
            for setitem in Set.objects.all():
                Partition.objects.create(set=setitem, owner=self)

    @property
    def callfunds_query(self):
        if self.date_begin is None:
            self.set_dates()
        return Q(date__gte=self.date_begin) & Q(date__lte=self.date_end)

    @property
    def payoff_query(self):
        if self.date_begin is None:
            self.set_dates()
        return Q(date__gte=self.date_begin) & Q(date__lte=self.date_end)

    def get_total_call(self):
        val = 0
        for callfunds in self.callfunds_set.filter(self.callfunds_query):
            val += currency_round(callfunds.get_total())
        return val

    def get_total_payed(self, ignore_payoff=-1):
        val = Supporting.get_total_payed(self, ignore_payoff=ignore_payoff)
        for callfunds in self.callfunds_set.filter(self.callfunds_query):
            callfunds.check_supporting()
            val += currency_round(callfunds.supporting.get_total_payed(ignore_payoff))
        return val

    @property
    def total_call(self):
        return format_devise(self.get_total_call(), 5)

    def get_total_initial(self):
        if self.date_begin is None:
            self.set_dates()
        third_total = self.third.get_total(self.date_begin, False)
        third_total -= get_amount_sum(EntryLineAccount.objects.filter(Q(third=self.third) & Q(
            entry__date_value=self.date_begin) & Q(entry__journal__id=1) & Q(account__type_of_account=0)).aggregate(Sum('amount')))
        third_total += get_amount_sum(EntryLineAccount.objects.filter(Q(third=self.third) & Q(
            entry__date_value=self.date_begin) & Q(entry__journal__id=1) & Q(account__type_of_account=1)).aggregate(Sum('amount')))
        return third_total

    @property
    def property_part(self):
        total_part = PropertyLot.get_total_part()
        if total_part > 0:
            total = self.propertylot_set.aggregate(sum=Sum('value'))
            if ('sum' in total.keys()) and (total['sum'] is not None):
                value = total['sum']
            else:
                value = 0
            return "%d/%d{[br/]}%.1f %%" % (value, total_part, 100.0 * float(value) / float(total_part))
        else:
            return "---"

    @property
    def total_initial(self):
        return format_devise(self.get_total_initial(), 5)

    @property
    def total_estimate(self):
        return format_devise(-1 * self.get_total_rest_topay(), 5)

    def get_total(self):
        return self.get_total_call() - self.get_total_initial()

    def get_total_ventilated(self):
        return self.get_total_payed() + self.get_total_initial() - self.third.get_total(self.date_end)

    @property
    def total_ventilated(self):
        return format_devise(self.get_total_ventilated(), 5)

    @property
    def total_real(self):
        return format_devise(self.third.get_total(self.date_end), 5)

    def get_max_payoff(self, ignore_payoff=-1):
        return 1000000

    def payoff_is_revenu(self):
        return True

    class Meta(object):
        verbose_name = _('owner')
        verbose_name_plural = _('owners')

    def support_validated(self, validate_date):
        return self

    def get_tax(self):
        return 0.0

    def get_payable_without_tax(self):
        return currency_round(max(0, self.get_total_rest_topay()))

    def payoff_have_payment(self):
        return (self.get_total_rest_topay() > 0.001)

    @classmethod
    def get_payment_fields(cls):
        return ["third", "information", 'callfunds_set', ((_('total estimate'), 'total_estimate'),)]

    def get_payment_name(self):
        return _('codominium of %s') % six.text_type(self.third)

    def get_docname(self):
        return _('your situation')


class Partition(LucteriosModel):
    set = models.ForeignKey(
        Set, verbose_name=_('set'), null=False, db_index=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        Owner, verbose_name=_('owner'), null=False, db_index=True, on_delete=models.CASCADE)
    value = models.DecimalField(_('value'), max_digits=7, decimal_places=2, default=0.0, validators=[
        MinValueValidator(0.0), MaxValueValidator(1000.00)])

    def __str__(self):
        return "%s : %s" % (self.owner, self.ratio)

    @classmethod
    def get_default_fields(cls):
        return ["set", "set.budget", (_('expense'), 'set.sumexpense_txt'), "owner", "value", (_("ratio"), 'ratio'), (_('ventilated'), 'ventilated_txt')]

    @classmethod
    def get_edit_fields(cls):
        return ["set", "owner", "value"]

    def get_ratio(self):
        total = self.set.total_part
        if abs(total) < 0.01:
            return 0.0
        else:
            return float(100 * self.value / total)

    def set_context(self, xfer):
        if xfer is not None:
            self.set.set_dates(convert_date(xfer.getparam("begin_date")), convert_date(
                xfer.getparam("end_date")))

    def get_ventilated(self):
        value = 0
        ratio = self.get_ratio()
        if abs(ratio) > 0.01:
            for expensedetail in self.set.get_expenselist():
                total = expensedetail.expenseratio_set.filter(owner=self.owner).aggregate(sum=Sum('value'))
                if ('sum' in total.keys()) and (total['sum'] is not None):
                    value += currency_round(total['sum'])
        return value

    @property
    def ventilated_txt(self):
        return format_devise(self.get_ventilated(), 5)

    @property
    def ratio(self):
        return "%.1f %%" % self.get_ratio()

    class Meta(object):
        verbose_name = _("class load")
        verbose_name_plural = _("class loads")
        default_permissions = []
        ordering = ['owner__third_id', 'set_id']


class PropertyLot(LucteriosModel):
    num = models.IntegerField(verbose_name=_('numeros'), null=False, default=1)
    value = models.IntegerField(_('value'), default=0, validators=[MinValueValidator(0), MaxValueValidator(10000)])
    description = models.TextField(_('description'), null=True, default="")
    owner = models.ForeignKey(
        Owner, verbose_name=_('owner'), null=False, db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return "[%s] %s" % (self.num, self.description)

    @classmethod
    def get_default_fields(cls):
        return ["num", "value", (_("ratio"), 'ratio'), "description", "owner"]

    @classmethod
    def get_edit_fields(cls):
        return ["num", "value", "description", "owner"]

    @classmethod
    def get_total_part(cls):
        total = cls.objects.all().aggregate(sum=Sum('value'))
        if ('sum' in total.keys()) and (total['sum'] is not None):
            return total['sum']
        else:
            return 0

    def get_ratio(self):
        total = self.get_total_part()
        if abs(total) < 0.01:
            return 0.0
        else:
            return 100.0 * float(self.value) / float(total)

    @property
    def ratio(self):
        return "%.1f %%" % self.get_ratio()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        LucteriosModel.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        for set_linked in Set.objects.filter(is_link_to_lots=True, set_of_lots__id=self.id):
            set_linked.refresh_ratio_link_lots()

    class Meta(object):
        verbose_name = _('property lot')
        verbose_name_plural = _('property lots')
        default_permissions = []
        ordering = ['num']


class CallFundsSupporting(Supporting):

    def __str__(self):
        return self.callfunds.__str__()

    def get_total(self):
        return self.callfunds.get_total()

    def get_third_mask(self):
        return current_system_account().get_societary_mask()

    def payoff_is_revenu(self):
        return True

    @classmethod
    def get_payment_fields(cls):
        return ["third", "callfunds.num", "callfunds.date", (_('total'), 'callfunds.total')]

    def support_validated(self, validate_date):
        return self.callfunds

    def get_tax(self):
        return 0

    def get_payable_without_tax(self):
        return self.get_total_rest_topay()

    def payoff_have_payment(self):
        return (self.status == 1) and (self.get_total_rest_topay() > 0.001)

    class Meta(object):
        default_permissions = []


class CallFunds(LucteriosModel):
    owner = models.ForeignKey(Owner, verbose_name=_('owner'), null=True, db_index=True, on_delete=models.PROTECT)
    supporting = models.OneToOneField(CallFundsSupporting, on_delete=models.CASCADE, default=None, null=True)
    num = models.IntegerField(verbose_name=_('numeros'), null=True)
    date = models.DateField(verbose_name=_('date'), null=False)
    comment = models.TextField(_('comment'), null=True, default="")
    type_call = models.IntegerField(verbose_name=_('type of call'),
                                    choices=((0, _('current')), (1, _('exceptional')), (2, _('cash advance'))), null=False, default=0, db_index=True)
    status = FSMIntegerField(verbose_name=_('status'),
                             choices=((0, _('building')), (1, _('valid')), (2, _('ended'))), null=False, default=0, db_index=True)

    def __str__(self):
        return _('call of funds #%(num)d - %(date)s') % {'num': self.num, 'date': get_value_converted(self.date)}

    @classmethod
    def get_default_fields(cls):
        return ["num", 'type_call', "date", "owner", "comment", (_('total'), 'total'), (_('rest to pay'), 'supporting.total_rest_topay')]

    @classmethod
    def get_edit_fields(cls):
        return ["status", 'type_call', "date", "comment"]

    @classmethod
    def get_show_fields(cls):
        return [("num", "date"), ("owner", 'type_call'), "calldetail_set", "comment", ("status", (_('total'), 'total'))]

    def get_total(self):
        self.check_supporting()
        val = 0
        for calldetail in self.calldetail_set.all():
            val += currency_round(calldetail.price)
        return val

    @property
    def total(self):
        return format_devise(self.get_total(), 5)

    def can_delete(self):
        if self.status != 0:
            return _('"%s" cannot be deleted!') % six.text_type(self)
        return ''

    transitionname__valid = _("Valid")

    @transition(field=status, source=0, target=1, conditions=[lambda item:(len(Owner.objects.all()) > 0) and (len(item.calldetail_set.all()) > 0)])
    def valid(self):
        val = CallFunds.objects.exclude(status=0).aggregate(Max('num'))
        if val['num__max'] is None:
            new_num = 1
        else:
            new_num = val['num__max'] + 1
        last_call = None
        calls_by_owner = {}
        for owner in Owner.objects.all():
            calls_by_owner[owner.id] = CallFunds.objects.create(num=new_num, date=self.date, owner=owner, comment=self.comment,
                                                                status=1, supporting=CallFundsSupporting.objects.create(third=owner.third))
            last_call = calls_by_owner[owner.id]
        for calldetail in self.calldetail_set.all():
            amount = float(calldetail.price)
            new_detail = None
            for part in calldetail.set.partition_set.all().order_by('value'):
                if part.value > 0.001:
                    new_detail = CallDetail.objects.create(
                        set=calldetail.set, designation=calldetail.designation)
                    new_detail.callfunds = calls_by_owner[part.owner.id]
                    new_detail.price = currency_round(float(
                        calldetail.price) * part.get_ratio() / 100.0)
                    amount -= new_detail.price
                    new_detail.save()
            if abs(amount) > 0.0001:
                new_detail.price += amount
                new_detail.save()
        for new_call in calls_by_owner.values():
            if new_call.get_total() < 0.0001:
                new_call.delete()
        self.delete()
        if last_call is not None:
            self.__dict__ = last_call.__dict__

    transitionname__close = _("Closed")

    @transition(field=status, source=1, target=2)
    def close(self):
        pass

    def check_supporting(self):
        if (self.owner is not None) and (self.supporting is None):
            self.supporting = CallFundsSupporting.objects.create(third=self.owner.third)
            self.save()

    class Meta(object):
        verbose_name = _('call of funds')
        verbose_name_plural = _('calls of funds')


class CallDetail(LucteriosModel):
    callfunds = models.ForeignKey(
        CallFunds, verbose_name=_('call of funds'), null=True, default=None, db_index=True, on_delete=models.CASCADE)
    set = models.ForeignKey(
        Set, verbose_name=_('set'), null=False, db_index=True, on_delete=models.PROTECT)
    designation = models.TextField(verbose_name=_('designation'))
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=3, default=0.0, validators=[
        MinValueValidator(0.0), MaxValueValidator(9999999.999)])

    @classmethod
    def get_default_fields(cls):
        return ["set", "designation", (_('price'), 'price_txt')]

    @classmethod
    def get_edit_fields(cls):
        return ["set", "designation", "price"]

    @property
    def price_txt(self):
        return format_devise(self.price, 5)

    class Meta(object):
        verbose_name = _('detail of call')
        verbose_name_plural = _('details of call')
        default_permissions = []


class Expense(Supporting):
    num = models.IntegerField(verbose_name=_('numeros'), null=True)
    date = models.DateField(verbose_name=_('date'), null=False)
    comment = models.TextField(_('comment'), null=True, default="")
    expensetype = models.IntegerField(verbose_name=_('expense type'),
                                      choices=((0, _('expense')), (1, _('asset of expense'))), null=False, default=0, db_index=True)
    status = FSMIntegerField(verbose_name=_('status'),
                             choices=((0, _('building')), (1, _('valid')), (2, _('ended'))), null=False, default=0, db_index=True)
    entries = models.ManyToManyField(EntryAccount, verbose_name=_('entries'))

    def __str__(self):
        if self.expensetype == 0:
            typetxt = _('expense')
        else:
            typetxt = _('asset of expense')
        return "%s %s - %s" % (typetxt, self.num, self.comment)

    @classmethod
    def get_default_fields(cls, status=-1):
        fields = ["num", "date", "third", "comment", (_('total'), 'total')]
        if status == 1:
            fields.append(Supporting.get_payoff_fields()[-1][-1])
        return fields

    def get_third_mask(self):
        return current_system_account().get_provider_mask()

    @classmethod
    def get_edit_fields(cls):
        return ["status", 'expensetype', "date", "comment"]

    @classmethod
    def get_show_fields(cls):
        return ["third", ("num", "date"), "expensetype", "expensedetail_set", "comment", ("status", (_('total'), 'total'))]

    def get_total(self):
        val = 0
        for expensedetail in self.expensedetail_set.all():
            val += currency_round(expensedetail.price)
        return val

    def payoff_is_revenu(self):
        return self.expensetype == 1

    def default_date(self):
        return self.date

    def entry_links(self):
        if self.entries is None:
            return []
        else:
            return list(self.entries.all())

    def can_delete(self):
        if self.status != 0:
            return _('"%s" cannot be deleted!') % six.text_type(self)
        return ''

    @property
    def total(self):
        return format_devise(self.get_total(), 5)

    def generate_revenue_entry(self, is_asset, fiscal_year):
        for detail in self.expensedetail_set.all():
            detail.generate_revenue_entry(is_asset, fiscal_year)

    def generate_expense_entry(self, is_asset, fiscal_year):
        third_account = self.get_third_account(
            current_system_account().get_provider_mask(), fiscal_year)
        detail_sums = {}
        for detail in self.expensedetail_set.all():
            cost_accounting = detail.set.cost_accounting_id
            if cost_accounting == 0:
                cost_accounting = None
            if cost_accounting not in detail_sums.keys():
                detail_sums[cost_accounting] = {}
            detail_account = ChartsAccount.get_account(
                detail.expense_account, fiscal_year)
            if detail_account is None:
                raise LucteriosException(
                    IMPORTANT, _("code account %s unknown!") % detail.expense_account)
            if detail_account.id not in detail_sums[cost_accounting].keys():
                detail_sums[cost_accounting][detail_account.id] = 0
            detail_sums[cost_accounting][
                detail_account.id] += currency_round(detail.price)
        entries = []
        for cost_accounting, detail_sum in detail_sums.items():
            new_entry = EntryAccount.objects.create(
                year=fiscal_year, date_value=self.date, designation=self.__str__(),
                journal=Journal.objects.get(id=2), costaccounting_id=cost_accounting)
            total = 0
            for detail_accountid, price in detail_sum.items():
                EntryLineAccount.objects.create(
                    account_id=detail_accountid, amount=is_asset * price, entry=new_entry)
                total += price
            EntryLineAccount.objects.create(
                account=third_account, amount=is_asset * total, third=self.third, entry=new_entry)
            no_change, debit_rest, credit_rest = new_entry.serial_control(
                new_entry.get_serial())
            if not no_change or (abs(debit_rest) > 0.001) or (abs(credit_rest) > 0.001):
                raise LucteriosException(GRAVE, _("Error in accounting generator!") +
                                         "{[br/]} no_change=%s debit_rest=%.3f credit_rest=%.3f" % (no_change, debit_rest, credit_rest))
            entries.append(six.text_type(new_entry.id))
        self.entries = EntryAccount.objects.filter(id__in=entries)

    def check_if_can_reedit(self):
        is_close = False
        for detail in self.expensedetail_set.all():
            is_close = is_close or ((detail.entry is not None) and detail.entry.close)
        for entry in self.entries.all():
            is_close = is_close or entry.close
        for payoff in self.payoff_set.all():
            is_close = is_close or ((payoff.entry is not None) and payoff.entry.close)
        return not is_close

    transitionname__reedit = _("Re-edit")

    @transition(field=status, source=1, target=0, conditions=[lambda item:item.check_if_can_reedit()])
    def reedit(self):
        def del_entry(entry_id):
            current_entry = EntryAccount.objects.get(id=entry_id)
            current_entry.delete()
        for payoff in self.payoff_set.all():
            payoff.delete()
        for detail in self.expensedetail_set.all():
            del_entry(detail.entry_id)
            detail.entry = None
            detail.save()
        for entry in self.entries.all():
            del_entry(entry.id)

    transitionname__valid = _("Valid")

    @transition(field=status, source=0, target=1, conditions=[lambda item:item.get_info_state() == ''])
    def valid(self):
        if self.expensetype == 0:
            is_asset = 1
        else:
            is_asset = -1
        fiscal_year = FiscalYear.get_current()
        val = Expense.objects.filter(date__gte=fiscal_year.begin, date__lte=fiscal_year.end).exclude(status=0).aggregate(Max('num'))
        if val['num__max'] is None:
            self.num = 1
        else:
            self.num = val['num__max'] + 1
        self.generate_expense_entry(is_asset, fiscal_year)
        self.generate_revenue_entry(is_asset, fiscal_year)

    transitionname__close = _("Closed")

    @transition(field=status, source=1, target=2)
    def close(self):
        if self.entries is not None:
            for entry in self.entries.all():
                entry.closed()
        for detail in self.expensedetail_set.all():
            if detail.entry is not None:
                detail.entry.closed()
        for payoff in self.payoff_set.all():
            if payoff.entry is not None:
                payoff.entry.closed()

    def get_info_state(self):
        info = []
        if self.status == 0:
            info = Supporting.get_info_state(
                self, current_system_account().get_provider_mask())
        info.extend(self.check_date(self.date.isoformat()))
        return "{[br/]}".join(info)

    class Meta(object):
        verbose_name = _('expense')
        verbose_name_plural = _('expenses')
        ordering = ['-date']


class ExpenseDetail(LucteriosModel):
    expense = models.ForeignKey(
        Expense, verbose_name=_('expense'), null=True, default=None, db_index=True, on_delete=models.CASCADE)
    set = models.ForeignKey(
        Set, verbose_name=_('set'), null=False, db_index=True, on_delete=models.PROTECT)
    designation = models.TextField(verbose_name=_('designation'))
    expense_account = models.CharField(
        verbose_name=_('account'), max_length=50)
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=3, default=0.0, validators=[
        MinValueValidator(0.0), MaxValueValidator(9999999.999)])
    entry = models.ForeignKey(
        EntryAccount, verbose_name=_('entry'), null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%s: %s" % (self.expense, self.designation)

    @classmethod
    def get_default_fields(cls):
        return ["set", "designation", "expense_account", (_('price'), 'price_txt'), (_('ratio'), 'ratio_txt')]

    @classmethod
    def get_edit_fields(cls):
        return ["set", "designation", "expense_account", "price"]

    @property
    def price_txt(self):
        return format_devise(self.price, 5)

    @property
    def ratio_txt(self):
        ratio = ""
        if self.expense.status == 0:
            for part in self.set.partition_set.exclude(value=0.0):
                ratio += six.text_type(part)
                ratio += "{[br/]}"
        else:
            for part in self.expenseratio_set.all():
                ratio += six.text_type(part)
                ratio += "{[br/]}"
        return ratio

    def generate_revenue_entry(self, is_asset, fiscal_year):
        self.generate_ratio(is_asset)
        cost_accounting = self.set.cost_accounting_id
        if cost_accounting == 0:
            cost_accounting = None
        detail_account = ChartsAccount.get_account(self.set.revenue_account, fiscal_year)
        if detail_account is None:
            raise LucteriosException(
                IMPORTANT, _("code account %s unknown!") % self.set.revenue_account)
        price = currency_round(self.price)
        new_entry = EntryAccount.objects.create(
            year=fiscal_year, date_value=self.expense.date, designation=self.__str__(),
            journal=Journal.objects.get(id=3), costaccounting_id=cost_accounting)
        EntryLineAccount.objects.create(account=detail_account, amount=is_asset * price, entry=new_entry)
        for ratio in self.expenseratio_set.all():
            third_account = self.expense.get_third_account(current_system_account().get_societary_mask(), fiscal_year, ratio.owner.third)
            EntryLineAccount.objects.create(account=third_account, amount=ratio.value, entry=new_entry, third=ratio.owner.third)
        no_change, debit_rest, credit_rest = new_entry.serial_control(new_entry.get_serial())
        if not no_change or (abs(debit_rest) > 0.001) or (abs(credit_rest) > 0.001):
            raise LucteriosException(GRAVE, _("Error in accounting generator!") +
                                     "{[br/]} no_change=%s debit_rest=%.3f credit_rest=%.3f" % (no_change, debit_rest, credit_rest))
        self.entry = new_entry
        self.save()

    def generate_ratio(self, is_asset):
        price = currency_round(self.price)
        last_line = None
        total = 0
        for part in Partition.objects.filter(set=self.set).order_by('value'):
            amount = currency_round(price * part.get_ratio() / 100.0)
            if amount > 0.0001:
                last_line, _created = ExpenseRatio.objects.get_or_create(expensedetail=self, owner=part.owner)
                last_line.value = is_asset * amount
                last_line.save()
                total += amount
        if (last_line is not None) and (abs(price - total) > 0.0001):
            last_line.value += is_asset * (price - total)
            last_line.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.expense_account = correct_accounting_code(self.expense_account)
        return LucteriosModel.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta(object):
        verbose_name = _('detail of expense')
        verbose_name_plural = _('details of expense')
        default_permissions = []


class ExpenseRatio(LucteriosModel):
    expensedetail = models.ForeignKey(
        ExpenseDetail, verbose_name=_('detail of expense'), null=False, db_index=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        Owner, verbose_name=_('owner'), null=False, db_index=True, on_delete=models.CASCADE)
    value = models.DecimalField(_('value'), max_digits=7, decimal_places=2, default=0.0, validators=[
        MinValueValidator(0.0), MaxValueValidator(1000.00)])

    def __str__(self):
        return "%s : %.1f %%" % (six.text_type(self.owner.third), 100.0 * float(abs(self.value)) / float(self.expensedetail.price))

    class Meta(object):
        verbose_name = _('detail of expense')
        verbose_name_plural = _('details of expense')
        default_permissions = []
        ordering = ['owner__third_id']


@Signal.decorate('checkparam')
def condominium_checkparam():
    Parameter.check_and_create(name='condominium-default-owner-account', typeparam=0, title=_("condominium-default-owner-account"),
                               args="{'Multi':False}", value='450')
