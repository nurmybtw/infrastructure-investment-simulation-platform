# Analysis and Simulation Dashboard for Kazakhstan's Infrastructure Investment

## Overview / Обзор

This is a full-stack application with the following structure / Это приложение со следующей структурой:

-   **client**: A Next.js project for the frontend / Проект на Next.js для фронтенда.
-   **server**: A FastAPI project for the backend / Проект на FastAPI для бэкенда.

The main application will be available at `/`, serving the homepage from the Next.js project.

Главное приложение доступно по адресу `/`, где главная страница предоставляется из Next.js проекта.

---

## How to Run / Как запустить

### Prerequisites / Предварительные требования

1. Install Python 3.8+ and Node.js / Установите Python 3.8+ и Node.js.
2. Make sure `pip` and `npm` are installed / Убедитесь, что установлены `pip` и `npm`.

---

### Steps / Шаги

#### Backend / Бэкенд

1. Navigate to the `server` directory / Перейдите в папку `server`:

    ```bash
    cd server
    ```

2. Install dependencies / Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the FastAPI server / Запустите сервер FastAPI:
    ```bash
    uvicorn server:app --port 8080 --reload
    ```

#### Frontend / Фронтенд

1. Navigate to the `client` directory / Перейдите в папку `client`:

    ```bash
    cd client
    ```

2. Install dependencies / Установите зависимости:

    ```bash
    npm install
    ```

3. Run the Next.js app / Запустите Next.js приложение:
    ```bash
    npm run dev
    ```

By default, the frontend will be running at `http://localhost:3000`

По умолчанию фронтенд будет доступен по адресу `http://localhost:3000`
