#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# regex.py -
# Copyright (C) 2015-2016 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import datetime
import re

from bormeparser.acto import ACTO
from bormeparser.cargo import CARGO

esc_arg_keywords = [x.replace('.', '\.').replace('(', '\(').replace(')', '\)') for x in ACTO.ARG_KEYWORDS]
esc_colon_keywords = [x.replace('.', '\.') for x in ACTO.COLON_KEYWORDS]
esc_rare_keywords = [x.replace('.', '\.') for x in ACTO.RARE_KEYWORDS]
esc_noarg_keywords = [x.replace('.', '\.').replace('(', '\(').replace(')', '\)') for x in ACTO.NOARG_KEYWORDS]
esc_ending_keywords = [x.replace('.', '\.') for x in ACTO.ENDING_KEYWORDS]

esc_cargos_keywords = [x.replace('.', '\.') for x in CARGO.KEYWORDS]

# -- ACTOS --
# OR de las palabras clave con argumentos
RE_ARG_KEYWORDS = '(%s)' % '|'.join(esc_arg_keywords)
RE_ALL_KEYWORDS = '(%s|%s|%s|%s)' % ('|'.join(esc_arg_keywords), '|'.join(esc_colon_keywords),
                                     '|'.join(esc_noarg_keywords), esc_ending_keywords[0])
# OR de las palabras clave, "non grouping"
RE_ALL_KEYWORDS_NG = '(?:%s|%s|%s|%s)' % ('|'.join(esc_arg_keywords), '|'.join(esc_colon_keywords),
                                          '|'.join(esc_noarg_keywords), esc_ending_keywords[0])
# OR de las palabras clave sin argumentos
RE_NOARG_KEYWORDS = '(%s)' % '|'.join(esc_noarg_keywords)
# OR de las palabras clave con argumentos seguidas por :
RE_COLON_KEYWORDS = '(%s)' % '|'.join(esc_colon_keywords)
RE_RARE_KEYWORDS = '(%s)' % '|'.join(esc_rare_keywords)
RE_ENDING_KEYWORD = '(%s)' % esc_ending_keywords[0]

# -- CARGOS --
# OR de las palabras clave
RE_CARGOS_KEYWORDS = '(%s)' % '|'.join(esc_cargos_keywords)
# RE para capturar el cargo y los nombres
RE_CARGOS_MATCH = RE_CARGOS_KEYWORDS + ":\s(.*?)(?:\.$|\. |\s*$)"

"""
DEPRECATED
REGEX1 = re.compile('^(\d+) - (.*?)\.\s*' + RE_ALL_KEYWORDS_NG)
# Captura cada palabra clave con sus argumentos
REGEX2 = re.compile('(?=' + RE_ARG_KEYWORDS + '\.\s+(.*?)\.\s*' + RE_ALL_KEYWORDS_NG + ')')
REGEX3 = re.compile(RE_COLON_KEYWORDS + ':\s+(.*?)\.\s*' + RE_ALL_KEYWORDS_NG)
REGEX4 = re.compile(RE_ENDING_KEYWORD + '\.\s+(.*)\.\s*')
REGEX5 = re.compile(RE_NOARG_KEYWORDS + '\.')
"""

REGEX_NOARG = re.compile(RE_NOARG_KEYWORDS + '\.\s*(.*)', re.UNICODE)
REGEX_ARGCOLON = re.compile(RE_COLON_KEYWORDS + ': (.*?)(?:\.\s+)(.*)', re.UNICODE)
REGEX_RARE = re.compile(RE_RARE_KEYWORDS + ': (.*?)\.\s*' + RE_ALL_KEYWORDS + '(.*)', re.UNICODE)

REGEX_EMPRESA = re.compile('^(\d+)\s+-\s+(.*?)(?:\.$|$)')
REGEX_PDF_TEXT = re.compile('^\((.*)\)Tj$')
REGEX_BORME_NUM = re.compile(u'^Núm\. (\d+)', re.UNICODE)
REGEX_BORME_FECHA = re.compile('^\w+ (\d+) de (\w+) de (\d+)')
REGEX_BORME_CVE = re.compile('^cve: (.*)$')

MESES = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7,
         'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}


