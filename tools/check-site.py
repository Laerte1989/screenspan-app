#!/usr/bin/env python3
"""
Controlli sul sito di ScreenSpan.

PERCHE' ESISTE. Il sito e' fatto di tre pagine bilingui in HTML scritto a
mano, e ognuno dei difetti che cerca qui sotto e' un difetto che c'e'
stato davvero:

  - un link nel footer che puntava a una pagina inesistente (privacy.html),
    rimasto li' per mesi perche' nessuno clicca il proprio footer;
  - una pagina senza <meta viewport>, che sul telefono si apriva
    rimpicciolita - ed era la guida, cioe' l'unica pagina che si legge
    con il telefono in mano;
  - due attributi class= sullo stesso tag, dove il secondo veniva
    ignorato in silenzio dal browser;
  - un blocco tradotto presente in italiano e mancante in inglese, che
    non si vede a occhio perche' l'altra lingua e' nascosta.

Nessuno di questi rompe la pagina in modo evidente: la pagina si apre,
sembra funzionare, e il difetto lo trova un visitatore. Questi controlli
costano due secondi e li trovano prima.

Si lancia a mano dalla radice del repository:

    python3 tools/check-site.py

Esce con codice 1 se qualcosa non va, cosi' la CI se ne accorge.
"""

import os
import re
import sys

PAGES = ["index.html", "guide.html", "privacy.html"]

# Il sito e' pubblico: qualunque di queste stringhe sarebbe un errore
# grave, non un dettaglio da sistemare poi.
SEGRETI = [
    r"AIza[A-Za-z0-9_-]{15,}",          # chiave API Google
    r"screenspan-[0-9a-f]{5}",          # id del progetto Firebase
    r"firebasedatabase\.app",
    r"apps\.googleusercontent\.com",
    r"PLAY_SERVICE_ACCOUNT",
    r"storePassword|keyAlias|keyPassword",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
]

problemi = []


def errore(pagina, testo):
    problemi.append(f"{pagina}: {testo}")


def controlla(pagina):

    if not os.path.exists(pagina):
        errore(pagina, "la pagina non esiste")
        return

    s = open(pagina, encoding="utf-8").read()

    # ── la testa della pagina ────────────────────────────────────────────
    if "<meta charset" not in s:
        errore(pagina, "manca <meta charset>")

    if 'name="viewport"' not in s:
        errore(pagina, "manca <meta viewport>: sul telefono si apre rimpicciolita")

    if "<title>" not in s:
        errore(pagina, "manca <title>")

    # ── link interni ────────────────────────────────────────────────────
    for href in sorted(set(re.findall(r'href="([^"#:]+\.(?:html|jpg|png|css|js))"', s))):
        if not os.path.exists(href):
            errore(pagina, f'il link "{href}" punta a un file che non esiste')

    for src in sorted(set(re.findall(r'src="((?!data:|https?:)[^"]+)"', s))):
        if not os.path.exists(src):
            errore(pagina, f'l\'immagine "{src}" non esiste')

    # ── attributi class duplicati ───────────────────────────────────────
    for tag in re.findall(r"<[a-zA-Z][^>]*>", s):
        if tag.count("class=") > 1:
            errore(pagina, f"due attributi class sullo stesso tag: {tag[:80]}")

    # ── bilanciamento delle due lingue ──────────────────────────────────
    it = len(re.findall(r'data-lang="it"', s))
    en = len(re.findall(r'data-lang="en"', s))

    if it != en:
        errore(pagina, f"blocchi tradotti sbilanciati: it={it}, en={en}")

    # Ogni blocco inglese deve partire attivo: l'inglese e' la lingua
    # predefinita, e senza "active" quel pezzo resta invisibile finche'
    # il JavaScript non gira - cioe' per sempre, se e' disattivato.
    for tag in re.findall(r'<[a-z]+[^>]*data-lang="en"[^>]*>', s):
        if "active" not in tag:
            errore(pagina, f"blocco EN che non parte attivo: {tag[:80]}")

    # ── segreti ─────────────────────────────────────────────────────────
    for pattern in SEGRETI:
        trovato = re.search(pattern, s, re.IGNORECASE)
        if trovato:
            errore(pagina, f"possibile segreto nel testo: {trovato.group(0)[:30]}")


# Le vocali accentate scritte con l'apostrofo: "e'" invece di "e",
# "piu'" invece di "piu". Nei commenti del codice sorgente di questo
# progetto e' la convenzione voluta; nel TESTO CHE LEGGE L'UTENTE e' un
# errore di ortografia, e sono due cose che si confondono facilmente
# lavorando sugli stessi file. Ne sono passate sette in una sola
# modifica, incluse una nella <meta description> - che e' il testo che
# Google mostra nei risultati - e un "c'e'" che un primo controllo piu'
# ingenuo non aveva visto.
ACCENTI_MANCATI = [
    "e", "piu", "gia", "perche", "cosi", "puo", "meta", "sara",
    "verra", "potra", "dovra", "citta", "qualita", "possibilita",
    "necessita", "cioe", "ventitre", "tre",
]


