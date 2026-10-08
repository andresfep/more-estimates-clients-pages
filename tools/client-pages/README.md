# Client page generator

`template.html` is the Hampton Design funnel with every client- and niche-specific string replaced by a `{{TOKEN}}`.
`render.py` holds the per-client configs (name, offer, niche, GoHighLevel tracking/location IDs) and writes a complete,
deploy-ready Cloudflare Pages repo per client to `out/<slug>/` (or `$OUT/<slug>/`).

```
python3 tools/client-pages/render.py
```

To add a client, append a dict to `CLIENTS`. To change shared copy, edit `template.html`; niche copy lives in the
`CLOSET` / `BATH` dicts. `tools/client-pages/out/` is git-ignored.
