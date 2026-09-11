# Roadmap

Where ScreenSpan has got to, and where it is going.

*🇮🇹 [Versione italiana](ROADMAP.it.md) · These are intentions in order of
priority, not dates: the only thing here with a date is the technical
deadline Android imposes (see «Ongoing»).*

---

## ✅ Done

Everything already in the published app.

- [x] **One screen across several phones**
      An app you choose runs on a screen larger than the phone's own, and
      the part that does not fit is shown by the other phones.
- [x] **Touch and typing from every phone**
      Taps, drags, two-finger gestures, text and the Back button: they
      start on any phone and land on the shared app.
- [x] **A direct link between the phones**
      Wi-Fi Direct with automatic advertising and discovery: no router,
      no shared network, and the images never travel over the internet.
- [x] **Two arrangements**
      Phones side by side (upright) or stacked (sideways), with the
      arrangement decided by the sharing phone and announced to the
      other.
- [x] **Setup done once**
      About two minutes on the sharing phone only, walked through screen
      by screen, with an
      [illustrated guide](https://laerte1989.github.io/screenspan-app/guide.html).
      It stays done across restarts and reinstalls.
- [x] **Quality adjustable while sharing**
      Frames per second and sharpness change mid-session, with the
      maximum measured on the phone rather than guessed.
- [x] **Free trial and subscription**
      15 minutes a day to try it, a yearly subscription for everyday
      use, and whoever watches never pays.
- [x] **Automatic recovery**
      The decoder rebuilds itself, discovery restarts on its own, and the
      authorisation is redone when the phone stops trusting the key it
      already paired.

---

## 🎯 Next

In order of how much they change the experience, not of how easy they
are.

### 1. Puzzle layout

Today the phones can only all be upright side by side, or all sideways
stacked. A **mixed** arrangement is the most natural request: two
upright phones next to one sideways, an L shape, a 2×2 grid with one
phone rotated.

These are two pieces of work that go together, because neither is any
use without the other:

- the sharing phone must be able to build a screen of any shape and
  assign each phone any rectangle, instead of one equal slice each;
- there needs to be a **screen where you drag the phones** into the
  position they actually occupy on the table. Without it, a free
  arrangement becomes impossible to explain.

This is where ScreenSpan keeps its promise all the way: **you build the
foldable yourself**, in whatever shape you need at that moment, out of
the phones you already have at home.

### 2. A guide for the phone you own

The setup guide is photographed on a realme, and its own text has to
warn that "other phones may call it something else". This is where most
people are lost: whoever cannot find the item under that name will stop
right there.

A version per brand — Samsung, Xiaomi, Pixel, Huawei, Motorola — with
the real names those phones use and screenshots taken on them. It is not
code: it is the single thing that would most help the people who already
installed the app get to the end.

### 3. Shared clipboard

Copy on one phone and paste on the other, given that the two are already
connected and already exchange the text you type.

---

## 🔄 Ongoing

It never ends, and it is worth putting in writing.

- [ ] **New Android versions**
      Every release changes something exactly where ScreenSpan works:
      permissions, foreground services, display handling. The deadline
      already known and dated is **`targetSdk 37`**, when Android will
      stop honouring the orientation an app asks for on large screens:
      by then the watching phone must adapt to the shape it receives
      instead of demanding one.
- [ ] **New phones**
      Wi-Fi Direct is the part every manufacturer implements its own
      way, and nearly every real defect in this app comes from there.
      Every model tested is one less model that behaves unexpectedly.
- [ ] **Testing on real phones, not just compiling**
      The last serious regression was found only by putting two phones on
      a table, and no automated test would have caught it. After every
      change to the link between the phones, it gets tried on the
      hardware again.

---

## 🚫 Not planned

Saying so avoids being asked three times.

- **Connecting over an ordinary Wi-Fi network.** Wi-Fi Direct is the
  only transport by choice: it works where there is no network at all,
  and it does not route the images through a router we do not control.
- **iPhone.** iOS offers nothing equivalent: neither the direct link
  used here, nor the ability to create an extra screen for an app. It is
  not a matter of time — it cannot be done.
- **Root or system modifications.** The authorisation ScreenSpan uses is
  a standard Android feature, revocable at any time. It will not go
  further than that.

---

## Got an idea?

The [Issues](https://github.com/Laerte1989/screenspan-app/issues) are
open, and there is a form ready for proposals. The most useful thing you
can write is not the solution: it is **what you were trying to do** and
what stopped you.