# https://es.wikipedia.org/wiki/Anexo:Tipos_de_sociedad_mercantil_en_Espa%C3%B1a
SOCIEDADES = {'AIE': 'Agrupación de Interés Económico',
              'AEIE': 'Agrupación Europea de Interés Económico',
              'COOP': 'Cooperativa',
              'FP': 'Fondo de Pensiones',
              'SA': 'Sociedad Anónima',
              'SAD': 'Sociedad Anónima Deportiva',
              'SAL': 'Sociedad Anónima Laboral',
              'SAP': 'Sociedad Anónima P?',
              'SAS': 'Sociedad por Acciones Simplificada',
              'SAU': 'Sociedad Anónima Unipersonal',
              'SC': 'Sociedad Comanditaria',
              'SCP': 'Sociedad Civil Profesional',
              'SL': 'Sociedad Limitada',
              'SLL': 'Sociedad Limitada Laboral',
              'SLLP': 'Sociedad Limitada Laboral P?',
              'SLNE': 'Sociedad Limitada Nueva Empresa',
              'SLP': 'Sociedad Limitada Profesional',
              'SLU': 'Sociedad Limitada Unipersonal',
              'SRL': 'Sociedad de Responsabilidad Limitada',
              'SRLL': 'Sociedad de Responsabilidad Limitada Laboral',
              'SRLP': 'Sociedad de Responsabilidad Limitada Profesional',
              }
# SOCIEDAD COOPERATIVA DE CREDITO
# FONDOS DE PENSIONES

# Tipos de sociedades extranjeras
SOCIEDADES.update({
    # Bélgica
    # BVBA: Sociedad Privada de Responsabilidad Limitada
    'BVBA': 'Besloten vennootschap met beperkte aansprakelijkheid',

    # Holanda:
    # BV: Sociedad Privada de Responsabilidad Limitada
    'BV': 'Besloten vennootschap met beperkte aansprakelijkheid',
    # NV: Sociedad Anónima (Holanda)
    'NV': 'Naamloze Vennootschap',
})


def is_acto_cargo_entrante(data):
    """ Comprueba si es un acto que aporta nuevos cargos """

    if not is_acto_cargo(data) and not is_acto_rare_cargo(data):
        raise ValueError('No es un acto con cargos: %s' % data)
    return data in ['Reelecciones', 'Nombramientos']


def is_acto_cargo(data):
    """ Comprueba si es un acto que tiene como parámetro una lista de cargos """
    actos = ['Revocaciones', 'Reelecciones', 'Cancelaciones de oficio de nombramientos', 'Nombramientos', 'Ceses/Dimisiones',
             u'Emisión de obligaciones', u'Modificación de poderes']
    return data in actos


def is_acto_noarg(data):
    """ Comprueba si es un acto que no tiene parametros """
    return data in ACTO.NOARG_KEYWORDS


def is_acto_rare_cargo(data):
    """ Como is_acto_cargo pero se parsean de forma distinta """
    actos = (u'Declaración de unipersonalidad', u'Cambio de identidad del socio único',
             u'Escisión parcial', u'Escisión total', u'Fusión por unión')
    return data in actos


def is_acto_rare(data):
    for acto in ACTO.RARE_KEYWORDS:
        if data.startswith(acto):
            return True
    return False


def is_company(data):
    """ Comprueba si es algún tipo de sociedad o por el contrario es una persona física """
    siglas = list(SOCIEDADES.keys())
    siglas = list(map(lambda x: ' %s' % x, siglas))
    return any(data.endswith(s) for s in siglas)


def is_acto_escision(nombreacto):
    return nombreacto in (u'Escisión total. Sociedades beneficiarias de la escisión', u'Escisión parcial')


def is_acto_fusion(nombreacto):
    return nombreacto == u'Fusión por unión'


# HACK
def regex_argcolon(data):
    """ Captura el acto y su argumento y el siguiente acto """
    acto_colon, arg_colon, nombreacto = REGEX_ARGCOLON.match(data).groups()
    return acto_colon, arg_colon, nombreacto


# HACK
def regex_noarg(data):
    """ Captura el acto sin argumento y el siguiente acto """
    nombreacto, siguiente_acto = REGEX_NOARG.match(data).groups()
    return nombreacto, siguiente_acto


def regex_empresa_tipo(data):
    empresa = data
    tipo = ''
    for t in SOCIEDADES.keys():
        if data.endswith(' %s' % t):
            empresa = data[:-len(t) - 1]
            tipo = t
            if empresa.endswith(','):
                empresa = empresa[:-1]
    return empresa, tipo


