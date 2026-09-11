#!/usr/bin/env python3
"""
Checks for the ScreenSpan website.

WHY THIS EXISTS. The site is three hand-written bilingual HTML pages, and
every defect looked for below is a defect that actually happened:

  - a footer link pointing at a page that did not exist (privacy.html),
    left there for months because nobody clicks their own footer;
  - a page with no <meta viewport>, which opened shrunk on a phone - and
    it was the guide, i.e. the one page people read with a phone in hand;
  - two class= attributes on the same tag, where the second one was
    silently ignored by the browser;
  - a translated block present in Italian and missing in English, which
    is invisible to the eye because the other language is hidden.

None of these breaks the page in an obvious way: the page opens, it looks
like it works, and the defect is found by a visitor. These checks cost
two seconds and find them first.

Run it by hand from the repository root:

    python3 tools/check-site.py

Exits with status 1 if anything is wrong, so CI notices.
"""

import os
import re
import sys

PAGES = ["index.html", "guide.html", "privacy.html"]

# The site is public: any of these strings would be a serious mistake,
# not a detail to fix later.
SECRETS = [
    r"AIza[A-Za-z0-9_-]{15,}",          # Google API key
    r"screenspan-[0-9a-f]{5}",          # Firebase project id
    r"firebasedatabase\.app",
    r"apps\.googleusercontent\.com",
    r"PLAY_SERVICE_ACCOUNT",
    r"storePassword|keyAlias|keyPassword",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
]

problems = []


def fail(page, text):
    problems.append(f"{page}: {text}")


def check_page(page):

    if not os.path.exists(page):
        fail(page, "the page does not exist")
        return

    s = open(page, encoding="utf-8").read()

    # -- the head of the page -------------------------------------------
    if "<meta charset" not in s:
        fail(page, "missing <meta charset>")

    if 'name="viewport"' not in s:
        fail(page, "missing <meta viewport>: it opens shrunk on a phone")

    if "<title>" not in s:
        fail(page, "missing <title>")

    # -- internal links ------------------------------------------------
    for href in sorted(set(re.findall(r'href="([^"#:]+\.(?:html|jpg|png|css|js))"', s))):
        if not os.path.exists(href):
            fail(page, f'the link "{href}" points at a file that does not exist')

    for src in sorted(set(re.findall(r'src="((?!data:|https?:)[^"]+)"', s))):
        if not os.path.exists(src):
            fail(page, f'the image "{src}" does not exist')

    # -- duplicate class attributes ------------------------------------
    for tag in re.findall(r"<[a-zA-Z][^>]*>", s):
        if tag.count("class=") > 1:
            fail(page, f"two class attributes on the same tag: {tag[:80]}")

    # -- the two languages must stay balanced --------------------------
    it = len(re.findall(r'data-lang="it"', s))
    en = len(re.findall(r'data-lang="en"', s))

    if it != en:
        fail(page, f"unbalanced translated blocks: it={it}, en={en}")

    # Every English block must start active: English is the default
    # language, and without "active" that piece stays invisible until the
    # JavaScript runs - i.e. forever, if it is disabled.
    for tag in re.findall(r'<[a-z]+[^>]*data-lang="en"[^>]*>', s):
        if "active" not in tag:
            fail(page, f"EN block that does not start active: {tag[:80]}")

    # -- secrets -------------------------------------------------------
    for pattern in SECRETS:
        found = re.search(pattern, s, re.IGNORECASE)
        if found:
            fail(page, f"possible secret in the text: {found.group(0)[:30]}")


# Italian accented vowels written with an apostrophe: "e'" instead of "è",
# "piu'" instead of "più". In this project's source comments that is the
# intended convention; in TEXT THE USER READS it is a spelling mistake,
# and the two are easy to confuse while working on the same files. Seven
# of them slipped through in a single change, including one inside the
# <meta description> - the text Google shows in its results - and a
# "c'e'" that a first, more naive version of this check did not see.
MISSING_ACCENTS = [
    "e", "piu", "gia", "perche", "cosi", "puo", "meta", "sara",
    "verra", "potra", "dovra", "citta", "qualita", "possibilita",
    "necessita", "cioe", "ventitre", "tre", "li", "ne", "si",
]


