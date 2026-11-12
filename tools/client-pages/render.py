import os, shutil, html, json
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(os.path.dirname(HERE)); OUT = os.environ.get('OUT', os.path.join(HERE, 'out'))
T = open(os.path.join(HERE, 'template.html')).read()
BUILD = '2026-10-08.1'

CLOSET = dict(
  HEADLINE='Save Hundreds On Your Dream Custom Closet', PRO_LABEL='Closet Pros', THING='closet', THING_CAP='Closet', THING_PLURAL='Closets',
  THING_SPACE='space', EVENT='Closet', Q1='Which space would you like to organize?',
  Q1_OPTIONS='''            <button type="button" class="opt" data-value="Walk-In Closet"><span class="ico">👗</span>Walk-In Closet</button>
            <button type="button" class="opt" data-value="Reach-In Closet"><span class="ico">🚪</span>Reach-In Closet</button>
            <button type="button" class="opt" data-value="Pantry"><span class="ico">🥫</span>Pantry</button>
            <button type="button" class="opt" data-value="Garage"><span class="ico">🧰</span>Garage</button>
            <button type="button" class="opt wide" data-value="Multiple Spaces">Multiple Spaces — Organize It All</button>''',
  HOW_H2='3 Simple Steps To An Organized Home', STEP2_H3='Book Your Free In-Home Design Consult',
  STEP2_P='Pick a time that works. A friendly local designer measures your space, shows you a 3D layout, and confirms your exact price. No pressure.',
  STEP3_H3='Enjoy Your Custom Closet', STEP3_TAIL='A place for everything from day one.',
  REVIEWS='''          <!-- PLACEHOLDER REVIEWS — replace with real, verifiable customer reviews before launch -->
          <div class="review">
            <div class="stars">★★★★★</div>
            <p>"Our walk-in went from a pile of shoes to something that looks like a boutique. The designer listened, the install crew was fast and clean, and it came in right at the quoted price."</p>
            <div class="who"><span><span class="av">M</span>Melissa R.</span><span class="v">✓ VERIFIED</span></div>
          </div>
          <div class="review">
            <div class="stars">★★★★★</div>
            <p>"We did the pantry and the reach-in closets in both kids' rooms. Everything finally has a place. Getting the design consult for free made the decision easy."</p>
            <div class="who"><span><span class="av">D</span>David &amp; Karen T.</span><span class="v">✓ VERIFIED</span></div>
          </div>
          <div class="review">
            <div class="stars">★★★★★</div>
            <p>"No hard sell at all. They measured, showed us the 3D layout on the spot, and the install took one day. Mornings are so much easier now."</p>
            <div class="who"><span><span class="av">J</span>Jasmine W.</span><span class="v">✓ VERIFIED</span></div>
          </div>''',
  ABOUT="{NAME} began with a simple idea: home organization should be functional, beautiful, and affordable. Every closet starts with a free in-home consultation where a designer measures your space and builds a 3D layout with you — so you see exactly what you're getting before anything is ordered. Our systems are custom-cut for your home and installed by our own trained crews, never subcontractors.",
  PHOTO_ALT='Custom walk-in closet with white built-in cabinetry, center island and LED-lit shelving',
  FEAT_TOP='''        <div>📐 <span>Custom-Designed For Your Exact Space</span></div>
        <div>🖥️ <span>Free 3D Design Consultation</span></div>''',
  FAQ='''      <details>
        <summary>How much does a custom closet cost?</summary>
        <p>It depends on the size of your space, the materials, and the features you choose — drawers, islands, lighting, and so on. A reach-in closet costs far less than a full walk-in. Your designer confirms an exact, all-in price during your free in-home consult, and with this event you'll get {OFFER_LOWER} on top of it.</p>
      </details>
      <details>
        <summary>Am I signing up for a pitch?</summary>
        <p>No. The consult is a working design session: your designer measures, listens to how you use the space, and shows you a 3D layout with pricing. There's no obligation and no pressure to decide on the spot.</p>
      </details>
      <details>
        <summary>Can I start with just one closet?</summary>
        <p>Absolutely. Many homeowners start with a single closet or pantry and add more later. The {OFFER_LOWER} offer applies to any qualifying project, large or small.</p>
      </details>
      <details>
        <summary>How long does installation take?</summary>
        <p>Most single closets are installed in one day. Larger walk-ins or multiple rooms may take two. Your designer gives you a firm schedule before anything is ordered.</p>
      </details>''',
  SERVICE='Custom Closets', PRODUCT='custom closet system', SCOPE_LABEL='What is the scope of this closet project?',
  META_DESC='Limited-time closet event from {NAME}: {OFFER_LOWER}. Answer 5 quick questions and book your free in-home design consult.',
  PHOTO_SRC=(f'{SRC}/hampton-design/closets/assets/closet.jpg', f'{SRC}/hampton-design/closets/assets/closet.webp'), PATH='closets',
)
BATH = dict(
  HEADLINE='Save Thousands On Your Dream Bathroom', PRO_LABEL='Bath Remodel Pros', THING='bathroom', THING_CAP='Bathroom', THING_PLURAL='Bathrooms',
  THING_SPACE='bathroom', EVENT='Bath', Q1='Which bathroom project are you planning?',
  Q1_OPTIONS='''            <button type="button" class="opt" data-value="Walk-In Shower"><span class="ico">🚿</span>Walk-In Shower</button>
            <button type="button" class="opt" data-value="Tub-To-Shower Conversion"><span class="ico">🛁</span>Tub-To-Shower</button>
            <button type="button" class="opt" data-value="Vanity &amp; Fixtures"><span class="ico">🪞</span>Vanity &amp; Fixtures</button>
            <button type="button" class="opt" data-value="Tile &amp; Flooring"><span class="ico">🧱</span>Tile &amp; Flooring</button>
            <button type="button" class="opt wide" data-value="Complete Bathroom Remodel">Complete Remodel — Do It All</button>''',
  HOW_H2='3 Simple Steps To Your New Bathroom', STEP2_H3='Book Your Free In-Home Consultation',
  STEP2_P='Pick a time that works. A friendly local specialist measures your bathroom, walks you through styles and materials, and confirms your exact price. No pressure.',
  STEP3_H3='Enjoy Your New Bathroom', STEP3_TAIL='Most projects are finished in days, not weeks.',
  REVIEWS='''          <!-- PLACEHOLDER REVIEWS — replace with real, verifiable customer reviews before launch -->
          <div class="review">
            <div class="stars">★★★★★</div>
            <p>"They converted our old tub into a walk-in shower in two days. The tile work is flawless and the crew left the house cleaner than they found it. Worth every penny."</p>
            <div class="who"><span><span class="av">R</span>Rebecca L.</span><span class="v">✓ VERIFIED</span></div>
          </div>
          <div class="review">
            <div class="stars">★★★★★</div>
            <p>"We'd put off the master bath for years. The in-home consult made it easy — they showed us options, gave us a firm price, and stuck to it. It looks like a hotel now."</p>
            <div class="who"><span><span class="av">M</span>Mark &amp; Dana P.</span><span class="v">✓ VERIFIED</span></div>
          </div>
          <div class="review">
            <div class="stars">★★★★★</div>
            <p>"No pressure at all. They measured, answered every question, and the install crew was professional and on time. Our guests keep asking who did it."</p>
            <div class="who"><span><span class="av">T</span>Tanya W.</span><span class="v">✓ VERIFIED</span></div>
          </div>''',
  ABOUT="{NAME} began with a simple idea: a bathroom remodel should be beautiful, stress-free, and affordable. Every project starts with a free in-home consultation where a specialist measures your space and walks you through styles, tile, and fixtures — so you see exactly what you're getting before anything is ordered. Our work is installed by our own trained crews, never subcontractors.",
  PHOTO_ALT='Remodeled bathroom with frameless glass walk-in shower, freestanding tub and floating oak double vanity',
  FEAT_TOP='''        <div>🚿 <span>Walk-In Showers &amp; Tub Conversions</span></div>
        <div>🧱 <span>Premium Tile, Fixtures &amp; Vanities</span></div>''',
  FAQ='''      <details>
        <summary>How much does a bathroom remodel cost?</summary>
        <p>It depends on the size of the bathroom, the materials you choose, and the scope — a tub-to-shower conversion costs far less than a full gut remodel. Your specialist confirms an exact, all-in price during your free in-home consultation, and with this event you'll get {OFFER_LOWER} on top of it.</p>
      </details>
      <details>
        <summary>Am I signing up for a pitch?</summary>
        <p>No. The consultation is a working design session: your specialist measures, listens to how you use the space, and walks you through options with pricing. There's no obligation and no pressure to decide on the spot.</p>
      </details>
      <details>
        <summary>Can I start with just one bathroom?</summary>
        <p>Absolutely. Many homeowners start with the master or guest bath and do the next one later. The {OFFER_LOWER} offer applies to any qualifying project, large or small.</p>
      </details>
      <details>
        <summary>How long does the remodel take?</summary>
        <p>Most tub-to-shower conversions and shower replacements are finished in one to two days. Full remodels take longer and your specialist gives you a firm schedule before anything is ordered.</p>
      </details>''',
  SERVICE='Bathroom Remodel', PRODUCT='bathroom remodel', SCOPE_LABEL='What is the scope of this bathroom project?',
  META_DESC='Limited-time bath event from {NAME}: {OFFER_LOWER}. Answer 5 quick questions and book your free in-home consultation.',
  PHOTO_SRC=(os.path.join(HERE, 'assets/bathroom.jpg'), os.path.join(HERE, 'assets/bathroom.webp')), PATH='bathroom',
)

