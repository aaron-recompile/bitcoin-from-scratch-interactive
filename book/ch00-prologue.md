# Prologue · Borrowed Bricks, an Original House

## Start by clearing up a misconception

Satoshi Nakamoto was not trying to invent a currency. He was trying to solve a problem,
and the currency is what the solution turned out to look like.

The problem was this:

> **How do a group of strangers, who don't trust each other and have no central authority,
> agree on who owns what?**

A signature can prove "I authorized this payment." It cannot stop me from spending the same
coin twice. And preventing *that* appears to **require a center** — someone watching the ledger,
a bank.

This book is about removing that center. Not reading about it — **removing it yourself, in code.**

---

## Six people, six bricks

Before you write a line, look carefully at one thing: **most of the parts you are about to
build were not invented by Satoshi.**

| Year | Who | What they contributed | Where you'll build it |
|---|---|---|---|
| 1976–77 | Diffie, Hellman, Rivest–Shamir–Adleman | **Public-key cryptography and digital signatures** | Chapters 2–3 |
| 1982 | David Chaum | **Digital cash** (DigiCash / eCash) — but it needed a central bank to stop double-spends | — (this is the target he had to beat) |
| 1991 | Haber & Stornetta | **The hash time-stamp chain** — hashes linked head to tail | Chapter 4 |
| 1997 | Adam Back | **Proof-of-work** (Hashcash), invented to fight email spam | Chapter 5 |
| 1998 | Wei Dai (b-money) | The idea that **a group could keep a ledger together, voting with computation** | Chapters 6–7 |
| 1998–2005 | Nick Szabo (Bitgold) | **Proof-of-work + a chained structure + decentralization** — nearly Bitcoin's direct ancestor | Chapters 6–8 |

Three things in that table deserve a pause.

**Haber and Stornetta are the most underrated entry.** They invented their chain for a boring
reason: to time-stamp documents so nobody could backdate them. Change anything early, and
everything after it breaks. That is where the "chain" in blockchain comes from — and Satoshi
cites them more than anyone else in the whitepaper.

**Adam Back is the first citation in the whitepaper.** He built proof-of-work as *postage* —
a stamp that costs almost nothing to send one email and ruins you at a million. Satoshi
repurposed it into something entirely different: **a way to decide who gets to write the next
page of the ledger.**

**Dai and Szabo stopped at the paper.** Both had the right direction. Neither shipped a
running system. Satoshi's real difference is that two months after publishing, **the network
was live.**

So what did he actually invent?

> **Using economic incentives and a most-work rule, he got strangers with no central authority
> to converge on the same ledger.**

Rewriting history means redoing the network's proof-of-work — expensive enough not to be worth
it. Meanwhile honest mining pays. **Security does not come from people being good; it comes
from cheating being a bad deal.**

Cryptography was his brick supply. Building a bank with no manager out of those bricks
was the invention.

---

## The whitepaper is mostly not cryptography

This is the book's thesis, and it is also why the book is shaped the way it is.

Lay out what is actually *in* the whitepaper, and label each piece by field:

| In the whitepaper | What it is | Field |
|---|---|---|
| The double-spend problem | Why the whole system needs to exist | **Systems** |
| Blockchain structure | Transactions batched into blocks, each committing to the previous | **Systems** |
| Mining (proof-of-work) | Find a nonce so the block hash is below a target | **Systems** |
| Longest-chain consensus | "The chain with the most work is the truth" | **Consensus + game theory** |
| Economic incentives | Block reward, halving, the 21-million cap | **Economics** |
| UTXOs and Script | Money is a pile of unspent outputs, each with a spending condition | **Systems** |
| Digital signatures | Proving a payment was authorized | Cryptography |
| Merkle trees | Verifying transactions efficiently | Cryptography |

Look at the right-hand column. Most of it says **systems, consensus, economics**.

So the book is shaped like this: **chapters 1–3 fire the bricks; from chapter 4 on, you are
building the house.**

Only two later chapters detour back into cryptography — chapter 11 (Merkle trees) and
chapter 13 (the real curve). The remaining thirteen are systems, consensus, game theory,
and economics.

**That ratio is not my editorial choice. It is the whitepaper's own ratio.**

---

## Why he published a *paper*

In October 2008 Satoshi posted a nine-page document to a cryptography mailing list.
**Not to a journal.**

That decision is worth understanding, because it rhymes with the technology you are about to learn.

- It follows the cypherpunk tradition: publish the idea, let the harshest readers attack it.
  If it survives, it counts.
- **He was anonymous, so he had no reputation to lend.** He could not say "trust me, I'm
  someone." He could only say: "here is the design — **check it yourself**."

**Public verification, private key never revealed.** That is how a signature works, and it is
also how he made his argument. An anonymous person can only replace "believe who I am"
with "anyone can check this."

In the genesis block he embedded a headline from *The Times*, 3 January 2009:
**"Chancellor on brink of second bailout for banks."** That is the clearest surviving clue
about motive. In the wreckage of 2008 he wanted money that did not depend on a bank,
could not be printed at will, and required trusting no intermediary.

---

## How to read this book

**One small step at a time; intuition before detail.** Every chapter runs in the same order:
pin the new idea to a picture you already have, write the code, run it, read the output field
by field, then count how many lines were cryptography and how many were something else.

**Everything is written by hand.** The single exception is `hashlib` — the internals of SHA-256
are another book's subject. This book cares about what you can build once you have it.
Elliptic curves, signatures, ledgers, consensus: all of it is a few dozen lines of your own Python.

**Do not skip chapters.** Later code reuses earlier functions directly. The `sign`/`verify`
from chapter 3, the chain from chapter 4, the miner from chapter 5 — from chapter 6 onward
they get picked up and used as tools.

**Some errors are the lesson.** A few places deliberately walk you into an exception
(the corrupted hex in chapter 1, for instance). That is not a bug; it is the point of the section.

**"YOUR TURN" means your turn.** Those blocks are not homework. They are the conclusion of
the section, and you will not really believe them until you've typed them yourself.

---

## Where you end up

By the end of chapter 17 you will have a chain running across several Docker containers.
Each one keeps its own mempool, mines on its own, broadcasts blocks, and independently
verifies everyone else's work. None of them trusts any other. **They converge on the same
ledger anyway.**

You will have written every line of it, starting from a single byte.

The bricks are borrowed and the house is original — and this time, you're the one who built it.