def check_accents(page, s):
    """Look for the apostrophe-instead-of-accent in visible text only."""

    # The Italian text of the translated blocks, plus the meta tags -
    # which show up in search results and link previews.
    #
    # IT CLOSES ON THE TAG NAME, not on the first "</" it meets: the
    # first version of this check stopped at a </strong> inside the
    # paragraph and never looked at the rest, where a "c'e'" was in fact
    # hiding.
    chunks = re.findall(
        r'<([a-z0-9]+)[^>]*data-lang="it"[^>]*>(.*?)</\1>', s, re.S)
    chunks = [text for _tag, text in chunks]
    chunks += re.findall(r'<meta name="description" content="([^"]*)"', s)

    words = "|".join(MISSING_ACCENTS)

    for chunk in chunks:
        # No lookbehind on a letter: this way the second half of "c'e'"
        # is seen too.
        # Case-insensitive: an "E'" at the start of a sentence is exactly
        # where the habit shows up, and the first version of this list
        # only looked at lowercase.
        for found in re.findall(r"(?<![A-Za-zÀ-ÿ])(" + words + r")'", chunk,
                                re.IGNORECASE):
            fail(page, f"accent written with an apostrophe in visible text: \"{found}'\"")


def links_to(doc, target):
    """True if `doc` contains a clickable markdown link to `target`.

    It looks for the LINK, not for the file name: a first version of this
    check searched for the plain string and passed happily, because the
    other language's file name also appears in the file listing at the
    bottom of the README - where it is not clickable and leads nowhere.
    """
    s = open(doc, encoding="utf-8").read()

    return f"]({target})" in s


# -- THE TWO ROADMAPS MUST NOT DIVERGE ---------------------------------
#
# The roadmap exists as two files, one per language, because the two
# buttons on the site lead to two different documents. Two copies of the
# same list diverge at the first cut made on one side only - and it has
# already happened in this repository: the summary section on the home
# page announced, among "the next three", an item just removed from the
# file.
#
# It is not the TEXT that gets compared, which is translated and so
# different by definition: it is the STRUCTURE. If an item is added,
# removed or moved to another section in one language only, the counts
# stop matching and CI notices.
ROADMAP_IT = "ROADMAP.it.md"
ROADMAP_EN = "ROADMAP.md"


def roadmap_structure(path):
    s = open(path, encoding="utf-8").read()

    return {
        "sections": len(re.findall(r"^## ", s, re.M)),
        "upcoming items": len(re.findall(r"^### \d+\. ", s, re.M)),
        "done items": len(re.findall(r"^- \[x\]", s, re.M)),
        "ongoing items": len(re.findall(r"^- \[ \]", s, re.M)),
    }


def check_roadmap():

    for path in (ROADMAP_IT, ROADMAP_EN):
        if not os.path.exists(path):
            fail(path, "the roadmap does not exist")
            return

    it = roadmap_structure(ROADMAP_IT)
    en = roadmap_structure(ROADMAP_EN)

    for key in it:
        if it[key] != en[key]:
            fail(ROADMAP_EN,
                 f"{key}: {it[key]} in Italian, {en[key]} in English"
                 " - an item was changed in one language only")

    # And they must point at each other: a translation you cannot reach
    # from the other one is a translation nobody will read.
    if not links_to(ROADMAP_IT, ROADMAP_EN):
        fail(ROADMAP_IT, f"does not link to {ROADMAP_EN}")

    if not links_to(ROADMAP_EN, ROADMAP_IT):
        fail(ROADMAP_EN, f"does not link to {ROADMAP_IT}")


