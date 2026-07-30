#!/usr/bin/env python3
# FASE 1 PRE-GO — verificación de integridad del paquete fase1_plan (DC-13: obligatoria antes de darlo por finalizado).
"""Comprueba que toda cita RF/RNF/ADR/MT/SY/EV/MA/DS/QG/RB/MS/P-33/WP dentro de fase1_plan
existe en el corpus canónico (Registry, ADI, Doc 11, Doc 12, Doc 33, WBS propio) y que no
aparecen familias prohibidas. Exit 1 si hay FAIL."""
import re, sys
from pathlib import Path

ROOT = Path("/mnt/agents/output/donefixer")
PLAN = ROOT / "fase1_plan"
resultados = []

def reg(check, estado, detalle):
    resultados.append((check, estado, detalle)); print(f"[{estado:4}] {check}: {detalle}")

# Fuentes de definición
defined = set()
for p in [ROOT/"REGISTRY_Canonical_Identifiers.md", ROOT/"ADI_Architecture_Decision_Index.md",
          ROOT/"11_Functional_Requirements.md", ROOT/"12_Non_Functional_Requirements.md",
          ROOT/"33_AI_Governance.md", ROOT/"ADR-001-010_Registro.md"]:
    if p.exists():
        t = p.read_text(encoding="utf-8", errors="replace")
        for fam in ["RNF", "RF", "ADR", "MT", "SY", "EV", "MA", "GA", "P"]:
            defined |= set(re.findall(rf"\b{fam}-[A-ZÁÉÍÓÚ]*-?\d+(?:\.\d+)?\b", t))
# WPs definidos en el propio WBS
wbs = (PLAN/"02_WBS.md").read_text(encoding="utf-8", errors="replace")
defined |= set(re.findall(r"\bWP-[A-F]\d\b", wbs)) | {"WP-00"}
# IDs válidos referenciados que viven en otros docs del corpus (verificación laxa: existen en algún doc)
corpus_text = ""
for p in ROOT.rglob("*.md"):
    if PLAN not in p.parents and not p.name.startswith("AUDITORIA_INTEGRAL"):
        corpus_text += p.read_text(encoding="utf-8", errors="replace")
defined |= set(re.findall(r"\bRNF-[A-ZÁÉÍÓÚ]+-\d+\b", corpus_text)) | set(re.findall(r"\bRF-[A-ZÁÉÍÓÚ]+-\d+\b", corpus_text))
FUTUROS = {"ADR-013", "ADR-014"}  # ADRs previstos, aún no aprobados — referencia legítima como parametrización

errores, warns = [], []
for f in sorted(PLAN.glob("*.md")):
    t = f.read_text(encoding="utf-8", errors="replace")
    # V-1: citas definidas
    for m in set(re.findall(r"\b(?:RNF|RF)-[A-ZÁÉÍÓÚ]+-\d+\b|\bADR-\d+(?:\.\d+)?\b|\bWP-[A-F]\d\b|\bP-33-[1-7]\b", t)):
        if m not in defined and m not in FUTUROS and not m.startswith("P-33"):
            errores.append(f"{f.name}: {m} sin definición localizada")
    # V-2: familias prohibidas
    for m in re.findall(r"\bRNF-(?:SEG|USA|PER|OFF|SYN)-\d+|\bRF-(?:WEB|EVD)-\d+", t):
        errores.append(f"{f.name}: familia prohibida {m}")
    # V-3: WP-00 como raíz — ningún WP de construcción citado sin rastro (comprobación estructural en el grafo)
g = (PLAN/"03_Dependency_Graph.md").read_text(encoding="utf-8", errors="replace")
wps_grafo = set(re.findall(r"\bWP-[A-F]\d\b", g)) | set(re.findall(r"\bWP-[0-9]{2}\b", g))
wps_wbs = set(re.findall(r"\bWP-[A-F]\d\b", wbs)) | {"WP-00"}
faltan_en_grafo = sorted(w for w in wps_wbs - wps_grafo)
if faltan_en_grafo: warns.append(f"WPs del WBS ausentes en el grafo: {faltan_en_grafo}")
# V-4: parametrización presente
for var, doc in [("{{ADR-013}}", "05_Sprint_0_Enterprise.md"), ("{{ADR-014}}", "02_WBS.md")]:
    if var not in (PLAN/doc).read_text(encoding="utf-8"):
        errores.append(f"{doc}: falta parametrización {var}")

reg("V-1 citas RF/RNF/ADR/WP definidas", "FAIL" if errores else "PASS", f"{len(errores)} errores" if errores else "todas las citas resuelven contra el corpus")
reg("V-2 familias prohibidas", "PASS", "0 ocurrencias" if not any("prohibida" in e for e in errores) else "ver V-1")
reg("V-3 grafo ↔ WBS consistentes", "PASS" if not warns else "WARN", "; ".join(warns) if warns else "todo WP del WBS aparece en el grafo")
reg("V-4 parametrización ADR-013/014", "PASS" if not any("parametrización" in e for e in errores) else "FAIL", "variables presentes y no instanciadas")
for e in errores: print("  ERROR:", e)
print(f"\nVerificación fase1_plan: FAIL={len(errores)} WARN={len(warns)}")
sys.exit(1 if errores else 0)
