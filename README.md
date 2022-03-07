# Normalization
Program, który konwertuje wejściowy schemat relacji do 3PN
- parsuje wejściowy schemat relacji jako zbiór atrybutów oraz zbiór zależności funkcyjnych
- oblicza domknięcie dla każdego podzbioru zbioru atrybutów
- oblicza minimalny zbiór kluczy kandydujących oraz nadklucze oraz wypisuje atrybuty kluczowe jak i nie kluczowe
- oblicza bazę minimalną dla wejściowego zbioru zależności funkcyjnych,
- sprawdza czy podany schemat relacji jest w 2 oraz 3 postaci normalnej (zakładamy na wejściu co najmniej 1 postać normalną),
- jeżeli schemat nie jest w 3 postaci normalnej, to normalizuje go przy pomocy algorytmu syntezy.
