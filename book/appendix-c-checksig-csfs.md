# Appendix C · CHECKSIG vs CSFS: Same Lamp, Different Piece of Paper

In chapter 14 you wrote an `OP_CHECKSIG`. It looked like this:

```text
elif item == "OP_CHECKSIG":
    pub = stack.pop()
    sig = stack.pop()
    stack.append(verify(pub, msg, sig))
```

Notice the `msg` — **it comes in as a function parameter, not off the stack.**

At the time that was an implementation detail. **This appendix explains that it is one of
Bitcoin's most consequential restrictions, and why some people want to change it.**

---

## C.1 A signature has always been "stamping a specific piece of text"

Signing was never only about payments. What it actually is:

> **Use a seal (private key) to stamp one specified piece of text, so that anyone can check it
> with a lamp (public key).**

Ordinary life is full of it: a teacher marking **this essay** as reviewed, you initialling
**this contract**, Apple signing **this installer**, you signing **this email**.

**The text being stamped varies. The action is identical**: stamp with the seal, check with the
lamp, change one character and the stamp is void.

---

## C.2 Signing a transaction vs signing a message

| | Signing a transaction | Signing a message |
|---|---|---|
| The text being stamped is | **this transaction** (who, how much…) | **any text at all** (a price, "I agree", a number…) |
| Who **chooses** that text | **The protocol fixes it**: spending must sign this transaction | **You choose freely**: put up whatever you want |

**The action is the same. The only difference is who decides what gets stamped.**

That one sentence is the entire difference between the two opcodes below.

---

## C.3 Two lamps

Bitcoin script has two signature-checking opcodes. **Both are lamps.** They differ in
**which piece of paper** the stamp is on.

### OP_CHECKSIG: a lamp welded in place

**It only recognizes a stamp made on this transaction.**

The message being signed **is** the transaction, hard-wired, and a script author cannot point it
somewhere else.

That is what chapter 14's line means: `msg` is computed by the VM's caller (the node) from the
current transaction, and **the script has no influence over it.**

So it exists to serve **spending**: proving "I authorize this specific transaction."

### OP_CHECKSIGFROMSTACK (CSFS): a lamp you can aim

**Put any text on the stack and it checks whether the signature was made over that text.**

Written in chapter 14's code, the difference is one line:

```text
# CHECKSIG (today)
pub = stack.pop()
sig = stack.pop()
stack.append(verify(pub, msg, sig))          # msg comes from the protocol; the script can't touch it

# CSFS (proposed)
pub = stack.pop()
msg = stack.pop()                             # <- msg comes off the stack too
sig = stack.pop()
stack.append(verify(pub, msg, sig))
```

**One extra `msg = stack.pop()`.**

That is the whole difference. The signed message is now **chosen freely by the script** — a
price, a quote, another transaction, a promise.

> **CHECKSIG: the lamp is welded, and only shines on this transaction.**
> **CSFS: whatever you put in front of it, it shines on.**

---

## C.4 Why this matters

CSFS promotes a signature from "**can only endorse this transaction**" to
"**can endorse any statement**," which turns signatures into a **general-purpose building block**:

### ① Bringing in external facts

An oracle stamps the sentence "BTC = 100,000" and a script checks it with CSFS —
**pulling an off-chain fact onto the chain.**

Section 18.4 said scripts must not read the outside world, because nodes would compute different
results. CSFS sidesteps this: **it does not read the outside world; it verifies a signature
about the outside world.** That signature is part of the transaction data, identical for every
node, so **determinism is untouched.**

That distinction is subtle, and it is the crux.

### ② Signatures become quotable and reusable

Because it signs **an independent statement** rather than a particular transaction,
the same signature can be referenced elsewhere.

### ③ Assembling covenants

Let a script check that "a certain promised statement was properly signed," without depending on
the transaction itself. Combine that with an opcode that can assemble messages
(`OP_CAT`, section 18.6) and you can constrain **how the money is allowed to move next.**

**That is what the word "covenant" means here**: not merely *who* may spend, but
**where it may go.**

---

## C.5 One sentence, and one note of restraint

> **CHECKSIG is a lamp that only reads this cheque. CSFS is a lamp that reads any paper.**
>
> Precisely because it is general, a signature stops being only a spending authorization and
> becomes an endorsement of **any statement** — which is the root of everything more complex
> that could be built on top.

But keep chapter 18 open beside this.

**Every new opcode is a new expressive power in this language.** And every limit in chapter 18
exists to remind you that expressive power is a natural enemy of validation cost,
determinism, and **the ability of ordinary people to run a full node.**

CSFS, CTV, CAT and the rest have been debated in the Bitcoin community for years, and
**the argument has never been "is this useful." It is "is it worth the cost."**

That is not a technical question. It is chapter 9's question: **with nobody in charge,
how do the rules ever change?**

---

*Following this road any further leaves the scope of this book. But you are now equipped to
read those proposals yourself: chapter 14 told you what a script is, chapter 18 told you why
restraint is necessary, and this appendix told you where the argument actually is.*