def regex_empresa(data, sanitize=True):
    """ Captura el número de acto y el nombre de la empresa """
    acto_id, empresa = REGEX_EMPRESA.match(data).groups()
    if sanitize:
        empresa = regex_nombre_empresa(empresa)
    return int(acto_id), empresa


# TODO: Devolver palabras clave como SICAV, SUCURSAL EN ESPAÑA, EN LIQUIDACION
# UNION TEMPORAL DE EMPRESAS LEY 18 1982 DE 26 DE MAYO
def regex_nombre_empresa(nombre):
    sucursal_spain = False

    if nombre.endswith(u'(R.M. A CORUÑA)'):
        nombre = nombre[:-15]
    if nombre.endswith('(R.M. PALMA DE MALLORCA)'):
        nombre = nombre[:-24]
    if nombre.endswith('(R.M. PUERTO DE ARRECIFE)'):
        nombre = nombre[:-25]
    if nombre.endswith('(R.M. PUERTO DEL ROSARIO)'):
        nombre = nombre[:-25]
    if nombre.endswith('(R.M. SANTIAGO DE COMPOSTELA)'):
        nombre = nombre[:-29]
    if nombre.endswith('(R.M. SANTA CRUZ DE TENERIFE)'):
        nombre = nombre[:-29]
    if nombre.endswith('(R.M. SANTA CRUZ DE LA PALMA)'):
        nombre = nombre[:-29]
    if nombre.endswith('(R.M. LAS PALMAS)'):
        nombre = nombre[:-17]
    if nombre.endswith('(R.M. EIVISSA)'):
        nombre = nombre[:-14]
    if nombre.endswith('(R.M. MAHON)'):
        nombre = nombre[:-12]
    if nombre.endswith('EN LIQUIDACION'):
        nombre = nombre[:-15]
    if u'SUCURSAL EN ESPAÑA' in nombre:
        nombre = nombre.replace(u' SUCURSAL EN ESPAÑA', '')
        sucursal_spain = True
    nombre.rstrip()
    if nombre.endswith(' S.L.'):
        nombre = nombre[:-4] + 'SL'
    if nombre.endswith(' S.L'):
        nombre = nombre[:-3] + 'SL'
    if nombre.endswith(' S L'):
        nombre = nombre[:-3] + 'SL'
    elif nombre.endswith(' SOCIEDAD LIMITADA'):
        nombre = nombre[:-17] + 'SL'
    elif nombre.endswith(' SOCIETAT LIMITADA'):
        nombre = nombre[:-17] + 'SL'
    elif nombre.endswith(' SOCIEDAD ANONIMA DEPORTIVA'):
        nombre = nombre[:-26] + 'SAD'
    elif nombre.endswith(' S.A.L'):
        nombre = nombre[:-5] + 'SAL'
    elif nombre.endswith(' SOCIEDAD ANONIMA LABORAL'):
        nombre = nombre[:-24] + 'SAL'
    elif nombre.endswith(' S.A'):
        nombre = nombre[:-3] + 'SA'
    elif nombre.endswith(' S.A.'):
        nombre = nombre[:-4] + 'SA'
    elif nombre.endswith(' B.V.'):
        nombre = nombre[:-4] + 'BV'
    elif nombre.endswith(' B.V'):
        nombre = nombre[:-3] + 'BV'
    elif nombre.endswith(' N.V'):
        nombre = nombre[:-3] + 'NV'
    elif nombre.endswith(' N.V.'):
        nombre = nombre[:-4] + 'NV'
    elif nombre.endswith(' SOCIEDAD ANONIMA'):
        nombre = nombre[:-16] + 'SA'
    elif nombre.endswith(' S L L'):
        nombre = nombre[:-5] + 'SLL'
    elif nombre.endswith(' S.L.L'):
        nombre = nombre[:-5] + 'SLL'
    elif nombre.endswith(' SOCIEDAD LIMITADA LABORAL'):
        nombre = nombre[:-25] + 'SLL'
    elif nombre.endswith(' SOCIEDAD CIVIL PROFESIONAL'):
        nombre = nombre[:-26] + 'SCP'
    elif nombre.endswith(' SOCIEDAD LIMITADA PROFESIONAL'):
        nombre = nombre[:-29] + 'SLP'
    elif nombre.endswith(' S.L.P'):
        nombre = nombre[:-5] + 'SLP'
    elif nombre.endswith(' S. L. P'):
        nombre = nombre[:-7] + 'SLP'
    elif nombre.endswith(' S.L. PROFESIONAL'):
        nombre = nombre[:-16] + 'SLP'
    elif nombre.endswith(' SA UNIPERSONAL'):
        nombre = nombre[:-14] + 'SAU'
    elif nombre.endswith(' S.L UNIPERSONAL'):
        nombre = nombre[:-15] + 'SLU'
    elif nombre.endswith(' SL UNIPERSONAL'):
        nombre = nombre[:-14] + 'SLU'
    elif nombre.endswith(' SOCIEDAD LIMITADA UNIPERSONAL'):
        nombre = nombre[:-29] + 'SLU'
    elif nombre.endswith(' SOCIEDAD LIMITADA NUEVA EMPRESA'):
        nombre = nombre[:-31] + 'SLNE'
    elif nombre.endswith(' S.L.N.E'):
        nombre = nombre[:-7] + 'SLNE'
    elif nombre.endswith(' S.L.N.E.'):
        nombre = nombre[:-8] + 'SLNE'
    elif nombre.endswith(' SOCIEDAD DE RESPONSABILIDAD LIMITADA'):
        nombre = nombre[:-36] + 'SRL'
    elif nombre.endswith(' SOCIEDAD DE RESPONSABILIDAD LIMITADA LABORAL'):
        nombre = nombre[:-44] + 'SRLL'
    elif nombre.endswith(' SOCIEDAD DE RESPONSABILIDAD LIMITADA PROFESIONAL'):
        nombre = nombre[:-48] + 'SRLP'
    elif nombre.endswith(' A.I.E'):
        nombre = nombre[:-5] + 'AIE'
    elif nombre.endswith(' AGRUPACION DE INTERES ECONOMICO'):
        nombre = nombre[:-31] + 'AIE'
    elif nombre.endswith(' FONDO DE PENSIONES'):
        nombre = nombre[:-18] + 'FP'
    elif nombre.endswith(' SOCIEDAD ANONIMA PROFESIONAL'):
        nombre = nombre[:-28] + 'SAP'
    elif nombre.endswith(' SOCIEDAD COMANDITARIA'):
        nombre = nombre[:-21] + 'SC'
    elif nombre.endswith(' SOCIEDAD COMANDITARIA SIMPLE'):  # SC simple
        nombre = nombre[:-28] + 'SC'
    elif nombre.endswith(' SOCIEDAD COMANDITARIA POR ACCIONES'):  # SC por acciones
        nombre = nombre[:-34] + 'SC'
    elif nombre.endswith(' A.E.I.E'):
        nombre = nombre[:-7] + 'AEIE'

    if nombre.endswith(' SOCIEDAD ANONIMA DE INVERSION DE CAPITAL VARIABLE'):
        nombre = nombre[:-49] + 'SICAV'
    if nombre.endswith(' S.I.C.A.V. SA'):
        nombre = nombre[:-13] + 'SICAV'
    if nombre.endswith(' SA SICAV'):
        nombre = nombre[:-8] + 'SICAV'

    # TODO: return sucursal_spain
    return nombre


