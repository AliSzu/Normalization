import re
from itertools import combinations
import numpy as np
from nltk import flatten
from collections import Counter

kandydujace_klucze = []
kandydujace_klucze2 = []
klucze_baza_minimalna = []
nadklucze = []
poprawne = []
pierwszy_klucz = 0
minimalna_ilosc_kluczy = 0


def posortuj_argumenty_po_przecinku(zaleznosci_do_sortowania):
    for zaleznosc in zaleznosci_do_sortowania:
        if (zaleznosc[0].find(',') != -1):
            tmp_string = ""
            tmp = zaleznosc[0].split(",")
            tmp.sort()
            for x in tmp:
                if (x == tmp[-1]):
                    tmp_string = tmp_string + x
                else:
                    tmp_string = tmp_string + x + ","
            zaleznosc.pop(0)
            zaleznosc.insert(0, tmp_string)
            tmp.clear()

    return zaleznosci_do_sortowania


def usun_powtorzenia(zaleznosci_do_poprawy):
    for zaleznosc in zaleznosci_do_poprawy:
        if (zaleznosc[0] == zaleznosc[1]):
            index = zaleznosci_do_poprawy.index(zaleznosc)
            zaleznosci_do_poprawy.pop(index)

    return zaleznosci_do_poprawy


def podaj_atrybuty_kluczowe():
    global kandydujace_klucze2
    kandydujace_klucze2 = kandydujace_klucze[:]
    atrybuty_kluczowe = [j for i in kandydujace_klucze for j in i]
    atrybuty_kluczowe = list(set(atrybuty_kluczowe))
    atrybuty_kluczowe.sort()

    return atrybuty_kluczowe


def podaj_atrybuty_niekluczowe(atrybuty_wszystkie, atrybuty_kluczowe):
    atrybuty_niekluczowe = np.setdiff1d(atrybuty_wszystkie, atrybuty_kluczowe)

    return atrybuty_niekluczowe


def attributes_split(attributes_string):
    attributes = attributes_string.replace(" ", "").replace(",", " ").split(" ")
    return attributes


# Rozkład zależności na osobne atrybuty
def functional_split_to_attributes(zaleznosci_funkcyjne):
    zaleznosci_funkcyjne_attr = []
    tmp = " "
    zaleznosci_funkcyjne_string = tmp.join(zaleznosci_funkcyjne)
    tmp2 = re.split('[, -> ]', zaleznosci_funkcyjne_string)

    for zaleznosc in tmp2:
        if (zaleznosc != ""):
            zaleznosci_funkcyjne_attr.append(zaleznosc)

    return zaleznosci_funkcyjne_attr


def verification(attributes, zaleznosci_funkcyjne_attributes):
    zaleznosci_funkcyjne_attributes = list(set(zaleznosci_funkcyjne_attributes))

    attributes.sort()
    zaleznosci_funkcyjne_attributes.sort()

    print(attributes == zaleznosci_funkcyjne_attributes)


def postac_kanoniczna_function(zaleznosci_funkcyjne):
    tmp2 = []

    for zaleznosc in zaleznosci_funkcyjne:
        if (zaleznosc.find('->') != -1):
            strzalka_index_1 = zaleznosc.find("->")  # index -
            strzalka_index_2 = strzalka_index_1 + 1  # index >

            if (zaleznosc[strzalka_index_2 + 1: len(zaleznosc)].find(",") != -1):
                tmp1 = (zaleznosc[strzalka_index_2 + 1: len(zaleznosc)]).replace(" ", "").split(
                    ",")  # to co jest na prawo od > i rozdzielanie gdy np A,B
                tmp2.append(zaleznosc[0: strzalka_index_1 - 1])  # to co jest na lewo od -
                ilosc_do_rozdzielenia = len(tmp1)
                i = 0

                while (ilosc_do_rozdzielenia > 0):  # skłądanie rozlozonych do jednego stirngu
                    tmp_string = tmp2[0] + ' -> ' + tmp1[i]
                    postac_kanoniczna.append(tmp_string)
                    i = i + 1
                    ilosc_do_rozdzielenia = ilosc_do_rozdzielenia - 1

                tmp1.clear()
                tmp2.clear()
            else:
                postac_kanoniczna.append(zaleznosc)

            for x in postac_kanoniczna:  # rozkladanie do jednej tablicy w formie [['a','b']]
                tmp = x.replace(" ", "").split("->")
                if (tmp not in postac_kanoniczna_split):
                    postac_kanoniczna_split.append(tmp)
    # posortuj_argumenty_po_przecinku(postac_kanoniczna_split)

    return postac_kanoniczna