CLIENTS = [
  dict(slug='elite-bath-solutions', NAME='Elite Bath Solutions', LOGO_BOLD='Elite', LOGO_LIGHT='Bath Solutions', niche=BATH,
       OFFER='Up To 50% Off + In-Home Consultation', OFFER_BIG='<em>Up To 50% Off</em><br>+ In-Home Consultation', OFFER_LOWER='up to 50% off plus an in-home consultation',
       TRACKING_ID='tk_ca25aae4ac8a48c39294816ed00bb6ee', LOCATION_ID='M3pAlUWTMMVdaLtYrZPr',
       EXTRA_CSS='  @media (max-width:520px){.offer .big{font-size:clamp(22px,6vw,30px)}.opt{font-size:13px}.opt.wide{font-size:14px}}\n'),
  dict(slug='sterling-closets', NAME='Sterling Closets', LOGO_BOLD='Sterling', LOGO_LIGHT='Closets', niche=CLOSET,
       OFFER='50% Off Installation + Free Design Consult', OFFER_BIG='<em>50% Off</em> Installation<br>+ Free Design Consult', OFFER_LOWER='50% off installation plus a free design consult',
       TRACKING_ID='tk_eaada1a0cd6b457cb50f322bf34b3ad1', LOCATION_ID='8FJDGLr4259P8SKdrcX0',
       CALENDAR_URL='https://api.leadconnectorhq.com/widget/booking/xQXe8M5ie5g0Yv1i6pk8'),
  dict(slug='nj-doors-closets', NAME='NJ Doors & Closets', LOGO_BOLD='NJ Doors', LOGO_LIGHT='& Closets', niche=CLOSET,
       OFFER='50% Off Installation + Free Design Consult', OFFER_BIG='<em>50% Off</em> Installation<br>+ Free Design Consult', OFFER_LOWER='50% off installation plus a free design consult',
       TRACKING_ID='tk_dfc961022fbd48a1a7fac22cb6e3cdf2', LOCATION_ID='o48OIwcn2U62znaVMvQC'),
  dict(slug='cutting-edge', NAME='Cutting Edge', LOGO_BOLD='Cutting', LOGO_LIGHT='Edge', niche=CLOSET,
       OFFER='50% Off Installation + Free Design Consult', OFFER_BIG='<em>50% Off</em> Installation<br>+ Free Design Consult', OFFER_LOWER='50% off installation plus a free design consult',
       TRACKING_ID='tk_a4180a7aeac64a38826794cc388e01d6', LOCATION_ID='jTTy5QUZh8cbPD0IfGUx', OFFER_PLACEHOLDER=True),
]

