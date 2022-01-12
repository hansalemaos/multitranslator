import ast
import copy
import math
import regex
import regex as re
from pprint import pprint as pp
import json
import pandas as pd
import re
import numpy as np

def isnan(wert, nanzurueck=False, debug=False):
    allenanvalues = ['<NA>', '<NAN>', '<nan>', 'np.nan', 'NoneType', 'None', '-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN',
                     '#N/A N/A', '#N/A', 'N/A', 'n/a', 'NA', '', '#NA', 'NULL', 'null', 'NaN', '-NaN', 'nan', '-nan']
    try:
        if pd.isna(wert) is True:
            if nanzurueck is True: return np.nan
            return True
    except Exception as Fehler:
        if debug is True: print(Fehler)

    try:
        if pd.isnull(wert) is True:
            if nanzurueck is True: return np.nan
            return True
    except Exception as Fehler:
        if debug is True: print(Fehler)

    try:
        if math.isnan(wert) is True:
            if nanzurueck is True: return np.nan
            return True
    except Exception as Fehler:
        if debug is True: print(Fehler)

    try:
        if wert is None:
            return True
    except Exception as Fehler:
        if debug is True: print(Fehler)

    for allaaa in allenanvalues:
        try:
            nanda = regex.findall(str(fr'^\s*{wert}\s*$'), allaaa)
            if any(nanda):
                return True
        except Exception as Fehler:
            if debug is True: print(Fehler)
            return False

    return False


def flattenlist_neu_ohne_tuple(iterable, nanundleerweg=False):
    """24.10"""

    if nanundleerweg is True:
        if isinstance(iterable, list):
            try:
                iterable = [i for i in iterable if isnan(i) is False]
            except:
                pass

    def iter_flatten(iterable):
        it = iter(iterable)
        for e in it:

            if isinstance(e, list):
                for f in iter_flatten(e):
                    yield f
            else:
                yield e


    a = [i for i in iter_flatten(iterable)]
    if nanundleerweg is True:

        try:
            a = [i for i in a if isnan(i) is False]
        except:
            pass

    if any(a):
        if len(a) == 1:
            try:
                a = a[0]
            except:
                a= ''.join(a)

    try:
        a = [i for i in a if i!='' ]
    except:
        pass
    return a





