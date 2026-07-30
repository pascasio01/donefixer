# Anexo de Reproducibilidad — N-1 (medición en dispositivo)

Misma disciplina que la REGLA ADICIONAL del Fundador para Fase 2: **sin este anexo completo, ninguna métrica fundamenta ADR-013.**

## 1. Versiones de software
| Componente | Versión exacta | Comando |
|---|---|---|
| Flutter SDK | | `flutter --version` |
| RN / Expo SDK | | `npx expo --version`, package.json |
| Android del dispositivo | | Ajustes → Acerca del teléfono |
| Backend Spike | | hash de archivos del harness |

## 2. Hardware
| Dispositivo | Modelo | RAM | SoC | SO | Batería inicial |
|---|---|---|---|---|---|
| (el MISMO para ambas apps) | | | | | |

## 3. Configuración
Build release de ambas (comandos literales), mismo backend por Wi-Fi local, misma red, mismo guion J-2, mismo orden de ejecución (Flutter → RN, mismo día). Prohibido comparar builds debug.

## 4. Scripts ejecutados
Comandos ADB / CLI literales con fecha-hora UTC de cada medición.

## 5. Datos brutos
`metricas_n1_*.csv` de cada app (export del MetricsLogger), salidas de `dumpsys meminfo`, `top`, Battery Historian, `cloc`, tamaños de APK — adjuntos o referenciados con hash.

## 6. Metodología
3 mediciones de arranque en frío (app matada entre cada una), promedio; muestreo de CPU cada 2 s durante sync; batería en ventana de 2 h de uso mixto J-2 + sync periódica.

## 7. Limitaciones conocidas
Un solo modelo de dispositivo (gama media); red Wi-Fi local no representa latencia celular; batería en ventana corta. Métricas afectadas → SU donde aplique.

## 8. Pasos para reproducir
Secuencia numerada desde `git`-like snapshot de `spike/` hasta la comparación de CSV. Criterio: desviación reproducible ≤ ±15 %; si no, reclasificar a SU.
