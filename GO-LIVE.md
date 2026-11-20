# partners.alurei.app go-live (L1)

The go-live copy lives in **rsq-code12/alurei-partners** (GitHub Pages, branch `main`, root). It is built from
rsq-code12/partner-preview with `python3 tools/make-release.py` (output `release/`, not committed here).
Preview stays at https://rsq-code12.github.io/partner-preview/ and is unchanged.

Current DNS (checked 20 Nov 2026): alurei.app uses Porkbun nameservers; `partners.alurei.app` does not exist yet;
no wildcard record; no CAA record (so GitHub's certificate can be issued). alurei.app and www stay on the existing server.

## Before the day (optional, recommended, 2 minutes)
1. GitHub → your avatar → Settings → Pages → "Add a domain" → `alurei.app` → GitHub shows a TXT record.
2. Porkbun → alurei.app → DNS → add that TXT record exactly as shown (type TXT, host `_github-pages-challenge-rsq-code12`, answer = the code GitHub shows).
3. Back in GitHub, click Verify. (Stops anyone else's GitHub Pages site from claiming partners.alurei.app.)

## Go-live day
1. Assistant (or you) activates the domain on the go-live copy: `gh api -X PUT repos/rsq-code12/alurei-partners/pages -f cname=partners.alurei.app` (same as renaming `CNAME.staged` to `CNAME`).
2. Porkbun → alurei.app → DNS → Add record: Type `CNAME`, Host `partners`, Answer `rsq-code12.github.io`, TTL `600`. ← the only DNS change.
3. Wait 10–30 minutes, then open https://partners.alurei.app (and /signup.html) and check it loads with the padlock.
4. Turn on HTTPS-only: `gh api -X PUT repos/rsq-code12/alurei-partners/pages -F https_enforced=true` (or GitHub → alurei-partners → Settings → Pages → tick "Enforce HTTPS").
5. Point the partner emails and alurei.app's "Partners" link to https://partners.alurei.app.

## Undo (any time)
1. Porkbun → delete the `partners` CNAME record. The page goes offline; nothing else on alurei.app is affected.

## Updating the page after go-live
1. Change files in partner-preview, check the preview, then `python3 tools/make-release.py` and copy `release/` into alurei-partners (keep its `CNAME`).

## Not touched
- No DNS changed, nothing on the Hostinger server, no Caddy change, no Alurei-Org repo.
- Sign-up address (FORM_ENDPOINT) still blank: on partners.alurei.app the sign-up shows the calm "opens very soon, email hello@alurei.app" card and the WhatsApp box says the same, so nothing looks broken and nothing is silently lost.
