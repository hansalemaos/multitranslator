import os
import shutil
from einfuehrung import einfuehrung
from bs4 import BeautifulSoup
from pytablewriter import ExcelXlsxTableWriter
from pprint import pprint as pp
from yeekit_tr import yeekit_tr
import translators as ts
import subprocess
import sys
from deep_translator import GoogleTranslator
from random import randrange as randomrandrange
from farbprinter.farbprinter import Farbprinter
from time import sleep, strftime
import pandas as pd
from CLASS_SUPERDICT2 import Superdict
from pytablewriter import HtmlTableWriter
import webbrowser
drucker = Farbprinter()
import kthread
from satzmetzger.satzmetzger import Satzmetzger
from regex import regex
tempfilename = 'xxxtempfilexxxxtranslation.txt'
tempfilenameout = 'xxxtempfilexxxxtranslation-tr.txt'
from ftlangdetect import detect
from sprache_waehlen import get_sprache
# text = '''Dass das Wlan mal Zicken macht, kennt wohl jeder. Doch warum genau, ist meist nicht klar. Zu den Feiertagen gibt es einen weiteren, äußerst skurrilen Verdächtigen: die Weihnachtsbeleuchtung.
# Wer saß abends noch nicht auf der Couch und ärgerte sich über die ruckelnde Wlan-Verbindung. Was beim ganz normalen Surfen schon nervig sein kann, macht andere Aktivitäten schlicht zur Qual. Durch das ewige Nachladen wird selbst die beste Serie oder der spannendste Film bei Netflix und Co. zur ungenießbaren Zeitverschwendung. Warum die Verbindung so schlecht ist, findet man allerdings selten heraus. Meist fällt der Verdacht schnell auf den Internetanbieter, nicht immer zu Recht. Zumindest an den Festtagen könnte durchaus die großzügig mit Lichterketten dekorierte Wohnung schuld sein.
# Denn dass die Verbindung schlecht ist, hängt in vielen Fällen zwar daran, dass der Provider nicht mehr Geschwindigkeit liefern kann oder gar technische Probleme hat. Das Heimnetzwerk spielt aber in der Mehrheit der Fälle ebenfalls eine Rolle. Das hat eine Studie der britischen Regulierungsbehörde Ofcom herausgefunden. Sie sammelte Beschwerden der Bevölkerung bei Problemen mit TV-, Mobil- und Internetempfang und suchte nach den Ursachen. Dabei stellte sich heraus: Bei über 75 Prozent der Haushalte mit schlechten Internetgeschwindigkeiten war auch die Verbindungsqualität im Heimnetzwerk ein relevanter Faktor.
# Elektronische Störenfriede
# Gründe für die Störungen gibt es viele. Häufig ist schlicht der Router schlecht platziert, so dass Möbel und Wände den Empfang verschlechtern oder die Reichweite nicht groß genug ist. Manchmal sind einfach die Antennen nicht richtig ausgerichtet. Eine Fehlerquelle haben viele Nutzer aber gar nicht auf dem Schirm: Elektrische Geräte wie Mikrowellen, Fernseher und Co. können die Verbindung ganz empfindlich stören, wenn sie zu nah am Router stehen. Und hier kommen die Lichterketten ins Spiel.'''
yeekitlimit=2000
sougolimit=2000
tencentlimit=500
binglimit =500
argoslimit = 500
icibalimit = 2000
googlelimit = 4000



def create_folder_in_documents_folder():
    timefolder = strftime("%Y_%m_%d_%H_%M_%S")
    documentsfolder = os.path.expanduser('~\\Documents')
    ganzerpfad = documentsfolder + '\\' + timefolder
    if not os.path.exists(ganzerpfad):
        try:
            os.makedirs(ganzerpfad)
            print(drucker.f.brightgreen.black.normal(f'Pfad: {ganzerpfad} erstellt!'))

        except:
            print(drucker.f.brightred.black.normal(f'Pfad: {ganzerpfad} konnte nicht erstellt werden!'))
            return None
    return ganzerpfad


def schlafen(min=4, max=10):
    min = min * 10
    max = max * 10
    try:
        sleep(randomrandrange(min, max) / 10)
    except:
        pass


