# Roadmap

Dove è arrivato ScreenSpan e dove sta andando.

*🇬🇧 [English version](ROADMAP.md) · Sono intenzioni in ordine di
priorità, non date.*

---

## ✅ Fatto

Tutto quello che è già nell'app pubblicata.

- [x] **Schermo unito su più telefoni**
      Un'app scelta dall'utente gira su uno schermo più grande di quello
      del telefono, e la parte che non ci sta la mostrano gli altri.
- [x] **Tocco e scrittura da ogni telefono**
      Tocchi, trascinamenti, gesti a due dita, testo e tasto Indietro:
      partono da qualunque telefono e arrivano sull'app condivisa.
- [x] **Collegamento diretto fra i telefoni**
      Wi-Fi Direct con annuncio e ricerca automatica: nessun router,
      nessuna rete in comune, e le immagini non passano da internet.
- [x] **Due disposizioni**
      Telefoni affiancati (in verticale) o impilati (in orizzontale),
      con la disposizione decisa dal telefono che condivide e annunciata
      all'altro.
- [x] **Preparazione una volta sola**
      Circa due minuti sul solo telefono che condivide, con procedura
      guidata schermata per schermata e
      [guida illustrata](https://laerte1989.github.io/screenspan-app/guide.html).
      Resta fatta dopo riavvii e reinstallazioni.
- [x] **Qualità regolabile a caldo**
      Fotogrammi al secondo e nitidezza si cambiano mentre si condivide,
      con il massimo misurato sul telefono invece che indovinato.
- [x] **Prova gratuita e abbonamento**
      15 minuti al giorno per provarla, abbonamento annuale per l'uso
      quotidiano, e chi guarda non paga mai.
- [x] **Riprese automatiche dai guasti**
      Il decoder si ricostruisce da solo, la ricerca riparte, e
      l'autorizzazione si rifà quando il telefono smette di fidarsi
      della chiave già accoppiata.

---

## 🎯 In arrivo

In ordine di quanto cambiano l'esperienza, non di quanto sono facili.

### 1. Disposizione a puzzle

Oggi i telefoni possono stare solo tutti in verticale affiancati o tutti
in orizzontale impilati. La disposizione **mista** è la richiesta più
naturale: due telefoni in verticale accanto a uno in orizzontale, una L,
una griglia 2×2 con un telefono ruotato.

Sono due lavori che vanno insieme, perché uno senza l'altro non serve:

- il telefono che condivide deve poter costruire uno schermo di forma
  qualunque e assegnare a ciascun telefono un rettangolo qualunque, non
  più una fetta uguale alle altre;
- serve una **schermata dove trascinare i telefoni** al posto in cui
  stanno davvero sul tavolo. Senza quella, una disposizione libera
  diventa impossibile da spiegare.

È il punto dove ScreenSpan mantiene la promessa fino in fondo: **il
telefono pieghevole te lo costruisci tu**, della forma che ti serve in
quel momento, con i telefoni che hai già in casa.

### 2. La guida per il telefono che hai

La guida all'accoppiamento è fotografata su un realme, e il testo stesso
deve avvisare che «su altri telefoni può chiamarsi diversamente». È il
punto in cui si perdono più persone: chi non trova la voce con quel nome
si fermerà lì.

Una versione per marca — Samsung, Xiaomi, Pixel, Huawei, Motorola — con
i nomi veri di quelle voci e gli screenshot di quei telefoni. Non è
codice: è la cosa che più farebbe arrivare in fondo chi ha installato.

### 3. Appunti condivisi

Copiare su un telefono e incollare sull'altro, dato che i due sono già
collegati e già si scambiano il testo digitato.

---

## 🔄 Sempre in corso

Non finisce mai, e vale la pena metterlo per iscritto.

- [ ] **Nuovi telefoni**
      Il Wi-Fi Direct è la parte che ogni produttore implementa a modo
      suo, e quasi ogni difetto vero di quest'app viene da lì. Ogni
      modello provato è un modello in meno che si comporta a sorpresa.
- [ ] **Prove su telefoni veri, non solo compilazione**
      L'ultima regressione seria è stata trovata solo mettendo due
      telefoni sul tavolo, e nessun test automatico l'avrebbe vista.
      Dopo ogni modifica al collegamento fra i telefoni, si riprova
      sull'hardware.

---

## 🚫 Non in programma

Dirlo evita che venga richiesto tre volte.

- **Collegamento su rete Wi-Fi normale.** Il Wi-Fi Direct è l'unico
  trasporto per scelta: funziona anche dove non c'è nessuna rete, e non
  fa passare le immagini per un router che non controlliamo.
- **iPhone.** iOS non offre nulla di equivalente: né il collegamento
  diretto usato qui, né la possibilità di creare uno schermo aggiuntivo
  per un'app. Non è una questione di tempo, è che non si può.
- **Root o modifiche al sistema.** L'autorizzazione che ScreenSpan usa è
  una funzione standard di Android, revocabile in qualunque momento. Non
  si andrà oltre.

---

## Hai un'idea?

Le [Issues](https://github.com/Laerte1989/screenspan-app/issues) sono
aperte, e c'è un modulo pronto per le proposte. La cosa più utile che
puoi scrivere non è la soluzione: è **cosa stavi provando a fare** e
cosa te lo ha impedito.