def regex_cargos(data, sanitize=True):
    """
    :param data:
    'Adm. Solid.: RAMA SANCHEZ JOSE PEDRO;RAMA SANCHEZ JAVIER JORGE.'
    'Auditor: ACME AUDITORES SL. Aud.Supl.: MACIAS MUÑOZ FELIPE JOSE.'

    :return:

    {'Adm. Solid.': {'RAMA SANCHEZ JOSE PEDRO', 'RAMA SANCHEZ JAVIER JORGE'}}
    {'Auditor': {'ACME AUDITORES SL'}, 'Aud.Supl.': {'MACIAS MUÑOZ FELIPE JOSE'}}
    """
    cargos = {}
    for cargo in re.findall(RE_CARGOS_MATCH, data, re.UNICODE):
        entidades = set()
        for e in cargo[1].split(';'):
            e = e.rstrip('.')
            e = e.strip()
            if sanitize:
                e = regex_nombre_empresa(e)
            entidades.add(e)
        if cargo[0] in cargos:
            cargos[cargo[0]].update(entidades)
        else:
            cargos[cargo[0]] = entidades
    return cargos


def regex_decl_unip(data):
    """
    data: "Declaración de unipersonalidad. Socio único: BRENNAN KEVIN LIONEL. Nombramientos."
          "Cambio de identidad del socio único: OLSZEWSKI GRZEGORZ. Ceses/Dimisiones."
    """
    #import pdb; pdb.set_trace()
    acto_colon, arg_colon, nombreacto, nombreacto2 = REGEX_RARE.match(data).groups()
    if acto_colon == u'Declaración de unipersonalidad. Socio único':
        acto_colon = u'Declaración de unipersonalidad'
    arg_colon = {u'Socio Único': {arg_colon}}
    nombreacto += nombreacto2
    return acto_colon, arg_colon, nombreacto