def render(c):
  n = c['niche']; path = n['PATH']
  v = {k: val for k, val in n.items() if k not in ('PHOTO_SRC',)}
  v.update({k: val for k, val in c.items() if k not in ('niche','slug','OFFER_PLACEHOLDER')})
  name_html = html.escape(c['NAME'], quote=False)
  v['NAME_JS'] = c['NAME'].replace("'", "\\'"); v['NAME'] = name_html
  v['LOGO_BOLD'] = html.escape(c['LOGO_BOLD'], quote=False); v['LOGO_LIGHT'] = html.escape(c['LOGO_LIGHT'], quote=False)
  v['OFFER'] = html.escape(c['OFFER'], quote=False)
  v['SLUG'] = c['slug'].replace('-','_'); v['BUILD'] = BUILD; v['CITY'] = ''; v['SERVICE_AREA'] = 'homeowners across our service area'
  v['CALENDAR_URL'] = c.get('CALENDAR_URL',''); v['SCOPE_FIELD_ID'] = ''; v['EXTRA_CSS'] = c.get('EXTRA_CSS','')
  for k in ('ABOUT','META_DESC','FAQ'):
    v[k] = v[k].replace('{NAME}', name_html).replace('{OFFER_LOWER}', v['OFFER_LOWER'])
  out = T
  for k, val in v.items(): out = out.replace('{{'+k+'}}', val)
  left = [m for m in __import__('re').findall(r'\{\{[A-Z_0-9]+\}\}', out)]
  assert not left, (c['slug'], left)
  return out, path

