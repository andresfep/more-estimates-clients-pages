# More Estimates — Client Landing Pages

Static, self-contained lead-gen landing pages, one folder per client and service. No build step.

| Client | Service | Path |
|---|---|---|
| Hampton Design | Custom closets (50% off installation + free design consult) | `hampton-design/closets/index.html` |

## Deploying to Cloudflare Pages

1. Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to Git** and pick this repo.
2. Build settings:
   - Framework preset: **None**
   - Build command: *(leave empty)*
   - Build output directory: `hampton-design`  (the page is served at `/closets`; `/` redirects there)
   - Root directory: `/` (default)
   These match `wrangler.toml`, which the dashboard also reads.
3. **Settings → Variables and Secrets** → add secret `LEAD_WEBHOOK_URL` with the GoHighLevel inbound
   webhook (or Zapier/Make URL) that should receive each lead. Without it, leads still reach the
   calendar but are only logged by the function.
4. Custom domain: `hamptondesign.moreestimatespro.site`. Ad URLs look like
   `https://hamptondesign.moreestimatespro.site/closets?location=Houston&utm_source=fb`.

CLI alternative: `npx wrangler pages deploy` from the repo root.

### What is where

- `hampton-design/closets/index.html` — the page. Client-specific values (city, phone, rating,
  calendar URL, GoHighLevel tracking/location IDs) live in the `CONFIG` object at the top of the `<script>` block.
  On the final quiz step the page sends a GoHighLevel form-tracking event (creates/updates the contact),
  then opens the prefilled booking calendar.
- `hampton-design/_headers` — cache and security headers served by Pages.
- `hampton-design/_redirects` — `/` → `/closets`.
- `hampton-design/robots.txt` — blocks crawlers (paid-traffic page).
- `hampton-design/closets/assets/` — drop `logo.png` and `closet.jpg` here (see its README).
- `functions/api/lead.js` — Pages Function at `/api/lead`; receives the quiz payload, adds IP/geo
  metadata, forwards to `LEAD_WEBHOOK_URL`.

### Before launch

- Paste the custom field ID for `{{contact.what_is_the_scope_of_this_closet_project}}` into `CONFIG.ghl.scopeFieldId`
  so the chosen space lands in that field (it is also written to the appointment notes).

- Replace the placeholder reviews marked with `PLACEHOLDER` comments.
- Add the logo and project photo to `assets/`.
- Fill in the real phone number and service area in `CONFIG`.
- Point the Privacy Policy / Terms links in the footer at real pages.