def copy_file(src, dest):
    try:
        if os.path.isfile(src):
            dpath, dfile = os.path.split(dest)
            if not os.path.isdir(dpath):
                os.makedirs(dpath)
            try:
                shutil.copy2(src, dest)
                print(drucker.f.brightgreen.black.italic(f'The file {src} has just been copied to {dest}'))
                return True
            except Exception as Fehler:
                return False
    except:
        return False
    return False


def textsortieren(alleoriginaltexte, alleubertexte):
    resultdict = {}
    zaehler = 1
    for ori, uber in zip(alleoriginaltexte, alleubertexte):

        maximalezahl = int(regex.findall(r'^\s*0+(\d+)\s*\)\s+', ori.splitlines()[-1].strip())[0])
        for zahl in range(maximalezahl):
            resultdict[zaehler] = {}
            textsplittenoriginal = ori.splitlines()
            uebersetzter_text = uber.splitlines()
            zahlsuchen = str(zahl + 1).zfill(5)
            for orisatz in textsplittenoriginal:
                try:
                    detext = regex.findall(rf'^\s*{zahlsuchen}[^\n\r\v]+', orisatz)[0]
                    resultdict[zaehler]['de'] = detext
                    break
                except:
                    detext = ''
                    resultdict[zaehler]['de'] = detext
                    continue
            for ubersatz in uebersetzter_text:
                try:
                    uebersetztertext = regex.findall(rf'^\s*{zahlsuchen}[^\n\r\v]+', ubersatz)[0]
                    resultdict[zaehler]['andere'] = uebersetztertext
                    break
                except:
                    uebersetztertext = ''
                    resultdict[zaehler]['andere'] = uebersetztertext
                    continue
            zaehler = zaehler + 1
    return resultdict.copy()



def split_in_laenge(gesplittetertext, limit=5000, prozentsicherheit=10):
    gesplittetertext = [f'{x})\t\t{y}' for x, y in gesplittetertext]
    sicherheit = int(limit / prozentsicherheit)
    neueslimit = limit - sicherheit
    gesplittetertextneu = []
    laenge = 0
    zwischenergebnis = []
    for tt in gesplittetertext:
        if laenge >= neueslimit:
            laenge = 0
            zwischenergebnis.append(tt)
            gesplittetertextneu.append(zwischenergebnis.copy())
            zwischenergebnis.clear()
        if laenge < neueslimit:
            laenge = laenge + len(tt)
            zwischenergebnis.append(tt)
    if len(zwischenergebnis) > 0:
        gesplittetertextneu.append(zwischenergebnis)
    gesplittetertextneu = ['\n'.join(t) for t in gesplittetertextneu]
    return gesplittetertextneu.copy()


def get_file_path(datei):
    pfad = sys.path
    pfad = [x.replace('/', '\\') + '\\' + datei for x in pfad]
    exists = []
    for p in pfad:
        if os.path.exists(p):
            exists.append(p)
    return list(dict.fromkeys(exists))

def write_text_to_file(text):
    metzgerle = Satzmetzger()
    gesplittetertext =metzgerle.zerhack_den_text(text)
    gesplittetertext = [(str(ini+1).zfill(5),x) for ini,x in enumerate(gesplittetertext)]
    ganzerstring = ''
    for saetze in gesplittetertext:
        ganzerstring = ganzerstring + saetze[0] + ')'+ '\t\t' + saetze[1] + '\n\n'
    with open(tempfilename,  mode='w', encoding='utf-8') as f:
        f.write(ganzerstring)
    return gesplittetertext


def write_results_to_textfile(filepath, uebersetztertext):
    with open(filepath,  mode='w', encoding='utf-8') as f:
        f.write(str(uebersetztertext))


def create_symlink(dateipfad, symlink, withending=False):
    'use like this: create_symlink(r"c:\folder oder file with\shi--y name", "nicename", withending=False)'
    if not os.path.isdir(dateipfad):
        dateipfadendung = dateipfad.split('.')[-1]
        os.close(os.open(dateipfad, os.O_CREAT))
    try:
        if os.path.islink(symlink) is True:
            os.remove(symlink)
    except:
        pass
    if withending is True:
        symlink = symlink + '.' + dateipfadendung
    os.symlink(dateipfad, symlink)
    return symlink

