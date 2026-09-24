# AES-128 with Elliptic Curve Diffie-Hellman Key Exchange

A small but complete cryptosystem built from scratch. Two parties agree on a shared secret using Elliptic Curve Diffie-Hellman (ECDH), then use that secret as an AES-128 key to send encrypted messages over a TCP socket.

All the cryptography is implemented by hand. No crypto libraries are used for AES or the elliptic curve math. The only helpers are `sympy` for generating a random prime, and `numpy` and `BitVector` for some byte-level work.

## How it fits together

```
   ALICE (sender)                                  BOB (receiver)
   ──────────────                                  ──────────────
   generate curve (a, b, p) and point G
   pick secret Ka, compute A = Ka·G
                      ── a, b, G, p, A ──►
                                                   pick secret Kb, compute B = Kb·G
                      ◄──────── B ────────
   shared R = Ka·B                                 shared R = Kb·A
   AES key = x-coordinate of R                     AES key = x-coordinate of R

   encrypt message (AES-128, CBC)
                      ──── IV + ciphertext ──►
                                                   decrypt and print it
```

Both sides end up with the same point `R`, because `Ka·(Kb·G) = Kb·(Ka·G)`. An eavesdropper only sees `A` and `B`, and recovering the secret from those means solving the elliptic curve discrete log problem.

## Files

All code is in the `Code/` folder:

| File | What it does |
|---|---|
| `1905098_f1.py` | The core library: AES (S-box generation, key schedule, rounds, CBC encrypt/decrypt) and elliptic curve math (point addition, scalar multiplication, modular square roots) |
| `1905098_f2.py` | **Task 1.** Standalone AES demo. You type a key and a message, and it encrypts, decrypts, and reports timings |
| `1905098_f3.py` | **Task 2.** ECDH benchmark. It times computing A, B, and the shared key R for 128, 192, and 256-bit curves, averaged over 5 trials |
| `1905098_f4.py` | **Bob**, the receiver. A TCP server that completes the key exchange and decrypts incoming messages |
| `1905098_f5.py` | **Alice**, the sender. A TCP client that sets up the curve, completes the key exchange, and encrypts whatever you type |

## Implementation notes

### AES-128 (`f1`)

- **S-box.** Instead of hardcoding the S-box, it's generated at startup from the GF(2⁸) math (the multiplicative inverse followed by the affine transform). The inverse S-box is a lookup table.
- **Key schedule.** Expands the 16-byte key into 44 words (11 round keys) using the usual `RotWord → SubWord → XOR Rcon` step on every fourth word.
- **Rounds.** 10 rounds of SubBytes, ShiftRows, MixColumns, and AddRoundKey, with MixColumns skipped in the last round. Decryption runs the inverse steps in reverse order.
- **CBC mode.** Each block is XORed with the previous ciphertext block before it's encrypted. A random 16-byte IV is generated for every message and sent in front of the ciphertext, so the receiver knows where to start.
- **Padding.** The last block is padded with spaces.

### ECDH (`f1`, `f3`)

- **Curve setup.** Pick a random `k`-bit prime `p`. Then pick small random `a` and `b`, rejecting them if the curve would be singular (`4a³ + 27b² ≡ 0 mod p`).
- **Finding a base point G.** Pick a random `x`, compute `x³ + ax + b`, and check whether it has a square root mod `p` using the **Tonelli-Shanks** algorithm. If it doesn't, try another `x`.
- **Scalar multiplication.** Double-and-add over the bits of the scalar, with point addition and doubling done using modular inverses from the extended Euclidean algorithm.
- **Private keys.** Chosen at random below `p + 1 − 2√p`. That's the lower Hasse bound on the number of points on the curve, which keeps the key within the group's order without computing the exact order.

## Running it

You'll need Python 3 and three packages:

```bash
pip install numpy BitVector sympy
```

Run everything from inside the `Code/` folder, since the scripts import `1905098_f1` from the current directory.

**AES on its own:**

```bash
python 1905098_f2.py
```

Enter a key (16 characters for a full 128-bit key) and a message. It prints the plaintext, ciphertext, and decrypted text in both hex and ASCII, along with the time taken for key scheduling, encryption, and decryption.

**ECDH benchmark:**

```bash
python 1905098_f3.py
```

Prints a table of the average time to compute A, B, and R for each key size.

**The full sender/receiver system.** Open two terminals and start Bob first, since he's the server:

```bash
# terminal 1
python 1905098_f4.py

# terminal 2
python 1905098_f5.py
```

Alice connects on `127.0.0.1:12345`, the two sides do the key exchange, and then Alice is asked for a message. Bob prints the decrypted result. A fresh curve and key are negotiated for every message. Type `quit` to close both sides.

### Some Limitations

This was built to understand how the pieces work, not to protect anything real. In particular:

- **The curves are random, not standardized.** Real systems use vetted curves like P-256 or Curve25519. A randomly generated curve could turn out to be weak.
- **Space padding is ambiguous.** If your message ends in spaces, they can't be told apart from padding. PKCS#7 padding fixes this, but I kept spaces for simplicity.
- **Nothing is authenticated.** CBC without a MAC won't detect tampering, and the key exchange is open to a man-in-the-middle attack because neither side proves who they are.
- **The socket code is basic.** It assumes each message fits in a single `recv` call and only handles text, so long messages or binary files won't work.

## Author

**Rakib Kibria** (1905098) · [GitHub](https://github.com/rakibkibriaa)
Department of Computer Science and Engineering, BUET
