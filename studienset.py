"""
Studienset-Auswahl und Einbettung
---------------------------------
Waehlt aus use_cases.json die feste Interview-Menge aus und baut sie direkt in eine
fertige Simulator-Datei ein: simulator_studie.html. Diese Datei enthaelt die zehn
Use Cases bereits, du oeffnest sie per Doppelklick, ohne Upload.

Reihenfolge:
  1. perception_layer.py   (erzeugt variablen.json)
  2. decisionlayer.py      (erzeugt use_cases.json)
  3. studienset.py         (baut die festen 10 in simulator_studie.html ein)

Voraussetzung: simulator.html liegt im selben Ordner (dient als Vorlage).

Zusammensetzung der zehn Stimuli (alle aus dem Generator):
  Proaktiv:    Tunnel (4,5), Glatteis Waldabschnitt (7,1), Glatteis Bruecke (7,2)
  Empfehlung:  Kalte Morgenfahrt (1,1), Kind an Bord (2,3), Stau (3,1),
               Terminverzug physisch (5,1), Heimkehr (6,1), Beifahrer (8,3),
               Terminverzug virtuell (5,3)
  Zwei Kontrastpaare: Terminverzug physisch gegen virtuell, Glatteis Wald gegen Bruecke.
  Die Paare stehen nicht direkt nebeneinander.
"""

import json

AUSWAHL = [
    (1, 1),  # Kalte Morgenfahrt        -> Empfehlung
    (2, 3),  # Kind an Bord am Morgen    -> Empfehlung
    (3, 1),  # Stau, Entspannung         -> Empfehlung
    (4, 5),  # Tunnel, Luftqualitaet     -> proaktiv
    (5, 1),  # Terminverzug physisch     -> Empfehlung (Kontrast zu 5,3)
    (6, 1),  # Heimkehr bei Dunkelheit   -> Empfehlung
    (7, 1),  # Glatteis Waldabschnitt    -> proaktiv (Kontrast zu 7,2)
    (8, 3),  # Schlafender Beifahrer      -> Empfehlung
    (5, 3),  # Terminverzug virtuell     -> Empfehlung (Kontrast zu 5,1)
    (7, 2),  # Glatteis Bruecke          -> proaktiv (Kontrast zu 7,1)
]

with open("use_cases.json", "r", encoding="utf-8") as f:
    alle = json.load(f)

index = {(u["szenario_id"], u["variante"]): u for u in alle}

studie = []
for key in AUSWAHL:
    if key in index:
        studie.append(index[key])
    else:
        print("Nicht gefunden, bitte AUSWAHL pruefen:", key)

with open("use_cases_studie.json", "w", encoding="utf-8") as f:
    json.dump(studie, f, ensure_ascii=False, indent=2)
with open("use_cases_data.js", "w", encoding="utf-8") as f:
    f.write("window.USE_CASES = " + json.dumps(studie, ensure_ascii=False) + ";")

try:
    with open("simulator.html", "r", encoding="utf-8") as f:
        html = f.read()
    eingebettet = "<script>window.USE_CASES = " + json.dumps(studie, ensure_ascii=False) + ";</script>"
    if '<script src="use_cases_data.js"></script>' in html:
        html = html.replace('<script src="use_cases_data.js"></script>', eingebettet)
    with open("simulator_studie.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("simulator_studie.html mit eingebetteten Use Cases geschrieben.")
except FileNotFoundError:
    print("Hinweis: simulator.html nicht gefunden, simulator_studie.html nicht erstellt.")

print(f"\nStudienset mit {len(studie)} Use Cases:")
for u in studie:
    print(f"  P{u['szenario_id']}.{u['variante']}  {u['vorgeschlagener_modus']:22}  {u.get('konkrete_funktion','')[:45]}")