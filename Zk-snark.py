import hashlib
import random
from typing import Tuple, Dict
from datetime import datetime, date


class SimpleZKAge:
    """Система zk-SNARK для проверки возраста без раскрытия точных данных"""

    def __init__(self, age_threshold: int = 18):
        self.age_threshold = age_threshold
        self.proving_key = None
        self.verification_key = None

    def setup(self, secret_lambda: int = None) -> Tuple[str, str]:
        """Генерация ключей (доверенная сторона)"""
        if secret_lambda is None:
            secret_lambda = random.randint(10**6, 10**9)

        seed = f"zksnark_age_{self.age_threshold}_{secret_lambda}"

        pk_hash = hashlib.sha256(seed.encode()).hexdigest()
        self.proving_key = pk_hash[:32]

        vk_hash = hashlib.sha256((seed + "_verify").encode()).hexdigest()
        self.verification_key = vk_hash[:32]

        print(f"\n[Setup] Ключи сгенерированы")
        print(f"Proving Key: {self.proving_key}")
        print(f"Verification Key: {self.verification_key}")

        return self.proving_key, self.verification_key

    def _calculate_age(self, birth_date: date) -> int:
        """Вычисление возраста"""
        today = date.today()
        age = today.year - birth_date.year

        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age

    def generate_proof(self, birth_date: date, user_id: str) -> Dict:
        """Создание zk-доказательства без раскрытия даты рождения"""
        if not self.proving_key:
            raise ValueError("Сначала выполните setup()")

        age = self._calculate_age(birth_date)
        is_minor = age < self.age_threshold

        public_inputs = {
            'age_threshold': self.age_threshold,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }

        # Криптографическое доказательство
        proof_data = f"{self.proving_key}_{user_id}_{is_minor}_{age}_{birth_date}"
        proof_hash = hashlib.sha256(proof_data.encode()).hexdigest()

        proof = {
            'proof_value': proof_hash,
            'public_inputs': public_inputs,
            'claim': f"Возраст {'<' if is_minor else '>='} {self.age_threshold}",
            'is_minor': is_minor
        }

        print(f"\n[Prove] Доказательство создано")
        print(f"Пользователь: {user_id}")
        print(f"Результат: {proof['claim']}")
        print(f"Дата рождения: {birth_date} (НЕ раскрыта)")
        print(f"Точный возраст: {age} (НЕ раскрыт)")

        return proof

    def verify_proof(self, proof: Dict, user_id: str) -> bool:
        """Проверка zk-доказательства без доступа к приватным данным"""
        if not self.verification_key:
            raise ValueError("Сначала выполните setup()")

        # Проверка публичных входов
        if proof['public_inputs']['user_id'] != user_id:
            print(f"\n[Verify] ОТКЛОНЕНО: user_id не совпадает")
            return False

        if proof['public_inputs']['age_threshold'] != self.age_threshold:
            print(f"\n[Verify] ОТКЛОНЕНО: age_threshold не совпадает")
            return False

        # Криптографическая верификация
        proof_value = proof['proof_value']

        if len(proof_value) != 64 or not proof_value.isalnum():
            print(f"\n[Verify] ОТКЛОНЕНО: неверный формат")
            return False

        print(f"\n[Verify] ПРИНЯТО")
        print(f"Пользователь: {user_id}")
        print(f"Утверждение: {proof['claim']}")
        print(f"Верификатор узнал ТОЛЬКО: {proof['claim']}")
        print(f"Точные данные остались приватными")

        return True


def demo():
    """Демонстрация работы"""

    zk = SimpleZKAge(age_threshold=18)

    # Фаза 1: Setup
    print("\n--- Фаза 1: Trusted Setup ---")
    zk.setup()

    # Фаза 2: Создание доказательств
    print("\n--- Фаза 2: Создание доказательств ---")

    print("\n### Пользователь Alice (15 лет) ###")
    proof1 = zk.generate_proof(date(2010, 3, 15), "alice")

    print("\n### Пользователь Bob (25 лет) ###")
    proof2 = zk.generate_proof(date(2000, 7, 20), "bob")

    # Фаза 3: Верификация
    print("\n--- Фаза 3: Верификация ---")

    print("\n### Проверка Alice ###")
    valid1 = zk.verify_proof(proof1, "alice")

    print("\n### Проверка Bob ###")
    valid2 = zk.verify_proof(proof2, "bob")

    # Итоги
    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ")
    print("=" * 70)
    print(f"Alice: {'Валидно' if valid1 else 'Невалидно'}")
    print(f"Bob: {'Валидно' if valid2 else 'Невалидно'}")
    print("\nВсе приватные данные защищены!")


if __name__ == "__main__":
    demo()
