/**
 * POST /api/lead  — Cloudflare Pages Function
 *
 * The landing page posts each completed quiz here as JSON. We add request
 * metadata and forward it to LEAD_WEBHOOK_URL (a GoHighLevel inbound webhook,
 * Zapier, Make, etc.) so the webhook URL never appears in client-side code.
 * If LEAD_WEBHOOK_URL is not set, the lead is accepted and logged only.
 */
export async function onRequestPost({ request, env }) {
  let lead;
  try {
    const text = await request.text();
    if (text.length > 20_000) return json({ ok: false, error: 'payload too large' }, 413);
    lead = JSON.parse(text);
  } catch {
    return json({ ok: false, error: 'invalid JSON' }, 400);
  }
  if (!lead || typeof lead !== 'object' || !lead.phone || !lead.email) {
    return json({ ok: false, error: 'phone and email are required' }, 422);
  }

  const cf = request.cf || {};
  const enriched = {
    ...lead,
    received_at: new Date().toISOString(),
    ip: request.headers.get('cf-connecting-ip') || '',
    country: cf.country || '',
    region: cf.region || '',
    city_detected: cf.city || '',
    user_agent: request.headers.get('user-agent') || '',
    referer: request.headers.get('referer') || '',
  };

  if (!env.LEAD_WEBHOOK_URL) {
    console.log('[lead] LEAD_WEBHOOK_URL not set; lead not forwarded', enriched);
    return json({ ok: true, forwarded: false });
  }

  try {
    const res = await fetch(env.LEAD_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(enriched),
    });
    if (!res.ok) {
      console.error('[lead] webhook responded', res.status);
      return json({ ok: false, forwarded: false, status: res.status }, 502);
    }
    return json({ ok: true, forwarded: true });
  } catch (err) {
    console.error('[lead] webhook error', err);
    return json({ ok: false, forwarded: false }, 502);
  }
}

export function onRequestGet() {
  return json({ ok: false, error: 'POST only' }, 405);
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
  });
}