def dopelnienie_Fplus(atrybuty, zaleznosci_funkcyjne, czyWypisac):
    global pierwszy_klucz
    global minimalna_ilosc_kluczy

    a = []
    atrybuty = list(atrybuty)

    dopelnienie_string = "{"

    atrybuty_dopelnienia = atrybuty[:]
    ilosc_atr = len(atrybuty)

    for atrybut in atrybuty:  # - przygowywanie stringa do wydrukowania
        if (atrybut == atrybuty_dopelnienia[-1]):
            dopelnienie_string = dopelnienie_string + atrybut + "}" + "+" + " =" + " {"
        else:
            dopelnienie_string = dopelnienie_string + atrybut + ", "

    i = 1
    while (i > 0):
        i = i - 1
        for zaleznosci in zaleznosci_funkcyjne:
            if (len(zaleznosci[0]) > 1):
                tmp = zaleznosci[0].split(",")  # gdy jest atrybut typu A,B to rozkladamy go na A i B
                if (all(item in atrybuty_dopelnienia for item in
                        tmp)):  # sprawdzamy czy wszystkie rozlozone atrybuty znajdują się w dopelnieniu
                    if (zaleznosci[1] not in atrybuty_dopelnienia):
                        atrybuty_dopelnienia.append(
                            zaleznosci[1])  # jesli tam to dodajemy to o na co wskauzje, czyli A,B -> C dodajemy C
                        i = i + 1
                        a.append(zaleznosci)

            if (zaleznosci[0] in atrybuty_dopelnienia):
                if (zaleznosci[1] not in atrybuty_dopelnienia):
                    atrybuty_dopelnienia.append(zaleznosci[1])
                    i = i + 1
                    a.append(zaleznosci)

    atrybuty_dopelnienia.sort()

    for atrybut in atrybuty_dopelnienia:  # tworzenie stringa w stylu {A,B}
        if (atrybut == atrybuty_dopelnienia[-1]):
            dopelnienie_string = dopelnienie_string + atrybut + "}"
        else:
            dopelnienie_string = dopelnienie_string + atrybut + ","

    if (len(atrybuty_dopelnienia) == len(
            attributes)):  # znajdywanie najmniejszego klucza i zapisywanie sobie jego długości etc
        pierwszy_klucz = pierwszy_klucz + 1
        if (pierwszy_klucz == 1):
            minimalna_ilosc_kluczy = ilosc_atr
        if (minimalna_ilosc_kluczy == ilosc_atr):
            dopelnienie_string = dopelnienie_string + "     <- Minimalny klucz kandydujący"
            kandydujace_klucze.append(atrybuty)
            klucze_baza_minimalna.append(atrybuty)
        if (ilosc_atr > minimalna_ilosc_kluczy):
            dopelnienie_string = dopelnienie_string + "     <- Nadklucz"
            nadklucze.append(atrybuty)
    if (czyWypisac):
        # print(dopelnienie_string)
        return dopelnienie_string
    else:
        return atrybuty_dopelnienia, a


def dopelnienie_nowej_bazy(zaleznosc, atrybuty):
    global poprawne
    sprawdzenie = []
    for i in range(1, len(atrybuty) + 1):
        comb = combinations(atrybuty, i)
        for j in list(comb):
            sprawdzenie.append(dopelnienie_Fplus(list(j), zaleznosc, True))
    if sprawdzenie == poprawne:
        return True
    else:
        return False


def usuwanie_zbednych(zaleznosc, atrybuty):
    do_usuniecia = []  # usuwam po jednym elemencie i sprawdzam czy bez niego baza nadal jest taka sama, czyli czy dopelnienia są sobie rowne
    for x in zaleznosc:
        index = zaleznosc.index(x)
        zaleznosc.pop(index)
        if dopelnienie_nowej_bazy(zaleznosc, atrybuty):
            do_usuniecia.append(x)
        else:
            zaleznosc.insert(index, x)
    return do_usuniecia


