// Возвращает строку-пример для выбранного типа
// Назначение: по ключу типа данных вернуть простое демонстрационное значение
function getExampleByType(typeKey) {
  const examples = {
    // целое число
    int: 52,
    // число с плавающей точкой
    float: 52.52,
    // логический тип
    bool: true,
    // одиночный символ
    char: 'A',
    // строка
    str: 'Привет, мир!',
    // массив/список
    list: [1, 2, 3],
    // кортеж/структура
    tuple: [1, 'текст', true],
    // словарь/объект (пары ключ → значение)
    dict: { ключ: 'значение', год: 2025 }
  };

  return examples[typeKey];
}

// Отображает пример значения на экране
// Назначение: взять значение, превратить в читаемую строку и показать в блоке вывода
function renderExample(value) {
  const output = document.getElementById('output');

  // для сложных типов сделаем человекочитаемое представление
  let text;
  if (Array.isArray(value)) {
    text = JSON.stringify(value);
  } else if (value && typeof value === 'object') {
    text = JSON.stringify(value, null, 2);
  } else if (typeof value === 'string') {
    text = `"${value}"`;
  } else if (typeof value === 'boolean' || typeof value === 'number') {
    text = String(value);
  } else if (value === undefined) {
    text = 'Сначала выберите тип';
  } else {
    text = String(value);
  }

  output.textContent = text;
}

// Настраивает обработчики событий страницы
// Назначение: повесить клик на кнопку и читать выбранный тип из списка
function initPageInteractions() {
  const select = document.getElementById('typeSelect');
  const btn = document.getElementById('showBtn');

  btn.addEventListener('click', () => {
    const selected = select.value;
    const example = getExampleByType(selected);
    renderExample(example);
  });
}

// Точка входа при загрузке страницы
// Назначение: инициализировать взаимодействия сразу после построения DOM
document.addEventListener('DOMContentLoaded', initPageInteractions);


