# Demo video script (about 3 minutes)

The judges score the video on being thorough and straightforward, so keep to one story: **a message with personal details and links goes to an AI, and the AI only sees opaque tokens for every detected value and URL.**

## Before recording
- Backend running with a real `GEMINI_API_KEY` (no "Demo mode" banner in the interface). Check `http://127.0.0.1:8000/api/v1/private/status` says `"provider": "gemini"`.
- Frontend at `http://localhost:3000`, browser zoom 100%, window about 1280 wide, notifications off.
- Second terminal in `backend` ready to run `python -m pytest tests/private -q`.
- Do one dry run first so the Gemini model is warm.

## Script

**0:00 - The problem (15 s).** Show the sample message.
> "Phishing messages contain the victim's own details. To ask an AI about one, people paste all of it into a hosted model. We built a gateway so the AI can help without seeing those detected details or raw URLs."

**0:15 - Paste and analyze (20 s).** Open **Private analysis**, click *Use a sample with personal details*, click **Analyze privately**.
> "This message has a name, a suspicious link, an email, a phone number, a card number, a password and a verification code."

**0:35 - What left the server (35 s).** Scroll to the two panes.
> "On the left, what I wrote, with every sensitive value underlined. On the right, exactly what Gemini received. Every detected value and URL is replaced with a random token, while the raw link is scored locally on our server."

Optional proof: open DevTools, Network tab, click the `analyze` request and show `sanitized_text` in the response.

**1:10 - The answer (20 s).** Scroll to the verdict.
> "Gemini analyzed the tokenized text and answered. Its reasons mention tokens, not people. The domain check ran only on this server, because the original message never leaves it."

**1:30 - Key custody (45 s).** Scroll to *Unlock the protected values*.
> "The original values are sealed with AES-256-GCM. The key is split into three shares, and any two rebuild it. One share is mathematically useless."

Click **Holder A**, click **Unlock with 1 holder**. Point at the refusal.
> "One holder: refused."

Click **Holder C**, click **Unlock with 2 holders**.
> "Two holders: unlocked. The reasons now show the real name. This happened on our server, and Gemini never saw it."

**2:15 - Prove it (30 s).** Scroll to *What we can prove*, click **Run the security self-test**.
> "Ten checks run live: no detected sentinel value or URL reaches the provider, one share is refused, any two work, tampering is rejected, wrong keys fail, and if Gemini is down the local result still works."

**2:45 - Limits and close (15 s).**
> "To be clear: this is tokenization with encrypted key custody, not encrypted inference. Gemini still reads the words we did not recognize as sensitive. The math is Shamir over a 521-bit prime field and AES-GCM, with 75 automated privacy tests (125 total)."

Optional last shot: the terminal showing `python -m pytest tests/private -q` finishing with `68 passed`.

## Tips
- Say "tokens" and "shares", not "encrypted prompt". It keeps the claim accurate.
- If Gemini is slow, trim the wait in editing rather than speeding up the narration.
- Upload to YouTube as unlisted and paste the link in the submission.