def znajdz_baze_minimalna(zaleznosci_funkcyjne, atrybuty):
    tmp2 = []
    baza_minimalna = []
    baza_minimalna_string = ""
    baza_minimalna_split = []
    do_usuniecia = []

    for zaleznosci in zaleznosci_funkcyjne:
        if (zaleznosci[0].find(',') != -1):  # -- sprawdzanie czy mozna rozłozyc zaleznosc typu A,B -> C
            i = 0
            tmp1 = zaleznosci[0].split(",")
            tmp2.append(zaleznosci[1])

            for atrybut in tmp1:
                dopelnienie = dopelnienie_Fplus(atrybut, zaleznosci_funkcyjne,
                                                False)  # dla każdego atrybutu sprawdzamy jego dopelnienie

                dopelnienie = flatten(dopelnienie)
                dopelnienie = list(set(dopelnienie))
                if (all(item in dopelnienie for item in
                        tmp2)):  # sprawdzam czy dopelnienie atrybutu pokrywa się z tym na co złozony atrybut wskazywał i czy moge go zastąpic
                    listToStr = ' '.join(map(str, tmp2))
                    baza_minimalna.append(baza_minimalna_string + atrybut + " -> " + listToStr)
                    i = i + 1
            if (i == 0):
                baza_minimalna.append(baza_minimalna_string + zaleznosci[0] + " -> " + zaleznosci[1])
        else:
            baza_minimalna.append(baza_minimalna_string + zaleznosci[0] + " -> " + zaleznosci[1])

    baza_minimalna = list(set(baza_minimalna))
    for x in baza_minimalna:
        tmpb = x.replace(" ", "").split("->")
        if (tmpb not in baza_minimalna_split):
            baza_minimalna_split.append(
                tmpb)  # tworzenie bazy minimalnej w postacie [['A','B']] dla łatwiejszeog liczenia później

    do_usuniecia = usuwanie_zbednych(baza_minimalna_split, atrybuty)  # -- usuwanie elementu ktory jest zbędny
    if (len(do_usuniecia) > 0):
        for element in do_usuniecia:
            if element in baza_minimalna_split:
                baza_minimalna_split.remove(element)

    # baza_minimalna_split.sort(key = lambda x: x[0])
    baza_minimalna_split = posortuj_argumenty_po_przecinku(baza_minimalna_split)
    baza_minimalna_split.sort(key=lambda x: x[0])

    baza_tmp = []

    if (len(baza_minimalna_split) > 0):
        for baza in baza_minimalna_split:
            string_tmp = baza[0] + " -> " + baza[1]
            baza_tmp.append(string_tmp)

    baza_minimalna_split.clear()
    baza_tmp.sort(key=len)
    for baza in baza_tmp:
        tmp = baza.replace(" ", "").split("->")
        baza_minimalna_split.append(flatten(tmp[:]))

    if (len(baza_minimalna_split) > 0):
        for baza in baza_minimalna_split:
            print(baza[0] + " -> " + baza[1])
    else:
        print("(brak)")

    return baza_minimalna_split


