import hashlib

def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)
    
    return sha256_hash.hexdigest()

def check_file_integrity(file_path, known_hash):
    file_hash = calculate_file_hash(file_path)
    
    print(f"Файл: {file_path}")
    print(f"Вычисленный хеш: {file_hash}")
    print(f"Известный хеш: {known_hash}")
    
    if file_hash == known_hash:
        print("\nФайл целостен)")
        return True
    else:
        print("\nФайл поврежден или изменен!")
        return False

# Параметры для проверки
file_path = "Fundamentals-of-algorithmization-and-programming/HW_SHA256/meow.txt"
known_hash = "ccd758e72a8a8cb5f140bab26837f363908550f2558ed86d229ec9016fed49b9"

check_file_integrity(file_path, known_hash)
