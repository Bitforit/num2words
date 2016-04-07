# -*- encoding: utf-8 -*-
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

ZERO = (u'nulle',)

ONES = {
    1: (u'viens',),
    2: (u'divi',),
    3: (u'trīs',),
    4: (u'četri',),
    5: (u'pieci',),
    6: (u'seši',),
    7: (u'septiņi',),
    8: (u'astoņi',),
    9: (u'deviņi',),
}

TENS = {
    0: (u'desmit',),
    1: (u'vienpadsmit',),
    2: (u'divpadsmit',),
    3: (u'trīspadsmit',),
    4: (u'četrpadsmit',),
    5: (u'piecpadsmit',),
    6: (u'sešpadsmit',),
    7: (u'septiņpadsmit',),
    8: (u'astoņpadsmit',),
    9: (u'deviņpadsmit',),
}

TWENTIES = {
    2: (u'divdesmit',),
    3: (u'trīsdesmit',),
    4: (u'četrdesmit',),
    5: (u'piecdesmit',),
    6: (u'sešdesmit',),
    7: (u'septiņdesmit',),
    8: (u'astoņdesmit',),
    9: (u'deviņdesmit',),
}

HUNDRED = (u'simts', u'simti', u'simtu')

THOUSANDS = {
    1: (u'tūkstotis', u'tūkstoši', u'tūkstošu'),
    2: (u'miljons', u'miljoni', u'miljonu'),
    3: (u'miljards', u'miljardi', u'miljardu'),
    4: (u'triljons', u'triljoni', u'triljonu'),
    5: (u'kvadriljons', u'kvadriljoni', u'kvadriljonu'),
    6: (u'kvintiljons', u'kvintiljoni', u'kvintiljonu'),
    7: (u'sikstiljons', u'sikstiljoni', u'sikstiljonu'),
    8: (u'septiljons', u'septiljoni', u'septiljonu'),
    9: (u'oktiljons', u'oktiljoni', u'oktiljonu'),
    10: (u'nontiljons', u'nontiljoni', u'nontiljonu'),
}

CURRENCIES = {
    'LVL': (
        (u'lats', u'lati', u'latu'), (u'santīms', u'santīmi', u'santīmu')
    ),
    'EUR': (
        (u'eiro', u'eiro', u'eiro'), (u'cents', u'centi', u'centu')
    ),
    'USD': (
        (u'dolārs', u'dolāri', u'dolāru'), (u'cents', u'centi', u'centu')
    ),
    'GBP': (
        (u'mārciņa', u'mārciņas', u'mārciņu'), (u'penijs', u'peniji', u'peniju')
    ),
    'RUB': (
        (u'rublis', u'rubļi', u'rubļu'), (u'kapeika', u'kapeikas', u'kapeiku')
    ),
}


def splitby3(n):
    length = len(n)
    if length > 3:
        start = length % 3
        if start > 0:
            yield int(n[:start])
        for i in range(start, length, 3):
            yield int(n[i:i+3])
    else:
        yield int(n)


def get_digits(n):
    return [int(x) for x in reversed(list(('%03d' % n)[-3:]))]


def pluralize(n, forms):
    # gettext implementation:
    # (n%10==1 && n%100!=11 ? 0 : n != 0 ? 1 : 2)

    form = 0 if (n % 10 == 1 and n % 100 != 11) else 1 if n != 0 else 2

    return forms[form]


def int2word(n):
    if n == 0:
        return ZERO[0]

    words = []
    chunks = list(splitby3(str(n)))
    i = len(chunks)
    for x in chunks:
        i -= 1
        n1, n2, n3 = get_digits(x)

        if n3 > 0:
            words.append(ONES[n3][0])
            if n3 > 1:
                words.append(HUNDRED[1])
            else:
                words.append(HUNDRED[0])

        if n2 > 1:
            words.append(TWENTIES[n2][0])

        if n2 == 1:
            words.append(TENS[n1][0])
        elif n1 > 0:
            words.append(ONES[n1][0])

        if i > 0:
            words.append(pluralize(x, THOUSANDS[i]))

    return ' '.join(words)


def n2w(n):
    n = str(n).replace(',', '.')
    if '.' in n:
        left, right = n.split('.')
        return u'%s komats %s' % (int2word(int(left)), int2word(int(right)))
    else:
        return int2word(int(n))


def to_currency(n, currency='EUR', cents=True, seperator=','):
    if type(n) == int:
        if n < 0:
            minus = True
        else:
            minus = False

        n = abs(n)
        left = n / 100
        right = n % 100
    else:
        n = str(n).replace(',', '.')
        if '.' in n:
            left, right = n.split('.')
        else:
            left, right = n, 0
        left, right = int(left), int(right)
        minus = False
    cr1, cr2 = CURRENCIES[currency]

    if minus:
        minus_str = "mīnus "
    else:
        minus_str = ""

    if cents:
        cents_str = int2word(right)
    else:
        cents_str = "%02d" % right

    return u'%s%s %s%s %s %s' % (
        minus_str,
        int2word(left),
        pluralize(left, cr1),
        seperator,
        cents_str,
        pluralize(right, cr2)
    )


class Num2Word_LV(object):
    def to_cardinal(self, number):
        return n2w(number)

    def to_ordinal(self, number):
        raise NotImplementedError()


class Num2Currency_LV(object):
    def convert(self, number, currency):
        return to_currency(number, currency, False)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
