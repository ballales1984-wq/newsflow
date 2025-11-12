"""
Script per ottimizzare screenshot per Product Hunt
Dimensioni ottimali: 1200x675px (16:9)
"""
import os
from PIL import Image

def ottimizza_screenshot(input_path, output_path, target_size=(1200, 675)):
    """Ridimensiona e ottimizza screenshot per Product Hunt"""
    try:
        # Apri immagine
        img = Image.open(input_path)
        
        # Converti RGBA in RGB se necessario (per PNG con trasparenza)
        if img.mode == 'RGBA':
            # Crea sfondo bianco
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # Usa canale alpha come maschera
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calcola dimensioni mantenendo aspect ratio
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Crea nuova immagine con dimensioni esatte
        new_img = Image.new('RGB', target_size, (255, 255, 255))
        
        # Centra l'immagine
        x_offset = (target_size[0] - img.size[0]) // 2
        y_offset = (target_size[1] - img.size[1]) // 2
        new_img.paste(img, (x_offset, y_offset))
        
        # Salva ottimizzata
        new_img.save(output_path, 'JPEG', quality=90, optimize=True)
        
        print(f"✅ {os.path.basename(input_path)} → {os.path.basename(output_path)} ({target_size[0]}x{target_size[1]}px)")
        return True
    except Exception as e:
        print(f"❌ Errore con {input_path}: {e}")
        return False

def main():
    # Directory screenshot
    input_dir = "screenshots_linkedin"
    output_dir = "screenshots_producthunt"
    
    # Crea directory output se non esiste
    os.makedirs(output_dir, exist_ok=True)
    
    # Lista screenshot da ottimizzare
    screenshots = [
        "newsflow-homepage.png",
        "newsflow-category-filter.png",
        "newsflow-dark-mode.png",
        "newsflow-explain-modal.png",
        "newsflow-user-menu.png"
    ]
    
    print("🎨 Ottimizzazione screenshot per Product Hunt...\n")
    
    success_count = 0
    for screenshot in screenshots:
        input_path = os.path.join(input_dir, screenshot)
        if os.path.exists(input_path):
            # Nome output (JPEG per Product Hunt)
            output_name = screenshot.replace('.png', '_ph.jpg')
            output_path = os.path.join(output_dir, output_name)
            
            if ottimizza_screenshot(input_path, output_path):
                success_count += 1
        else:
            print(f"⚠️  File non trovato: {input_path}")
    
    print(f"\n✨ Completato! {success_count}/{len(screenshots)} screenshot ottimizzati")
    print(f"📁 Screenshot salvati in: {output_dir}/")

if __name__ == "__main__":
    main()

