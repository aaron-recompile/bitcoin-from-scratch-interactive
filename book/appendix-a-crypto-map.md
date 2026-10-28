# Appendix A · The Cryptography Map: Roads This Book Does Not Take

Across eighteen chapters this book used exactly three cryptographic objects:
**hashes, key pairs, and signatures.**

That is not because cryptography contains only three things. It is because
**Bitcoin needs only three.**

This appendix lays out the whole map so you know where you are standing and where the
neighbouring roads go. No code; about ten minutes.

---

## A.1 Encryption: the one primitive this book skipped

**Encryption is "you can get back" — because you kept a secret.**

You need to send an order to the front line: `ATTACK`. The messenger might be captured.
So the general and the front line **agree on a number in advance** — say 3. Before sending,
shift every letter forward by three: A→D, T→W. `ATTACK` becomes `DWWDFN`.

The enemy intercepts `DWWDFN` and learns nothing. The front line knows the number is 3,
shifts back, and reads `ATTACK`.

That is encryption: **one agreed secret both locks the message and opens it.**

(This is a Caesar cipher, and it is of course not secure — twenty-six possibilities, break it
by hand. But the structure — *use a shared secret to transform content and transform it back* —
is the same as any modern cipher.)

### How it differs from hashing

| | Hash | Encryption |
|---|---|---|
| Can you get back? | **No** | **Yes** |
| Mapping | Many-to-one (information destroyed) | One-to-one (information preserved) |
| Is there a key? | No inverse operation exists | There is a key |

Section 1.1 covered this; one addition here: **encryption is inherently paired** —
there is a lock and there is an opening. An "encryption" nobody can reverse is useless,
because your own side cannot read it either.

### Why this book does not need it

**Because Bitcoin barely uses encryption.**

On-chain transactions are **public**: anyone can see how much moved and to whom.
Bitcoin protects "**only I can spend my money**," not "nobody can read this."

So the thing it uses every day is **signing**, not encrypting. Both use the same key pair,
running in opposite directions (the table in section 2.5).

> **This is one of the book's quieter conclusions: a system worth a trillion dollars can be
> built without encryption at all.**

---

## A.2 Zero-knowledge proofs: proving it's true without saying why

**In one line: you end up convinced, and you received no secret.**

### Ali Baba's cave

Picture a **ring-shaped** cave. Just inside, the path splits left and right. Deep at the back
the two branches are blocked by a **magic door** that opens only for the right password,
letting you pass from one side to the other.

Ali Baba says he **knows the password** but **absolutely will not say it.** How can he convince
you without telling you?

Play a **three-step** game — **and these three steps are the skeleton of every zero-knowledge
proof:**

1. **Commit (lock in a choice)** — Ali Baba enters and **picks** left or right, walking to the
   door. Once chosen he cannot change — and **from the entrance you cannot see which he took.**
2. **Challenge (you make it hard)** — you **shout** a direction: "come out on the **right**!"
   You chose at random just now, so he could not have prepared.
3. **Respond (he delivers)** — if he **really knows the password**, then whichever side he
   entered, he can pass the door and emerge on the side you named.

**And if he doesn't know it?** He only makes it if he **guessed right** — a fifty-fifty chance.

**Which is why the game must be repeated.** One round and a fraud has even odds, so it means
nothing. But each extra round he must guess right **again** — two rounds is 1/4, three is 1/8,
ten is about one in a thousand. Twenty rounds of emerging from whichever side you name at random
and **you are effectively certain.**

**And you never heard a syllable of the password.**

### Why the "commit" step is essential

Because if Ali Baba could **hear your shout first** and then choose a side, he'd succeed every
time without knowing anything.

He must lock in his choice **before you shout.** **That is precisely what section 1.2's
commitment is for.**

But it differs from the guessing game in one way: that commitment **is opened publicly at the
end**; the cave's commitment **is never opened** — he locked in "left or right," and that choice
is **never revealed.** You only ever see him come out where you asked.

> **Zero-knowledge = committed but never opened; no hash to publish; and certainly no encryption.**

### One line: how much do you end up knowing?

| | Encryption | Commitment | Zero-knowledge |
|---|---|---|---|
| You end up with | **the content** | content you can check afterwards | **only true/false** |
| Endpoint | you **know** the secret | you **checked** the secret | you **never touched** the secret |
| In a phrase | move the content to you | lock first, reveal later | no content at all, just conviction |

