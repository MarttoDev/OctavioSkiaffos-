import os
from PIL import Image, ImageOps

# --- CONFIGURACIÓN ---
INPUT_FOLDER = 'img'       
OUTPUT_FOLDER = 'optimizadas_web'
MAX_WIDTH = 2560           
QUALITY_VAL = 85           

print(f"🚀 Iniciando optimización recursiva (buscando en subcarpetas de '{INPUT_FOLDER}')...")
print("-" * 50)

procesadas = 0
errores = 0

# os.walk permite "caminar" por todo el árbol de carpetas
for root, dirs, files in os.walk(INPUT_FOLDER):
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            try:
                # Ruta completa del archivo original
                input_path = os.path.join(root, filename)
                
                # Calcular la estructura de carpetas para replicarla en la salida
                # Si original está en 'img/bodas', relative_path será 'bodas'
                relative_path = os.path.relpath(root, INPUT_FOLDER)
                current_output_dir = os.path.join(OUTPUT_FOLDER, relative_path)

                # Crear la subcarpeta de destino si no existe
                if not os.path.exists(current_output_dir):
                    os.makedirs(current_output_dir)

                # --- PROCESAMIENTO DE IMAGEN ---
                with Image.open(input_path) as img:
                    
                    # 1. Corregir orientación (EXIF)
                    img = ImageOps.exif_transpose(img)

                    # 2. Convertir a sRGB
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    # 3. Redimensionar si es gigante
                    if img.width > MAX_WIDTH:
                        ratio = MAX_WIDTH / float(img.width)
                        new_height = int((float(img.height) * float(ratio)))
                        img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                    
                    # 4. Guardar como WebP
                    new_filename = os.path.splitext(filename)[0] + '.webp'
                    output_path = os.path.join(current_output_dir, new_filename)
                    
                    img.save(output_path, 'WEBP', quality=QUALITY_VAL, method=6)
                    
                    # Mostramos solo el nombre para no ensuciar la consola
                    print(f"✅ [{relative_path}] {filename} -> WebP")
                    procesadas += 1

            except Exception as e:
                print(f"❌ Error con {filename}: {e}")
                errores += 1

print("-" * 50)
if procesadas == 0:
    print("⚠️  AVISO: Seguimos sin encontrar fotos. Verifica:")
    print(f"1. Que la carpeta '{INPUT_FOLDER}' exista al lado de este script.")
    print("2. Que dentro de esa carpeta realmente haya imágenes (.jpg, .png).")
else:
    print(f"🏁 ¡Listo! Fotos procesadas: {procesadas}")
    print(f"Revisa la carpeta '{OUTPUT_FOLDER}' (mantiene tu estructura de subcarpetas).")