import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def bruteforce_password(target_hash, password_list):
    print(f"Целевой хеш: {target_hash}\n")
    print("Начинаем перебор паролей...\n")
    
    for password in password_list:
        current_hash = hash_password(password)
        print(f"Проверяем '{password}' -> {current_hash}")
        
        if current_hash == target_hash:
            print(f"\nПароль найден: {password}")
            return password
    
    print("\nПароль не найден в списке")
    return None

# Данные для проверки
target_hash = "5e884898da28047151d0e56f8dc6292773603d0d6a88a4b5021eea1b7e7d9f1b"
password_list = ['password', '123456', 'hello', 'secret', 'letmein']

bruteforce_password(target_hash, password_list)
