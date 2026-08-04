

# LlmOcr

[English](README.md) | [中文](README.zh-CN.md)

LlmOcr es una herramienta ligera de OCR para facturas desarrollada con Streamlit y la API del modelo de visión y lenguaje Qwen. Extrae campos estructurados de imágenes de facturas, admite procesamiento por lotes y permite a los usuarios descargar los resultados en archivos CSV, Excel o JSON.

El proyecto está diseñado para flujos de trabajo prácticos y pequeños de procesamiento de documentos donde los usuarios desean una interfaz web sencilla, implementación con Docker y una lógica de extracción reproducible.

## Características

- Extrae la fecha de la factura, el monto, el número de factura, el número de vehículo, la hora de recogida y la hora de entrega a partir de imágenes de facturas.
- Admite cargas por lotes de archivos JPG, JPEG y PNG.
- Exporta los resultados en formato CSV, Excel (`.xlsx`) o JSON.
- Proporciona una interfaz web con Streamlit.
- Admite implementación con Docker y Docker Compose.
- Lee la clave API de Qwen desde variables de entorno en lugar de codificar secretos directamente en el código.

## Requisitos

### API de Qwen

Necesitas una clave API válida de Qwen desde Alibaba Cloud DashScope:

https://dashscope.console.aliyun.com/apiKey

Establécela como la variable de entorno `QWEN_API_KEY` antes de ejecutar la aplicación.

### Implementación con Docker

- Docker Desktop para Windows/macOS, o Docker Engine con Docker Compose en Linux.

### Implementación local con Python

- Se recomienda Python 3.12 o una versión más reciente.
- `pip` para instalar las dependencias de Python.

## Inicio rápido

### Opción 1: Docker Compose

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Albert7519/LlmOcr.git
   cd LlmOcr
   ```

2. Crea un archivo local `.env`:

   ```bash
   cp .env.example .env
   ```

3. Edita `.env` y establece tu clave API real de Qwen:

   ```env
   QWEN_API_KEY=your_qwen_api_key_here
   ```

4. Construye e inicia la aplicación:

   ```bash
   docker-compose up -d --build
   ```

5. Abre la aplicación web:

   ```text
   http://localhost:8502
   ```

### Opción 2: Docker Run

Descarga la imagen precompilada:

```bash
docker pull albert151/llmocr:latest
```

Establece tu clave API:

```bash
export QWEN_API_KEY="your_qwen_api_key_here"
```

Ejecuta el contenedor:

```bash
docker run -d --name LlmOcr_run -p 8502:8502 -e QWEN_API_KEY="$QWEN_API_KEY" --restart always albert151/llmocr:latest
```

Para Windows PowerShell:

```powershell
$env:QWEN_API_KEY = "your_qwen_api_key_here"
docker run -d --name LlmOcr_run -p 8502:8502 -e QWEN_API_KEY=$env:QWEN_API_KEY --restart always albert151/llmocr:latest
```

### Opción 3: Python local

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Albert7519/LlmOcr.git
   cd LlmOcr
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   En Windows:

   ```cmd
   venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Establece tu clave API de Qwen:

   ```bash
   export QWEN_API_KEY="your_qwen_api_key_here"
   ```

5. Ejecuta la aplicación:

   ```bash
   streamlit run app.py
   ```

6. Abre la URL local que muestra Streamlit, generalmente:

   ```text
   http://localhost:8502
   ```

## Uso

1. Abre la aplicación en ejecución en un navegador.
2. Selecciona el formato de salida: CSV, Excel o JSON.
3. Carga una o más imágenes de facturas en formato JPG, JPEG o PNG.
4. Visualiza la vista previa de las imágenes cargadas.
5. Haz clic en el botón de extracción.
6. Revisa la tabla extraída y las estadísticas de procesamiento.
7. Descarga los resultados en el formato seleccionado.

## Solución de problemas con Docker

- Si `http://localhost:8502` no es accesible, revisa los registros (logs) del contenedor:

  ```bash
  docker logs LlmOcr
  ```

  o, para el contenedor de `docker run`:

  ```bash
  docker logs LlmOcr_run
  ```

- Asegúrate de que Docker Desktop o Docker Engine esté en ejecución.
- Si otro dispositivo en la misma red no puede acceder a la aplicación, verifica las reglas del firewall para el puerto TCP `8502`.
- Para acceder desde otro dispositivo, utiliza la IP de red local de la máquina anfitrión, por ejemplo `http://192.168.x.x:8502`.

## Notas sobre seguridad y privacidad

- No hagas commit de claves API ni de archivos `.env` reales.
- No codifiques `QWEN_API_KEY` directamente en el código fuente.
- Ten cuidado al cargar facturas o documentos que contengan información personal o empresarial sensible.
- La aplicación envía las imágenes cargadas al punto final de la API de Qwen configurado para realizar inferencias. No la utilices para documentos que no puedan ser procesados por una API externa.

## Notas para mantenedores

Actualmente, este es un proyecto de código abierto con un solo mantenedor. Los issues y pull requests son bienvenidos si incluyen suficiente contexto para reproducir el comportamiento.

Las áreas de contribución útiles incluyen:

- correcciones de implementación y Docker;
- mejoras en los prompts de extracción;
- pruebas para el análisis y el comportamiento de exportación de CSV;
- mejoras en la interfaz de usuario para la carga, el manejo de errores y la descarga de resultados;
- actualizaciones de documentación para la configuración y la solución de problemas.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta [LICENSE](LICENSE) para más detalles.
