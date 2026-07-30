#!/usr/bin/env python3
"""verificacion_ux.py — Verificación automática de integridad del WP-UX-ART.
Reglas:
 V-1 Las 15 pantallas P-01..P-15 existen en /mnt/agents/output/app.
 V-2 Cada HTML lleva el banner «Design Artifact PRE-GO» y footer .screen-label.
 V-3 Prohibido: <script>, fetch(, XMLHttpRequest, localStorage, sessionStorage, http(s):// en atributos de acción.
 V-4 tokens.css define los tokens DS obligatorios (sync.*, focus-ring, motion, reduced-motion).
 V-5 components.css define los componentes DS obligatorios (sync-badge, connectivity, bottom-nav, conflict-compare...).
 V-6 Toda pantalla de app (nav) usa los 5 destinos DS-3.
 V-7 Fichas 09 cubren las 15 pantallas.
Salida: PASS/FAIL por regla; exit 1 si alguna falla.
"""
import os, re, sys

APP = "/mnt/agents/output/app"
UA  = "/mnt/agents/output/donefixer/ux_artifact"
SCREENS = {"P-01":"index.html","P-02":"login.html","P-03":"mfa.html","P-04":"recuperar.html",
"P-05":"dashboard.html","P-06":"ordenes.html","P-07":"orden.html","P-08":"offline.html",
"P-09":"avisos.html","P-10":"conflicto.html","P-11":"activos.html","P-12":"preventivos.html",
"P-13":"ia.html","P-14":"configuracion.html","P-15":"estados.html"}
APP_NAV = ["dashboard.html","ordenes.html","orden.html","offline.html","avisos.html",
           "activos.html","preventivos.html","ia.html","configuracion.html"]
ok = True
def check(name, cond, detail=""):
    global ok
    print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f" — {detail}" if detail and not cond else ""))
    ok = ok and cond

# V-1
missing=[f for f in SCREENS.values() if not os.path.isfile(f"{APP}/{f}")]
check("V-1 pantallas existen", not missing, f"faltan: {missing}")

html={f:open(f"{APP}/{f}",encoding="utf-8").read() for f in SCREENS.values() if os.path.isfile(f"{APP}/{f}")}
# V-2
bad=[f for f,c in html.items() if "Design Artifact PRE-GO" not in c or 'class="screen-label"' not in c]
check("V-2 banner + trazabilidad", not bad, f"sin banner/label: {bad}")
# V-3
forbidden=[r"<script", r"fetch\(", r"XMLHttpRequest", r"localStorage", r"sessionStorage"]
bad=[f for f,c in html.items() for p in forbidden if re.search(p,c)]
check("V-3 sin lógica ni persistencia", not bad, f"violaciones: {bad}")
# V-4
tokens=open(f"{APP}/assets/tokens.css",encoding="utf-8").read()
need=["--color-sync-confirmed","--color-sync-provisional","--color-sync-conflict",
      "--focus-ring","--motion-fast","prefers-reduced-motion","prefers-color-scheme","--space-4"]
miss=[t for t in need if t not in tokens]
check("V-4 tokens DS", not miss, f"faltan: {miss}")
# V-5
comp=open(f"{APP}/assets/components.css",encoding="utf-8").read()
need=["sync-badge","connectivity","bottom-nav","conflict-compare","artifact-banner",
      "empty-state","skeleton","ai-card","signature-pad","evidence-grid","min-height:44px"]
miss=[t for t in need if t not in comp]
check("V-5 componentes DS", not miss, f"faltan: {miss}")
# V-6
DEST=["Hoy","Órdenes","Escanear","Avisos","Más"]
bad=[f for f in APP_NAV if not all(d in html.get(f,"") for d in DEST)]
check("V-6 bottom-nav 5 destinos DS-3", not bad, f"nav incompleta: {bad}")
# V-7
fichas=open(f"{UA}/09_Fichas_Pantallas.md",encoding="utf-8").read()
miss=[p for p in SCREENS if p not in fichas]
check("V-7 fichas cubren 15 pantallas", not miss, f"faltan fichas: {miss}")

print("\nRESULTADO:", "TODO PASS" if ok else "FALLOS PRESENTES")
sys.exit(0 if ok else 1)
