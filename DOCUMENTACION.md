# Documentacion tecnica del proyecto

## 1. Objetivo

El proyecto se utilizo para practicar el flujo basico de trabajo con Git y
GitHub, y posteriormente para configurar un proceso automatico de calidad
para una aplicacion pequena de Python.

El proceso final realiza estas tareas:

1. Descarga el codigo del repositorio.
2. Configura Python.
3. Instala las dependencias.
4. Revisa el codigo con Ruff.
5. Ejecuta las pruebas con pytest.
6. Construye una imagen Docker.
7. Publica la imagen en GitHub Container Registry (GHCR).

## 2. Estructura relevante

```text
miweb/
|-- .github/
|   `-- workflows/
|       `-- test_and_build.yaml
|-- src/
|   |-- main.py
|   |-- test.py
|   `-- requirements.txt
|-- Dockerfile
|-- DOCUMENTACION.md
`-- README.md
```

### `src/main.py`

Contiene la clase `calculator` y el metodo `sum(a, b)`, que devuelve la suma
de dos numeros.

### `src/test.py`

Contiene una prueba automatizada que verifica que `sum(2, 2)` devuelva `4`.

### `src/requirements.txt`

Lista las herramientas necesarias para trabajar con el proyecto:

```text
pytest==8.3.4
ruff==0.16.7
```

### `Dockerfile`

Define la imagen de Python que se construye en GitHub Actions. Instala las
dependencias, copia el contenido de `src` y deja pytest como comando por
defecto del contenedor.

## 3. GitHub Actions

El workflow esta en `.github/workflows/test_and_build.yaml` y se llama
`Test and build`.

### Cuando se ejecuta

- Cuando se hace `push` a `main`.
- Cuando se crea o actualiza un Pull Request hacia `main`.
- Cuando se ejecuta manualmente con `workflow_dispatch`.

Por eso los cambios deben llegar a GitHub mediante `git push`; los cambios
locales no aparecen en la pestaña **Actions** hasta estar publicados en el
repositorio remoto.

### Permisos

El workflow utiliza:

```yaml
permissions:
  contents: read
  packages: write
```

`contents: read` permite descargar el codigo del repositorio. `packages:
write` permite publicar la imagen en GHCR usando `GITHUB_TOKEN`.

### Version de las acciones

Se utilizan estas acciones:

- `actions/checkout@v5` para descargar el repositorio.
- `actions/setup-python@v6` para instalar Python 3.13.
- `docker/login-action@v4` para iniciar sesion en GHCR.
- `docker/build-push-action@v7` para construir y publicar la imagen.

Se actualizaron `checkout` y `setup-python` porque las versiones anteriores
usaban Node.js 20 y GitHub mostraba una advertencia de obsolescencia. Las
versiones actuales utilizan Node.js 24.

### Orden del pipeline

El job `test_and_build` se ejecuta en `ubuntu-latest` y realiza los pasos en
este orden:

```text
checkout
    -> configurar Python 3.13
    -> instalar dependencias
    -> ejecutar Ruff
    -> ejecutar pytest
    -> iniciar sesion en GHCR
    -> construir y publicar la imagen
```

Si Ruff o pytest fallan, el workflow se detiene y no intenta publicar la
imagen. Esto evita publicar una imagen de una version que no cumple los
controles de calidad.

## 4. Correcciones realizadas

### Workflow YAML

El workflow original tenia problemas de sintaxis e indentacion. Se corrigio
la estructura de `on`, `jobs`, `permissions` y los pasos del job.

Tambien se corrigieron estos aspectos:

- La rama se declaro correctamente como `main`.
- Se agrego la ejecucion para Pull Requests.
- Se agrego la ejecucion manual.
- Se indico la ruta correcta de dependencias: `src/requirements.txt`.
- Las pruebas se ejecutan dentro de `src`.
- Se agregaron permisos para publicar paquetes.

### Prueba intencionalmente fallida

Durante la demostracion inicial, `calculator.sum()` devolvia `0` aunque la
prueba esperaba `4`. Esto se dejo intencionalmente para comprobar que Actions
detectara un fallo real.

Despues se corrigio el metodo para devolver:

```python
return a + b
```

### Ruff

Ruff detecto inicialmente un import de `os` que no se utilizaba y problemas
de formato en los bloques de imports. Esos problemas fueron corregidos.

La verificacion actual se ejecuta con:

```powershell
ruff check src
```

## 5. Docker y GHCR

### Problema del nombre de la imagen

Se intento publicar una imagen con este nombre:

```text
ghcr.io/HaroldM126/inicio:latest
```

Docker rechazo el nombre porque los repositorios de imagen deben usar
minusculas. El nombre correcto es:

```text
ghcr.io/haroldm126/inicio:latest
```

### Problema del Dockerfile inexistente

Docker intento abrir `Dockerfile`, pero el archivo no estaba guardado con ese
nombre exacto. En sistemas Linux se diferencian las mayusculas y minusculas,
por lo que `DOCKERFILE`, `dockerfile` y `Dockerfile` son nombres distintos.

Se dejo el archivo con el nombre exacto `Dockerfile` en la raiz del proyecto.

### Problema del Dockerfile vacio

Despues de encontrar el archivo, Docker informo que estaba vacio. Se agrego
una configuracion basada en `python:3.13-slim`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY src/requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY src/ ./

CMD ["python", "-m", "pytest", "test.py"]
```

## 6. Ejecucion local

Instalar las dependencias:

```powershell
python -m pip install -r src/requirements.txt
```

Ejecutar Ruff:

```powershell
ruff check src
```

Ejecutar las pruebas:

```powershell
python -m pytest src/test.py
```

Construir la imagen localmente, si Docker esta instalado y ejecutandose:

```powershell
docker build -t ghcr.io/haroldm126/inicio:latest .
```

Ejecutar las pruebas dentro del contenedor:

```powershell
docker run --rm ghcr.io/haroldm126/inicio:latest
```

## 7. Flujo para publicar cambios

Desde la rama `main`:

```powershell
git add .github/workflows/test_and_build.yaml Dockerfile src/main.py src/test.py src/requirements.txt DOCUMENTACION.md
git commit -m "Documentar pipeline y corregir construccion Docker"
git push origin main
```

Despues del `push`, GitHub mostrara la ejecucion en **Actions**. Si todos los
pasos terminan correctamente, la imagen quedara publicada como:

```text
ghcr.io/haroldm126/inicio:latest
```

## 8. Estado esperado

El estado correcto del proyecto es:

- Ruff sin errores.
- La prueba de suma aprobada.
- El Dockerfile presente y no vacio.
- El nombre de la imagen en minusculas.
- El workflow con permisos para escribir paquetes.
- El job de Actions terminado correctamente.

Los avisos locales relacionados con `.pytest_cache` no representan un fallo
del codigo ni del workflow; son advertencias de permisos de la cache local de
pytest.
