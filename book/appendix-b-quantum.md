# Appendix B · Why a Quantum Computer Breaks Public Keys but Not Hashes

Chapters 2 and 13 kept saying: **there is no shortcut from a public key back to a private key;
you can only try every possibility.**

That statement carried an unstated qualifier: **no shortcut for a classical computer.**

This appendix is about the exception.

---

## B.1 Three misconceptions to clear first

### ① It is a physical machine, not a program

A quantum computer is **hardware**, just like the one on your desk, built from different parts.
The key-breaking algorithm — **Shor's algorithm** — is **software running on that machine**,
and only a quantum machine can run it.

### ② Its components can be "0 and 1 at once"

A classical bit is 0 or 1, like **a coin lying flat on a table** — heads or tails.

A qubit can be in a **superposition** of 0 and 1, like **a coin still spinning** — a bit of both.
Many spinning coins can hold many possibilities **superposed and computed at once.**

### ③ It is not "a faster computer"

For games, video, or addition it is **not fast at all — it is slower and vastly more fragile.**
**It has magic only for a very small set of problems.**

That is worth contrasting with a mining rig, because the two "speeds" come from opposite places:

| | Mining rig | Quantum computer |
|---|---|---|
| Where the speed comes from | **brute strength** | **a clever route** |
| How | copy the same circuit tens of thousands of times and grind | superposition and interference: wrong answers cancel, right answers amplify |
| Still trying one at a time? | **Yes**, just with more hands | **No** — it sidesteps trying-one-at-a-time entirely |

> **A mining rig is ten thousand people brute-forcing in parallel.
> A quantum computer is one person who found a way not to brute-force.**

---

## B.2 What lets it break a key pair

Return to chapter 2's picture: **the private key is a number of hops; the public key is where
you land.**

A classical computer — even ten thousand mining rigs — can only go "1 hop, 2 hops, 3 hops…"
and against 2²⁵⁶ positions that runs until the end of time.

**But the track has a structure a classical algorithm cannot exploit: it has a rhythm, and it
repeats.**

The points on an elliptic curve form a cyclic group — hop `n` times and you return to the start
(you verified `n·G = None` in section 13.3). That **periodicity** is a necessary consequence of
the group structure. Classical algorithms cannot use it. **A quantum algorithm can.**

Finding a **hidden period** is precisely what quantum computers are best at. Rather than trying
values one by one, it puts all of them in superposition and lets them **interfere**,
**shaking the hidden period out directly.**

Once you know the period, recovering the private key drops from "run forever"
to "a handful of steps."

> **A classical computer breaking a key is groping in the dark, one guess at a time.
> A quantum computer doesn't guess — it hears the rhythm of the lock turning and
> cuts the key to match.**

**A wall no amount of brute force could climb gets walked around by a side path.**

---

## B.3 So why are hashes safe?

A hash **has no rhythm to hear.** It is just **mess** — no period, no algebraic structure.

The quantum trick of finding periods **has nothing to grip**, so it falls back to brute force.
And at brute force it is only mildly better than a classical machine
(Grover's algorithm, roughly a square-root speedup) —

**which you cancel out by doubling the length of the fingerprint.**

| | Key pairs (elliptic curves) | Hash-based signatures (Lamport family) |
|---|---|---|
| What's inside | **structure and rhythm** | structureless mess |
| Can quantum break it? | **Yes** (find the period, take the shortcut) | **No** (no shortcut to find) |
| The fix | **new mathematics required** | **double the fingerprint length** |

**Notice what just happened:**

A hash's "mess" is exactly why you cannot invert it and must publish the original to verify
(section 3.0's weakness); **and it is exactly why a quantum computer finds no rhythm
(this section's protection).**

**The same property, once a liability and once a lifeline.**

---

## B.4 Can you build signatures out of hashes?

Yes. That road was walked long ago: **Lamport signatures** (1979).

Section 3.0 hit a wall: use a hash as an identity and **the secret burns on first use.**

Lamport's fix is plain: **if a secret can only be used once, prepare several and reveal a
selected subset according to what you're signing.**

Signing a single bit (answering one yes/no question) looks like this:

```text
1. Make keys: secretly hold two secrets -- one for "0", one for "1".
             Publish both of their hashes as the public key.
2. Sign     : to sign 0, reveal only the secret for "0"; keep the other hidden.
3. Verify   : anyone hashes the revealed secret and checks it against that slot.
```

**Forging the other answer is impossible** — you never revealed that secret, and it cannot be
recovered from the hash.

Signing a full message means preparing a pair of secrets for each bit (256 bits, 256 pairs),
**and then using a Merkle tree to bundle many signatures together**, turning a one-time scheme
into one you can use repeatedly.

> **Spot the Merkle tree?** That is chapter 11's construction, doing a completely different job
> here — compressing a pile of one-time public keys into one short published commitment.

The cost of this road is **large signatures** (kilobytes rather than ECDSA's 71 bytes),
which is why nobody wants to use it — **until the quantum threat gets close enough.**

---

## B.5 How close is it, really?

**Not very.**

That spinning coin is extraordinarily delicate — heat it or shake it and it collapses into an
ordinary heads-or-tails (this is **decoherence**). Today's quantum computers need to be cooled
near absolute zero and heavily shielded, and the number of stably operable qubits is
**orders of magnitude** short of what breaking secp256k1 would require.

**But the threat is real**, and Bitcoin has one timing quirk that matters:

> **A quantum attacker can read public keys straight off the chain — but only where the public
> key has already been exposed.**

Recall P2PKH from section 14.4: **the address commits to a hash of the public key, and the key
itself only appears when you spend.**

So:

| Address state | Visible on chain | Quantum risk |
|---|---|---|
| Only ever received, **never spent from** | just a hash of the key | **Low** (you'd have to break the hash first) |
| **Already spent from once** | the full public key | **High** (the private key can be computed) |

**This is the second reason not to reuse addresses** — section 2.0 gave the privacy reason;
this adds a layer of quantum buffer.

(There is also a batch of very early **P2PK** addresses where the public key sits in plain sight
on the chain, including the coins Satoshi mined. Those are the first to be exposed.)

**The Bitcoin community is already discussing how a post-quantum signature scheme could be
soft-forked in.** This is a genuine engineering problem on a real clock, not science fiction.

---

## B.6 Three sentences

1. **A quantum computer holds many possibilities at once and uses wave interference to amplify
   the right answer.**
2. **Key pairs hide a repeating rhythm, and finding rhythms is a quantum computer's specialty →
   breakable.**
3. **Hashes are structureless mess with no rhythm to find → not breakable this way.**

*(Every analogy here serves intuition. The actual quantum mechanics is more precise, and
more beautiful.)*
