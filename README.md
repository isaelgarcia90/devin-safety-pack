# Safety Pack: plugin de Devin para software automotriz con evidencia de seguridad

Devin escribe código rápido, pero no trae de fábrica las reglas de seguridad automotriz.
**Safety Pack** es un plugin que hace que Devin trabaje como lo exige la industria:

- **Trazabilidad:** cada función se liga a un requisito (`/* @req REQ-xxx */`).
- **Verificación:** cada requisito tiene al menos un test (`/* @verifies REQ-xxx */`).
- **MISRA C** (Motor Industry Software Reliability Association: reglas para escribir C seguro): las violaciones se corrigen o se justifican.
- **Evidencia en cada PR** (Pull Request, solicitud de cambio): un "Safety Impact Analysis" listo para el auditor.
- **Gate en CI** (Continuous Integration, pruebas que corren solas en cada cambio): si falta evidencia, el cambio se bloquea.

Inspirado en ISO 26262 (norma de seguridad funcional para vehículos) y ASPICE (modelo de calidad de procesos de software automotriz).
**No certifica nada:** genera evidencia para un auditor humano.

## Contenido (formato oficial de plugins de Devin)

| Archivo | Qué hace |
|---|---|
| `.devin-plugin/plugin.json` | Manifiesto del plugin |
| `AGENTS.md` | Regla siempre activa en cada sesión de Devin |
| `skills/trace-matrix` | Matriz requisito → código → test, detecta huecos y los cierra |
| `skills/misra-check` | Corre cppcheck (analizador estático) con reglas MISRA, corrige o documenta desviaciones |
| `skills/safety-pr` | Abre el PR con el Safety Impact Analysis |
| `tools/safety_gate.py` | Gate determinista (falla si falta evidencia) |
| `.github/workflows/safety-gate.yml` | Corre tests y gate en cada cambio |

Los hooks de plugins en Devin son *best effort / fail open* ([docs](https://docs.devin.ai/cli/extensibility/plugins/overview)), por eso el control duro vive en CI y no en un hook.

## Demo con código real

`demo/uds-c` es la librería de diagnóstico vehicular open source [openxc/uds-c](https://github.com/openxc/uds-c)
del proyecto OpenXC de Ford (licencia BSD-3). UDS = Unified Diagnostic Services (ISO 14229), el protocolo de diagnóstico de los autos.

- **Antes (`main`):** 0/10 requisitos trazados, 72 violaciones MISRA sin documentar → gate en rojo.
- **Después (PR):** Devin con el plugin traza 10/10 requisitos, escribe los tests que faltaban y documenta las desviaciones MISRA → gate en verde.

## Instalar

```bash
devin plugins install isaelgarcia90/devin-safety-pack
```
Luego en una sesión: `/safety-pack:trace-matrix demo/uds-c`.

## Correr el gate localmente

```bash
sudo apt-get install -y cppcheck check
(cd demo/uds-c && make test)
python3 tools/safety_gate.py --project demo/uds-c --out safety-report
```

## Roadmap
- Calificación de herramienta (ISO 26262-8) y reportes en formato de auditor.
- Mismo enfoque para aeroespacial (DO-178C) y dispositivos médicos (IEC 62304).