# TODO: Parser
def regex_escision(nombreacto, data):
    """
    data: "Escisión parcial. Sociedades beneficiarias de la escisión: JUAN SL."
    data: "Escisión total. Sociedades beneficiarias de la escisión: PEDRO ANTONIO 2001 SOCIEDAD LIMITADA. PEDRO ANTONIO EXPLOTACIONES SL."
    """
    if nombreacto == u'Escisión total. Sociedades beneficiarias de la escisión':
        nombreacto = u'Escisión total'
    else:
        data = data.split(u'Sociedades beneficiarias de la escisión: ', 1)[1]
    companies = data.split('. ')
    companies[-1] = companies[-1][:-1]  # Punto final
    beneficiarias = {'Sociedades beneficiarias': set(companies)}
    return nombreacto, beneficiarias


def regex_fusion(data):
    """
    acto: Fusión por unión.
    data: "Sociedades que se fusiónan: YOLO SOCIEDAD ANONIMA."
    """
    if not data.startswith(u'Sociedades que se fusiónan: '):  # SIC
        raise ValueError(data)
    company = data.split(u'Sociedades que se fusiónan: ', 1)[1][:-1]
    return {'Sociedades fusionadas': set([company])}


def regex_constitucion(data):

    def parse_capital(amount):
        # '3.000,00 Euros', '3.000.000 Ptas'
        amount = amount.group(1).strip()
        if 'Euros' in amount:
            amount = amount.split(' Euros')[0]
            amount = float(amount.replace('.', '').replace(',', '.'))
        elif 'Ptas' in amount:
            amount = amount.split(' Ptas')[0]
            amount = int(amount.replace('.', ''))
        else:
            raise ValueError('Capital ni Ptas ni Euros: {0}'.format(amount))
        return amount

    all_keywords = ['Comienzo de operaciones', 'Duración', 'Objeto social', 'Domicilio', 'Capital', 'Capital suscrito', 'Desembolsado']
    all_keywords.append('$')
    all_or_ng = '(?:{0})'.format('|'.join(all_keywords))

    date = re.search('Comienzo de operaciones: (.*?){0}'.format(all_or_ng), data).group(1).strip()
    if len(date) > 1 and date[1] == '.':
        date = date[:7]
    elif len(date) > 2 and date[2] == '.':
        date = date[:8]
    if date.endswith('.'):
        date = date[:-1]
    try:
        # 'dd.mm.yy', 'd.mm.yy', 'dd.m.yy', 'd.m.yy', 'dd/mm/yy', '2-10-2009', '21 DE FEBRERO DE 2006'
        if '/' in date or '-' in date:
            n = re.findall('(\d{1,4})', date)  # ['17', '04', '2013']
            if len(n) != 3:
                raise ValueError
            date = {'day': int(n[0]), 'month': int(n[1]), 'year': int(n[2])}
            date = datetime.date(**date)
        elif ' de ' in date.lower():
            match = re.match('(\d+) de (\w+) de (\d+)', date.lower())
            if not match:
                raise ValueError
            day, month, year = match.groups()
            date = datetime.date(day=int(day), month=MESES[month], year=int(year))
        else:
            date = datetime.datetime.strptime(date, '%d.%m.%y').date()
        date = date.isoformat()
    except ValueError:
        print('ERROR CON Comienzo de operaciones: {0}'.format(date))

    duration = re.search('Duración: (.*?){0}'.format(all_or_ng), data)
    if duration:
        duration = duration.group(1).strip()

    activity = re.search('Objeto social: (.*?){0}'.format(all_or_ng), data)
    if activity:
        activity = activity.group(1).strip()
        activity = capitalize_sentence(activity)

    address = re.search('Domicilio: (.*?){0}'.format(all_or_ng), data)
    if address:
        address = address.group(1).strip().title()

    capital = re.search('Capital: (.*?){0}'.format(all_or_ng), data)
    if capital:
        try:
            capital = parse_capital(capital)
        except ValueError:
            raise ValueError('Capital ni Ptas ni Euros: {0}'.format(capital))

    suscrito = re.search('Capital suscrito: (.*?){0}'.format(all_or_ng), data)
    if suscrito:
        try:
            suscrito = parse_capital(suscrito)
        except ValueError:
            raise ValueError('Suscrito ni Ptas ni Euros: {0}'.format(suscrito))

    desembolsado = re.search('Desembolsado: (.*?){0}'.format(all_or_ng), data)
    if desembolsado:
        try:
            desembolsado = parse_capital(desembolsado)
        except ValueError:
            raise ValueError('Desembolsado ni Ptas ni Euros: {0}'.format(desembolsado))

    return (date, activity, address, capital)