shutil.rmtree(OUT, ignore_errors=True)
for c in CLIENTS:
  page, path = render(c); root = os.path.join(OUT, c['slug']); os.makedirs(f'{root}/{path}/assets'); os.makedirs(f'{root}/functions/api')
  open(f'{root}/{path}/index.html','w').write(page)
  # photo
  jpg, webp = c['niche']['PHOTO_SRC']
  if webp: shutil.copy(jpg, f'{root}/{path}/assets/photo.jpg'); shutil.copy(webp, f'{root}/{path}/assets/photo.webp')
  else:
    im = Image.open(jpg).convert('RGB'); w,h = im.size; tw = int(h*1.6); l=(w-tw)//2; im = im.crop((l,0,l+tw,h))
    im.save(f'{root}/{path}/assets/photo.jpg','JPEG',quality=78,optimize=True,progressive=True); im.save(f'{root}/{path}/assets/photo.webp','WEBP',quality=78,method=6)
  open(f'{root}/{path}/assets/README.md','w').write(f"Drop client image files here:\n\n- `logo.png` — white {c['NAME']} logo on a transparent background (header + footer, ~30px tall on a black bar).\n- `photo.jpg` / `photo.webp` — the project photo in the about section (1228×768). Currently an AI render; swap for a real install photo when available.\n")
  open(f'{root}/_redirects','w').write(f"# Site root sends visitors to the funnel (query string is preserved).\n/  /{path}  302\n")
  open(f'{root}/_headers','w').write(f"/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n  Cache-Control: public, max-age=0, must-revalidate\n\n/{path}/assets/*\n  Cache-Control: public, max-age=86400\n")
  open(f'{root}/robots.txt','w').write("# Paid-traffic landing page; not meant for organic indexing (matches the noindex meta tag).\nUser-agent: *\nDisallow: /\n")
  shutil.copy(f'{SRC}/functions/api/lead.js', f'{root}/functions/api/lead.js')
  open(f'{root}/.gitignore','w').write("node_modules/\n.wrangler/\n.dev.vars\n.DS_Store\n")
  ph = ' **Offer text is a placeholder** (none was provided) — change `OFFER`, the two offer boxes and the footer disclaimer once confirmed.' if c.get('OFFER_PLACEHOLDER') else ''
  open(f'{root}/README.md','w').write(f"""# {c['NAME']} — {c['niche']['SERVICE']} Landing Page

Static lead-gen funnel served by Cloudflare Pages. No build step.{ph}

**Live path:** `/{path}` (the site root redirects there). Ad URLs: `https://<domain>/{path}?location=Houston&utm_source=fb`

## Cloudflare Pages setup
Workers & Pages → Create → Pages → Connect to Git → this repo. Framework preset **None**, build command empty,
build output directory **empty** (repo root). Production branch `main`. Then add the custom domain.

Optional: Settings → Variables and Secrets → `LEAD_WEBHOOK_URL` (GoHighLevel inbound webhook) so `/api/lead` forwards each lead.

## Where things live
- `{path}/index.html` — the page. Everything client-specific is in the `CONFIG` object at the top of the `<script>`:
  phone, service area, calendar URL, GoHighLevel tracking ID `{c['TRACKING_ID']}` / location ID `{c['LOCATION_ID']}`, scope custom field ID.
- `{path}/assets/` — logo and photo (see its README).
- `functions/api/lead.js` — Pages Function that forwards leads to `LEAD_WEBHOOK_URL`.
- `_redirects`, `_headers`, `robots.txt` — Pages platform files.

## Still to fill in
- `CONFIG.calendarUrl` — GoHighLevel booking calendar link. Until set, the final step shows a "we'll reach out" confirmation instead of the booking popup.
- `CONFIG.ghl.scopeFieldId` — ID of the "scope of project" custom field in this sub-account. Until set, the answer is sent in the contact's notes.
- `CONFIG.phone` / `phoneDisplay` / `serviceArea`.
- Real reviews (three placeholders are marked in the HTML) and the logo.
""")
  print('rendered', c['slug'], '->', path, f"{os.path.getsize(f'{root}/{path}/index.html')//1024}KB html")
