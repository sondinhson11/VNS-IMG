import os
from pathlib import Path
from PIL import Image

try:
    from rembg import remove
except ImportError:
    print("Lỗi: Chưa cài đặt thư viện 'rembg' hoặc 'onnxruntime'.")
    print("Vui lòng chạy lệnh: pip install rembg onnxruntime Pillow")
    exit()

# Cố định thư mục input và output
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

def setup_folders():
    """Tự động tạo thư mục input và output nếu chưa có"""
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def process_remove_background():
    print(f"\n📁 Đang quét ảnh trong thư mục: {INPUT_DIR.absolute()}")
    count = 0
    
    for filepath in INPUT_DIR.rglob('*'):
        if filepath.is_file() and filepath.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
            count += 1
            try:
                # Tái tạo lại cấu trúc thư mục con từ input sang output
                rel_path = filepath.relative_to(INPUT_DIR)
                out_path = OUTPUT_DIR / rel_path
                out_path.parent.mkdir(parents=True, exist_ok=True)

                # Ép đuôi thành PNG để giữ được nền trong suốt
                out_file = out_path.with_suffix('.png') 
                print(f"✂️ Đang xóa nền: {filepath.name} -> {out_file.name}")

                with open(filepath, 'rb') as i:
                    input_data = i.read()
                    output_data = remove(input_data)

                with open(out_file, 'wb') as o:
                    o.write(output_data)

            except Exception as e:
                print(f"❌ Lỗi khi xử lý {filepath.name}: {e}")
                
    if count == 0:
        print("\n⚠️ Không tìm thấy ảnh nào trong thư mục 'input'!")
        print("👉 Hãy copy ảnh vào thư mục 'input' rồi chạy lại tool nhé.")
    else:
        print(f"\n✅ HOÀN THÀNH XÓA NỀN CHO {count} ẢNH! (Kiểm tra thư mục 'output')")

def process_convert_format(target_format):
    print(f"\n📁 Đang quét ảnh trong thư mục: {INPUT_DIR.absolute()}")
    target_ext = f".{target_format.lower()}"
    count = 0

    for filepath in INPUT_DIR.rglob('*'):
        if filepath.is_file() and filepath.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
            count += 1
            try:
                rel_path = filepath.relative_to(INPUT_DIR)
                out_path = OUTPUT_DIR / rel_path
                out_path.parent.mkdir(parents=True, exist_ok=True)

                out_file = out_path.with_suffix(target_ext)
                print(f"🔄 Đang chuyển đổi: {filepath.name} -> {out_file.name}")

                with Image.open(filepath) as img:
                    if target_format.lower() in ['jpg', 'jpeg']:
                        # Xử lý nền trong suốt khi convert sang JPG (đổ nền trắng)
                        if img.mode in ('RGBA', 'LA', 'P'):
                            bg = Image.new("RGB", img.size, (255, 255, 255))
                            if img.mode == 'P':
                                img = img.convert('RGBA')
                            bg.paste(img, mask=img.split()[3])
                            img = bg
                        else:
                            img = img.convert("RGB")
                            
                    img.save(out_file, format=target_format.upper() if target_format.lower() != 'jpg' else 'JPEG')

            except Exception as e:
                print(f"❌ Lỗi khi xử lý {filepath.name}: {e}")
                
    if count == 0:
        print("\n⚠️ Không tìm thấy ảnh nào trong thư mục 'input'!")
        print("👉 Hãy copy ảnh vào thư mục 'input' rồi chạy lại tool nhé.")
    else:
        print(f"\n✅ HOÀN THÀNH CHUYỂN ĐỔI CHO {count} ẢNH! (Kiểm tra thư mục 'output')")

def main():
    # Khởi tạo thư mục ngay khi chạy script
    setup_folders()
    
    print("="*50)
    print("  TOOL 2 TRONG 1: XÓA NỀN & CHUYỂN ĐỔI ĐỊNH DẠNG  ")
    print("="*50)
    print("📌 Đã tự động tạo thư mục 'input' và 'output'.")
    print("📌 Hãy đảm bảo bạn đã bỏ ảnh vào thư mục 'input' trước khi chọn.")
    print("="*50)
    print("1. Xóa nền ảnh (Tự động lưu thành PNG)")
    print("2. Chuyển đổi đuôi ảnh (PNG, JPG, WEBP)")
    
    choice = input("👉 Chọn tính năng (Nhập 1 hoặc 2): ").strip()

    if choice == '1':
        process_remove_background()
    elif choice == '2':
        print("\nChọn định dạng bạn muốn đổi ĐẾN:")
        print("1. PNG")
        print("2. WEBP")
        print("3. JPG")
        fmt_choice = input("👉 Nhập lựa chọn (1, 2 hoặc 3): ").strip()
        format_map = {'1': 'png', '2': 'webp', '3': 'jpg'}

        if fmt_choice in format_map:
            process_convert_format(format_map[fmt_choice])
        else:
            print("❌ Lựa chọn không hợp lệ!")
    else:
        print("❌ Lựa chọn không hợp lệ, vui lòng chạy lại tool.")

if __name__ == "__main__":
    main()