# This is a way not to use datetime.strftime, which requires es_ES.utf8 locale generated.
def regex_fecha(data):
    """
    Martes 2 de junio de 2015

    >>> REGEX_BORME_FECHA.match(dd).groups()
    ('2', 'junio', '2015')
    """

    day, month, year = re.match('\w+ (\d+) de (\w+) de (\d+)', data, re.UNICODE).groups()
    return (int(year), MESES[month], int(day))


def borme_c_separa_empresas_titulo(titulo):
    """ This function is far from being perfect """
    #
    #        if len(empresas) > 0:
    #            # ['SOCIEDAD ANONIMA BLABLA (SOCIEDAD ABSORBENTE)', ' CABALUR, SOCIEDAD LIMITADA UNIPERSONAL (SOCIEDAD ABSORBIDA)']
    #            # ['MONTE ALMACABA, S.L. (SOCIEDAD BENEFICIARIA DE LA ESCISION DE NUEVA CREACION)', ' AGROPECUARIA SANTA MARIA DE LA CABEZAS S.L. (SOCIEDAD QUE SE ESCINDE PARCIALMENTE)']
    #            empresas = list(map(lambda x: re.sub('\(.*?\)', '', x), empresas))
    #            empresas = list(map(lambda x: x.strip(), empresas))
    #            # ['MONTE ALMACABA, S.L.', 'AGROPECUARIA SANTA MARIA DE LA CABEZAS,S.L.']
    #            empresa = empresas[0]
    #            relacionadas = empresas[1:]
    #
    empresas = []
    lines = []

    if not '\n' in titulo:
        lines = re.findall('.*? \([\w\s]+\)', titulo, re.UNICODE)
    if len(lines) == 0:
        lines = titulo.split('\n')

    for line in lines:
        empresa = re.sub('\(.*?\)', '', line)
        #empresa = line.replace('(SOCIEDAD ABSORBENTE)', '')
        #empresa = empresa.replace('(SOCIEDAD ABSORBIDA)', '')
        #empresa = empresa.replace('(SOCIEDAD ESCINDIDA)', '')
        #empresa = empresa.replace('(SOCIEDAD BENEFICIARIA)', '')
        #empresa = empresa.replace('(SOCIEDADES ABSORBIDAS)', '')
        #empresa = empresa.replace('(EN LIQUIDACIÓN)', '')
        #empresa = empresa.replace('(SOCIEDAD ABSORBENTE Y PARCIALMENTE ESCINDIDA)', '')
        #empresa = empresa.replace('(SOCIEDADES BENEFICIARIAS DE LA ESCISIÓN PARCIAL)', '')
        empresa = empresa.replace('SOCIEDAD ABSORBENTE', '')
        empresa = empresa.replace('SOCIEDAD ABSORBIDA', '')
        empresa = empresa.strip()
        empresa = empresa.rstrip(',')
        empresa = empresa.strip()
        empresas.append(empresa)
        # TODO: regex_empresa

    if len(empresas) > 1:
        # ['COEMA']
        empresas = [e for e in empresas if len(e) > 4]

    return empresas


def capitalize_sentence(string):
    # TODO: espacio de más tras coma/punto
    string = re.sub(r'([,/\.]+)(?! )', r'\1 ', string)
    if string == string.upper():
        string = string.lower()
    sentences = string.split(". ")
    while '' in sentences:
        sentences.remove('')
    sentences2 = [sentence[0].capitalize() + sentence[1:] for sentence in sentences]
    string2 = '. '.join(sentences2)
    if not string2.endswith('.'):
        string2 += '.'

    return string2
