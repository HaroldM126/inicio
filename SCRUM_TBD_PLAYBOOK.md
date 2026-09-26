# Scrum + TBD Playbook: Guía Operativa del Equipo
**Proyecto:** miweb (Calculadora / API de Servicios)  
**Versión:** 1.0 - Adaptación a Trunk-Based Development y Continuous Deployment  
**Facilitador / Autor:** Harold M  

---

## 1. Principios Acordados (Las 5 Reglas del Equipo)
1. **La rama `main` es sagrada y siempre releasable:** El código en `main` debe compilar, superar las pruebas automatizadas y estar listo para producción en todo momento.
2. **Ramas efímeras (Short-lived branches):** Ninguna rama de feature puede vivir más de 24 horas sin integrarse a `main`. Si una tarea toma más tiempo, debe dividirse en sub-tareas más pequeñas.
3. **Lotes pequeños (Small Batches):** Favorecemos Pull Requests pequeños (menos de 200–300 líneas de código). Son más fáciles de revisar, no generan conflictos y reducen el riesgo.
4. **Desacoplar Despliegue de Lanzamiento:** Desplegar a producción es un proceso técnico continuo y automatizado; liberar la funcionalidad al usuario final es una decisión de negocio mediante **Feature Toggles (Feature Flags)**.
5. **Cultura "Stop the Line" (Paren las máquinas):** Si el pipeline de `main` se rompe, la prioridad absoluta de todo el equipo es devolver `main` a verde antes de mergear cualquier otro cambio.

---

## 2. Roles Adaptados a TBD + CD

### Product Owner (PO)
* **Responsabilidad:** Prioriza no solo por valor de negocio, sino considerando el riesgo de despliegue y el tamaño del lote.
* **Práctica clave:** Participa activamente en el rebanado vertical (*story slicing*) y administra el ciclo de vida de los Feature Flags (cuándo encender, apagar o retirar un toggle).
* **Compromiso:** *"Diseñaré historias que puedan desplegarse de forma incremental en producción mediante Feature Flags sin esperar al final del sprint."*

### Developers
* **Responsabilidad:** Ownership colectivo del pipeline de CI/CD y estabilidad de `main`.
* **Práctica clave:** Integración diaria a `main`, desarrollo guiado por pruebas (TDD o tests rigurosos en Pytest) y revisión prioritaria de PRs.
* **Compromiso:** *"Ninguna rama mía vivirá más de un día. Priorizaré revisar los PRs de mis compañeros sobre escribir código nuevo."*

### Scrum Master
* **Responsabilidad:** Facilitar la disciplina de integración continua y eliminar las fuentes de fricción y miedo al despliegue.
* **Práctica clave:** Monitorear métricas de flujo (Lead Time, Cycle Time, salud del CI) y asegurar que el equipo tenga tiempo para mejorar la infraestructura y pruebas.
* **Compromiso:** *"Protegeré al equipo para que arreglar un pipeline en rojo sea la tarea prioritaria y velaré por que no existan bloqueos en las revisiones de código."*

---

## 3. Reglas de Oro de Integración a Main
* **Branch Protection:** La rama `main` está protegida en GitHub. Requiere al menos 1 revisión aprobada y que todos los checks de CI (`ruff` y `pytest`) estén en verde.
* **Tiempo de revisión:** Un PR debe ser revisado en un máximo de 2 a 4 horas laborales tras ser solicitado.
* **Límite de tamaño:** Máximo 300 líneas de cambio por PR (excluyendo migraciones o autogenerados).
* **Feature Flag obligatorio:** Todo código que represente trabajo en progreso (WIP) o funciones incompletas debe entrar a `main` protegido por un Feature Toggle apagado por defecto.
* **Regla de los 10 minutos:** Si un cambio en `main` genera fallas en producción o en el CI, el equipo tiene 10 minutos para corregirlo; si no, se ejecuta un `git revert` inmediato.

---