**The further right you go, the less you need to know — which is the "zero" in zero-knowledge:
the knowledge you receive is zero, the certainty is total.**

(Bitcoin's main chain does not use zero-knowledge proofs. But they turn up nearby: several
sidechains and L2s use them for privacy and compression, and schemes like BitVM try to use
Bitcoin's existing script to verify proofs about external computation. This is an active frontier.)

---

## A.3 Secure multi-party computation: compute together, reveal nothing

**Andrew Yao, 1982, the Millionaires' Problem:**

Two millionaires want to know **who is richer**, and **neither will say how much they have.**
Can you compute just the comparison without leaking the numbers?

That question opened an entire field: **secure multi-party computation (MPC).**

### It needs a new brick: computable encryption

**Homomorphic encryption.** Ordinary encryption locks things away; to compute on them you must
first unlock.

"Computable encryption" **lets you compute while everything stays locked**: lock 5 in one box
and 3 in another, add the two locked boxes without opening them, and get a locked 8.
Anyone who opens it sees 8, and **nobody ever saw the 5 or the 3.**

### It is zero-knowledge's sibling, with a different job

| | Zero-knowledge proof | Multi-party computation |
|---|---|---|
| How many people hold secrets | **One** | **Several**, each with their own |
| What is wanted | prove **a statement is true** | **jointly compute** a result |
| In a phrase | I prove, you believe | we compute together, nobody shows their hand |

(MPC does have real Bitcoin applications: **threshold signatures**, where a private key is split
across several parties and enough of them must cooperate to sign, while **the complete key never
exists on any single machine.** Several institutional custody products work this way.)

---

## A.4 The whole map

Cryptography is **layered**. Grasp these three layers and everything else has somewhere to hang.

| Layer | Contains | Note |
|---|---|---|
| **Base primitive** | Hashing | A one-way fingerprint — neither encryption nor commitment |
| **Tools (uses)** | Encryption / commitment / signatures | Commitments are usually built from hashes |
| **Advanced primitive** | Homomorphic encryption | Computable while locked |
| **Machines (protocols)** | Zero-knowledge proofs / MPC | Assembled from the pieces above |

| Thing | In a phrase | Analogy | Core property |
|---|---|---|---|
| Hash | one-way fingerprint | blender / fingerprint | irreversible |
| Encryption | hide it for a specific reader | battlefield cipher | secret, reversible |
| Commitment | lock now, reveal later | a sealed envelope | binding |
| Symmetric key | both sides share one secret | a shared cipher | shared secret |
| Key pair | one hidden, one public | piggy bank / curve hopping | trapdoor one-way |
| Signature | stamp anyone can check, seal stays home | signet ring + lamp | public verification, no leak |
| Zero-knowledge | prove it's true without saying why | Ali Baba's cave | verifiable, zero leakage |
| MPC | compute together, reveal nothing | compare without stating | joint result, private inputs |

---

## A.5 Three cuts through the three most-confused items

Put **hashing**, **public-key encryption** and **public-key signing** side by side, and
separate them with three questions:

| | Hash | Key pair · encryption | Key pair · signing |
|---|---|---|---|
| Easy forwards, hard backwards? | Yes | Yes | Yes |
| Is there a reversible "decrypt"? | **No** | **Yes** (public locks, private opens) | Related but not secret (private signs, public verifies) |
| How do you "open" or verify it? | **You publish the original** and re-check | **Private key decrypts** | **Public key verifies** (private key never appears) |

**Three things to remember:**

**① "Easy forwards, hard backwards" is the shared floor of hashing and key pairs.**
Hashing is easy to compute and hard to invert; a private key easily yields a public key and
the reverse is infeasible. Same magic.

**② A hash is not encryption.** It has no key and no decryption step. The only way to
"open" it is for **you to publish the original**, which is not an algorithm doing anything.

**③ The fact that a hash "must be published" is sometimes a weakness and sometimes a weapon:**

| Context | Which | Chapter |
|---|---|---|
| Used as an identity or signature | **Weakness** (single-use — which is what forced real signatures) | Section 3.0 |
| Used as a commitment | **Weapon** (reveal only when the time comes) | Section 1.2 |
| Used as a Merkle tree | **Weapon** (one root commits to a whole block) | Section 11.5 |
| Facing a quantum computer | **Weapon** (structureless, so there is no shortcut) | Appendix B |

**One property, four contexts, both signs.**

This is the single most transferable habit in the book:
**a technical property is neither good nor bad on its own. It becomes one or the other
depending on where you put it.**
