# ZapočtovýProgram
# Konvertor z kamerového záznamu so svetelným signálom do morzeovky. 
Convertor of light signal into morse

Program sníma obraz z web kamery z ktorej podľa svetelnej signalizácie (pravidla morzeovky) preloží signál do abecedy. System morzeovej abecedy sa skladá z rôznych kombinácií krátkych a dlhých signálov. Krátky signal symbolizuje bodku a dlhší signál čiarku. Zvyčajne sa vyskytuju v pomere 1:2 alebo 1:3.

PRAVIDLA VYSIELANIA MORZEOVEJ ABECEDY:
1. Dĺžka bodky je jedna časový jednotka
2. Čiarka trvá 3 časové jednotky
3. Medzera medzi symbolmi toho istého písmena je 1 časová jednotka
4. Medzera medzi písmenami sú 3 časové jednotky
5. Medzera medzi slovami je 7 časových jednotiek

ABECEDA:
[Klikni tu](https://miro.medium.com/max/1163/0*dSma6M7d5vatzPyH.jpg)


Program vyžaduje knižnice:
 - cv2 
 - time
 - numpy

Pri vstupe program žiada od používateľa
1. Časovú jednotku - ČJ - určuje dlžku zakladneho svetelneho signálu resp. absencie svetelneho signálu po určite násobky (vyššie pravidla vysielania morzeovej abecedy). Udáva sa v sekundách (0.3, 1, ...)
2. Kamerový port - určuje ktorý port bude využitý pre nahravanie obrazu. Vstavané kamery su označované 0, kamery s dodatočným pripojením maju číslo bežne radovo po 0.

Po spustení programu a vložení požadovaných vstupov sa otvorí okno "Webcam". 
Na pravej strane okna je obdlžnik do ktoreho je potrebne svietiť svetelným zdrojom (odporúčam telefon) v príslušných untervaloch. Pre toto vysielanie svetelneho signálu odporúčam aplikáciu, ktora precízne vysiela signál podľa stanovených pravidiel (používala som Flashlight (ČJ - 0.3 secs) a MorseLight (ČJ - 1sec)). Dá sa vysielať aj pomocou obyčajnej baterky s preciznym časovaním intervalov.
Pre správne zaznamenanie nie/svietenia je dôležité nastaviť svetelnu hranicu (treshold). Tento udaj je najlepšie nastaviť tesne pod hodnotu svetelnosti pri stave svietenia svetla. V tmavších miestnostiach môže byť táto hranica aj nižšia. V miestnosti s vysokým osvetlením je tento udaj veľmi dôležitý, pretože ak nie je nastavený správne, neeviduje sa zapnuté svetlo. 

V programe sa nastavuju údaje pomocou klávesnice. Keď sa zapne kamera, použivateľ pomocou kláves "w" a "s" prispôsobi svetelnu hranicu (treshold) a keď je pripravený podrží kláves "o" a začne sa nahravanie signálu. Po dokončení vysielania použíteľ ukončí nahrávanie svetelných signálov klavesou "q" a vyskočí mu posledne okno s preloženou správou. Nasledne ho uzavrie klávesou "r", čím sa ukončí celý program. Ďalšie klávesy su uvedene priamo v programe.
