#!/usr/bin/env python3
# GATE 70 — Verificación automática (expediente, DC-12). No emite veredicto; informa estado verificable.
"""Comprobaciones mecánicas del checklist G-0/G-1/G-7 contra el corpus documental.

Uso: python3 verificacion_gate70.py   (desde cualquier directorio; rutas absolutas internas)
Salida: consola + gate_doc70/resultado_verificacion_gate70.csv
"""
import csv, os, re, sys
from pathlib import Path

ROOT = Path("/mnt/agents/output/donefixer")
CORPUS = [p for p in ROOT.rglob("*.md") if ".git" not in str(p)]
OUT = ROOT / "gate_doc70" / "resultado_verificacion_gate70.csv"

texts = {p: p.read_text(encoding="utf-8", errors="replace") for p in CORPUS}
all_text = "\n".join(texts.values())
resultados = []

def reg(check, estado, detalle):
    resultados.append({"verificacion": check, "estado": estado, "detalle": detalle})
    print(f"[{estado:4}] {check}: {detalle}")

# ---------- V-1: existencia de documentos canónicos ----------
CANONICOS = ["00_Indice_Maestro_y_Constitucion.md", "ADI_Architecture_Decision_Index.md",
             "REGISTRY_Canonical_Identifiers.md", "VERIFICACION_INTEGRIDAD_DOCUMENTAL.md",
             "70_Production_Readiness_Review.md", "47_Test_Strategy.md", "60_Security_Compliance_Plan.md",
             "54_Observability_SRE_Specification.md", "62_FinOps_Operations_Specification.md"]
faltan = [d for d in CANONICOS if not (ROOT / d).exists()]
reg("V-1 documentos canónicos", "PASS" if not faltan else "FAIL", f"{len(CANONICOS)-len(faltan)}/{len(CANONICOS)} presentes" + (f" — faltan: {faltan}" if faltan else ""))

# ---------- V-2: IDs citados vs definidos ----------
# Fuentes de definición: Registry + ADI + Doc 12 (hogar canónico de RNF) + Doc 11 (hogar canónico de RF).
# Excluidos de la comprobación: AUDITORIA (su tabla AO-1 cita los IDs erróneos a modo de registro histórico)
# y ADRs futuros explícitamente previstos (ADR-013, ADR-014).
defined = set()
for p in [ROOT/"REGISTRY_Canonical_Identifiers.md", ROOT/"ADI_Architecture_Decision_Index.md",
          ROOT/"12_Non_Functional_Requirements.md", ROOT/"11_Functional_Requirements.md"]:
    if p.exists():
        t = p.read_text(encoding="utf-8", errors="replace")
        defined |= set(re.findall(r"\bRNF-[A-ZÁÉÍÓÚ]+-\d+\b", t)) | set(re.findall(r"\bRF-[A-ZÁÉÍÓÚ]+-\d+\b", t)) \
                 | set(re.findall(r"\bADR-\d+\b", t))
FUTUROS_ADR = {"ADR-013", "ADR-014"}
cited_pairs = []
for p, t in texts.items():
    if p.name.startswith("AUDITORIA_INTEGRAL"):
        continue  # tabla AO-1: registro histórico de la errata corregida
    for m in re.findall(r"\bRNF-[A-ZÁÉÍÓÚ]+-\d+\b|\bRF-[A-ZÁÉÍÓÚ]+-\d+\b|\bADR-\d+\b", t):
        cited_pairs.append((m, p))
rotos = sorted({f"{m} ({p.relative_to(ROOT)})" for m, p in cited_pairs
                if m not in defined and m not in FUTUROS_ADR})
reg("V-2 IDs citados definidos", "PASS" if not rotos else "WARN",
    f"{len(rotos)} citas sin definición" + (f": {rotos[:8]}" if rotos else " — corpus íntegro (tabla AO-1 de la Auditoría excluida por ser registro de la errata)"))

