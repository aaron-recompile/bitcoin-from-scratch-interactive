---
title: Bitcoin from Scratch
subtitle: Build your own Bitcoin chain
---

Eighteen chapters. No libraries. From a single byte to a network running across several machines.

Everything uses only the Python standard library. No Bitcoin libraries, no black-box APIs,
no "just copy this for now, you'll understand later." Every term you've heard (hash, public key,
signature, block, mining, consensus, UTXO, Merkle tree, Script) becomes code you wrote yourself
*before* it is allowed to carry that name.

:::{tip} Every code cell on this site runs in your browser
Press the **power** button at the top of a chapter, then run cells in order.
Python runs locally in the page; nothing is installed and nothing is sent anywhere.
See [](./running-the-code.md).
:::

## This book argues one thing

> **The genuinely original part of Bitcoin is not the cryptography. It is everything else.**

Satoshi's building blocks were almost all borrowed: digital signatures
(Diffie–Hellman / RSA, 1976–77), proof-of-work (Adam Back, 1997), hash time-stamp chains
(Haber–Stornetta, 1991), the *idea* of a decentralized ledger (Wei Dai / Nick Szabo, 1998),
and the first serious attempt at digital cash (David Chaum, 1982).

What he invented was **how to build a bank with no manager out of those bricks**.

That claim is easy to say and hard to prove, so this book **counts it**. Every chapter ends
with a ledger: of the code you just wrote, which lines are cryptography, and which are systems
design, consensus, game theory, or economics. By chapter 18 the tally speaks for itself.

The bricks are borrowed. The house is original.

**Start here: [Prologue: Borrowed Bricks, an Original House](./book/ch00-prologue.md)**

## Contents

### Part I · Bricks: the cryptographic floor

| Ch | Title | What you build by hand |
|---|---|---|
| [1](./book/ch01-bytes-hash-commitment.ipynb) | Bytes, Hashes, Commitments | `sha256()`, and `commit()` / `verify()`: a guessing game nobody can cheat |
| [2](./book/ch02-finite-field-ecc-pubkey.ipynb) | Finite Fields, Elliptic Curves, Public Keys | Hop around a curve mod 97, derive a public key, then brute-force it back |
| [3](./book/ch03-signatures-ecdsa.ipynb) | Digital Signatures | Real ECDSA, then count how many times `priv` appears inside `verify` |

### Part II · Retracing the ancestors

| Ch | Title | What you build by hand |
|---|---|---|
| [4](./book/ch04-hash-chain.ipynb) | The Hash Time-Stamp Chain | Haber–Stornetta's chain; edit one old block and watch everything after it break |
| [5](./book/ch05-proof-of-work.ipynb) | Proof-of-Work | Hashcash-style mining, and a lesson about luck that most books skip |

### Part III · The house: building a chain

| Ch | Title | What you build by hand |
|---|---|---|
| [6](./book/ch06-transactions-doublespend.ipynb) | Transactions and Double-Spending | A UTXO ledger, and your first problem cryptography cannot solve |
| [7](./book/ch07-blocks-consensus.ipynb) | Blocks and Longest-Chain Consensus | The rule that settles double-spends: **this chapter contains zero cryptography** |
| [8](./book/ch08-incentives-issuance.ipynb) | Incentives and Issuance | Block rewards, halving, 21 million: making the machine run itself |
| [9](./book/ch09-forks-upgrades.ipynb) | Forks and Upgrades | Changing the rules with nobody in charge |

### Part IV · Surviving the long run

| Ch | Title | What you build by hand |
|---|---|---|
| [10](./book/ch10-fees-difficulty.ipynb) | Fees and Difficulty Adjustment | Two negative-feedback loops that keep the system steady |
| [11](./book/ch11-merkle-tree.ipynb) | Merkle Trees and Efficient Verification | Prove a transaction is in a block without downloading the block |
| [12](./book/ch12-mempool-fees-confirmations.ipynb) | Mempool, Fee Market, Confirmations | RBF, CPFP, reorgs: why your transaction is stuck |
| [13](./book/ch13-secp256k1.ipynb) | Switching to the Real Curve | Swap the toy curve for the one Bitcoin actually uses |

### Part V · Toward real engineering

| Ch | Title | What you build by hand |
|---|---|---|
| [14](./book/ch14-script-vm.ipynb) | The Script VM | Spending conditions are not a database field; they are a running program |
| [15](./book/ch15-wallet-hd-keys.ipynb) | Wallets and HD Key Trees | How twelve words grow a thousand addresses |
| [16](./book/ch16-hardware-signer.ipynb) | Hardware Signing | Why the private key lives in a room with no network cable |
| [17](./book/ch17-docker-network.md) | A Multi-Node Network | Run your chain across several machines and watch them converge |
| [18](./book/ch18-script-safety-limits.ipynb) | Why Script Is Deliberately Weak | How loops, global state, and one bad opcode could kill every node |

### Appendices

| | |
|---|---|
| [A](./book/appendix-a-crypto-map.md) | The cryptography map: roads this book does not take (encryption, zero-knowledge proofs, MPC) |
| [B](./book/appendix-b-quantum.md) | Why a quantum computer breaks public keys but not hashes |
| [C](./book/appendix-c-checksig-csfs.md) | CHECKSIG vs CSFS: same lamp, different piece of paper |

## One thread

bytes → hash → commitment → finite field → elliptic curve → public key → signature →
chain → mining → transactions → consensus → incentives → upgrade coordination →
efficient verification → the real curve → mempool and confirmations →
Script → wallets → hardware signing → a real network → the limits of the script engine

Later chapters reuse functions you wrote in earlier ones. **Read in order.**

## Other ways to read it

- **PDF / EPUB**: [Leanpub](https://leanpub.com/bitcoin-from-scratch). Buying a copy is the best way to support the book.
- **Code only**: [bitcoin-from-scratch-code](https://github.com/aaron-recompile/bitcoin-from-scratch-code) on GitHub.

:::{warning} Teaching code, not wallet code
Tiny curves, predictable nonces, and simplifications made so the mechanism is visible.
**Never use it with real money.** Chapter 13 explains what still stands between this code and
something safe, and most of it has nothing to do with mathematics.
:::
