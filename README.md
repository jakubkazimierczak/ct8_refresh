[English version of README](README.en.md)

# CT8 Refresher
**Odświeżaj ważność swoich kont na CT8 jednym prostym poleceniem**!

Ten program loguje się automatycznie do panelu przy użyciu podanych danych. Logowanie
do usługi panelu przedłuża ważność konta o 90 dni (tak zapisane jest w regulaminie).

Uwaga: Ten program wymaga posiadania ważnego i aktywnego konta w hostingu CT8. Program nie zadziała, jeśli 
Twoje konto już wygasło. Jeśli potrzebujesz konta w CT8, [zarejestruj się](https://www.ct8.pl/offer/create_new_account)
zanim przejdziesz dalej.


# Funkcje
* [x] Automatyczne logowanie do wielu kont
* [x] Podgląd dat wygaśnięcia kont oraz pozostałych dni do wygaśnięcia<sup>1</sup> 
* [x] Łatwe zarządzanie kontami użytkowników
* [x] Logowanie tylko do wybranych kont

<sup>1</sup> Nie uwzględnia to manualnego logowania się przez użytkownika. 


# Instalacja
# Wymagania
Instalacja w poniżej wymienionych krokach wymaga posiadania zainstalowanego 
[Python 3](https://www.python.org/downloads/) oraz
[pipx](https://pipxproject.github.io/pipx/installation/).

Jeśli masz już zainstalowanego Pythona, by zainstalować pipx, wpisz poniższe komendy (jeśli używasz Windowsa zamiast `python3` użyj `python`):
```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```
> Uwaga: Jeśli dopiero co zainstalowałeś pipx, będziesz musiał uruchomić ponownie terminal lub ponownie się zalogować.
Uruchom polecenie `python3 -m pipx ensurepath` ponownie, by upewnić się, że pipx został zainstalowany poprawnie. 

> Zobacz [oficjalny poradnik instalacji pipx](https://pipxproject.github.io/pipx/installation/) by dowiedzieć się więcej.

## Zainstaluj program z użyciem pipx (zalecana metoda)
By zainstalować program, użyj polecenia `pipx install`:
```
pipx install git+https://github.com/jakubkazimierczak/ct8_refresh
```
Program będzie globalnie dostępny w terminalu pod nazwą `ct8_refresh` (lub `ct8_refresh.exe` w systemie Windows).  


## Uruchom bez instalacji
By uruchomić program bez instalacji, użyj `pipx run`:
```
pipx run --spec git+https://github.com/jakubkazimierczak/ct8_refresh ct8_refresh -h
```
Jeśli chcesz używać programu w ten sposób komendy dopisujesz na samym końcu polecenia, np.:
```
pipx run --spec git+https://github.com/jakubkazimierczak/ct8_refresh ct8_refresh -h
pipx run --spec git+https://github.com/jakubkazimierczak/ct8_refresh ct8_refresh user --add jan_kowalski
```


# Użycie
## Wyświetlenie pomocy
By wyświetlić pomoc dla programu użyj `ct8_refresh --help` (lub `-h`).

Program składa się z osobnych komend, z których każda z nich posiada własną stronę pomocy, np.:
`ct8_refresh run -h` wyświetli pomoc dla komendy `run`.

## Pierwsze użycie
*To tylko krótki poradnik. Nie przedstawia on wszystkich dostępnych komend. Aby dowiedzieć się więcej o dostępnych
komendach, skorzystaj z dołączone do programu pomocy (`-h`)*.
### Dodawanie użytkowników
**UWAGA: Twoje konto musi być wcześniej zarejestrowane w CT8.pl. Ten skrypt nie tworzy konta za Ciebie!** 

Po pierwsze musisz dodać konto, na które chcesz się automatycznie logować:
```
ct8_refresh user --add twoj_login
```
> Zostaniesz poproszony o hasło — nie martw się, nie pojawi się ono w konsoli.

Jeśli masz kilku użytkowników, możesz dodać ich wszystkich, oddzielając loginy spacjami: 
```
ct8_refresh user --add twoj_login twoj_inny_login jeszcze_inny_login
```
### Uruchomienie automatycznego logowania
Po dodaniu wszystkich użytkowników możesz się nimi zalogować, wpisując jedno polecenie: 
```
ct8_refresh run
```
Program spróbuje zalogować się na wszystkie dodane i **aktywne** konta.
> **Uwaga**: Przy pierwszym uruchomieniu zostanie pobrany specjalny Chrome (headless). Wielkość pobierania to około 150 MB.
### Wyświetlanie użytkowników oraz dat wygaśnięcia kont
Jeśli chcesz wyświetlić wszystkich użytkowników oraz daty wygaśnięcia kot użyj polecenia:
```
ct8_refresh user --show
```
### Wykluczanie użytkowników z logowania
Jeśli masz użytkownika, którym nie chcesz się logować, możesz go wyłączyć, zamiast go usuwać:
```
ct8_refresh user -d login
```


# Zgłaszanie błędów
Jeśli trafiłeś na błąd podczas używania tego programu - [zgłoś issue](https://github.com/jakubkazimierczak/ct8_refresh/issues/new/choose) 
(by zgłosić issue, musisz posiadać konto w serwisie GitHub). 
Byłoby dobrze, jeśli do problemu dołączyłbyś logi używania programu. Uruchom program dodając flagę `--debug` np.:
```
ct8_refresh --debug run
```
Aby dowiedzieć się, gdzie przechowywane są logi, użyj polecenia:
```
ct8_refresh --debug-path
```


# Znane problemy
* Gdy używany jest debug mode, ścieżka logów jest wypisywana podwójnie.