def Czy_jest_2PN_3PN(atrybuty_kluczowe, atrybuty_niekluczowe, zaleznosci_funkcyjne, baza_minimalna):
    global nadklucze
    global kandydujace_klucze2
    czy_2PN = True
    czy_3PN = True
    tmp = []
    bledne_zaleznosci = []
    for klucz in atrybuty_kluczowe:
        klucz = klucz.split(" ")
        dopelnienie, zaleznosci_dopelnienia = dopelnienie_Fplus(klucz, zaleznosci_funkcyjne, False)
        if (any(item in atrybuty_niekluczowe for item in
                dopelnienie)):  # czy jakikolwiek atrybut niekluczowy znajduje sie w dopelnieniu klucza
            for b in zaleznosci_dopelnienia:
                if (not (any(item in b[1] for item in atrybuty_niekluczowe))):
                    index = zaleznosci_dopelnienia.index(b)
                    zaleznosci_dopelnienia.pop(index)
                else:
                    bledne_zaleznosci.append(klucz)
                    bledne_zaleznosci.append(b)

    if (len(bledne_zaleznosci) > 0):
        print("Relacja nie jest w 2 postaci normalnej.")
        print("")
        print("W podanym schemacie istnieje przyjemniej jedna częściowa zależność funkcyjna, która narusza 2PN.")
        print("Te zależności to:")
        czy_2PN = False
        for zaleznosci in bledne_zaleznosci:
            if (len(zaleznosci) == 1):
                klucz_tmp = zaleznosci[0]
            else:
                print(klucz_tmp + " -> " + zaleznosci[1])

        print("Relacja nie jest 3 postaci normalnej, ponieważ nie jest w 2 postaci normalnej.")
        print("")

    if (len(bledne_zaleznosci) == 0):
        print("Relacja jest w 2 postaci normalnej.")
        print("")
    bledne_zaleznosci2 = []
    # -- Dla 3PN sprawdzamy czy zależnosci sie nietrywialne, czyli czy element po prawej stronie nie znajduje sie takze po lewej np A,B -> A to jest trywialne
    for zaleznosc in zaleznosci_funkcyjne:
        if (zaleznosc[0].find(zaleznosc[1]) != -1):
            bledne_zaleznosci2.append(zaleznosc)
    if (len(bledne_zaleznosci2) > 0):
        if (not czy_2PN):
            print("Pondato nie wszystkie zależnosci są nietrywialne")
        else:
            print("Relacja nie jest w 3PN ponieważ nie wszystkie zależnosci są nietrywialne")
        print("W podanym schemacie istnieje przyjemniej jedna częściowa zależność funkcyjna, która narusza 3PN.")
        print("Te zależności to:")
        for zaleznosc in bledne_zaleznosci2:
            print(zaleznosc[0] + " -> " + zaleznosc[1])
        bledne_zaleznosci2.clear()
    else:
        tmp_klucze = []
        for klucz in kandydujace_klucze2:  # zamieniam liste typu [['A','B'], ['C','D']] na ['A,B', 'C,D']
            klucz_string = ""
            for x in klucz:
                klucz_string = klucz_string + x + ","
                if (x == klucz[-1]):
                    klucz_string = klucz_string[:-1]
                    tmp_klucze.append(klucz_string)
        tmp_klucze = list(dict.fromkeys(tmp_klucze))
        for zaleznosc in baza_minimalna:
            prawda = 0
            for klucz in tmp_klucze:
                res = Counter(filter(str.isalnum, klucz)) == Counter(
                    filter(str.isalnum, zaleznosc[0]))  # czy x jest kluczem podstawowym, b,e i e,b to to samo
                if (res):
                    prawda = prawda + 1
            if (zaleznosc[0].find(',') != -1):
                tmp = zaleznosc[0].split(",")
            if (len(tmp) > 0 and tmp in nadklucze):
                prawda = prawda + 1
            tmp.clear()
            if (all(item in nadklucze for item in zaleznosc[0])):  # - 𝑿 jest nadkluczem
                prawda = prawda + 1
            if (zaleznosc[1] in atrybuty_kluczowe):
                prawda = prawda + 1
            if (all(item in atrybuty_kluczowe for item in zaleznosc[1])):  # - 𝐴 jest atrybutem kluczowym.
                prawda = prawda + 1
            if (prawda == 0):
                bledne_zaleznosci2.append(zaleznosc)
        if (len(bledne_zaleznosci2) > 0):
            czy_3PN = False
            if (not czy_2PN):
                print("Pondato")
            else:
                print("Relacja nie jest w 3PN.")
            print("W podanym schemacie istnieje przyjemniej jedna częściowa zależność funkcyjna, która narusza 3PN.")
            print("Te zależności to:")
            for zaleznosc in bledne_zaleznosci2:
                print(zaleznosc[0] + " -> " + zaleznosc[1])
            bledne_zaleznosci2.clear()
        else:
            print("Relacja jest w 3 postaci normalnej.")

    return czy_3PN


