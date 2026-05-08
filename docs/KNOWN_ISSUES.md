# Known Issues — to address before client release

A running list of things that work today but need polish before
shipping to a paying customer.

---

## UI / Responsiveness

### Login page does not handle narrow windows gracefully
- **Severity:** low (POS systems run maximised in real use)
- **Where:** `app/ui/pages/login_page.py`
- **Symptoms:**
  - Below ~1100px window width, the 520px login card gets squeezed
  - Below ~900px, the left branding panel and right form panel fight for space
  - At very narrow widths, content can overflow horizontally
- **Fix plan (when ready):**
  - Below 900px viewport: hide the left branding panel, show only the form, centred
  - Replace `border_frame.setFixedWidth(520)` with min/max width
  - Wrap the entire login page in a `QScrollArea` so very tight viewports still scroll
- **Effort:** ~30 minutes
- **Status:** deferred — fix during pre-release polish pass

---

## Cleanup

### Stray `desktop.ini` in fonts folder
- **Severity:** trivial
- **Where:** `app/resources/fonts/desktop.ini`
- **Symptoms:** Windows-generated metadata file accidentally tracked in repo
- **Fix:** add `desktop.ini` to `.gitignore`, remove from repo
- **Status:** to do at next housekeeping pass

---

## Architecture

### Auth not yet implemented
- **Severity:** blocker for v1 release
- **Where:** `login_page.py` `_on_sign_in()` only prints to console
- **Status:** in queue — will tackle next

### No first-run setup flow
- **Severity:** blocker for v1 release
- **Symptoms:** Fresh install has no users, so login is impossible
- **Fix plan:** detect empty users table on app start; if empty, route to a "create first admin" wizard before showing the login page
- **Status:** in queue — will tackle alongside auth

---

## How to add to this list

When you find or defer an issue, add an entry with:
1. Severity: trivial / low / medium / high / blocker
2. Where: file path or general area
3. Symptoms: what's wrong from the user's perspective
4. Fix plan: how we'd address it
5. Effort: rough estimate
6. Status: deferred / in queue / blocked / fixing