# The same trap as the roadmap, one level up: the README is the first
# page a visitor sees, and it exists in two languages. English is the
# default one (README.md) because this repository is meant to be read
# from anywhere; the Italian one has to stay reachable from it, and the
# other way round.
README_IT = "README.it.md"
README_EN = "README.md"


def check_readme():

    for path in (README_IT, README_EN):
        if not os.path.exists(path):
            fail(path, "the README does not exist")
            return

    if not links_to(README_EN, README_IT):
        fail(README_EN, f"does not link to {README_IT}")

    if not links_to(README_IT, README_EN):
        fail(README_IT, f"does not link to {README_EN}")

    # Each README must point at the roadmap in its own language: linking
    # the other one sends the reader into a language they did not pick.
    if not links_to(README_IT, ROADMAP_IT):
        fail(README_IT, f"does not link to {ROADMAP_IT}")

    if not links_to(README_EN, ROADMAP_EN):
        fail(README_EN, f"does not link to {ROADMAP_EN}")


# Files that must exist and be listed: a document referenced by the
# README but absent from the repository is a 404 on the busiest page.
LINKED_DOCS = ["SECURITY.md", "CODE_OF_CONDUCT.md", "LICENSE"]


def check_markdown_links():
    """Relative links between the markdown documents must resolve."""

    docs = [README_EN, README_IT, ROADMAP_EN, ROADMAP_IT] + LINKED_DOCS

    for doc in docs:
        if not os.path.exists(doc):
            fail(doc, "the file does not exist")
            continue

        if not doc.endswith(".md"):
            continue

        s = open(doc, encoding="utf-8").read()

        for target in sorted(set(re.findall(r"\]\(([^)#:]+\.md)\)", s))):
            if not os.path.exists(target):
                fail(doc, f'the link "{target}" points at a file that does not exist')


# The demo video's id lives in three places: the player on the home page
# and the "watch the demo" link at the top of each README. Changing the
# video means changing all three, and nothing about a stale one looks
# broken - the old video simply keeps playing, which is the kind of
# mistake that survives for months.
VIDEO_HOLDERS = ["index.html", README_EN, README_IT]


def check_video():

    found = {}

    for f in VIDEO_HOLDERS:
        if not os.path.exists(f):
            continue

        ids = set(re.findall(r"(?:youtu\.be/|youtube-nocookie\.com/embed/)([A-Za-z0-9_-]{11})",
                             open(f, encoding="utf-8").read()))

        if not ids:
            fail(f, "no demo video link found")
        else:
            found[f] = ids

    everything = set().union(*found.values()) if found else set()

    if len(everything) > 1:
        for f, ids in sorted(found.items()):
            fail(f, f"demo video id {sorted(ids)} - the three copies disagree:"
                    f" {sorted(everything)}")


def check_sharing():
    """The sharing meta tags, only visible when the link is pasted."""

    s = open("index.html", encoding="utf-8").read()

    for prop in ["og:title", "og:description", "og:image", "og:url"]:
        if f'property="{prop}"' not in s:
            fail("index.html", f"missing the {prop} meta tag")

    m = re.search(r'property="og:image" content="([^"]+)"', s)

    if m:
        name = m.group(1).rsplit("/", 1)[-1]

        if not os.path.exists(name):
            fail("index.html", f"og:image points at {name}, which is not in the repository")


def main():

    if not os.path.exists("index.html"):
        print("Run this from the repository root.", file=sys.stderr)
        return 1

    for page in PAGES:
        check_page(page)

        if os.path.exists(page):
            check_accents(page, open(page, encoding="utf-8").read())

    check_sharing()
    check_roadmap()
    check_readme()
    check_video()
    check_markdown_links()

    if problems:
        print(f"\n{len(problems)} problems:\n")
        for p in problems:
            print(f"  ✗ {p}")
        print()
        return 1

    print(f"✓ {len(PAGES)} pages checked, everything in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
