"""
Auditoria rapida de amaru_fo PDF TOOL.

Crea archivos temporales y valida comandos principales sin tocar documentos reales.
"""

from __future__ import annotations

import argparse
import importlib.util
import tempfile
import zipfile
from pathlib import Path

import fitz

import pdftool


def make_sample_pdf(path: Path) -> None:
    doc = fitz.open()
    for page_number in range(1, 4):
        page = doc.new_page(width=595, height=842)
        page.insert_text((72, 96), f"Documento de auditoria - pagina {page_number}", fontsize=20)
        page.draw_rect(fitz.Rect(72, 140, 520, 260), color=(0.1, 0.4, 0.7), width=1.2)
        page.insert_text((90, 190), "Prueba de texto, render, metadata y seguridad", fontsize=13)
    doc.save(path)
    doc.close()


def make_sample_docx(path: Path) -> None:
        document_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body>
        <w:p><w:r><w:t>Documento Word de auditoria</w:t></w:r></w:p>
        <w:p><w:r><w:t>Texto extraido desde DOCX hacia TXT.</w:t></w:r></w:p>
    </w:body>
</w:document>
"""
        with zipfile.ZipFile(path, "w") as docx:
                docx.writestr("word/document.xml", document_xml)


def require_file(path: Path) -> None:
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(f"No se genero correctamente: {path}")


def run_audit(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = output_dir / "sample.pdf"
    sample_docx = output_dir / "sample_word.docx"
    sample_docx_txt = output_dir / "sample_word.txt"
    sample_pdf_txt = output_dir / "sample.txt"
    numbered = output_dir / "sample_numbered.pdf"
    watermarked = output_dir / "sample_watermark.pdf"
    metadata = output_dir / "sample_metadata.pdf"
    protected = output_dir / "sample_protected.pdf"
    merged = output_dir / "sample_merged.pdf"
    split_dir = output_dir / "split"
    images_dir = output_dir / "rendered"
    images_pdf = output_dir / "sample_from_images.pdf"

    make_sample_pdf(sample)
    make_sample_docx(sample_docx)
    require_file(sample)
    require_file(sample_docx)

    pdftool.cmd_number(sample, numbered, reverse=True)
    pdftool.cmd_watermark(sample, watermarked, "AUDITORIA", opacity=0.18)
    pdftool.cmd_metadata(sample, metadata, title="Auditoria PDF TOOL", author=pdftool.AUTHOR_NAME)
    pdftool.cmd_protect(sample, protected, "clave-auditoria")
    pdftool.cmd_merge([numbered, watermarked], merged)
    split_files = pdftool.cmd_split(sample, split_dir, every=1)
    image_files = pdftool.cmd_pdf_to_images(sample, images_dir, pages_spec="1-2", dpi=120)
    pdftool.cmd_images_to_pdf(image_files, images_pdf)
    pdftool.cmd_files_to_txt([sample_docx, sample], extensions=".docx,.pdf")

    for path in [numbered, watermarked, metadata, protected, merged, images_pdf, sample_docx_txt, sample_pdf_txt, *split_files, *image_files]:
        require_file(path)

    if "Documento Word de auditoria" not in sample_docx_txt.read_text(encoding="utf-8"):
        raise RuntimeError("El TXT generado desde DOCX no contiene el texto esperado")

    protected_doc = fitz.open(protected)
    if not protected_doc.is_encrypted:
        protected_doc.close()
        raise RuntimeError("El PDF protegido no quedo cifrado")
    protected_doc.close()

    print("AUDITORIA OK")
    print(f"Carpeta revisada: {output_dir}")


def check_installation() -> int:
    print("Estado de dependencias:")
    modules = [
        ("fitz", "pymupdf", True),
        ("rich", "rich", True),
        ("pikepdf", "pikepdf", False),
        ("pytesseract", "pytesseract", False),
        ("PIL", "pillow", False),
        ("pymupdf4llm", "pymupdf4llm", False),
        ("docling", "docling", False),
        ("marker", "marker-pdf", False),
    ]
    missing_required = 0
    for module_name, package_name, required in modules:
        present = importlib.util.find_spec(module_name) is not None
        flag = "OK" if present else ("FALTA" if required else "opcional, no instalado")
        marker = " [REQUERIDO]" if required else ""
        print(f"  {package_name:<15s} {flag}{marker}")
        if required and not present:
            missing_required += 1
    tess = pdftool._detect_tesseract_path()
    print(f"  tesseract bin   {'OK ('+tess+')' if tess else 'no encontrado'}")
    if missing_required:
        print(f"FALTAN {missing_required} dependencias requeridas")
        return 1
    print("INSTALACION OK")
    return 0


def run_ai_audit(output_dir: Path) -> None:
    sample = output_dir / "sample.pdf"
    if not sample.exists():
        make_sample_pdf(sample)
    backends_to_try = []
    if pdftool._pymupdf4llm_available():
        backends_to_try.append("pymupdf4llm")
    if pdftool._docling_available():
        backends_to_try.append("docling")
    if pdftool._marker_available():
        backends_to_try.append("marker")
    if not backends_to_try:
        print("Conversion IA: ningun motor instalado, omitido.")
        return
    ai_dir = output_dir / "ai"
    ai_dir.mkdir(parents=True, exist_ok=True)
    for backend in backends_to_try:
        target = ai_dir / backend
        target.mkdir(parents=True, exist_ok=True)
        try:
            outputs = pdftool.cmd_convert_ai(
                [sample], backend=backend, formats="md,json", output_dir=target,
            )
            for output in outputs:
                require_file(output)
            print(f"Conversion IA con {backend}: OK ({len(outputs)} archivos en {target})")
        except Exception as exc:
            print(f"Conversion IA con {backend}: FALLO ({type(exc).__name__}: {exc})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditoria rapida de amaru_fo PDF TOOL")
    parser.add_argument("--output-dir", type=Path, default=None, help="Carpeta donde dejar archivos de auditoria")
    parser.add_argument("--check-installation", action="store_true", help="Verificar que dependencias estan instaladas y salir")
    parser.add_argument("--include-ai", action="store_true", help="Probar tambien conversion IA (pymupdf4llm/Docling/Marker) si estan instalados")
    args = parser.parse_args()

    if args.check_installation:
        return check_installation()

    if args.output_dir:
        run_audit(args.output_dir)
        if args.include_ai:
            run_ai_audit(args.output_dir)
    else:
        with tempfile.TemporaryDirectory(prefix="pdftool_audit_") as temp_dir:
            temp_path = Path(temp_dir)
            run_audit(temp_path)
            if args.include_ai:
                run_ai_audit(temp_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())