def controlla_accenti(pagina, s):
    """Cerca l'apostrofo al posto dell'accento nel solo testo visibile."""

    # Il testo italiano dei blocchi tradotti, piu' le meta - che si
    # vedono nei risultati di ricerca e nelle anteprime dei link.
    #
    # SI CHIUDE SUL NOME DEL TAG, non sul primo "</" che capita: la
    # prima versione di questo controllo si fermava al </strong> dentro
    # al paragrafo e non guardava il resto, dove infatti si nascondeva
    # un "c'e'" che e' passato liscio.
    pezzi = re.findall(
        r'<([a-z0-9]+)[^>]*data-lang="it"[^>]*>(.*?)</\1>', s, re.S)
    pezzi = [testo for _tag, testo in pezzi]
    pezzi += re.findall(r'<meta name="description" content="([^"]*)"', s)

    parole = "|".join(ACCENTI_MANCATI)

    for pezzo in pezzi:
        # Niente lookbehind su lettera: cosi' anche la seconda meta' di
        # "c'e'" viene vista.
        for trovato in re.findall(r"(?<![A-Za-z\u00c0-\u00ff])(" + parole + r")'", pezzo):
            errore(pagina, f"accento scritto con l'apostrofo nel testo visibile: \"{trovato}'\"")


# ── LE DUE ROADMAP NON DEVONO DIVERGERE ──────────────────────────────────
#
# La roadmap esiste in due file, uno per lingua, perche' i due pulsanti
# sul sito portano a due documenti diversi. Due copie dello stesso
# elenco divergono al primo taglio fatto da un lato solo - ed e' gia'
# successo in questo repository: la sezione riassunta sulla home
# annunciava fra le "prossime tre" una voce appena rimossa dal file.
#
# Non si confronta il TESTO, che e' tradotto e quindi diverso per
# definizione: si confronta la STRUTTURA. Se una voce viene aggiunta,
# rimossa o spostata di sezione in una lingua sola, i conti non tornano
# piu' e la CI se ne accorge.
ROADMAP_IT = "ROADMAP.md"
ROADMAP_EN = "ROADMAP.en.md"


def struttura_roadmap(percorso):
    s = open(percorso, encoding="utf-8").read()

    return {
        "sezioni": len(re.findall(r"^## ", s, re.M)),
        "voci in arrivo": len(re.findall(r"^### \d+\. ", s, re.M)),
        "voci fatte": len(re.findall(r"^- \[x\]", s, re.M)),
        "voci sempre in corso": len(re.findall(r"^- \[ \]", s, re.M)),
    }


def controlla_roadmap():

    for percorso in (ROADMAP_IT, ROADMAP_EN):
        if not os.path.exists(percorso):
            errore(percorso, "la roadmap non esiste")
            return

    it = struttura_roadmap(ROADMAP_IT)
    en = struttura_roadmap(ROADMAP_EN)

    for chiave in it:
        if it[chiave] != en[chiave]:
            errore(ROADMAP_EN,
                   f"{chiave}: {it[chiave]} in italiano, {en[chiave]} in inglese"
                   " - una voce e' stata cambiata in una lingua sola")

    # E si rimandano a vicenda: una traduzione che non si raggiunge
    # dall'altra e' una traduzione che nessuno leggera'.
    if ROADMAP_EN not in open(ROADMAP_IT, encoding="utf-8").read():
        errore(ROADMAP_IT, f"non rimanda a {ROADMAP_EN}")

    if ROADMAP_IT not in open(ROADMAP_EN, encoding="utf-8").read():
        errore(ROADMAP_EN, f"non rimanda a {ROADMAP_IT}")


def controlla_condivisione():
    """Le meta per le condivisioni, che si vedono solo incollando il link."""

    s = open("index.html", encoding="utf-8").read()

    for prop in ["og:title", "og:description", "og:image", "og:url"]:
        if f'property="{prop}"' not in s:
            errore("index.html", f"manca la meta {prop}")

    m = re.search(r'property="og:image" content="([^"]+)"', s)

    if m:
        nome = m.group(1).rsplit("/", 1)[-1]

        if not os.path.exists(nome):
            errore("index.html", f"og:image punta a {nome}, che nel repository non c'e'")


def main():

    if not os.path.exists("index.html"):
        print("Da lanciare dalla radice del repository.", file=sys.stderr)
        return 1

    for pagina in PAGES:
        controlla(pagina)

        if os.path.exists(pagina):
            controlla_accenti(pagina, open(pagina, encoding="utf-8").read())

    controlla_condivisione()
    controlla_roadmap()

    if problemi:
        print(f"\n{len(problemi)} problemi:\n")
        for p in problemi:
            print(f"  ✗ {p}")
        print()
        return 1

    print(f"✓ {len(PAGES)} pagine controllate, tutto a posto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
