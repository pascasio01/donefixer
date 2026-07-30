# 60 — Security & Compliance Plan

| Campo | Valor |
|---|---|
| Documento | 60_Security_Compliance_Plan |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Precedencia | Doc 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | Docs 12 (RNF-SEC/PRV), 26 (aislamiento), 25 (clasificación), 19 (RBAC/ABAC), ADR-012 (régimen crítico), 32/33 (IA), MASTER_PROMPT §SEGURIDAD |

> Principios rectores (DC, MASTER_PROMPT): Zero Trust · Least Privilege · Defense in Depth · Secure by Default · Secrets Management · Encryption at Rest/in Transit · Immutable Audit Logs.

---

## 1. Postura de seguridad por capas (defense in depth)

| Capa | Controles | Trazabilidad |
|---|---|---|
| Transporte | TLS 1.3 en todo extremo (RNF-SEC-001); HSTS; cert pinning en móvil (SU) | DC |
| Identidad | OIDC/OAuth 2.1, tokens corta vida, revocación por dispositivo, MFA admins (RNF-SEC-004/005) | DC |
| Autorización | RBAC+ABAC (Doc 19); servidor siempre re-valida (ADR-011); prohibiciones IA como ausencia de permisos | DC |
| Datos | Clasificación 4 niveles (Doc 25); AES-256 en reposo (RNF-SEC-002); SQLCipher local (RNF-SEC-003); RLS + filtro aplicación (MT-3) | DC |
| Aplicación | Input validation, output encoding, CSP, security headers (WA-8); rate limiting por tenant (RNF-SCL-003) | DC |
| Auditoría | Hash-encadenada inmutable, 100% eventos de seguridad y negocio (RNF-SEC-009); 10 campos (ADR-012) | DC |

## 2. STRIDE Threat Modeling

Modelo de amenazas por flujo crítico (metodología STRIDE), a mantener vivo — revisión por release mayor y al añadir módulos. (DC)

| Flujo | Amenaza STRIDE dominante | Mitigación arquitectónica |
|---|---|---|
| Pipeline tenant (JWT→RLS) | **Elevation of privilege** (cruce de tenant) | Defensa en profundidad (MT-3), `set_config` transaccional, batería de ataques en CI (RNF-SEC-006), RB-04 |
| Write-path sync | **Tampering / Repudiation** (operaciones manipuladas, repudio de acciones offline) | Idempotencia por `operation_id`, HLC, firma de dispositivo, veredictos auditados, evidencias con SHA-256 (RF-WO-003/007) |
| Intake público (RF-REQ-001) | **Denial of service** (abuso de formulario anónimo) | Rate limiting por IP/tenant, CAPTCHA adaptativo (SU), cuotas |
| Webhooks salientes | **Spoofing** (receptores falsos/replay) | HMAC-SHA256, secreto rotativo, timestamps (IN-4) |
| Subida de evidencias | **Tampering/DoS** (malware, archivos gigantes) | URLs firmadas, validación tipo/tamaño, escaneo (SU Etapa B), hash en captura |
| AI Gateway | **Information disclosure** (fuga a proveedor) | Enmascaramiento PII, niveles de datos, retención cero (AIA-4, PD-IA-1), P-33-6/7 |
| Consola de plataforma | **Elevation of privilege** (acción crítica indebida) | Régimen Fase 0-1: MFA+reauth+motivo+log inmutable+confirmación+rollback (ADR-012 §3.9) |

## 3. Supply Chain Security & SBOM

- **SBOM** (SPDX o CycloneDX) generado en cada build de cada artefacto (backend, web, móvil) y archivado con la release. (DC)
- Dependencias: pin de versiones, revisión de licencias, SCA en pipeline con bloqueo en críticas (RNF-SEC-007).
- **Dependency Governance:** nueva dependencia requiere justificación (problema que resuelve, alternativas, mantenimiento, licencia) — misma disciplina que tecnologías (condición permanente 2 Ola 3); revisión trimestral de dependencias abandonadas. (DC)
- Verificación de firma/procedencia de imágenes base de contenedores; builds reproducibles como objetivo Etapa B (SU).

## 4. Secret Management & Rotation

| Elemento | Política |
|---|---|
| Almacenamiento | Gestor de secretos del proveedor cloud; prohibido en código/CI logs/repositorio (RNF-SEC-007 escaneo) |
| Rotación | Secretos de servicio: ≤90 días automatizada; secreto de webhooks: rotativo por tenant (IN-4); claves de cifrado: rotación anual con re-cifrado planificado |
| Acceso | Least privilege; acceso humano a secretos de producción excepcional, con justificación y registro (régimen ADR-012) |
| Revocación | Runbook de compromiso: revocar→rotar→auditar (RB-04/RB-08) |

## 5. Vulnerability Management

| Actividad | Frecuencia | Criterio |
|---|---|---|
| SCA (dependencias) | Cada PR + escaneo diario | Críticas bloquean; altas ≤7 días |
| SAST | Cada PR | Críticas bloquean |
| DAST | Semanal contra staging | Altas ≤14 días |
| Pentest externo | Pre-lanzamiento + anual (RNF-SEC-008, SU) | Hallazgos con plan de remediación |
| Parches de SO/imágenes | Mensual o por CVE crítico | Ventana ≤30 días (críticos ≤72 h) |

## 6. Compliance Readiness (roadmap honesto)

| Marco | Estado Etapa A | Camino |
|---|---|---|
| OWASP ASVS | **Objetivo de diseño:** controles mapeados a ASVS L2 en el Doc 47 (security gates) | Verificación formal con pentest |
| SOC 2 Type I | Readiness: controles documentados (acceso, cambio, operación, incidentes) | Auditoría cuando haya clientes que lo exijan (Etapa B, costo SU) |
| SOC 2 Type II | Período de observación 3–12 meses tras Type I | Etapa B/C |
| ISO 27001 | Readiness parcial (SGSI informal: riesgos, controles, postmortems) | Certificación Etapa C |
| Privacidad (leyes de países piloto, PD-3) | RNF-PRV-001…005 operativos; registro de subprocesadores (RNF-PRV-005) | Evaluación legal con N-3/PD-3 |

> **Regla de honestidad (DC):** se comunica "readiness", nunca certificación no obtenida. Toda afirmación comercial de cumplimiento requiere evidencia.

## 7. Seguridad de IA (resumen normativo)

Prohibiciones P-33-1…7 como tests de permisos (RNF-AI-003); agentes como Service Accounts (AIA-2); cite-or-abstain (RNF-AI-001); evaluación con umbral de apagado (AIA-7); gobierno completo en Doc 33. (DC)

## 8. Criterios de aceptación del documento

1. Incluye los 6 elementos de la ampliación obligatoria (STRIDE, supply chain, SBOM, rotación, vulnerabilidades, dependency governance). ✅
2. Coherente con RNF-SEC/PRV y ADR-012. ✅
3. Compliance expresado como readiness con camino — sin afirmaciones no obtenidas. ✅

---

*Registro de cambios — v1.0 (2026-07-29): creación (Ola 4, documento 6 de 8) con las ampliaciones obligatorias del Fundador.*