def synteza_do_3PN(baza_minimalna):
    global kandydujace_klucze2
    tmp = []
    tmp2 = []
    i = 0
    for zaleznosc in baza_minimalna:
        x = zaleznosc[0]
        if (x not in tmp2):
            tmp2.append(x)
        tmp.clear()
        for zaleznosc2 in baza_minimalna:
            if (x == zaleznosc2[0]):
                if (len(tmp2) > 0 and isinstance(tmp2[-1], str)):
                    tmp.append(zaleznosc2[1])
        if (len(tmp) > 0):
            tmp2.append(tmp[:])

    tmp.clear()
    tmp3 = []
    for x in tmp2:
        if (isinstance(x, str)):
            if (len(tmp) > 1):
                tmp3.append(tmp[:])
                tmp.clear()
            tmp.append(x)
        elif (len(tmp) > 0 and isinstance(tmp[-1], str)):
            tmp.append(x)
    tmp3.append(tmp[:])
    tmp3_pomoc = tmp3[:]

    tmp.clear()

    tmp4 = []
    zaleznosci_syntezy = []
    for x in tmp3:
        x = flatten(x)
        x2 = x[:]
        for y in x:
            if (y.find(',') != -1):
                tmp = y.split(",")
                x2.remove(y)
                tmp4.append(tmp[:])
                tmp4.append(x2[:])
                x2.clear()
                zaleznosci_syntezy.append(flatten(tmp4[:]))
                tmp4.clear()
        if (len(x2) > 0):
            zaleznosci_syntezy.append(x2)

    # - sprawdzanie czy jakies zaleznosci sie zawierają w sobie
    zaleznosci_syntezy_pomoc = zaleznosci_syntezy[:]
    zaleznosci_syntezy2 = zaleznosci_syntezy[:]
    klucze_pomoc_tmp = kandydujace_klucze[:]
    atrybuty_Ui = []

    if_exists = True
    tmp5 = []
    for zaleznosc in zaleznosci_syntezy:
        index = zaleznosci_syntezy.index(zaleznosc)

        zaleznosci_syntezy_pomoc.pop(
            index)  # - usuwam obecnie przeglądaną zaleznosc zeby zobaczyc czy zawiera sie w innych, pozbywam sie przypadku gdy ona sama zawiera sie w sobie samej
        for pomoc in zaleznosci_syntezy_pomoc:
            if (all(x in pomoc for x in zaleznosc)):  # - jesli sie zawiera
                if (pomoc in zaleznosci_syntezy2):
                    index2 = zaleznosci_syntezy2.index(zaleznosc)  # - gdzie znajduje sie na oryginalnym miejscu
                    zaleznosci_syntezy2.remove(
                        zaleznosc)  # - usuwanie z listy pomocniczej zeby nie naruszac oryginalnej listy podczas gdy jest uzywana w pętli
                    pomoc2 = tmp3[index2]
                    for y in tmp3_pomoc:  # - usuwanie z listy z sformatowanymi zaleznosciami typu ['A,B', '[C]'] co jest rowne A,B -> C
                        if (y[0].find(',') != -1):  # - zmienianie ['A,B','[C]'] na ['A','B','C']
                            tmp = y[0].split(",")
                            tmp5.append((tmp[:]))
                            tmp5.append([y[1]])
                            tmp5 = flatten(tmp5)
                            tmp.clear()
                            if (tmp5 == pomoc):
                                y.append(tmp3[
                                             index2])  # - gdy znajdziemy zaleznosc a ktora zawiera w sobie zaleznosc b, dodajemy do zaleznosci a zaleznosc b, czyli np ['A,B', '[C], ['B', '[A]']]]
                            tmp5.clear()
                    tmp3.remove(pomoc2)
        zaleznosci_syntezy_pomoc.insert(index, zaleznosc)

    synteza_string = ""
    synteza_string_lista = []
    synteza_string_tmp = ""
    synteza_argumenty = ""
    for synteza in tmp3:  # wypisywanie
        synteza1 = " "
        synteza1 = synteza1.join(synteza[1])
        if (len(synteza) > 2):
            ostatni_element = synteza[-1]
            for x in synteza:
                if (isinstance(x, str) or len(x[
                                                  1]) > 1):  # - gdy pierwszy element listy jest stringiem to wtedy zaleznosci są odrazu po nim, albo gdy jest długi typu [A,[C,D]] to A wskazuje na C i A wskazuje na D
                    index = synteza.index(x)
                    if (len(x[1]) > 1):
                        synteza_argumenty = synteza_argumenty + x[0] + ","
                        for y in x[1]:
                            synteza_string_tmp = synteza_string_tmp + x[0] + " -> " + y + "; "
                    elif (len(synteza[
                                  index + 1]) > 1):  # - gdy kolejny element od stringu ma kilka elementów, to trzeba to rozlozyc na A -> B i A -> C
                        synteza_argumenty = synteza_argumenty + x + ","
                        for syn in synteza[index + 1]:
                            synteza_string_tmp = synteza_string_tmp + x + " -> " + syn + "; "
                        synteza.pop(index + 1)
                    else:
                        syn = " "
                        syn = syn.join(synteza[index + 1])
                        synteza_argumenty = synteza_argumenty + x + ","
                        synteza_string_tmp = synteza_string_tmp + x + " -> " + syn + "; "
                        synteza.pop(index + 1)
                else:
                    syn = " "
                    syn = syn.join(x[1])
                    synteza_argumenty = synteza_argumenty + x[0] + ","
                    synteza_string_tmp = synteza_string_tmp + x[0] + " -> " + syn + "; "
                if (ostatni_element == x):
                    synteza_argumenty = synteza_argumenty[:-1]
                    synteza_string = synteza_string[:-2]
                    synteza_string = "R" + str(i) + "(" + synteza_argumenty + ")" + " : " + synteza_string_tmp

        elif (len(synteza[1]) > 1):
            synteza_argumenty = synteza[0] + ","
            for x in synteza[1]:
                synteza_argumenty = synteza_argumenty + x + ","
                synteza_string_tmp = synteza_string_tmp + synteza[0] + " -> " + x + "; "
            synteza_argumenty = synteza_argumenty[:-1]
            synteza_string = synteza_string[:-2]
            synteza_string = "R" + str(i) + "(" + synteza_argumenty + ")" + " : " + synteza_string_tmp
        else:
            synteza_string = synteza_string + "R" + str(i) + "(" + synteza[0] + "," + synteza1 + ")" + " : " + synteza[
                0] + " -> " + synteza1
            tmp.append(synteza[0])
            tmp.append(synteza1)
            atrybuty_Ui.append(flatten(tmp[:]))
            tmp.clear()
        tmp = synteza_argumenty.split(",")
        atrybuty_Ui.append(flatten(tmp[:]))
        tmp.clear()
        synteza_string_lista.append(synteza_string)
        synteza_string = ""
        synteza_argumenty = ""
        synteza_string_tmp = ""
        i = i + 1
    for u in atrybuty_Ui:  # parsuje Ui
        for q in u:
            if (q.find(',') != -1):
                tmp = q.split(",")
                tmp4.append(tmp[:])
                index = u.index(q)
                u.remove(q)
                u.insert(index, flatten(tmp4[:]))
                tmp4.clear()
                tmp.clear()
    for u in atrybuty_Ui:
        u = flatten(u)

    for klucz in kandydujace_klucze2:  # sprawdzam czy klucz znajduje sie w jakichkolwiek atrybutach Ui
        for atrybut in atrybuty_Ui:
            if (all(x in flatten(atrybut) for x in klucz)):
                if_exists = False
    if (if_exists):
        synteza_string = "R" + str(i) + "("
        for x in klucze_pomoc_tmp[0]:
            if (x == klucze_pomoc_tmp[0][-1]):
                synteza_string = synteza_string + x
            else:
                synteza_string = synteza_string + x + ","
        synteza_string = synteza_string + ")" + " : " + "(brak)"
        synteza_string_lista.append(synteza_string)
        synteza_string = ""

    i = 0
    for string in synteza_string_lista:
        print(string)


