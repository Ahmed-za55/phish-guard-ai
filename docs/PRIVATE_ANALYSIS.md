# PhishGuard Private: ask an AI about a phishing message without handing it your secrets

**Track: AI pipeline secret sharing**

## The problem
A suspicious email or SMS usually contains the victim's own details: name, email, phone number, a card number, a one-time code, sometimes a password. To get an AI opinion on it, people paste all of that into a hosted LLM, and the provider may log or store it. We built a gateway that lets an LLM analyze the message while detected sensitive values and URLs never leave our side.

## What it does
You paste a message. Before anything reaches Gemini:

1. **Detect.** Full URLs (including credentials, paths, query strings, and fragments), emails, phone numbers, card numbers (Luhn-checked), IBANs (mod-97 checked), national IDs, SSNs, API keys, passwords, one-time codes, and any words you mark as protected.
2. **Tokenize.** Each value becomes a random token such as `[[EMAIL_1_k3f9]]`. Every occurrence is replaced in a single pass, so detected values and full URLs are tokenized everywhere they appear.
3. **Seal.** The token-to-value map is encrypted with AES-256-GCM under a fresh random key, generated for this request only.
4. **Split.** That key is split with Shamir secret sharing into 3 shares, any 2 of which rebuild it. The server does not store the key, only the sealed vault.
5. **Check, then send.** The outgoing text is scanned for every detected original value, raw key, and share. If anything is found, the request is blocked and the provider is never called (fail closed). Otherwise Gemini receives only fixed instructions plus the tokenized text.
6. **Validate the answer.** Gemini's reply is untrusted: strict schema, bounded sizes, unknown tokens removed, and any email or number the model invents is redacted.
7. **Unlock locally.** Original values are put back only when two valid shares open the vault, on our server, for tokens this request issued. One share is refused. After 5 failed attempts the vault is destroyed.

The interface shows the original text next to exactly what the provider received, three key-holder cards to unlock with, and a button that runs 10 security checks live.

## Evidence of using a host-provided LLM
The gateway calls the **Gemini API** through the `google-genai` SDK (model chain `gemini-3.6-flash`, then `gemini-3.5-flash-lite`, then `gemini-3.8-flash`, configurable). The API key exists only inside the provider adapter. The adapter receives a payload object with two fields, the instructions and the tokenized text, so no key, share, mapping or detected original value is reachable from it. The interface states which provider answered; without a key it says plainly that it is in demo mode.

## The mathematics

### Shamir secret sharing over $\mathbb{F}_p$, $p = 2^{521}-1$
Let $K$ be the 256-bit key, read as an integer $K < 2^{256} < p$. Draw $a_1$ uniformly from $\mathbb{F}_p$ and define
$$f(x) = K + a_1 x \pmod p, \qquad \text{share}_i = (i, f(i)), \quad i \in \{1,2,3\}.$$
Any two shares $(x_i, y_i)$ and $(x_j, y_j)$ give back the key by Lagrange interpolation at $0$:
$$K = \frac{y_i x_j - y_j x_i}{x_j - x_i} \pmod p .$$
For a general threshold $k$ the polynomial has degree $k-1$ and $K = \sum_i y_i \prod_{j\ne i} \frac{-x_j}{x_i - x_j} \pmod p$.

**One share reveals nothing.** Fix a share $(x_1, y_1)$ and any candidate key $K'$. Exactly one slope fits: $a_1' = (y_1 - K')\,x_1^{-1} \bmod p$. Because $a_1$ is uniform, $\Pr[\text{share} = (x_1,y_1) \mid K] = 1/p$ for every $K$, so the share is statistically independent of the key. This is information-theoretic, not computational, security. A unit test checks this algebra for several candidate keys.

**Wrong or mixed shares fail twice.** A reconstructed value is rejected unless it is below $2^{256}$; for a random element of $\mathbb{F}_p$ that happens with probability $2^{-265}$. Shares also carry a public 32-bit key id, so shares from different requests are rejected before any arithmetic. Finally the AES-GCM tag fails for any key but the right one.

### Authenticated encryption of the vault
The vault is $(C, T) = \mathrm{AES\text{-}256\text{-}GCM}_K(N,\ \mathrm{AAD},\ M)$, where $M$ is the JSON map from token to original value, $N$ a random 96-bit nonce, and
$$\mathrm{AAD} = \texttt{pg-vault | v1 | request\_id | key\_id}.$$
The key is fresh for every request, so a random nonce is never reused under the same key. Binding the request id and key id into the associated data means a vault cannot be moved to another request, and a flipped ciphertext bit is rejected by the tag. The cipher uses the `cryptography` library (OpenSSL's native AES-GCM implementation) when available, with a byte-identical NIST SP 800-38D pure-Python fallback for constrained serverless containers.

### Tokens carry no information
Tokens are a type label, a counter and a 4-character random suffix drawn per request. They do not depend on the value, so they cannot be reversed or compared across requests.

## Who sees what

| Party | Sees |
|---|---|
| Gemini | Fixed instructions and the tokenized text only |
| Attacker with one share | Nothing about the key (perfect secrecy) |
| Attacker with the sealed vault | Nothing without the key (AES-256-GCM) |
| This server | The original text while analyzing; stores only the sealed vault; issues the shares |
| Browser (demo mode) | The original text, the tokens, and all three shares so the demo can show custody |

## How we tested it
- **75 automated privacy tests (125 total across the backend suite)** for the gateway, including a fuzz test of 300 random mixtures of sensitive values that checks no detected value survives in the outgoing text, a spy provider that records everything it receives, tampering and wrong-key tests, mixed-share tests, malicious provider output, and provider outage.
- **10 live checks** in the interface (`GET /api/v1/private/selftest`): no sensitive value or share reaches the provider; two shares restore; one share is refused; any two of three work; tampered or moved vaults are rejected; mixed shares are rejected; untrusted output is cleaned; the gateway blocks a leaking payload; and an outage still returns local results.
- Provider output is validated against a strict schema before it is shown.

## A local layer that never leaves the server
Links in the message are scored on this server by a trained domain classifier (character n-grams and name features, evaluated on domains it never saw during training). When the verdict is "likely phishing", it is right 91.8% of the time, catches 56.5% of phishing domains and wrongly flags 4.9% of legitimate ones. It reads domain names only, not page content.

## What this is not
- **It is tokenization with encrypted key custody, not encrypted inference.** Gemini reads every word that was not recognized as sensitive. We do not claim the model computes on ciphertext (that would need fully homomorphic encryption).
- **Detection is pattern-based.** It cannot find every secret. Names and other free text the patterns do not know must be listed as protected words, otherwise they are sent.
- **Custody is simulated on one machine.** Real independence needs the three holders on different devices or services. The demo shows all three shares in the browser so the threshold can be demonstrated.
- The sealed vault lives in server memory for 15 minutes and is lost on restart. The key is rebuilt in server memory for the moment of unlocking.
- Only the analysis output is restored, not the original message.

## Built with
Python, FastAPI, the `cryptography` library, our own Shamir implementation, the Gemini API (`google-genai`), scikit-learn for the local domain model, and a Next.js and Tailwind interface.
