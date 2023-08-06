# -*- coding: utf-8 -*-
'''
Printmodel django module for condominium

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2016 sd-libre.fr
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

from django.utils.translation import ugettext_lazy as _

from diacamma.condominium.models import Owner

name = _("owner")
kind = 2
modelname = Owner.get_long_name()
value = """
<model hmargin="10.0" vmargin="10.0" page_width="210.0" page_height="297.0">
<header extent="25.0">
<text height="20.0" width="120.0" top="5.0" left="70.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="20" font_family="sans-serif" font_weight="" font_size="20">
{[b]}#OUR_DETAIL.name{[/b]}
</text>
<image height="25.0" width="30.0" top="0.0" left="10.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2">
#OUR_DETAIL.image
</image>
</header>
<bottom extent="10.0">
<text height="10.0" width="190.0" top="00.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="8" font_family="sans-serif" font_weight="" font_size="8">
{[italic]}
#OUR_DETAIL.address - #OUR_DETAIL.postal_code #OUR_DETAIL.city - #OUR_DETAIL.tel1 #OUR_DETAIL.tel2 #OUR_DETAIL.email{[br/]}#OUR_DETAIL.identify_number
{[/italic]}
</text>
</bottom>
<body>
<text height="8.0" width="190.0" top="0.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="15" font_family="sans-serif" font_weight="" font_size="15">
{[b]}%(title)s{[/b]}
</text>
<text height="8.0" width="190.0" top="8.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="13" font_family="sans-serif" font_weight="" font_size="13">
#date_begin - #date_end
</text>
<text height="20.0" width="100.0" top="25.0" left="80.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
{[b]}#third.contact.str{[/b]}{[br/]}#third.contact.address{[br/]}#third.contact.postal_code #third.contact.city
</text>

<text height="20.0" width="100.0" top="25.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
{[b]}%(info)s{[/b]}: #information
</text>

<table height="70.0" width="105.0" top="45.0" left="40.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2">
    <columns width="80.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="right" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    </columns>
    <columns width="25.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="right" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[i]}%(value)s{[/i]}
    </columns>
    <rows>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        {[b]}%(total_call)s{[/b]}
        </cell>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        #total_call{[br/]}
        </cell>
    </rows>
    <rows>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        {[b]}%(total_estimate)s{[/b]}
        </cell>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        #total_estimate
        </cell>
    </rows>
    <rows>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        {[b]}%(total_initial)s{[/b]}
        </cell>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        #total_initial
        </cell>
    </rows>
    <rows>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        {[b]}%(total_ventilated)s{[/b]}
        </cell>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        #total_ventilated
        </cell>
    </rows>
    <rows>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        {[b]}%(total_payed)s{[/b]}
        </cell>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        #total_payed
        </cell>
    </rows>
    <rows>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        {[b]}%(total_real)s{[/b]}
        </cell>
        <cell border_color="black" border_style="" border_width="0.2" text_align="right" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
        #total_real
        </cell>
    </rows>
</table>

<text height="10.0" width="100.0" top="115.0" left="25.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
{[b]}%(call of funds)s{[/b]}
</text>
<table height="20.0" width="150.0" top="125.0" left="20.0" padding="1.0" spacing="0.1" border_color="black" border_style="" border_width="0.2">
    <columns width="10.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(num)s{[/b]}
    </columns>
    <columns width="25.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(date)s{[/b]}
    </columns>
    <columns width="90.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(comment)s{[/b]}
    </columns>
    <columns width="25.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(total)s{[/b]}
    </columns>
    <rows data="callfunds_set">
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#num
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#date
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#comment
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#total
        </cell>
    </rows>
</table>

<text height="10.0" width="100.0" top="145.0" left="25.0" padding="1.0" spacing="1.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
{[b]}%(partition)s{[/b]}
</text>
<table height="20.0" width="150.0" top="155.0" left="20.0" padding="1.0" spacing="0.1" border_color="black" border_style="" border_width="0.2">
    <columns width="50.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(set)s{[/b]}
    </columns>
    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(budget)s{[/b]}
    </columns>
    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(expense)s{[/b]}
    </columns>
    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(value)s{[/b]}
    </columns>
    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(ratio)s{[/b]}
    </columns>
    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(ventilated)s{[/b]}
    </columns>
    <rows data="partition_set">
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#set
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#set.budget_txt
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#set.sumexpense_txt
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#value
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#ratio
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#ventilated_txt
        </cell>
    </rows>
</table>

<text height="10.0" width="100.0" top="175.0" left="25.0" padding="1.0" spacing="1.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
{[b]}%(payoff)s{[/b]}
</text>
<table height="20.0" width="150.0" top="185.0" left="20.0" padding="1.0" spacing="0.1" border_color="black" border_style="" border_width="0.2">
    <columns width="25.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(date)s{[/b]}
    </columns>
    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(amount)s{[/b]}
    </columns>
    <columns width="30.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(payer)s{[/b]}
    </columns>
    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(mode)s{[/b]}
    </columns>
    <columns width="25.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(bank_account)s{[/b]}
    </columns>
    <columns width="30.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(reference)s{[/b]}
    </columns>
    <rows data="payoff_set">
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#date
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#value
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#payer
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#mode
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#bank_account
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">
#reference
        </cell>
    </rows>
</table>


</body>
</model>""" % {'title': _('Owner situation'), 'info': _('information'), 'call of funds': _('call of funds'), 'num': _('numeros'), 'date': _('date'), 'comment': _('comment'), 'total': _('total'),
               'partition': _('partition'), 'set': _('set'), 'budget': _('budget'), 'expense': _('expense'), 'value': _('value'), 'ratio': _('ratio'), 'ventilated': _('ventilated'),
               'payoff': _('payoff'), 'amount': _('amount'), 'payer': _('payer'), 'mode': _('mode'), 'bank_account': _('bank account'), 'reference': _('reference'),
               'total_call': _('total call for funds'), 'total_estimate': _('total estimate'), 'total_initial': _('initial state'), 'total_ventilated': _('total ventilated'), 'total_payed': _('total payed'), 'total_real': _('total real')}
