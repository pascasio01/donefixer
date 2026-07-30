# FASE 1 PRE-GO — 08: Plan de Seguridad

**Norma:** DC-13 · Fuente: Doc 60 (STRIDE, SBOM, rotación ≤90 d), Doc 26 (RLS), Doc 29, lecciones empíricas de la Spike.

## 1. Threat model por módulo (obligatorio en DoR de cada WP)

| WP/Módulo | Amenazas prioritarias (STRIDE) | Controles |
|---|---|---|
| B2 Multi-tenancy | Elevation of Privilege, Information Disclosure | RLS + FORCE RLS + rol no privilegiado + test de ataque en CI (**lección Spike: superuser bypassa RLS**) |
| B3/B4 Auth | Spoofing, EoP | MFA para roles admin, revocación por dispositivo (RNF-SEC-005), políticas de sesión |
| C1/C2 Sync | Tampering, Repudiation, DoS | Idempotencia operation_id, HLC, re-validación servidor (ADR-011 v1.1), firma de evidencias (sha256), rate limiting |
| C3 Móvil | Information Disclosure (dispositivo perdido) | SQLCipher (RNF-SEC-003), borrado remoto (RNF-SEC-005), jailbreak/root detection |
| D1 Evidencias | Tampering, Repudiation | Hash SHA-256 en origen, inmutabilidad en OT cancelada/cerrada (RF-WO-003) |
| E1 Web | XSS, CSRF | CSP estricta, tokens httpOnly, SameSite |

## 2. Gates de seguridad (CI, etapa 7)

- SAST por stack; 0 hallazgos críticos/altos nuevos para merge.
- Análisis de dependencias + **SBOM diff**: nueva dependencia exige justificación en el PR (gobernanza de dependencias, Doc 60) y verificación de licencia (G-6 del Gate).
- Escaneo de secretos en cada commit; rotación de secretos ≤90 d con ensayo documentado (WP-F2).
- DAST sobre staging antes de cada release.
- Test de ataque RLS + tests de privesc RBAC: obligatorios, no desactivables sin ADR.

## 3. Inventario de secretos (Secrets Inventory — se mantiene vivo)

| Secreto | Dónde se usa | Rotación | Responsable |
|---|---|---|---|
| Credencial rol app PostgreSQL | backend | ≤90 d | Principal Database |
| Claves JWT identidad | auth | ≤90 d | Principal Security |
| Token/claves canal sync `{{ADR-014}}` | sync | según ADR-014 definitivo | Principal DevOps |
| Certificados TLS | edge | automatizada | Principal Cloud |
| Claves de firma de evidencias | módulo evidencias | ≤90 d | Principal Backend |

Regla: ningún secreto en repo, en logs ni en tickets; acceso solo vía secrets manager con auditoría (RNF-SEC-004).

## 4. Validación de entrada y protección de datos

- Validación en borde (API) y en dominio; contratos con límites explícitos (Doc 24).
- Cifrado en tránsito (TLS extremo a extremo) y en reposo (DB + SQLCipher móvil).
- Datos personales mínimos por diseño; retención según PD-RETENCIÓN cuando se cierre; registro de accesos a datos sensibles (auditoría Doc 26).

## 5. IA (si aplica en Fase 1)

- Toda función IA pasa por las prohibiciones P-33-1…7 (Doc 33 §4, canónicas): sin decisiones autónomas, cite-or-abstain, service account sin privilegios especiales, línea roja FinOps (coste IA < 30% revenue tenant, Doc 62).
