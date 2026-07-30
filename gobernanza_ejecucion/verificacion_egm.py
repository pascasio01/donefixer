#!/usr/bin/env python3
# EGM — verificación de integridad del paquete gobernanza_ejecucion (obligatoria por DC-14).
"""Confirma: existencia de RF/RNF/ADR citados, consistencia con el Registry,
ausencia de referencias inventadas y de familias prohibidas, y coherencia POL-EGM ↔ secciones.
Exit 1 si hay errores."""
import re, sys
from pathlib import Path

ROOT = Path("/mnt/agents/output/donefixer")
PKG = ROOT / "gobernanza_ejecucion"

defined = set()
for p in [ROOT/"REGISTRY_Canonical_Identifiers.md", ROOT/"ADI_Architecture_Decision_Index.md",
          ROOT/"11_Functional_Requirements.md", ROOT/"12_Non_Functional_Requirements.md"]:
    if p.exists():
        t = p.read_text(encoding="utf-8", errors="replace")
        defined |= set(re.findall(r"\bRNF-[A-ZÁÉÍÓÚ]+-\d+\b", t)) | set(re.findall(r"\bRF-[A-ZÁÉÍÓÚ]+-\d+\b", t)) \
                 | set(re.findall(r"\bADR-\d+\b", t))
corpus = ""
for p in ROOT.rglob("*.md"):
    if PKG not in p.parents and not p.name.startswith("AUDITORIA_INTEGRAL"):
        corpus += p.read_text(encoding="utf-8", errors="replace")
defined |= set(re.findall(r"\bRNF-[A-ZÁÉÍÓÚ]+-\d+\b", corpus)) | set(re.findall(r"\bRF-[A-ZÁÉÍÓÚ]+-\d+\b", corpus))
FUTUROS = {"ADR-013", "ADR-014"}

errores, warns = [], []
for f in sorted(PKG.glob("*.md")):
    if f.name.startswith("verificacion"): continue
    t = f.read_text(encoding="utf-8", errors="replace")
    for m in set(re.findall(r"\b(?:RNF|RF)-[A-ZÁÉÍÓÚ]+-\d+\b|\bADR-\d+(?:\.\d+)?\b", t)):
        if m not in defined and m not in FUTUROS:
            errores.append(f"{f.name}: {m} sin definición")
    for m in re.findall(r"\bRNF-(?:SEG|USA|PER|OFF|SYN)-\d+|\bRF-(?:WEB|EVD)-\d+", t):
        errores.append(f"{f.name}: familia prohibida {m}")

# Coherencia: las 18 políticas del índice deben existir como sección del manual
manual = (PKG/"01_EGM_Execution_Governance_Manual.md").read_text(encoding="utf-8")
indice = (PKG/"12_Indice_Politicas.md").read_text(encoding="utf-8")
pols_indice = set(re.findall(r"POL-EGM-\d{2}", indice))
pols_manual = set(re.findall(r"POL-EGM-\d{2}", manual))
if pols_indice - pols_manual: errores.append(f"políticas del índice ausentes en el manual: {sorted(pols_indice - pols_manual)}")
if pols_manual - pols_indice: warns.append(f"políticas del manual no indexadas: {sorted(pols_manual - pols_indice)}")
if len(pols_indice) != 18: warns.append(f"índice tiene {len(pols_indice)} políticas (esperadas 18)")

# No duplicación: el manual no debe redefinir umbrales (comprobación heurística)
for frase in ["el umbral queda en", "nuevo umbral", "redefine el SLO", "modifica el porcentaje de cobertura"]:
    if frase in manual.lower():
        errores.append(f"manual: posible redefinición de umbral ('{frase}')")

for c, e, d in [
    ("V-1 RF/RNF/ADR citados existen", errores and any("sin definición" in x for x in errores), errores),
    ("V-2 familias prohibidas", any("prohibida" in x for x in errores), [x for x in errores if "prohibida" in x]),
    ("V-3 coherencia POL-EGM manual↔índice", any("políticas" in x for x in errores), [x for x in errores if "políticas" in x] + warns),
    ("V-4 sin redefinición de umbrales (no duplicación)", any("umbral" in x.lower() or "redefinición" in x.lower() for x in errores), [x for x in errores if "umbral" in x.lower() or "redefinición" in x.lower()]),
]:
    estado = "FAIL" if e else "PASS"
    print(f"[{estado}] {c}: {len(d)} problema(s)" if d else f"[{estado}] {c}")
    for x in d[:8]: print("   -", x)
print(f"\nVerificación gobernanza_ejecucion: FAIL={len(errores)} WARN={len(warns)}")
sys.exit(1 if errores else 0)
