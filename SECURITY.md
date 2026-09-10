# Reporting a security issue

*🇮🇹 [Versione italiana](#-italiano) più in basso.*

## Do not open a public issue

If you think you have found a vulnerability in ScreenSpan, **do not
describe it in the Issues**: it would be readable by everyone before a fix
exists, and whoever reads it first is not necessarily trying to help.

Write to **[laerte.developer@gmail.com](mailto:laerte.developer@gmail.com)**
instead, with a subject line starting with `[SECURITY]`.

## What to include

The more precise, the sooner it gets fixed:

- What an attacker gains from it, in one sentence.
- The steps to reproduce it, in order.
- Phone models and Android versions where you saw it.
- Whether it requires being joined to the same Wi-Fi Direct group, or
  just being on the same ordinary Wi-Fi network.

## What to expect

- **Acknowledgement within 3 days.**
- An assessment of what I understood and what I intend to do, within 14
  days.
- If the fix ships in a released version, credit is yours if you want it —
  and you stay anonymous if you prefer.

There is no bounty programme: this is an app built by one person. What I
can offer is to take it seriously and to answer.

## Where to look, if you are curious

Two areas matter more than the rest, and it is worth saying so openly:

- **The three TCP ports** the phones open between themselves (video,
  commands, geometry). They accept connections only from the Wi-Fi Direct
  group's subnet or from the phone itself; traffic inside the group is
  unencrypted by us, protected by the group's own WPA2 encryption. Anyone
  already inside the group is treated as authorised: that is a stated
  decision, not an oversight.
- **The wireless debugging pairing** the sharing phone uses to create the
  extra screen. It is a standard Android feature, the pairing applies to
  that phone alone, and it can be revoked at any time from the system
  settings.

---

# 🇮🇹 Italiano

## Segnalare un problema di sicurezza

### Non aprire una issue pubblica

Se pensi di aver trovato una vulnerabilità in ScreenSpan, **non
descriverla nelle Issues**: sarebbe leggibile da tutti prima che esista
una correzione, e chi la legge per primo non è necessariamente chi vuole
aiutare.

Scrivi invece a **[laerte.developer@gmail.com](mailto:laerte.developer@gmail.com)**,
con oggetto che comincia per `[SECURITY]`.

### Cosa mettere nella segnalazione

Più preciso è, prima si corregge:

- Che cosa si ottiene sfruttandola, in una frase.
- I passaggi per riprodurla, nell'ordine.
- Modello dei telefoni e versione di Android su cui l'hai vista.
- Se serve essere collegati allo stesso gruppo Wi-Fi Direct, o basta
  essere sulla stessa rete Wi-Fi normale.

### Cosa aspettarsi

- **Conferma di ricezione entro 3 giorni.**
- Una valutazione con quello che ho capito e cosa intendo fare, entro 14
  giorni.
- Se la correzione arriva in una versione pubblicata, il merito è tuo se
  vuoi essere citato — e resta anonimo se preferisci.

Non c'è un programma di ricompense: è un'app sviluppata da una persona
sola. Quello che posso offrire è di prenderla sul serio e rispondere.

### Dove guardare, se ti interessa

Due punti valgono più degli altri, e vale la pena dirlo apertamente:

- **Le tre porte TCP** che i telefoni si aprono fra loro (video, comandi,
  geometria). Accettano connessioni solo dalla sottorete del gruppo Wi-Fi
  Direct o dal telefono stesso; il traffico dentro il gruppo è in chiaro,
  protetto dalla cifratura WPA2 del gruppo. Chi è già dentro il gruppo è
  considerato autorizzato: è una scelta dichiarata, non una dimenticanza.
- **L'accoppiamento con il debug wireless** di Android, che il telefono
  sorgente usa per creare lo schermo aggiuntivo. È una funzione standard
  di Android, l'accoppiamento vale solo per quel telefono, ed è revocabile
  in qualunque momento dalle impostazioni di sistema.