def translate_text():
    data =''
    test = subprocess.run(['deepl-tr-pp', '-p', tempfilename, '-f', 'de', '-t', outputlanguage, '--nooutput-docx'], capture_output=True)
    try:
        filename = regex.findall('File written to(.*\.txt)' , str(test.stderr))
        filename = filename[0].strip().replace('\\\\', '\\')
    except Exception as Fehler:
        filename = tempfilenameout
    try:
        with open(filename, encoding='utf-8') as f:
            data = f.read()
        os.remove(filename)
        try:
            os.remove(textfile_deepl_resultate)
        except:
            pass
        write_results_to_textfile(textfile_deepl_resultate, data)
    except Exception as Fehler:
        pass
    return data

def mit_iciba():
    global iciba_resultate
    auf5000 = split_in_laenge(allesaetzeuebersetzen, limit=binglimit, prozentsicherheit=20)
    alleergebnisse =[]

    for ini,wort in enumerate(auf5000):
        try:
            uebersetzter_text = ts.iciba(wort, from_language='de', to_language=outputlanguage)
            alleergebnisse.append(uebersetzter_text)
        except Exception as Fehler:
            pass
        schlafen()
    iciba_resultate = textsortieren(alleoriginaltexte=auf5000, alleubertexte=alleergebnisse)
    try:
        os.remove(textfile_iciba_resultate)
    except:
        pass
    write_results_to_textfile(textfile_iciba_resultate ,alleergebnisse)


def mit_argos():
    global argos_resultate
    auf5000 = split_in_laenge(allesaetzeuebersetzen, limit=binglimit, prozentsicherheit=20)
    alleergebnisse =[]

    for ini,wort in enumerate(auf5000):
        try:
            uebersetzter_text = ts.argos(wort, from_language='de', to_language=outputlanguage)
            alleergebnisse.append(uebersetzter_text)
        except Exception as Fehler:
            pass
        schlafen()
    argos_resultate = textsortieren(alleoriginaltexte=auf5000, alleubertexte=alleergebnisse)
    try:
        os.remove(textfile_argos_resultate)
    except:
        pass
    write_results_to_textfile(textfile_argos_resultate ,alleergebnisse)





def mit_bing():
    global bing_resultate
    auf5000 = split_in_laenge(allesaetzeuebersetzen, limit=binglimit, prozentsicherheit=20)
    alleergebnisse =[]

    for ini,wort in enumerate(auf5000):
        try:
            uebersetzter_text = ts.bing(wort, from_language='de', to_language=outputlanguage)
            alleergebnisse.append(uebersetzter_text)
        except Exception as Fehler:
            pass
        schlafen()
    bing_resultate = textsortieren(alleoriginaltexte=auf5000, alleubertexte=alleergebnisse)
    try:
        os.remove(textfile_bing_resultate )
    except:
        pass
    write_results_to_textfile(textfile_bing_resultate  ,alleergebnisse)


def mit_tencent():
    global tencent_resultate
    auf5000 = split_in_laenge(allesaetzeuebersetzen, limit=tencentlimit, prozentsicherheit=20)
    alleergebnisse =[]

    for ini,wort in enumerate(auf5000):
        try:
            uebersetzter_text = ts.tencent(wort, from_language='de', to_language=outputlanguage)
            alleergebnisse.append(uebersetzter_text)
        except Exception as Fehler:
            pass
        schlafen()
    tencent_resultate = textsortieren(alleoriginaltexte=auf5000, alleubertexte=alleergebnisse)
    try:
        os.remove(textfile_tencent_resultate )
    except:
        pass
    write_results_to_textfile(textfile_tencent_resultate  ,alleergebnisse)


def mit_yeekit():
    global yeekit_resultate
    auf5000 = split_in_laenge(allesaetzeuebersetzen, limit=yeekitlimit, prozentsicherheit=20)
    alleergebnisse =[]

    for ini,wort in enumerate(auf5000):
        try:
            uebersetzter_text = yeekit_tr(wort,from_lang='de', to_lang=outputlanguage)
            alleergebnisse.append(uebersetzter_text)
        except Exception as Fehler:
            pass
        schlafen()
    yeekit_resultate = textsortieren(alleoriginaltexte=auf5000, alleubertexte=alleergebnisse)
    try:
        os.remove(textfile_yeekit_resultate  )
    except:
        pass
    write_results_to_textfile(textfile_yeekit_resultate   ,alleergebnisse)