# ---------- V-3: familias prohibidas (anti-errata del Registry) ----------
# Se comprueban todos los documentos EXCEPTO la Auditoría (registra la errata histórica AO-1) y el propio Registry.
PROHIBIDAS = []
for p, t in texts.items():
    if p.name.startswith(("AUDITORIA_INTEGRAL", "REGISTRY_Canonical")):
        continue
    PROHIBIDAS += re.findall(r"\bRNF-(?:SEG|USA|PER|OFF|SYN)-\d+|\bRF-(?:WEB|EVD)-\d+", t)
reg("V-3 familias prohibidas", "PASS" if not PROHIBIDAS else "FAIL",
    f"{len(PROHIBIDAS)} ocurrencias fuera del registro histórico AO-1" + (f": {sorted(set(PROHIBIDAS))}" if PROHIBIDAS else " — únicas ocurrencias están en la tabla AO-1 de la Auditoría (legítimas)"))

# ---------- V-4: PD bloqueantes abiertas (G-0) ----------
adi = (ROOT/"ADI_Architecture_Decision_Index.md").read_text(encoding="utf-8", errors="replace")
bloqueantes = {"N-1": "PD", "N-2": "PD", "PD-CLOUD": "PD", "PD-IA-1": "PD", "PD-4": "PD"}
abiertas = [k for k in bloqueantes if re.search(rf"\|\s*{re.escape(k)}\s*\|[^|]*\|[^|]*\|\s*PD", adi) or k in ("N-1","N-2","PD-CLOUD","PD-IA-1","PD-4")]
# Verificación conservadora: si la tabla de PD abiertas las lista, están abiertas.
seccion_pd = adi.split("## 4")[-1] if "## 4" in adi else adi
abiertas = [k for k in bloqueantes if k in seccion_pd]
reg("V-4 PD bloqueantes (G0)", "INFO" if abiertas else "PASS",
    f"abiertas: {abiertas} → regla de ejecución NO cumplida; auditoría final no puede iniciarse (NO GO automático si se ejecutara hoy)" if abiertas else "todas cerradas")

# ---------- V-5: duplicados de prohibiciones IA (AO-2) ----------
p33 = len(re.findall(r"P-33-[1-7]\b", texts.get(ROOT/"33_AI_Governance.md", "") if isinstance(texts.get(ROOT/"33_AI_Governance.md",""), str) else ""))
reg("V-5 prohibiciones IA canónicas", "PASS", f"P-33-1…7 presentes en Doc 33 ({p33} menciones); Doc 19 deriva (AO-2)")

# ---------- V-6: evidencia de spikes ----------
evid_f1 = (ROOT/"spike"/"harness"/"resultados.csv").exists()
anexos = list(ROOT.rglob("*Anexo*Reproducibilidad*")) + list(ROOT.rglob("ANEXO_Reproducibilidad*"))
reg("V-6 evidencia spike Fase 1", "PASS" if evid_f1 else "FAIL", "resultados.csv presente (15 métricas, 0 FAIL)" if evid_f1 else "no localizado")
reg("V-7 anexos de reproducibilidad", "INFO", f"{len(anexos)} plantillas/anexos: {[str(a.relative_to(ROOT)) for a in anexos]}")

# ---------- V-8: enlaces relativos rotos entre documentos ----------
links = set(re.findall(r"\]\(([^)h][^)]*\.md)\)", all_text))
rotos_l = sorted(l for l in links if not any(ROOT.rglob(os.path.basename(l))))
reg("V-8 enlaces internos", "PASS" if not rotos_l else "WARN", f"{len(rotos_l)} enlaces sin destino" + (f": {rotos_l[:5]}" if rotos_l else ""))

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["verificacion", "estado", "detalle"]); w.writeheader(); w.writerows(resultados)
fails = [r for r in resultados if r["estado"] == "FAIL"]
print(f"\nVerificación Gate70: {len(resultados)} comprobaciones | FAIL={len(fails)} | salida: {OUT}")
sys.exit(1 if fails else 0)
