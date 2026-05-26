# amaru_fo PDF TOOL AMARU

Suite CLI visual para trabajar con PDFs en Windows y Linux: numerar, firmar, unir, dividir, proteger, convertir a texto y generar salidas Markdown/JSON para agentes IA.

- Pagina del autor: <https://amarufo.github.io/PAGE-AIP/>
- GitHub: <https://github.com/amarufo>
- Contacto: amaruf9523@gmail.com

## Que hace

PDF TOOL AMARU esta pensado para trabajo documental de oficina y expedientes: puedes abrir un menu guiado o usar comandos directos. Las funciones principales son:

- Foliar y firmar PDFs con vista previa.
- Unir, dividir, extraer, insertar, rotar y eliminar paginas.
- Agregar marca de agua, editar metadatos, proteger o reconstruir PDFs.
- Convertir PDFs a imagenes e imagenes a PDF.
- Convertir PDF/DOCX a TXT basico.
- Convertir documentos a Markdown y JSON para IA con deteccion automatica de motor.

## Cambios recientes

- Nueva opcion 24: conversion a Markdown/JSON con `auto`, `pymupdf4llm`, `docling` o `marker`.
- Mejor OCR para PDFs escaneados: Docling ahora usa Tesseract con idioma `spa` cuando detecta que el PDF no tiene capa de texto.
- Nuevo backend `pymupdf4llm`: rapido, ligero y recomendado para PDFs digitales.
- `convert-ai` ahora acepta `--ocr auto|on|off` y `--lang spa`.
- Instaladores actualizados por bloques: base, OCR/desbloqueo, IA MIT y Marker GPL-3.
- `run_pdftool.bat` detecta una instalacion existente en `%LOCALAPPDATA%\AmaruFoPdfTool` antes de reinstalar.
- Documentacion consolidada en este README; los documentos antiguos fueron retirados.

## Instalacion rapida

### Windows

1. Descarga o clona este repositorio.
2. Doble clic en `run_pdftool.bat`.
3. Si no hay instalacion previa, el BAT abre `install_windows.bat` automaticamente.
4. El instalador crea el entorno en `%LOCALAPPDATA%\AmaruFoPdfTool` y un acceso directo en el Escritorio.

Tambien puedes ejecutar directamente `install_windows.bat`.

El instalador intenta encontrar Python; si no existe, prueba instalarlo con `winget`. Para OCR en Windows recomienda Tesseract UB-Mannheim: <https://github.com/UB-Mannheim/tesseract>.

### Linux

```bash
chmod +x install_linux.sh run_pdftool.sh
./run_pdftool.sh
```

Si no existe `.venv/`, `run_pdftool.sh` ejecuta el instalador Linux y luego abre el menu.

En Debian/Ubuntu, si falta `venv`:

```bash
sudo apt install python3 python3-venv python3-pip
```

Para OCR del sistema:

```bash
sudo apt install tesseract-ocr tesseract-ocr-spa
```

## Uso basico

Menu interactivo:

```bash
./run_pdftool.sh
```

CLI directa:

```bash
./.venv/bin/python pdftool.py --help
./.venv/bin/python pdftool.py info documento.pdf
```

El banner indica que componentes opcionales estan disponibles:

```text
Motores -> pymupdf4llm: ON  Docling: ON  Marker: off  OCR: ON  pikepdf: ON
```

## Conversion IA a Markdown/JSON

La opcion 24 y el comando `convert-ai` generan Markdown y JSON utiles para lectura humana, busqueda y agentes IA. La seleccion `auto` decide asi:

- PDF escaneado sin capa de texto: usa Docling con OCR Tesseract.
- PDF digital con texto: usa `pymupdf4llm` si esta instalado.
- Si falta `pymupdf4llm`: cae a Docling.
- Marker queda como opcion manual por su licencia GPL-3 y peso de modelos.

Ejemplos:

```bash
# Automatico: recomendado
./.venv/bin/python pdftool.py convert-ai documento.pdf --formats md,json

# PDF escaneado en espanol: forzar OCR Tesseract
./.venv/bin/python pdftool.py convert-ai escaneado.pdf --backend docling --ocr on --lang spa --formats md,json

# PDF digital: motor ligero y rapido
./.venv/bin/python pdftool.py convert-ai digital.pdf --backend pymupdf4llm --formats md,json

# Carpeta recursiva
./.venv/bin/python pdftool.py convert-ai docs/ --recursive --output-dir docs_convertidos

# Marker, solo si aceptas GPL-3 y dependencias pesadas
./.venv/bin/python pdftool.py convert-ai paper.pdf --backend marker --formats md,json
```

Extensiones admitidas por `convert-ai`: `.pdf`, `.docx`, `.pptx`, `.xlsx`, `.html`, `.htm`, `.md`, `.png`, `.jpg`, `.jpeg`, `.tiff`, `.tif`, `.webp`.

## Ejemplo incluido

