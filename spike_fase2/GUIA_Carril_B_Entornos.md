# Guía Carril B — Habilitación de entornos (para el Fundador)

Tiempo estimado total: **45–75 min** (A: ~15 min; B: ~30–60 min según familiaridad con Docker).

## Entorno A — PowerSync Cloud (~15 min)

1. Crear cuenta gratuita en el dashboard de PowerSync (buscar "PowerSync dashboard signup"; verificar la URL oficial en ese momento — SU hasta confirmar).
2. Crear un proyecto/instancia nueva, nombre sugerido `donefixer-spike-f2`. Registrar **región** y **versión del servicio** (van al Anexo de Reproducibilidad).
3. Conectar la base de datos fuente: usar un PostgreSQL con `wal_level=logical` (puede ser el mismo compose del Entorno B levantado solo con el servicio `postgres`, o una instancia suya). Ejecutar `spike/harness/schema.sql` y el seed J-2.
4. Desplegar las Sync Rules (mismo contenido que `config/powersync.yaml`, sección `sync_rules`; validar la sintaxis contra la documentación oficial vigente — la plantilla es de referencia, clasificada SU).
5. Generar un **token de desarrollo** en el dashboard.
6. Copiar endpoint y token a `config/entorno_a_cloud.env`.
7. Verificación: `curl -H "Authorization: Bearer <token>" https://<instancia>/write-checkpoint2` debe responder JSON.

## Entorno B — PowerSync Self-Hosted (~30–60 min)

Requisito: Docker (o Docker Desktop / una VM con Docker). Sin Docker no hay Entorno B.

1. Copiar la carpeta `spike_fase2/config/` a la máquina con Docker.
2. Fijar el tag exacto de la imagen en `docker-compose.powersync.yml` (sustituir `latest` por el tag vigente; registrarlo en el Anexo).
3. Generar par de claves para tokens y completar `powersync.yaml` (sección `api.tokens`).
4. `docker compose -f docker-compose.powersync.yml up -d`
5. Aplicar `schema.sql` y el seed J-2 al Postgres del compose (puerto 5433).
6. Generar un JWT de prueba firmado con la clave privada; copiarlo a `config/entorno_b_selfhosted.env` junto con `PS_ENDPOINT=http://localhost:8080`.
7. Verificación: `curl http://localhost:8080/probe/liveness` responde OK.

## Ejecución de la batería (la realizo yo cuando ambos entornos estén listos)

Con los dos archivos `.env` completados, ejecuto por entorno:

```
set -a; source config/entorno_X.env; set +a
python3 harness_f2/test_j2_f2.py
python3 scripts/medicion.py latencia --iteraciones 50
# … resto de la batería F2 (chaos, carga, long-running) según SPIKE_F2_S1 §5
```

y completo los 10 entregables + Anexo de Reproducibilidad. **Los resultados se presentan a revisión del Fundador antes de cerrar N-2** (condición de EXENCIÓN-SPIKE-01).

## Precauciones

- Los `.env` con tokens reales **no** se copian a documentos; en el Anexo solo van huellas/identificadores.
- La sintaxis de `sync_rules` de la plantilla es de referencia (SU): confirmarla contra la documentación oficial de la versión instalada el día de la ejecución, y registrar la versión consultada.
