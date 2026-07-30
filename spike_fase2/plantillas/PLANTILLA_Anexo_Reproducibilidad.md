# Plantilla — Anexo de Reproducibilidad (REGLA ADICIONAL del Fundador, obligatorio)

**Sin este anexo completo, ninguna métrica de Fase 2 puede fundamentar el cierre de N-2.**

## 1. Versiones de software
| Componente | Versión exacta | Cómo se obtuvo (comando) |
|---|---|---|
| PostgreSQL | | `SELECT version();` |
| PowerSync (A: servicio / B: imagen) | | dashboard / `docker image inspect` |
| Cliente/SDK de medición | | |
| Python / .NET / SO del host de medición | | `python3 --version`, `uname -a` |

## 2. Configuración del entorno
- Archivos usados (copia literal o hash): `entorno_*.env` (sin secretos), `docker-compose.powersync.yml`, `powersync.yaml`, `schema.sql`.
- Región Cloud / topología self-hosted.

## 3. Hardware utilizado
| Host | CPU | RAM | Disco | Red (latencia base a Internet, medida) |
|---|---|---|---|---|
| Medición | | | | `ping` a registro de referencia |
| Servicio B | | | | |

## 4. Scripts ejecutados
Comandos literales en orden, con fecha/hora UTC de cada ejecución.

## 5. Datos brutos
- `resultados_f2.csv` completo (todas las filas, sin filtrar).
- Logs relevantes adjuntos o referenciados (ruta + hash).

## 6. Metodología de medición
- Número de iteraciones, warm-up descartado, intervalos, reloj usado (`time.perf_counter`).
- Cómo se simuló cada corte de red / carga; por qué 10.000 usuarios es SU.

## 7. Limitaciones conocidas
- (Ej.) host de medición compartido; latencia de red doméstica hacia Cloud; escalado simulado.

## 8. Pasos para reproducir
Secuencia numerada desde cero (clonar/copiar carpeta `spike_fase2`, preparar DB, levantar entorno, ejecutar, comparar CSV).

**Verificación:** un tercero con acceso a los mismos entornos debe poder reproducir cada métrica con desviación ≤ ±15%. Si no, la métrica se reclasifica SU.
