// Cloudflare Worker: proxy CORS solo para dominios renfe.com
export default {
  async fetch(req) {
    const cors = { "Access-Control-Allow-Origin": "*" };
    if (req.method === "OPTIONS") return new Response(null, { headers: { ...cors, "Access-Control-Allow-Methods": "GET" } });
    const u = new URL(req.url).searchParams.get("url") || "";
    let host = "";
    try { host = new URL(u).hostname; } catch (e) {}
    if (!(host === "renfe.com" || host.endsWith(".renfe.com")))
      return new Response("Dominio no permitido", { status: 403, headers: cors });
    try {
      const r = await fetch(u, { headers: { "User-Agent": "Mozilla/5.0", "Accept": "application/json" } });
      return new Response(r.body, {
        status: r.status,
        headers: { ...cors, "Content-Type": r.headers.get("Content-Type") || "application/json", "Cache-Control": "no-store" }
      });
    } catch (e) {
      return new Response("Error al consultar Renfe: " + e.message, { status: 502, headers: cors });
    }
  }
};