La carpeta `ejemplo/` contiene un caso real de PDF escaneado y sus resultados:

```text
ejemplo/
  7570263-ra-106-2025.pdf
  7570263-ra-106-2025.txt
  7570263-ra-106-2025.md
  7570263-ra-106-2025.json
```

El TXT se genera con OCR basico. El Markdown y JSON se generan con `convert-ai` usando Docling + Tesseract en espanol, lo que evita el problema de palabras pegadas en PDFs escaneados.

## Comandos frecuentes

```bash
./.venv/bin/python pdftool.py stamp documento.pdf --signature firma.png -o final.pdf --reverse --preview muestra.png
./.venv/bin/python pdftool.py number documento.pdf -o numerado.pdf --corner tr --reverse
./.venv/bin/python pdftool.py sign documento.pdf --signature firma.png -o firmado.pdf --corner br
./.venv/bin/python pdftool.py merge a.pdf b.pdf -o unido.pdf
./.venv/bin/python pdftool.py split documento.pdf -o partes -n 10
./.venv/bin/python pdftool.py extract documento.pdf:1,3-5 -o seleccion.pdf
./.venv/bin/python pdftool.py insert --host base.pdf --guest anexo.pdf --after 5 -o resultado.pdf
./.venv/bin/python pdftool.py rotate documento.pdf -o rotado.pdf --degrees 90 --pages 1,3-5
./.venv/bin/python pdftool.py delete-pages documento.pdf --pages 2,5-7 -o limpio.pdf
./.venv/bin/python pdftool.py compress documento.pdf -o optimizado.pdf
./.venv/bin/python pdftool.py watermark documento.pdf --text "CONFIDENCIAL" -o marcado.pdf
./.venv/bin/python pdftool.py pdf-to-images documento.pdf -o paginas --pages 1-3 --dpi 200
./.venv/bin/python pdftool.py images-to-pdf foto1.png foto2.jpg -o desde_imagenes.pdf
./.venv/bin/python pdftool.py totxt documento.pdf -o documento.txt --ocr --lang spa
./.venv/bin/python pdftool.py files-to-txt carpeta --extensions .docx,.pdf --recursive
./.venv/bin/python pdftool.py convert-ai documento.pdf --backend auto --formats md,json
./.venv/bin/python pdftool.py unlock protegido.pdf -o libre.pdf --password "clave"
./.venv/bin/python pdftool.py protect documento.pdf -o protegido.pdf --password "clave"
./.venv/bin/python pdftool.py metadata documento.pdf -o final.pdf --title "Expediente" --author "amaru_fo"
```

## Dependencias

| Bloque | Archivo | Uso |
|--------|---------|-----|
| Base | `requirements.txt` | PyMuPDF + Rich |
| OCR/desbloqueo | `requirements-optional.txt` | `pytesseract`, Pillow y `pikepdf` |
| IA MIT | `requirements-ai-docling.txt` | `pymupdf4llm` + Docling |
| IA GPL-3 | `requirements-ai-marker.txt` | Marker PDF |

Instalacion manual posterior:

```bash
./.venv/bin/python -m pip install -r requirements-optional.txt
./.venv/bin/python -m pip install -r requirements-ai-docling.txt
./.venv/bin/python -m pip install -r requirements-ai-marker.txt
```

## Auditoria

Verificar dependencias:

```bash
./.venv/bin/python audit_pdftool.py --check-installation
```

Auditoria funcional en carpeta temporal:

```bash
./.venv/bin/python audit_pdftool.py
```

Auditoria con salidas persistentes e IA:

```bash
./.venv/bin/python audit_pdftool.py --output-dir audit_output --include-ai
```

## Estructura del proyecto

```text
ascci.txt                    arte ASCII del banner
audit_pdftool.py             auditoria funcional y verificacion de dependencias
ejemplo/                     PDF real y salidas TXT/MD/JSON de referencia
install_linux.sh             instalador Linux
install_windows.bat          wrapper del instalador Windows
install_windows.ps1          instalador Windows principal
pdftool.py                   CLI principal y menu interactivo
README.md                    documentacion publica
requirements.txt             dependencias base
requirements-optional.txt    OCR y desbloqueo avanzado
requirements-ai-docling.txt  IA MIT: pymupdf4llm + Docling
requirements-ai-marker.txt   IA GPL-3: Marker
run_pdftool.bat              lanzador Windows con instalacion automatica
run_pdftool.sh               lanzador Linux con instalacion automatica
```

## Licencias y notas

- Este repositorio contiene codigo propio de amaru_fo.
- `docling`: MIT.
- `pymupdf4llm`: MIT, pero usa PyMuPDF.
- `pymupdf`: AGPL-3/comercial; revisa compatibilidad si distribuyes en contexto comercial.
- `marker-pdf`: GPL-3. Instalarlo y redistribuirlo puede imponer obligaciones GPL-3.
- `pikepdf`, `pytesseract` y Pillow tienen licencias propias permisivas o copyleft debil segun paquete.
