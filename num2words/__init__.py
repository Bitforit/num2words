# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import unicode_literals

from . import lang_EN
from . import lang_EN_GB
from . import lang_EN_IN
from . import lang_EN_EUR
from . import lang_EN_USD
from . import lang_EN_RUB
from . import lang_FR
from . import lang_FR_CH
from . import lang_DE
from . import lang_ES
from . import lang_LT
from . import lang_LV
from . import lang_PL
from . import lang_RU
from . import lang_ID
from . import lang_NO
from . import lang_DK
from . import lang_PT_BR


CONVERTER_CLASSES = {
    'en': lang_EN.Num2Word_EN(),
    'en_GB': lang_EN_GB.Num2Word_EN_GB(),
    'en_IN': lang_EN_IN.Num2Word_EN_IN(),
    'fr': lang_FR.Num2Word_FR(),
    'fr_CH': lang_FR_CH.Num2Word_FR_CH(),
    'de': lang_DE.Num2Word_DE(),
    'es': lang_ES.Num2Word_ES(),
    'id': lang_ID.Num2Word_ID(),
    'lt': lang_LT.Num2Word_LT(),
    'lv': lang_LV.Num2Word_LV(),
    'pl': lang_PL.Num2Word_PL(),
    'ru': lang_RU.Num2Word_RU(),
    'no': lang_NO.Num2Word_NO(),
    'dk': lang_DK.Num2Word_DK(),
    'pt_BR': lang_PT_BR.Num2Word_PT_BR(),
}


class Num2Currency_EN(object):
    def convert(self, number, currency):
        if currency == 'EUR':
            lng = lang_EN_EUR.Num2Word_EN_EUR()
        elif currency == 'GBP':
            lng = lang_EN_GB.Num2Word_EN_GB()
        elif currency == 'USD':
            lng = lang_EN_USD.Num2Word_EN_USD()
        elif currency == 'RUB':
            lng = lang_EN_RUB.Num2Word_EN_RUB()
        else:
            raise NotImplementedError()
        number = int('{0:.2f}'.format(number).replace('.', ''))
        return lng.to_currency(number)


CONVERT_CLASSES_CURRENCY = {
    'lv': lang_LV.Num2Currency_LV(),
    'lt': lang_LT.Num2Currency_LT(),
    'ru': lang_RU.Num2Currency_RU(),
    'en': Num2Currency_EN(),
}


def to_currency(number, lang, currency):
    if lang not in CONVERT_CLASSES_CURRENCY:
        raise NotImplementedError()
    return CONVERT_CLASSES_CURRENCY[lang].convert(number, currency)


def num2words(number, ordinal=False, lang='en'):
    # We try the full language first
    if lang not in CONVERTER_CLASSES:
        # ... and then try only the first 2 letters
        lang = lang[:2]
    if lang not in CONVERTER_CLASSES:
        raise NotImplementedError()
    converter = CONVERTER_CLASSES[lang]
    if ordinal:
        return converter.to_ordinal(number)
    else:
        return converter.to_cardinal(number)