def mit_google_ubersetzen():
    global google_resultate
    auf5000 = split_in_laenge(allesaetzeuebersetzen, limit=googlelimit, prozentsicherheit=10)
    alleergebnisse =[]

    for ini,wort in enumerate(auf5000):
        try:
            uebersetzter_text = GoogleTranslator(
                source="de", target=outputlanguage
            ).translate(wort)
            alleergebnisse.append(uebersetzter_text)

        except Exception as Fehler:
            pass
        schlafen()
    google_resultate = textsortieren(alleoriginaltexte=auf5000, alleubertexte=alleergebnisse)
    try:
        os.remove(textfile_google_resultate   )
    except:
        pass
    write_results_to_textfile(textfile_google_resultate    ,alleergebnisse)



def text_allestarten(ubersetzer):
    global deepl_resultate
    if ubersetzer == 'deepl':
        text = translate_text()
        text_lines = text.splitlines()
        resultat_original = []
        resultat_uebersetzungen = []
        for ini, line in enumerate(text_lines):
            deepl_resultate[ini] = {}
            lineformatiert = regex.sub(r'^\d+\)\s*', '', line)
            result = detect(text=lineformatiert, low_memory=False)
            if result['lang'] == 'de':
                deepl_resultate[ini]['de'] = line
                continue
            deepl_resultate[ini]['andere'] = line
        return resultat_original, resultat_uebersetzungen

    if ubersetzer == 'google':
        mit_google_ubersetzen()
    if ubersetzer == 'tencent':
        mit_tencent()
    if ubersetzer == 'argos':
        mit_argos()
    if ubersetzer == 'iciba':
        mit_iciba()
    if ubersetzer == 'bing':
        mit_bing()
    if ubersetzer == 'yeekit':
        mit_yeekit()

def read_textfiles(datei):
    with open(datei, encoding='utf-8') as f:
        data = f.read()


def write_to_excel(df, filename):
    datenframe = df.copy()
    datenframe['original'] = df.index
    writer = ExcelXlsxTableWriter()
    writer.from_dataframe(datenframe)
    writer.dump(filename)


def write_to_html(df, filename):
    datenframe = df.copy()
    datenframe['original'] = df.index
    writer = HtmlTableWriter()
    writer.from_dataframe(datenframe)
    coloredhtml = regex.sub(r'<thead>', r'<thead style="background-color:#ffff00">', str(writer), regex.DOTALL)
    coloredhtmllist = coloredhtml.splitlines()
    fertightml = []
    zaehler = 0
    for ini, line in enumerate(coloredhtmllist):
        if '<tr>' in line:
            if zaehler == 0:
                fertightml.append(line)
                zaehler = zaehler + 1
                continue
            if zaehler % 2 == 0:
                line = line.replace('<tr>', '<tr style="background-color:#ffff99">')
            fertightml.append(line)
            zaehler = zaehler + 1
            continue
        fertightml.append(line)

    fertightml = '''<h1 style="background-color:black;color:red;font-size:36px;">&ensp;&ensp;&ensp;&ensp;&ensp;Made by&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;<a href="https://www.queroestudaralemao.com.br/" style="background-color:black;color:yellow;font-size:48px;">queroestudaralemao.com.br</a></h1>''' + '\n'.join(fertightml)
    write_to_file(filepath=filename, text=fertightml)


def filename_from_text(text, ending='txt', length=30):
    dateiname = regex.sub(r'\W+', '_', text)
    dateiname = dateiname.strip('_')
    dateiname = dateiname.strip()
    dateiname = dateiname[:length]
    dateiname = dateiname +'.' + ending
    dateiname = dateiname.lower()
    return dateiname

