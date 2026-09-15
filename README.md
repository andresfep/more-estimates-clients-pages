# More Estimates — Client Landing Pages

Static, self-contained lead-gen landing pages, one folder per client and service.

| Client | Service | Path |
|---|---|---|
| Hampton Design | Custom closets (50% off installation + free design consult) | `hampton-design/closets/index.html` |

## Editing a page

Each page is a single `index.html` with no build step. Client-specific values (city, phone, rating, form endpoint) live in the `CONFIG` object at the top of the `<script>` block. Leads post as JSON to `CONFIG.formEndpoint`; leave it empty during development and submissions log to the browser console.

Before launch, replace the placeholder reviews and gallery blocks marked with `PLACEHOLDER` comments.
