# Chapter 17 · A Multi-Node Network

> **Part V · Toward real engineering**
> Sixteen chapters described mechanisms. This one puts them on separate machines.

Every line of code so far has run inside **one Python process**.

`chain` is a list, `mempool` is a list, and `choose()` compares two chains directly.
**Everything shares one block of memory, and everything can see everything.**

**Real Bitcoin is nothing like that.**

On a real network each node is an independent machine that learns about the others only
through messages, and those messages arrive late, out of order, or not at all. Chapter 7's line —

> **A shared ledger is not the starting point. It is the result of convergence.**

— is invisible inside a single process. This chapter makes you **watch it happen**.

---

:::{note} This chapter runs outside the browser
Every other chapter runs right here on the page. This one starts several
processes that talk to each other over HTTP, so it needs a real machine.
The code is in [`toycoin_network/`](https://github.com/aaron-recompile/bitcoin-from-scratch-code/tree/main/toycoin_network).
:::

## 17.1 This chapter is a project, not a snippet

```text
toycoin_network/
  node.py            a full node: mempool, tx and block validation, relaying
  miner.py           a miner: picks transactions by fee rate, mines
  wallet.py          a wallet: builds and broadcasts transactions
  Dockerfile
  docker-compose.yml starts 3 nodes and 2 miners
```

Under three hundred lines, with no third-party dependencies — `node.py` uses nothing but
Python's standard `http.server` and `urllib`.

**Docker plays the part of "several computers"**: each container is a separate process with
its own memory, its own mempool, its own chain. They can only shout at each other over HTTP.

The cast:

```text
node1, node2, node3: full nodes. Accept transactions, keep a mempool, validate and relay blocks.
miner1, miner2     : miners. Pull from a node's mempool, mine, submit the block back.
wallet.py          : a wallet. Broadcasts a transaction to one node.
```

**This is the assembly of the previous sixteen chapters:**

```text
wallet broadcasts -> node accepts into mempool -> miner picks by fee -> PoW -> nodes validate and relay
      ch 6                    ch 12                   ch 10, 12          ch 5           ch 9
```

---

## 17.2 Start the network

```bash
cd toycoin_network
docker compose up --build
```

Three nodes come up and two miners begin checking mempools every few seconds.

(No Docker? It doesn't matter — this is ordinary Python. Open five terminals and run one
process in each; the result is identical. Docker just saves effort.)

The line worth reading in `docker-compose.yml` is `PEERS`:

```yaml
node1:
  environment:
    PEERS: http://node2:8000,http://node3:8000
```

**Every node holds a list of neighbours.** When it receives a new transaction or block,
it forwards it to everyone on that list.

That is peer-to-peer networking in its most primitive form. Real Bitcoin is far more elaborate
(peer discovery, address books, connection management), but **the core action is exactly this:
receive → validate → forward to neighbours.**

---

## 17.3 Broadcast some transactions

In another terminal:

```bash
cd toycoin_network
python wallet.py http://localhost:8001 Bob 5
python wallet.py http://localhost:8001 Carol 20
python wallet.py http://localhost:8002 Dave 1
```

The third argument is the **fee**.

Note the third command goes to **node2** while the first two go to node1. **That is deliberate** —
what you are about to watch is a transaction submitted only to node2 finding its own way to
node1 and node3.

---

## 17.4 Inspect each node

```bash
curl http://localhost:8001/status
curl http://localhost:8002/status
curl http://localhost:8003/status
```

Three fields come back:

```text
height : current chain height
tip    : hash of the current chain tip
mempool: how many unconfirmed transactions
```

**This is the thing worth staring at.**

Immediately after broadcasting, the three nodes' `mempool` counts are **very likely different** —
the messages are still in flight. Query again a few seconds later and they converge.

A few seconds after that, a miner finds a block: `height` increments and `mempool` drops.

**And then all three nodes report the same `tip`.**

What you are looking at in that moment is chapter 7's sentence happening in reality:
**different local views, converging on one history through relaying and validation.**
Nobody coordinated it. Nobody voted. No central server announced the new tip.

### Look at the mempool and the chain

```bash
curl http://localhost:8001/mempool
curl http://localhost:8001/chain
```

This is chapter 12, except now you can touch it with `curl`:

```text
0 confirmations : the transaction is in /mempool
1+ confirmations: the transaction is in a block in /chain
```

**The instant a transaction moves from the first to the second is the physical meaning of the
word "confirmation."**

---

## 17.5 Code map

| File | Responsibility | Chapters |
|---|---|---|
| `wallet.py` | build and broadcast transactions | 6, 12 |
| `node.py` | mempool, `valid_tx`, `valid_block`, relaying | 7, 9, 12 |
| `miner.py` | pick transactions by fee rate, mine | 5, 10, 12 |
| `docker-compose.yml` | bring up nodes and miners | 9 |

Open `miner.py` and you'll find this line:

```text
txs = sorted(mempool, key=feerate, reverse=True)[:MAX_BLOCK_TXS]
```

**That is chapter 12's `pick_block`**, the same idea word for word.

Open `node.py` and you'll find `valid_tx()` and `valid_block()` — **that is chapter 9's
`bitcoin_rules_v1`**, except now it runs on three different machines, and
**each one runs it independently.**

> Chapter 9 said "nodes do not trust miners; nodes check miners." Here that is literal:
> the miner POSTs a block to a node, the node runs `valid_block()`, and if it fails the block
> is discarded. **The miner has no mechanism to force acceptance.**

---

## 17.6 Being honest about what is missing

This is **not** a complete Bitcoin node. It deliberately omits a great deal:

| Omitted | Covered in |
|---|---|
| Real ECDSA signatures | Chapters 3, 13 |
| A full UTXO set and double-spend checking | Chapter 6 |
| Difficulty adjustment | Chapter 10 |
| Merkle trees | Chapter 11 |
| Robust reorg handling | Chapter 12 |
| Peer discovery | — |

**Adding them back is the best exercise this book can leave you.** You have already written
every one of them in isolation; the remaining work is wiring them into `node.py`.

(A warning that doubles as a lesson: while doing this you will walk straight into chapter 9's
problem. If you change `valid_block()` and the three containers do not all update at once,
**you will personally create a rule fork.** There is no better teacher.)

---

## 17.7 Experiments worth running

1. **Fees.** Broadcast several transactions with different fees and watch the miner logs to see
   which gets packed first. → confirms chapter 12's fee-rate priority.
2. **Propagation.** Send a transaction only to `node1`, then check `/mempool` on nodes 2 and 3.
   → makes "a message travelling the network" visible.
3. **Difficulty.** Change `DIFFICULTY` from 3 to 4 in `docker-compose.yml` and see how much
   slower blocks arrive. → and notice **the slowdown factor is wildly inconsistent**,
   because of section 5.2's variance.
4. **Node failure.** Stop a node, wait a few minutes, restart it, and watch it catch up.
   → a miniature of a real node resyncing after downtime.
5. **Forks.** Two miners find blocks at almost the same moment; watch the three nodes disagree
   about `tip` briefly, then converge. → a **temporary fork** (section 9.3).

The fifth is worth waiting for. **You will not see it every time, but run the network long
enough and it is guaranteed to happen.** It is exactly what real Bitcoin experiences every week.

---

## 17.8 The ledger

| What you ran | Field |
|---|---|
| Process and container isolation | **Distributed systems** |
| HTTP relaying, neighbour lists | **Networking** |
| Each node validating independently | **Consensus** |
| Separating miner and node roles | **Systems architecture** |

**Zero cryptography.**

| Phenomenon | Where you see it |
|---|---|
| Transaction broadcast | `wallet.py` output, node logs |
| Mempool | `/mempool` |
| Fee-rate selection | the txs `miner.py` chooses |
| Mining | the nonce in miner logs |
| Block propagation | the three nodes' `/status` heights converging |
| Node validation | `node.py`'s `valid_tx()` / `valid_block()` |

**The sentence:**

> Bitcoin is not one program running on one computer.
> **It is a crowd of nodes each validating, relaying to each other, and eventually converging.**

---

## Next

**The last chapter: why Script is deliberately weak.**

In chapter 14 you wrote a script virtual machine that probably felt crude — no loops,
no variables, not even a function.

The next chapter shows you that **every one of those "deficiencies" was chosen on purpose.**

And understanding why requires precisely what you just started up:
**every full node has to validate every transaction.**