# Main
if __name__ == "__main__":
    postac_kanoniczna = []
    postac_kanoniczna_split = []
    zaleznosci_funkcyjne = []

    print("------------Witam w prostym programie do normalizacji------------")
    while (True):

        # Wczytywanie danych z pliku oraz ze standardowego wejścia
        print("Proszę wybrać jedną z możliwości testowania programu:")
        print("Wpisanie danych ręcznie:               1")
        print("Wczytanie danych z pliku:              2")
        print("Skrypt pokazujący możliwości programu: 3")

        odpowiedz = int(input())
        if (odpowiedz == 1):
            print("Wpisywanie danych ręcznie")
            print("Proszę podać atrybuty relacji oddzielone przecinkami")
            attributes_string = input()
            print("Proszę podać ile zależności funkcyjnych zostanie wpisane: ")
            ilosc_zaleznosci = int(input())
            print("Proszę podać zależności funkcyjne: ")
            for x in range(ilosc_zaleznosci):
                line = input()
                if (line.find(';') != -1):
                    line = line.replace(";", "")
                zaleznosci_funkcyjne.append(line)

        elif (odpowiedz == 2):
            print("Proszę wybrać numer pliku, z którego dane mają zostać odczytane. Dostępne możliwości to od 01 do 10")
            numer = input()
            f = open(r'Testy\test-' + numer + '.txt', "r")
            lines = f.read().splitlines()
            f.close()

            i_pomoc = 0
            for line in lines:
                if (i_pomoc == 0):
                    attributes_string = line
                else:
                    zaleznosci_funkcyjne.append(line)
                i_pomoc = i_pomoc + 1

        elif (odpowiedz == 3):
            # Przygotowanie skryptu prezentującego możliwości programu -- przykład z moodla
            attributes_string = ("A,B,C,QX")
            zaleznosci_funkcyjne = ["A -> B", "QX -> C", "B,C -> A"]

        else:
            print("Nie ma takiej opcji")

        if (len(attributes_string) > 0 and len(zaleznosci_funkcyjne) > 0):
            print("------------------------")
            attributes = attributes_split(attributes_string)
            print("Atrybuty relacji:")
            print(*attributes)
            print("")

            print("Zaleznosci:")
            for zaleznosc in zaleznosci_funkcyjne:
                print(zaleznosc)
            print("")

            # Weryfikacja czy wszystkie atrybuty z 𝓕 znajdują się w 𝓤 i vice versa
            zaleznosci_funkcyjne_attr = functional_split_to_attributes(zaleznosci_funkcyjne)
            print("Status weryfikacji:")
            verification(attributes, zaleznosci_funkcyjne_attr)
            print("")

            postac_kanoniczna = postac_kanoniczna_function(zaleznosci_funkcyjne)
            if (len(postac_kanoniczna) > 1):
                postac_kanoniczna_split = usun_powtorzenia(postac_kanoniczna_split)

            print("Postać kanoniczna: ")
            for postac in postac_kanoniczna_split:
                print(postac[0] + " -> " + postac[1])
            postac_kanoniczna_split = usun_powtorzenia(postac_kanoniczna_split)
            print("")
            for i in range(len(attributes)):
                comb = combinations(attributes, i)
                for j in list(comb):
                    if (len(j) != 0):  # - omija pustą tuple
                        poprawne.append(dopelnienie_Fplus(j, postac_kanoniczna_split, True))
            poprawne.append(dopelnienie_Fplus(attributes, postac_kanoniczna_split, True))  # - wszystkie atrybuty
            print("Dopełnienie: ")
            for dop in poprawne:
                print(dop)
            print("")

            print("Atrybuty kluczowe:")
            atrybuty_kluczowe = podaj_atrybuty_kluczowe()
            if (len(atrybuty_kluczowe) > 0):
                print(*atrybuty_kluczowe)
            else:
                print("(brak)")
            print("")

            print("Atrybuty niekluczowe:")
            atrybuty_niekluczowe = podaj_atrybuty_niekluczowe(attributes, atrybuty_kluczowe)
            if (len(atrybuty_niekluczowe) > 0):
                print(*atrybuty_niekluczowe)
            else:
                print("(brak)")
            print("")

            print("Baza minimalna: ")
            baza_minimalna = znajdz_baze_minimalna(postac_kanoniczna_split, attributes)

            print("")
            Czy_3PN = Czy_jest_2PN_3PN(atrybuty_kluczowe, atrybuty_niekluczowe, postac_kanoniczna_split, baza_minimalna)
            print("")

            print("Synteza do 3PN: ")
            if (Czy_3PN):
                print("Schemat już jest w 3 postaci normalnej")
            else:
                synteza_do_3PN(baza_minimalna)
            print("")

        # -- czyszcenie wszystkiego
        postac_kanoniczna_split.clear()
        postac_kanoniczna.clear()
        atrybuty_kluczowe.clear()
        attributes.clear()
        poprawne.clear()
        zaleznosci_funkcyjne_attr.clear()
        kandydujace_klucze.clear()
        klucze_baza_minimalna.clear()
        poprawne.clear()
        zaleznosci_funkcyjne.clear()
        pierwszy_klucz = 0
        minimalna_ilosc_kluczy = 0
        # --
        print("Chcesz użyć programu jeszcze raz? [T/N]: ")
        kontynuacja = input()
        if (kontynuacja == 'n' or kontynuacja == 'N'):
            break