def write_to_file(filepath, text):
    with open(filepath, encoding='utf-8', mode='w') as f:
        if isinstance(text, list):
            for l in text:
                try:
                    f.write(str(l))
                    f.write('\n')
                except:
                    continue
        if isinstance(text, str):
            f.write(str(text))
def txtdateien_lesen(text):
    try:
        dateiohnehtml = (
            b"""<!DOCTYPE html><html><body><p>""" + text + b"""</p></body></html>"""
        )
        soup = BeautifulSoup(dateiohnehtml, "html.parser")
        soup = soup.text
        return soup.strip()
    except Exception as Fehler:
        pass


def get_text():
    p = subprocess.run(get_file_path(r"Everything2TXT.exe")[0], capture_output=True)
    ganzertext = txtdateien_lesen(p.stdout)
    return ganzertext

def removetempfiles():
    try:
        os.remove(textfile_tencent_resultate)
    except:
        pass
    try:
        os.remove(textfile_bing_resultate)
    except:
        pass
    try:
        os.remove(textfile_argos_resultate)
    except:
        pass
    try:
        os.remove(textfile_iciba_resultate)
    except:
        pass
    try:
        os.remove(textfile_deepl_resultate)
    except:
        pass
    try:
        os.remove(textfile_google_resultate)
    except:
        pass
    try:
        os.remove(textfile_sogou_resultate)
    except:
        pass
    try:
        os.remove(textfile_yeekit_resultate)
    except:
        pass
    try:
        os.remove(tempfilename)
    except:
        pass

def find_same_elements_in_list(*args):
    """Examples: print(find_same_elements_in_list([1, 2, 3], [1, 2, 3, 4, 5], [2, 3, 4]))
        print(find_same_elements_in_list([1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 3, 4], [1, 4]))
        ne = find_same_elements_in_list([[1, 2], [3, 4]], [[1, 2]])
        print(ne)
        ne2 = find_same_elements_in_list([[1, 2], [3, 4]], [[1, 2]], [44,55, [1,2]])
        print(ne2)

        output:
        [2, 3]
        [1, 4]
        [[1, 2]]
        [[1, 2]]

        :param args: list
        :return : list
    """
    try:
        a_set = set(args[0])
        b_set = set(args[1])
        matches = a_set.intersection(b_set)
        if len(args) > 2:
            otherlists = list(args[2:])
            for other in otherlists:
                c_set = set(other)
                matches = matches.intersection(c_set)
        matches = list(matches)
        return matches
    except Exception as Fehler:
        ergebnisse = []
        listealsstring = []
        for arg in args:
            nestedlist = [str(x) for x in arg]
            listealsstring.append(nestedlist.copy())
        a_set = set(listealsstring[0])
        b_set = set(listealsstring[1])
        matches = a_set.intersection(b_set)
        if len(listealsstring) > 2:
            otherlists = listealsstring[2:]
            for other in otherlists:
                c_set = set(other)
                matches = matches.intersection(c_set)
            matches = list(matches)
        for arg in args:
            for li in arg:
                if str(li) in matches:
                    ergebnisse.append(li)
        tempstringlist = {}
        for ergi in ergebnisse:
            tempstringlist[str(ergi)] = ergi
        endliste = [tempstringlist[key] for key in tempstringlist.keys()]
        return endliste.copy()

def get_second_value(x):
    try:
        return x[1]
    except:
        return x
def find_different_elements_in_list(*args):
    """
    Examples:  print(find_different_elements_in_list([3, 1, 2, 4], [1, 2, 54, 99, 4], [33, 1, 2, 3]))
    print(find_different_elements_in_list([[1,2], [332,4]], [[55,55,1], [1,2],[33,44] ], [[22,4], [1,2]]))

    output:
    [54, 99, 33]
    [[332, 4], [55, 55, 1], [33, 44], [22, 4]]

    :param args: list
    :return : list
    """
    gleicheelemente = find_same_elements_in_list(*args)
    gleicheelemente =[str(x) for x in gleicheelemente]
    ergebnisse = []
    for listen in list(args):
        for element in listen:
            if str(element) not in gleicheelemente:
                ergebnisse.append(element)
    ergebnisse2 = [str(x) for x in ergebnisse]
    ergebnisse_zaehlen = [[ergebnisse2.count(str(x)),x] for x in ergebnisse]
    einzelneergebnisse = [x[1] for x in ergebnisse_zaehlen if x[0] == 1]
    return einzelneergebnisse

