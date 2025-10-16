#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <cmath>
#include <string>
#include <bitset>
using namespace std;

// Находим простые числа
bool isPrime(int n)
{
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++)
    {
        if (n % i == 0) return false;
    }
    return true;
}

// Получаем константы

// берём дробную часть и умножаем на 2^32
uint32_t getFractionalBits(double number)
{
    double fractional = number - (int)number;  // Берём только после точки
    return (uint32_t)(fractional * 4294967296.0);  // Умножаем на 2^32
}

// Делаем сдвиг

uint32_t rightRotate(uint32_t x, int n)
{
    return (x >> n) | (x << (32 - n));
}

// Основная функция

string sha256(string message)
{
    uint32_t H[8];
    int primeCount = 0;
    int number = 2;

    cout << "Начальные значения:\n";
    for (int i = 0; i < 8; i++)
    {
        while (!isPrime(number)) number++;
        double sqrtValue = sqrt((double)number);
        H[i] = getFractionalBits(sqrtValue);
        cout << "H[" << i << "] = sqrt(" << number << ") -> 0x"
            << hex << H[i] << dec << "\n";
        number++;
    }
    cout << "\n";

    uint32_t K[64];
    number = 2;

    cout << "Константы:\n";
    for (int i = 0; i < 64; i++)
    {
        while (!isPrime(number)) number++;
        double cbrtValue = cbrt((double)number);
        K[i] = getFractionalBits(cbrtValue);
        if (i < 8)
        {
            cout << "K[" << i << "] = cbrt(" << number << ") -> 0x"
                << hex << K[i] << dec << "\n";
        }
        number++;
    }
    cout << "\n";

    int originalLength = message.length();
    int bitLength = originalLength * 8;

    // Добавляем байт 0x80
    message += (char)0x80;

    // Дополняем до кратности 512 бит (64 байта)
    while (message.length() % 64 != 56) {
        message += (char)0x00;
    }

    // Добавляем нули до 56 байт (448 бит)
    while (message.length() % 64 != 56)
    {
        message += (char)0x00;
    }

    // Добавляем длину сообщения (8 байт)
    for (int i = 7; i >= 0; i--)
    {
        message += (char)((bitLength >> (i * 8)) & 0xFF);
    }

    cout << "Длина сообщения: " << message.length() << " байт\n\n";

    int totalBlocks = message.length() / 64;  // Количество блоков по 512 бит
    cout << "Сообщение разбито на " << totalBlocks << " блок(ов) по 512 бит\n\n";

    // Разбиваем на 16 слов по 32 бита
    uint32_t W[64] = { 0 };

    for (int block = 0; block < totalBlocks; block++) {

        cout << "Обработка блока " << (block + 1) << "/" << totalBlocks << "\n";

        // Разбиваем текущий блок на 16 слов по 32 бита
        uint32_t W[64] = { 0 };

        int offset = block * 64;  // Смещение для текущего блока

        for (int i = 0; i < 16; i++) {
            W[i] = ((uint8_t)message[offset + i * 4] << 24) |
                ((uint8_t)message[offset + i * 4 + 1] << 16) |
                ((uint8_t)message[offset + i * 4 + 2] << 8) |
                ((uint8_t)message[offset + i * 4 + 3]);
        }

        // Расширяем 16 слов до 64 слов
        for (int i = 16; i < 64; i++)
        {
            uint32_t s0 = rightRotate(W[i - 15], 7) ^ rightRotate(W[i - 15], 18) ^ (W[i - 15] >> 3);
            uint32_t s1 = rightRotate(W[i - 2], 17) ^ rightRotate(W[i - 2], 19) ^ (W[i - 2] >> 10);
            W[i] = W[i - 16] + s0 + W[i - 7] + s1;
        }

        uint32_t a = H[0];
        uint32_t b = H[1];
        uint32_t c = H[2];
        uint32_t d = H[3];
        uint32_t e = H[4];
        uint32_t f = H[5];
        uint32_t g = H[6];
        uint32_t h = H[7];

        for (int i = 0; i < 64; i++)
        {
            uint32_t S1 = rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25);
            uint32_t ch = (e & f) ^ ((~e) & g);
            uint32_t temp1 = h + S1 + ch + K[i] + W[i];

            uint32_t S0 = rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22);
            uint32_t maj = (a & b) ^ (a & c) ^ (b & c);
            uint32_t temp2 = S0 + maj;

            h = g;
            g = f;
            f = e;
            e = d + temp1;
            d = c;
            c = b;
            b = a;
            a = temp1 + temp2;
        }

        // Добавляем к исх значениям

        H[0] += a;
        H[1] += b;
        H[2] += c;
        H[3] += d;
        H[4] += e;
        H[5] += f;
        H[6] += g;
        H[7] += h;

        // Final

        string hash = "";
        for (int i = 0; i < 8; i++) {
            char buffer[9];
            sprintf_s(buffer, 9, "%08x", H[i]);
            hash += buffer;
        }

        return hash;
    }
}


int main()
{
    setlocale(0, "");
    string message = "Hello worldFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF";

    cout << "Сообщение: " << message << "\n\n";

    string hash = sha256(message);

    cout << "Результат:\n";
    cout << hash << "\n";

    return 0;
}
