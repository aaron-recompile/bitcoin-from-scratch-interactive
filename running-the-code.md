---
title: Running the Code
---

Every line of code in this book is on the page, in the order you need it, with the output it
printed when the site was built. You can read straight through without running anything.

But the book is meant to be poked at. Change a difficulty, flip one byte of a block, break a
signature on purpose, and see what happens.

## In your browser (nothing to install)

1. Open a chapter and press the **power** button in the top bar. The first time takes a few
   seconds while Python loads into the page.
2. Each code cell gets a **run** button. Run them **in order**: later cells reuse names defined
   earlier in the chapter.
3. Edit any cell and run it again. Reload the page to get the original back.

Python runs inside your browser tab ([Pyodide](https://pyodide.org)). Nothing is installed and
nothing is sent to a server. Every chapter works this way except chapter 17, which starts
several networked processes and needs a real machine.

## On your own machine

The same code, without the prose, is in
[bitcoin-from-scratch-code](https://github.com/aaron-recompile/bitcoin-from-scratch-code):

```bash
git clone https://github.com/aaron-recompile/bitcoin-from-scratch-code.git
cd bitcoin-from-scratch-code
pip install notebook
jupyter notebook
```

Or download any chapter of this site as a notebook from the download menu on its page.

## What you need

**Python 3.** That is the whole list.

No Bitcoin libraries are used anywhere in this book. The only import outside the standard
library appears in one optional cell in chapter 13, which cross-checks your hand-written public
key against the `ecdsa` package, and the chapter works fine without it.

Chapter 17 optionally uses Docker to run several nodes at once. Without Docker, open five
terminals instead; the code is ordinary Python and behaves identically.

## A warning worth repeating

This is a **teaching implementation**: tiny curves, predictable nonces, and simplifications
made so that the mechanism stays visible.

**Never use it with real money.**