if __name__ == "__main__":
    einfuehrung('Translatornator')
    outputlanguage = get_sprache('\nBitte Zielsprache eingeben:\n')[1]

    text = get_text()
    write_to_file(filepath=tempfilename, text=text)

    foldername = create_folder_in_documents_folder()
    filenamesave_txt = str(foldername) + '\\' + filename_from_text(text, ending='txt', length=30)
    filenamesave_xlsx =  str(foldername) + '\\' +filename_from_text(text, ending='xlsx', length=30)
    filenamesave_html =  str(foldername) + '\\' +filename_from_text(text, ending='html', length=30)


    textfile_tencent_resultate = 'tencent_resultate.txt'
    textfile_bing_resultate = 'bing_resultate.txt'
    textfile_argos_resultate = 'argos_resultate.txt'
    textfile_iciba_resultate = 'iciba_resultate.txt'
    textfile_deepl_resultate = 'deepl_resultate.txt'
    textfile_google_resultate = 'google_resultate.txt'
    textfile_sogou_resultate = 'sogou_resultate.txt'
    textfile_yeekit_resultate = 'yeekit_resultate.txt'

    tencent_resultate = {}
    bing_resultate = {}
    argos_resultate = {}
    iciba_resultate = {}
    deepl_resultate = {}
    google_resultate = {}
    yeekit_resultate ={}
    allesaetzeuebersetzen = write_text_to_file(text)
    alleuebersetzer = ['deepl', 'google', 'tencent', 'bing', 'argos', 'iciba', 'yeekit']

    allethreads = []
    for aktion in alleuebersetzer:
        allethreads.append(
            kthread.KThread(
                target=text_allestarten,
                name=aktion,
                args=(aktion,),
            )
        )
    gestartet = [los.start() for los in allethreads]
    nochamleben = [(t.name, t.is_alive()) for t in allethreads]
    nuramleben = [x[1] for x in nochamleben if x[1] == True]
    while any(nuramleben):
        nochamleben = [(t.name, t.is_alive()) for t in allethreads]
        for thr in nochamleben:
            if thr[1] is True:
                print(drucker.f.black.brightred.italic(f"{thr[0]} übersetzt noch!"))
            if thr[1] is False:
                print(drucker.f.black.brightgreen.italic(f"{thr[0]} ist fertig!"))
        sleep(2)
        nuramleben = [x[1] for x in nochamleben if x[1] == True]

    alleinfos = [tencent_resultate,
                    bing_resultate,
                    argos_resultate,
                    iciba_resultate,
                    google_resultate,
                    yeekit_resultate]

    dictzumeinlesen = Superdict()
    for ini,di in enumerate(alleinfos):
        for d in di.keys():
            try:
                if any(di[d]['de']):
                    deutsch = regex.sub(r'^\s*\d{5}\)\s+', '', di[d]['de']).strip()
                    sprache2 = regex.sub(r'^\s*\d{5}\)?\s*', '', di[d]['andere']).strip()
                    einfuegen = (ini, sprache2)
                    if einfuegen in dictzumeinlesen[deutsch] :
                        continue
                    dictzumeinlesen[deutsch] = (ini, sprache2)
            except:
                pass

    neuesdict = Superdict()
    for key, item in dictzumeinlesen.items():
        try:
            if len(item) == 6:
                neuesdict[key] = item
                continue
            if len(item) >= 7:
                checkenob6 =[]
                checkenob6zahl =[]
                rausmachen = item
                transp = [list(xaaa) for xaaa in zip(*rausmachen)][0]
                wegmachen = [[x[0], x[1], len(x[1]), transp.count(x[0])] for x in rausmachen]
                drucker.p.black.red.bold(wegmachen)
                wegmachen = [(x[0], x[1]) for x in wegmachen if x[3] == 1 or x[2] != 0]
                drucker.p.black.blue.bold(wegmachen)

                for weg in wegmachen:
                    if weg[0] not in checkenob6zahl:
                        checkenob6.append(weg)
                        checkenob6zahl.append(weg[0])
                        drucker.p.blue.yellow.bold(checkenob6zahl)
                neuesdict[key] = checkenob6.copy()
                continue
            if len(item) <6:
                neueliste = []
                checkliste = [0,1,2,3,4,5]
                reinmachen = item
                transp = [list(xaaa) for xaaa in zip(*reinmachen)][0]
                drucker.p.black.brightblue.italic(transp)

                fehlt = find_different_elements_in_list(checkliste, transp)
                drucker.p.black.brightmagenta.italic(fehlt)
                for rein in reinmachen:
                    neueliste.append(rein)
                if any(fehlt):
                    for f in fehlt:
                        neueliste.append((f, ''))
                neueliste.sort()
                drucker.p.yellow.black.italic(neueliste)
                neuesdict[key] = neueliste.copy()
                continue
        except Exception as Fehler:
            print(Fehler)
    neuesdict2 = Superdict()
    for key, item in neuesdict.items():
        try:
            if len(item) == 6:
                neuesdict2[key] = item
                continue
            if len(item) >= 7:
                checkenob6 =[]
                checkenob6zahl =[]
                rausmachen = item
                transp = [list(xaaa) for xaaa in zip(*rausmachen)][0]
                wegmachen = [[x[0], x[1], len(x[1]), transp.count(x[0])] for x in rausmachen]
                drucker.p.black.red.bold(wegmachen)
                wegmachen = [(x[0], x[1]) for x in wegmachen if x[3] == 1 or x[2] != 0]
                drucker.p.black.blue.bold(wegmachen)

                for weg in wegmachen:
                    if weg[0] not in checkenob6zahl:
                        checkenob6.append(weg)
                        checkenob6zahl.append(weg[0])
                        drucker.p.blue.yellow.bold(checkenob6zahl)
                neuesdict2[key] = checkenob6.copy()
                continue
            if len(item) <6:
                neueliste = []
                checkliste = [0,1,2,3,4,5]
                reinmachen = item
                transp = [list(xaaa) for xaaa in zip(*reinmachen)][0]
                drucker.p.black.brightblue.italic(transp)

                fehlt = find_different_elements_in_list(checkliste, transp)
                drucker.p.black.brightmagenta.italic(fehlt)
                for rein in reinmachen:
                    neueliste.append(rein)
                if any(fehlt):
                    for f in fehlt:
                        neueliste.append((f, ''))
                neueliste.sort()
                drucker.p.yellow.black.italic(neueliste)
                neuesdict2[key] = neueliste.copy()
                continue
        except Exception as Fehler:
            print(Fehler)
    df = pd.DataFrame(neuesdict2.to_dict())
    df = df.T.copy()
    colohnedeepl =  ['tencent', 'bing', 'argos', 'iciba', 'google', 'yeekit']
    try:
        df.columns =colohnedeepl
    except:
        pass

    hinzufuegendeepl = []
    zwischen = []
    for key, item in deepl_resultate.items():

        try:
            zwischen.append(item['de'][7:])

        except:
            pass
        try:
            hinzufuegen = regex.sub(r'^\s*\d+\)?\s*', '', item['andere'])
            zwischen.append(hinzufuegen)
            hinzufuegendeepl.append(zwischen.copy())
            zwischen.clear()

            # print(key)
        except:
            pass
    for key, value in hinzufuegendeepl:
        drucker.p.black.brightmagenta.italic(value)
        df.at[key, 'deepl'] = value


    for col in colohnedeepl:
        df[col] = df[col].apply(get_second_value)

    try:
        write_to_excel(df, filenamesave_xlsx)
        write_to_html(df, filenamesave_html)
    except Exception as Fehler:
        print(Fehler)
    drucker.f.black.brightmagenta.normal('Excel file saved:\t\t') + drucker.f.black.brightmagenta.negative(filenamesave_xlsx)
    drucker.f.black.brightmagenta.normal('HTML file saved:\t\t') + drucker.f.black.brightmagenta.negative(filenamesave_html)
    try:
        webbrowser.open(filenamesave_html)
    except:
        pass
    input(drucker.f.black.brightred.bold('ENTER drücken, um das Programm zu beenden.'))


