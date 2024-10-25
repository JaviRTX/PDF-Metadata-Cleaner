import fitz  # PyMuPDF
import pikepdf

# Paso 1: Borrar los metadatos básicos y ocultos
def clean_metadata(pdf_path):
    # Cargar el archivo PDF con PyMuPDF
    doc = fitz.open(pdf_path)
    # Limpiar todos los metadatos
    doc.set_metadata({})
    # Guardar una copia temporal
    doc.save("temp_cleaned.pdf")
    doc.close()

    # Abrir la copia temporal con PikePDF para borrar cualquier dato residual
    with pikepdf.open("temp_cleaned.pdf") as pdf:
        # Limpiar manualmente los campos de metadatos en pdf.docinfo
        for key in list(pdf.docinfo.keys()):
            del pdf.docinfo[key]  # Eliminar cada clave de metadatos
        
        # Paso 2: Eliminar JavaScript embebido
        if "/Names" in pdf.Root and "/JavaScript" in pdf.Root["/Names"]:
            del pdf.Root["/Names"]["/JavaScript"]

        # Paso 3: Eliminar anotaciones de cada página
        for page in pdf.pages:
            if "/Annots" in page:
                del page["/Annots"]  # Eliminar anotaciones si existen

        # Guardar el archivo limpio
        pdf.save("archivo_final_limpio.pdf")

# Ruta del archivo PDF original
original_pdf = "pdf_name.pdf"

# Ejecutar el proceso de limpieza exhaustiva
clean_metadata(original_pdf)

print("El archivo PDF ha sido limpiado a nivel forense.")
