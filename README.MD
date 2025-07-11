# 📚 Telegram-бот для автоматизации учебного процесса

## Описание проекта

Цель проекта — разработка Telegram-чат-бота для автоматизации учебного процесса и помощи преподавателям.  
Бот предназначен для взаимодействия между студентами, преподавателями и администратором и реализует интеллектуальные функции на основе LLM (*Large Language Model*).

---

## 📌 Основной функционал

- Генерация учебных тестов с помощью LLM.
- Ответы на вопросы студентов на базе ИИ.
- Удобный интерфейс взаимодействия для трёх ролей: **администратор**, **преподаватель**, **студент**.
- Визуальный дизайн-макет и карта взаимодействия пользователя.

---

## 👤 Роли пользователей

- **Администратор** — модерирует работу бота, следит за корректностью работы.
- **Преподаватель** — загружает учебные материалы (конспекты), просматривает статистику.
- **Студент** — задаёт вопросы, проходит тесты, изучает материалы.

---

## 🛠️ Структура решения

**Дизайн и планирование**
- Создан дизайн-макет Telegram-бота.
- Построена карта взаимодействия пользователя.

**Программная реализация**
- Обработчики пользовательских команд написаны на Python.
- Подключена LLM для генерации тестов и ответов на вопросы.
- Реализованы основные функции для студентов (вопросы и тесты).

---

## 🚀 Запуск проекта

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/LISA-ITMO/LLM-AI-Lector.git
    cd LLM-AI-Lector
    ```
2. Добавьте ваши токены:
    - Вставьте Telegram-токен в файл `config.py`.
    - Укажите токен вашей LLM (например, OpenAI API).

3. Запустите бота:
    ```bash
    python main.py
    ```

---

## 🔧 Технологии

- Python
- Telegram Bot API (*aiogram-telegram-bot*)
- Large Language Model (*например, OpenAI*)
- Возможна интеграция с БД для хранения статистики и конспектов

---

## ⚙️ Статус разработки

✅ Реализовано:
- Генерация тестов через LLM  
- Ответы на вопросы студентов  
- Структура ролей и логика обработки команд

---

## 📌 Планы на будущее

- Расширение функционала для преподавателей
- Хранение и анализ статистики прохождения тестов
- Интерфейс загрузки и отображения учебных материалов

---

## Примеры использования

Найти пример работы бота вы можете в google disk: https://drive.google.com/file/d/1yzJ0s9vADhw-C6IQjAQ1qgtpZOkpK6_y/view?usp=sharing

---

**🤝 Добро пожаловать к сотрудничеству!**


