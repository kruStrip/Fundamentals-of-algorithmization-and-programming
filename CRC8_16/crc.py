import time
from typing import List


# CRC-8
def crc8_bitwise(data: bytes, polynomial: int = 0x07, init: int = 0x00) -> int:
    """Вычисление CRC-8 побитовым сдвигом"""
    crc = init

    for byte in data:
        crc ^= byte

        for _ in range(8):
            if crc & 0x80:  # Если старший бит = 1
                crc = (crc << 1) ^ polynomial
            else:
                crc = crc << 1

            crc &= 0xFF

    return crc


def crc8_generate_table(polynomial: int = 0x07) -> List[int]:
    """Генерация таблицы lookup для CRC-8"""
    table = []

    for dividend in range(256):
        curr_byte = dividend

        for _ in range(8):
            if curr_byte & 0x80:
                curr_byte = (curr_byte << 1) ^ polynomial
            else:
                curr_byte = curr_byte << 1

            curr_byte &= 0xFF

        table.append(curr_byte)

    return table


def crc8_table(data: bytes, polynomial: int = 0x07, 
               init: int = 0x00, table: List[int] = None) -> int:
    """Вычисление CRC-8 через таблицу lookup"""
    if table is None:
        table = crc8_generate_table(polynomial)

    crc = init

    for byte in data:
        pos = crc ^ byte
        crc = table[pos]

    return crc


# CRC-16
def crc16_bitwise(data: bytes, polynomial: int = 0x1021, 
                  init: int = 0xFFFF) -> int:
    """Вычисление CRC-16 побитовым сдвигом (CCITT)"""
    crc = init

    for byte in data:
        crc ^= (byte << 8)

        for _ in range(8):
            if crc & 0x8000:  # Если старший бит = 1
                crc = (crc << 1) ^ polynomial
            else:
                crc = crc << 1

            crc &= 0xFFFF

    return crc


def crc16_generate_table(polynomial: int = 0x1021) -> List[int]:
    """Генерация таблицы lookup для CRC-16"""
    table = []

    for dividend in range(256):
        curr_byte = dividend << 8

        for _ in range(8):
            if curr_byte & 0x8000:
                curr_byte = (curr_byte << 1) ^ polynomial
            else:
                curr_byte = curr_byte << 1

            curr_byte &= 0xFFFF

        table.append(curr_byte)

    return table


def crc16_table(data: bytes, polynomial: int = 0x1021, 
                init: int = 0xFFFF, table: List[int] = None) -> int:
    """Вычисление CRC-16 через таблицу lookup"""
    if table is None:
        table = crc16_generate_table(polynomial)

    crc = init

    for byte in data:
        pos = ((crc ^ (byte << 8)) >> 8) & 0xFF
        crc = ((crc << 8) ^ table[pos]) & 0xFFFF

    return crc


# Тестирование и сравнение
def compare_methods(data: bytes) -> None:
    """Сравнение производительности методов"""
    print("=" * 70)
    print(f"Тестовые данные: {data[:50]}{'...' if len(data) > 50 else ''}")
    print(f"Длина данных: {len(data)} байт")
    print("=" * 70)

    # CRC-8
    print("\nРезультаты CRC-8:")
    print("-" * 70)

    crc8_lut = crc8_generate_table(0x07)

    start = time.perf_counter()
    crc8_bit = crc8_bitwise(data)
    time_bit = time.perf_counter() - start

    print(f"Побитовый: 0x{crc8_bit:02X} ({crc8_bit:3d}) - Время: {time_bit*1e6:8.2f} µs")

    start = time.perf_counter()
    crc8_tbl = crc8_table(data, table=crc8_lut)
    time_tbl = time.perf_counter() - start

    print(f"Табличный: 0x{crc8_tbl:02X} ({crc8_tbl:3d}) - Время: {time_tbl*1e6:8.2f} µs")
    print(f"Совпадение: {crc8_bit == crc8_tbl} | Ускорение: {time_bit/time_tbl:.2f}x")

    # CRC-16
    print("\nРезультаты CRC-16:")
    print("-" * 70)

    crc16_lut = crc16_generate_table(0x1021)

    start = time.perf_counter()
    crc16_bit = crc16_bitwise(data)
    time_bit = time.perf_counter() - start

    print(f"Побитовый: 0x{crc16_bit:04X} ({crc16_bit:5d}) - Время: {time_bit*1e6:8.2f} µs")

    start = time.perf_counter()
    crc16_tbl = crc16_table(data, table=crc16_lut)
    time_tbl = time.perf_counter() - start

    print(f"Табличный: 0x{crc16_tbl:04X} ({crc16_tbl:5d}) - Время: {time_tbl*1e6:8.2f} µs")
    print(f"Совпадение: {crc16_bit == crc16_tbl} | Ускорение: {time_bit/time_tbl:.2f}x")
    print("=" * 70)


def main():
    """Основная функция тестирования"""
    test_cases = [
        b"Hello, World!",
        b"A" * 100,
        b"Test data for CRC calculation" * 10
    ]

    for test_data in test_cases:
        compare_methods(test_data)
        print()


if __name__ == "__main__":
    main()