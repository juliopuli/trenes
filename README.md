# Trenes Renfe en tiempo real

App web (HTML + Leaflet) con trenes de Renfe sobre un mapa de España y alerta de proximidad:
rojo < 3 km, naranja < 5 km, verde en el resto.

## Puesta en marcha (sin instalar nada)

### 1. Proxy en Cloudflare (gratis)
1. Crea cuenta en https://dash.cloudflare.com
2. Workers & Pages → Create → Create Worker → ponle nombre (p. ej. `trenes`) → Deploy.
3. Edit code → borra todo, pega el contenido de `worker.js` → Deploy.
4. Copia la URL del Worker (`https://trenes.TU-USUARIO.workers.dev`).

### 2. Web en GitHub Pages
1. Crea un repositorio y sube `index.html`, `worker.js` y este `README.md`.
2. Settings → Pages → Source: *Deploy from a branch* → rama `main`, carpeta `/ (root)` → Save.
3. Tu web quedará en `https://TU-USUARIO.github.io/NOMBRE-REPO/`.

### 3. Conectar ambos
- Opción A: abre la web, escribe en «Proxy CORS»:
  `https://trenes.TU-USUARIO.workers.dev/?url={url}` (el navegador lo recuerda).
- Opción B: edita `index.html`, busca `DEFAULT_PROXY` y pega ahí esa misma dirección.

## Notas
- Las URL de Renfe (visor `flota.json` y GTFS-RT) pueden cambiar; se pueden sustituir con la fuente «URL personalizada».
- Fuente «Demo» funciona sin proxy.
- Local: `python servidor.py` (opcional, ver archivo) sirve la app y hace de proxy en http://localhost:8000.
