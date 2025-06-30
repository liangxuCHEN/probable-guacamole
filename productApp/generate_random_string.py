import secrets
import qrcode
import csv
from io import BytesIO
import os

# 定义字符集，排除容易混淆的字符
CHARSET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

# 生成8位随机字符串
def generate_random_string(length=8):
    return ''.join(secrets.choice(CHARSET) for _ in range(length))

# 生成二维码并保存为图片
def generate_qr_code(data, file_name):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer

# 将数据写入CSV文件
def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['String', 'QR Code'])
        for item in data:
            writer.writerow([item['string'], item['qr_code']])

# 主函数
def main():
    data = []
    num_strings = 10  # 生成10个随机字符串

    for _ in range(num_strings):
        random_string = generate_random_string()
        print(f"Generated String: {random_string}")
        
        # 生成二维码
        qr_code_buffer = generate_qr_code(random_string, f"{random_string}.png")
        
        # 保存二维码图片
        qr_code_path = f"{random_string}.png"
        with open(qr_code_path, 'wb') as f:
            f.write(qr_code_buffer.getvalue())
        
        # 保存到数据列表
        data.append({'string': random_string, 'qr_code': qr_code_path})
    
    # 保存到CSV文件
    save_to_csv(data, 'output.csv')
    print(f"Data saved to {os.path.abspath('output.csv')}")

if __name__ == "__main__":
    main()