## 4. Definition of Done (DoD) Preliminar

Una historia o tarea se considera **DONE (Terminada)** únicamente cuando satisface:

### Criterios Técnicos
- [ ] Código escrito siguiendo los estándares de estilo del proyecto (aprobado por `ruff check .`).
- [ ] Pruebas unitarias e integración añadidas en `src/test.py` (ejecutadas con éxito en `pytest`).
- [ ] PR revisado y aprobado por un compañero.
- [ ] Merge realizado a la rama `main`.
- [ ] Pipeline de GitHub Actions ejecutado en verde (test + build de imagen Docker en GHCR).
- [ ] Despliegue completado a producción o imagen publicada y lista para correr.
- [ ] Feature Toggle registrado (ej. en ConfigCat o variable de entorno) si la función no es pública aún.

### Criterios de Negocio
- [ ] Criterios de aceptación verificados activando el Feature Flag para usuarios internos o de prueba.
- [ ] Telemetría o logs mínimos agregados para monitorear el uso o fallas de la nueva funcionalidad.

---

## 5. Adaptación de Artefactos y Ceremonias

| Ceremonia / Artefacto | Versión Tradicional | Adaptación TBD + CD |
| :--- | :--- | :--- |
| **Product Backlog** | Historias de usuario grandes de 1 a 2 semanas. | Historias rebanadas (*vertical slices*) con estrategia de Feature Flag y criterios validables en producción. |
| **Sprint Backlog** | Lista estática de tareas comprometidas para el sprint. | Flujo continuo de micro-tareas orientadas a integrarse a `main` el mismo día. |
| **Incremento** | Paquete de software entregado al final de las 2 semanas. | **Cualquier commit en `main` que pase CI** es un incremento potencialmente puesto en producción. |
| **Daily Scrum** | "¿Qué hice ayer? ¿Qué haré hoy? ¿Qué me bloquea?" | **"¿Qué voy a integrar hoy a main y qué necesito para que sea seguro?"** |
| **Sprint Review** | Demostración en local o staging con datos simulados. | Demostración en producción real activando Feature Toggles ante los interesados y mostrando telemetría real. |
| **Sprint Retrospective** | Conversaciones generales sobre el proceso. | Inspección de la salud del pipeline, tiempo de ciclo de los PRs y frecuencia de integración a `main`. |

---

## 6. Caso Práctico de Story Slicing (Calculadora / API)

* **Historia General:** *"Como usuario, quiero calcular el interés compuesto de mis inversiones para proyectar mis ganancias a futuro."*
* **Slices para Trunk-Based Development:**
  1. **Slice 1 (Lógica de Negocio en Backend):** Crear la función matemática de interés compuesto y sus pruebas en `src/test.py`. Mergeado a `main` el día 1, cubierto bajo flag `FEATURE_INTERES_COMPUESTO=false`.
  2. **Slice 2 (Exposición de Interfaz / Endpoint):** Conectar la función al CLI o endpoint REST. Desplegado a `main` el día 2; activado solo para el equipo de desarrollo y QA en producción vía ConfigCat.
  3. **Slice 3 (Liberación y Telemetría):** Agregar métricas de cálculo y activar el Feature Flag al 100% de los usuarios. Retirar el Feature Toggle del código (limpieza técnica).

---

## 7. Decisiones Pendientes y Hoja de Ruta Tecnológica
* **Herramienta de Feature Flags:** Implementar **ConfigCat** (plan gratuito) o un gestor liviano por variables de entorno para controlar la visibilidad de nuevas operaciones.
* **Continuous Deployment (CD):** Completar el paso final del pipeline `ci.yaml`: no solo generar la imagen Docker en GHCR, sino gatillar el despliegue automático a un servidor (Render, Railway, AWS o Kubernetes).
* **Métricas DORA:** Configurar la medición de *Deployment Frequency* y *Lead Time for Changes* utilizando GitHub Insights o herramientas como Apache DevLake.
