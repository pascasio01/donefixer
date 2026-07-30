# Onboarding técnico — nuevo desarrollador (objetivo: productivo en WP el mismo día del GO)

**Norma:** Sprint 0 Execution v1.0 · Requisito previo de gobernanza: el proyecto ha recibido GO del Documento 70 (WP-00).

## Día 1 mañana — contexto (obligatorio, sin excepciones)

1. Leer en este orden: `00_Indice_Maestro_y_Constitucion.md` (reglas 1–7) → `ADI_Architecture_Decision_Index.md` (estados DC/SU/PD y PDs abiertas) → `REGISTRY_Canonical_Identifiers.md` (cómo citar IDs sin inventarlos) → `gobernanza_ejecucion/01` §§1–5 (cómo se trabaja).
2. Comprender las 5 líneas rojas: (a) la documentación manda sobre el código; (b) ningún WP sin DoR; (c) autor ≠ aprobador; (d) test de ataque RLS y suite J-2 indesactivables; (e) prohibiciones IA P-33 (Doc 33 §4).

## Día 1 tarde — entorno

```bash
git clone <repo> && cd donefixer
cp infra/env/.env.template infra/env/.env.development   # rellenar desde secrets manager (acceso lo da DevOps)
dotnet restore backend/DoneFixer.sln && dotnet build backend -c Debug
npm ci --prefix web
docker compose -f infra/dev-compose.yml up -d            # PostgreSQL 16 local con wal_level=logical
scripts/dev_check.sh                                     # linters + migraciones + tests rápidos
```

Verificación de entorno OK cuando `dev_check.sh` termina en verde, incluyendo el test de ataque RLS local.

## Día 2 — primer contacto con el flujo

1. Ejercicio guiado: WP de práctica (documentación) — abrir rama `chore/WP-A0-onboarding`, PR con checklist completo, recibir revisión. Se mergea solo si la verificación de integridad pasa.
2. Leer su primer WP real asignado: WBS (16 campos), DoR, matriz de pruebas aplicable.
3. Conocer su responsable de área (RACI) y el canal de preguntas de arquitectura (las dudas de norma se resuelven contra el corpus, no por opinión).

## Accesos (los gestiona DevOps/SRE el día 0)

- [ ] Repo (rol write, sin push a ramas protegidas) · [ ] Secrets manager (solo development) · [ ] Dashboards (lectura) · [ ] Tableros · [ ] Canal de incidentes (lectura; guardia solo tras 1 mes)

## Lo que NO debe hacer nunca

- Abrir trabajo sin DoR · pushear a develop/main · desactivar un gate · pegar secretos o datos de tenants en herramientas externas (incluidas IAs, POL-EGM-15) · crear IDs documentales fuera del Registry · modificar un ADR aprobado (se supersedes con uno nuevo).
