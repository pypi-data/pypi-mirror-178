# DMT-HTWK
## Eine IPython-Erweiterung zur Verbindung mit dem E-Assessment-Tool DMT (Data Management Tester)

Diese Erweiterung ermöglicht es Aufgaben aus dem E-Assessment-Tool DMT abzufragen und dynamisch im Notebook darzustellen.
Ebenso können die Eingaben und Lösungen an DMT gesendet werden, um ein automtatisches Feedback zu erhalten.

## %dmtCon

Dieser Befehl ermöglicht es die URL von DMT zu hinterlegen (z.B.: "%dmtCon http://localhost:8081")

## %dmt

Dieser Befehl fragt die Aufgaben-Attribute per REST-Request über eine gültige TaskID von DMT ab und erstellt abhängig vom TaskType ein dynamisches UI.
(z.B.: "%dmt modell:1") 
Druch einen Klick auf den generierten Button "Abgabe Überprüfen", werden alle UI-Felder ausgelesen und als Antwort an DMT geschickt.
Das Feedback, ob die Lösung richtig oder flasch ist, sowie die erhaltenen Punkte werden unter dem Button angezeigt.

## Nutzung

Nach der Installation sind folgende Schritte für die Nutzung nötig:
- %load_ext dmt_htwk
- %dmtCon + Basispfad der DMT-URL

Da nun das Package geladen, sowie eine URL hinterlegt ist, können sie mit der Nutzung von DMT beginnen.
Dazu schreiben sie folgenden Befehl in eine neue Cell:
- %dmt + gewünschte TaskID

Wenn alles geklappt hat, sollten sie nun die ensprechende Aufgabe aus DMT in ihrem Notebook bearbeiten können.