class Superdict(dict):

    def __init__(__self, *args, **kwargs):
        object.__setattr__(__self, '__parent', kwargs.pop('__parent', None))
        object.__setattr__(__self, '__key', kwargs.pop('__key', None))
        object.__setattr__(__self, '__frozen', False)

        for arg in args:
            if not arg:
                continue
            elif isinstance(arg, dict):
                for key, val in arg.items():
                    __self[key] = __self._hook(val)
            elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
                __self[arg[0]] = __self._hook(arg[1])
            else:
                for key, val in iter(arg):
                    __self[key] = __self._hook(val)

        for key, val in kwargs.items():
            __self[key] = __self._hook(val)

    def __setattr__(self, name, value):
        if hasattr(self.__class__, name):
            raise AttributeError("'Superdict' object attribute "
                                 "'{0}' is read-only".format(name))
        else:
            self[name] = value

    def __setitem__(self, name, value):
        debug = False
        isFrozen = (hasattr(self, '__frozen') and
                    object.__getattribute__(self, '__frozen'))
        if isFrozen and name not in super(Superdict, self).keys():
            raise KeyError(name)

        istdictda = isinstance(value, dict)

        if istdictda is True:
            super(Superdict, self).__setitem__(name, value)
        if istdictda is False:

            try:
                base = {}
                for key33, value2 in self.items():
                    # print(key33)
                    # print(value2)
                    if key33 == name:
                        value = value2.copy() + [value]
                    if isinstance(value2, (list, tuple)):
                        try:
                            if name == base:
                                base[key33].append(value2)
                        except:
                            continue
                    else:
                        base[key33].append(value2)
            except Exception as Fehler:
                if debug is True: print(Fehler)

            try:
                if isinstance(value[-1], set):
                    value = list(value[-1])
                    if len(value) == 1:
                        value = value[0]
            except: pass
            try:
                isttupleda = isinstance(value[-1], tuple)
                if isttupleda is True:
                    try:
                        if value[-1][0] == 'FLATTEN':
                            if value[-1][1] == 'FLATTEN':
                                    value = value[:-1]
                                    value = flattenlist_neu_ohne_tuple(value)
                    except Exception as Fehler:
                        if debug is True: print(Fehler)
            except Exception as Fehler:
                if debug is True: print(Fehler)

            islistda = isinstance(value, list)

            if islistda is False:
                super(Superdict, self).__setitem__(name, [value])
            if islistda is True:

                super(Superdict, self).__setitem__(name, value)
        try:
            p = object.__getattribute__(self, '__parent')
            key = object.__getattribute__(self, '__key')
        except AttributeError:

            p = None
            key = None
        if p is not None:
            p[key] = self
            object.__delattr__(self, '__parent')
            object.__delattr__(self, '__key')

    def __add__(self, other):
        if not self.keys():
            return other
        else:
            self_type = type(self).__name__
            other_type = type(other).__name__
            msg = "unsupported operand type(s) for +: '{}' and '{}'"
            raise TypeError(msg.format(self_type, other_type))

    @classmethod
    def _hook(cls, item):
        if isinstance(item, dict):
            return cls(item)
        elif isinstance(item, (list, tuple)):
            return type(item)(cls._hook(elem) for elem in item)
        return item

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __missing__(self, name):
        if object.__getattribute__(self, '__frozen'):
            raise KeyError(name)
        return self.__class__(__parent=self, __key=name)

    def __delattr__(self, name):
        del self[name]

    def to_dict(self):
        base = {}
        for key, value in self.items():
            if isinstance(value, type(self)):
                base[key] = value.to_dict()
            elif isinstance(value, (list, tuple)):
                base[key] = type(value)(
                    item.to_dict() if isinstance(item, type(self)) else
                    item for item in value)
            else:
                base[key] = value
        return base

    def copy(self):
        return copy.copy(self)

    def deepcopy(self):
        return copy.deepcopy(self)

    def __deepcopy__(self, memo):
        other = self.__class__()
        memo[id(self)] = other
        for key, value in self.items():
            other[copy.deepcopy(key, memo)] = copy.deepcopy(value, memo)
        return other

    def update(self, *args, **kwargs):
        other = {}
        if args:
            if len(args) > 1:
                raise TypeError()
            other.update(args[0])
        other.update(kwargs)
        for k, v in other.items():
            if ((k not in self) or
                    (not isinstance(self[k], dict)) or
                    (not isinstance(v, dict))):
                self[k] = v
            else:
                self[k].update(v)

    def __getnewargs__(self):
        return tuple(self.items())

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)

    def __or__(self, other):
        if not isinstance(other, (Superdict, dict)):
            return NotImplemented
        new = Superdict(self)
        new.update(other)
        return new

    def __ror__(self, other):
        if not isinstance(other, (Superdict, dict)):
            return NotImplemented
        new = Superdict(other)
        new.update(self)
        return new

    def __ior__(self, other):
        self.update(other)
        return self

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def freeze(self, shouldFreeze=True):
        object.__setattr__(self, '__frozen', shouldFreeze)
        for key, val in self.items():
            if isinstance(val, Superdict):
                val.freeze(shouldFreeze)

    def unfreeze(self):
        self.freeze(False)

    def convert_to_json(self):
        json_object = json.dumps(self, indent=4)
        return json_object

    def to_normal_exec_stringdict(self):
        tag_list = []

        def print_dict___xx(v, prefix=''):
            if isinstance(v, dict):
                for k, v2 in v.items():
                    k = str(k)
                    p2 = "{}['{}']".format(prefix, k)
                    print_dict___xx(v2, p2)
            elif isinstance(v, list):
                templiste = []
                for i, v2 in enumerate(v):
                    templiste.append(v2)
                p2 = "{}".format(prefix)
                print_dict___xx(str(templiste), p2)
            else:
                zum_drucken = '{} = {}'.format(prefix, repr(v))
                tag_list.append(zum_drucken)

        print_dict___xx(self, prefix='')

        tag_list = Superdict.delete_duplicates_from_nested_list(tag_list)
        return '\n'.join(tag_list)

    @staticmethod
    def string_dict_vorbereiten(string_von_dict):
        inlines = string_von_dict.splitlines()
        inlines = [re.sub(r'^\s*\[', 'dl\g<0>', line.strip()) for line in inlines if len(line) >= 3]
        inlines = [re.sub(r'"\[', '[', line) for line in inlines]
        inlines = [re.sub(r'\]"', ']', line) for line in inlines]
        return inlines.copy()

    def dict_zur_suche_vorbereiten(self, debug=False):

        blabla = self.to_normal_exec_stringdict()
        if debug is True: print(blabla)
        gesplittet = Superdict.string_dict_vorbereiten(blabla)
        if debug is True: print(gesplittet)
        liste = []
        for ge in gesplittet:
            ge2 = regex.sub(r'^dl(\[[^\]]+\])+(?![\s=])', '', ge)
            if debug is True: print(liste)
            liste.append(ge2)
        if debug is True: print(liste)
        return liste.copy()

    @staticmethod
    def string_to_superdict(string_von_dict, debug=False):
        if isinstance(string_von_dict, list):
            string_von_dict = Superdict.delete_duplicates_from_nested_list(string_von_dict)
            string_von_dict = '\n'.join(string_von_dict)

        dl = Superdict()

        inlines = Superdict.string_dict_vorbereiten(string_von_dict)
        aktualisiert = []
        for i in inlines:
            if debug is True: print(i)
            i = regex.sub(r"'(\[\d+\])'", '\g<1>', i )
            i = regex.sub(r"\bnp\.nan\b", 'None', i )
            i = regex.sub(r"\bnan\b", 'None', i)
            i = regex.sub(r"\bNA\b", 'None', i)

            #i = regex.sub(r"\]'\]", ']', i)
            aktualisiert.append(i)
        codeausfuehren = '\n'.join(aktualisiert)
        exec(codeausfuehren)
        return dl

    @staticmethod
    def delete_duplicates_from_nested_list(nestedlist):
        """01.11"""
        tempstringlist = {}
        for ergi in nestedlist:
            tempstringlist[str(ergi)] = ergi
        endliste = [tempstringlist[key] for key in tempstringlist.keys()]
        return endliste.copy()


    def suchen_einen_wert_im_ganzen_dict(self, gesuchterendschluessel):
        return self.keys_crawler(gesuchterendschluessel=gesuchterendschluessel)

    def suchen_keys_mit_regex(self, regexsuchekeys):
        return self.keys_crawler(regexsuchekeys=regexsuchekeys)

    def suchen_werte_mit_regex(self, regexsuche):
        return self.keys_crawler(regexsuche=regexsuche)

    def get_alle_items_als_tuple(self):
        return self.keys_crawler(alle_items_zurueck=True)

    def normalize_keys(self):
        return self.keys_crawler(normalize_keys=True)

    def zaehlen_values(self):
        return self.keys_crawler(values_zaehlen=True)

    def ersetzen_einen_wert_im_dict(self, gesuchter_wert, replace):
        return self.keys_crawler(gesuchter_wert=gesuchter_wert, replace=replace)

    def ersetzen_einen_key_im_dict(self, gesuchter_key, replace):
        return self.keys_crawler(gesuchter_key=gesuchter_key, replace=replace)

    def keys_crawler(self, regexsuche=None, regexsuchekeys=None, alle_items_zurueck=False, normalize_keys=False, values_zaehlen=False,gesuchter_wert=None, gesuchter_key=None, replace=None, gesuchterendschluessel=None, debug=False ):
        beidezusammen = []
        ergebnis = []
        dl = Superdict()


        dict_zur_suche_vorbereiten = self.dict_zur_suche_vorbereiten()
        for di in dict_zur_suche_vorbereiten:
            di = 'dl' + di
            di2 = regex.sub(r'''["\[\]\(\),\{\}']''', '', di)
            di2 = regex.split(r'\s*=\s*', di2)
            beidezusammen.append([di, di2])



        if values_zaehlen is True:
            zweitesergebnisdict = Superdict()
            [print(kk) for kk in beidezusammen]
            formatierung_mit_anfuehrungszeichen = []
            for reg in beidezusammen:
                reggi = reg[0]
                if debug is True: print(reggi)
                reggi = regex.sub(r'^(dl)+', '', reggi)
                if debug is True: print(reggi)
                gesplittet = regex.split(r'\s*=\s*', reggi)
                formatierung_mit_anfuehrungszeichen.append([reg[0], gesplittet])

            indexlist = [kk[1][1] for kk in formatierung_mit_anfuehrungszeichen]
            keyliste = [kk[1][0] for kk in formatierung_mit_anfuehrungszeichen]

            if debug is True: print(indexlist)

            for i,kka in zip(indexlist,keyliste):
                dl[i] = indexlist.count(str(i))
                indexes = [ii for ii, j in enumerate(indexlist) if str(j) == str(i)]
                dl[i] = indexes, kka
            for keys,values in dl.items():
                try:
                    for valli in values:
                        if isinstance(valli, tuple):
                            if debug is True: print(f'Der Wert {keys} ist in folgenden Keys {valli}')
                            valli = str(valli[-1]).strip('''['"]''')
                            if debug is True: print(valli)
                            keys = regex.sub(r'''^['"\s]+''', '', keys)
                            keys = regex.sub(r'''['"\s]+$''', '', keys)

                            befehlausfuehren = f'zweitesergebnisdict[{values[0]}]{keys} = "{valli}"'
                            if debug is True: print(befehlausfuehren)
                            exec(befehlausfuehren)
                except Exception as Fehler:
                    if debug is True: print(Fehler)
            if debug is True: pp(zweitesergebnisdict)
            return zweitesergebnisdict

        if gesuchterendschluessel is None:
            pass
        else:
            dictstring= self.to_normal_exec_stringdict()
            for bei,didi in zip(beidezusammen, dictstring.splitlines()):
                if debug is True: print(bei)
                if debug is True: print(didi)
                keys_und_values = regex.split(r'\s*=\s*', didi)
                keys_ohne_gaensefuessle = regex.split(r'''[\'"[\]]+''',keys_und_values[0])
                keys_ohne_gaensefuessle = flattenlist_neu_ohne_tuple(keys_ohne_gaensefuessle)
                if debug is True: print(keys_ohne_gaensefuessle)
                keys_ohne_gaensefuessle = flattenlist_neu_ohne_tuple(keys_ohne_gaensefuessle)
                if debug is True: print(keys_ohne_gaensefuessle)
                for keyy in keys_ohne_gaensefuessle:
                    zwischenergebnis = regex.findall(gesuchterendschluessel, keyy)
                    zwischenergebnis  = flattenlist_neu_ohne_tuple(zwischenergebnis, nanundleerweg=True)
                    if any(zwischenergebnis):
                        t1 = regex.sub(r'''^(dl)*['"]*\[''' , '[', keys_und_values[1])
                        t1 = regex.sub(r'''\]['"]*\s*$''' , ']', t1)
                        try:
                            t1 = ast.literal_eval(t1)
                        except:
                            try:
                                t1 = regex.sub(r'''^["'\s]*''', '', t1)
                                t1 = ast.literal_eval(t1)
                            except:
                                pass
                        try:
                            if len(t1) == 1:
                                if isinstance(t1[0], (list,tuple)):
                                    pass
                                else:
                                    t1 = t1[0]
                        except:
                            pass

                        ergebnis.append([keys_ohne_gaensefuessle, t1])
            return ergebnis.copy()

        if gesuchter_wert is None and gesuchter_key is None:
            pass
        else:
            dictstring = self.to_normal_exec_stringdict()
            beidezusammen = []
            valueschecken = False
            keyschecken = False
            if gesuchter_wert is not None:
                valueschecken = True
                suchen = gesuchter_wert
                ersetzen = replace
            if gesuchter_key is not None:
                keyschecken = True
                suchen = gesuchter_key
                ersetzen = replace
            if debug is True: print(f'{gesuchter_wert} {gesuchter_key} {suchen} {ersetzen}')
            dict_zur_suche_vorbereiten = self.dict_zur_suche_vorbereiten()
            for di in dict_zur_suche_vorbereiten:
                di = 'dl' + di
                di2 = regex.sub(r'''["\[\]\(\),\{\}']''', '', di)
                di2 = regex.split(r'\s*=\s*', di2)
                beidezusammen.append([di, di2])
                if debug is True: print(beidezusammen)
            for bei in beidezusammen:
                if debug is True: print(bei[0])
                gesplittet = regex.split(r'\s*=\s*', bei[0])
                ergebnisse_klein = []
                for eni, ge in enumerate(gesplittet):
                    if eni % 2 == 0:
                        if valueschecken is True:
                            ergebnisse_klein.append(ge)
                            continue
                        if debug is True: print('Keys checken')

                    if eni % 2 != 0:
                        if keyschecken is True:
                            ergebnisse_klein.append(ge)

                            continue
                        if debug is True: print('values checken')
                    temporaer_zum_suchen = regex.sub(r'''^(?:dl)?['"]*\[['"]*''', '', ge)
                    temporaer_zum_suchen = regex.sub(r'''["'\]]+$''', '', temporaer_zum_suchen)
                    zwischenersetzen = regex.sub(suchen, ersetzen, temporaer_zum_suchen)
                    endergebnis = regex.sub(regex.escape(temporaer_zum_suchen), zwischenersetzen, ge)
                    ergebnisse_klein.append(endergebnis)

                ergebnis.append(ergebnisse_klein.copy())

            if valueschecken is True:
                for ergs, didi in zip(ergebnis, dictstring.splitlines()):
                    if debug is True: print(didi)
                    if debug is True: print(ergs)
                    originalgesplittet = regex.split(r'\s*=\s*', didi)
                    originalgesplittet_key = originalgesplittet[0]
                    try:
                        ausfuehren = f'dl{originalgesplittet_key} = {ast.literal_eval(ergs[1])}'
                        exec(ausfuehren)

                    except:
                        ausfuehren = f'dl{originalgesplittet_key} = {ergs[1]}'
                        exec(ausfuehren)
                return dl

            if keyschecken is True:
                for ergs, didi in zip(ergebnis, dictstring.splitlines()):
                    didi = f'dl{didi}'
                    ersetzen = regex.sub(r'^(dl)+', '', ergs[0])
                    neuerkey = regex.sub(r'\[[^\]]+\](?=\s+=)', ersetzen, didi)
                    neuerkey = regex.split(r'\s*=\s*', neuerkey)
                    try:
                        neuerkey = f'{neuerkey[0]} = {ast.literal_eval(neuerkey[1])}'
                    except:
                        neuerkey = f'{neuerkey[0]} = {neuerkey[1]}'

                    try:
                        exec(neuerkey)
                    except:
                        exec(neuerkey)
                return dl

        if normalize_keys is True:
            for reg in beidezusammen:
                reggi = reg[0]
                reggi = regex.sub('^dl', '', reggi)
                gesplittet = regex.split(r'\s*=\s*', reggi)
                keys = gesplittet[0]
                keys = regex.sub(r"'\]\['", 'ÇYÇYÇ', keys)
                keys = regex.sub(r"'\](\[\d+\])?", 'ÇAÇAÇ', keys)
                keys = regex.sub(r"^\s*\['", 'ÇEÇEÇ', keys)
                keys = regex.sub(r'\W+', '_', keys)
                keys = regex.sub(r'_+Ç', 'Ç', keys)
                keys = regex.sub(r'Ç_+', 'Ç', keys)
                keys = regex.sub(r'Ç(\d+)', 'Çz_\g<1>', keys)
                keys = regex.sub('ÇYÇYÇ', "']['", keys)
                keys = regex.sub('ÇEÇEÇ', "dl['", keys)
                keys = regex.sub('ÇAÇAÇ', "']", keys)
                keys = keys.lower()
                keys = keys.strip(' _')
                try:
                    ergebnis.append(f'{keys} = {ast.literal_eval(gesplittet[1])}')
                except:
                    ergebnis.append(f'{keys} = {gesplittet[1]}')
            for eni, ergi in enumerate(ergebnis):
                if debug is True: print(ergi)
                exec(ergi)
            return dl

        if alle_items_zurueck is True:
            for reg in beidezusammen:
                valueformatieren = regex.sub(r'^[^=]+=\s*', '', reg[0])
                keyformatieren = regex.sub('^dl','',reg[1][0])

                try:
                    hinzufuegen = keyformatieren, ast.literal_eval(valueformatieren)
                except:
                    hinzufuegen = keyformatieren, valueformatieren
                ergebnis.append(hinzufuegen)
            return ergebnis.copy()

        if regexsuche is not None:
            for reg in beidezusammen:
                ergi = regex.findall(regexsuche, reg[1][1])
                ergi = flattenlist_neu_ohne_tuple(ergi)
                if any(ergi):
                    ergebnis.append(reg[0])
            for eni, ergi in enumerate(ergebnis):
                exec(ergi)
            return dl

        if regexsuchekeys is not None:
            for reg in beidezusammen:
                ergi = regex.findall(regexsuchekeys, reg[1][0])
                ergi = flattenlist_neu_ohne_tuple(ergi)
                if any(ergi):
                    ergebnis.append(reg[0])
            for eni, ergi in enumerate(ergebnis):
                exec(ergi)
            return dl
