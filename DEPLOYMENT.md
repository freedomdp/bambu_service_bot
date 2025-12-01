# Инструкция по развертыванию бота на сервере

## Требования

- Docker и Docker Compose установлены на сервере
- Доступ к серверу по SSH
- Домен или IP адрес для доступа к медиафайлам (опционально)

## Быстрый старт

### 1. Подготовка сервера

```bash
# Клонируем репозиторий
git clone https://github.com/freedomdp/bambu_service_bot.git
cd bambu_service_bot

# Создаем файл .env с настройками
cp .env.example .env
nano .env
```

### 2. Настройка переменных окружения

Отредактируйте файл `.env`:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
ENGINEER_TELEGRAM_ID=your_engineer_telegram_id
BASE_URL=http://your-server-ip:8000
MEDIA_STORAGE_PATH=./media
REDIS_HOST=redis
REDIS_PORT=6379
```

**Важно:** 
- `BASE_URL` должен указывать на ваш сервер, где будет доступен nginx для раздачи медиафайлов
- Если используете домен, укажите `BASE_URL=https://your-domain.com`

### 3. Запуск через Docker Compose

```bash
# Запускаем все сервисы
docker-compose -f docker/docker-compose.yml up -d

# Проверяем статус
docker-compose -f docker/docker-compose.yml ps

# Просмотр логов
docker-compose -f docker/docker-compose.yml logs -f bot
```

### 4. Проверка работы

```bash
# Проверка здоровья nginx
curl http://your-server-ip:8000/health

# Проверка логов бота
docker-compose -f docker/docker-compose.yml logs bot
```

## Структура развертывания

```
bambu_service_bot/
├── docker/
│   ├── Dockerfile              # Образ бота
│   ├── docker-compose.yml      # Конфигурация всех сервисов
│   └── nginx.conf              # Конфигурация веб-сервера
├── media/                      # Медиафайлы (создается автоматически)
│   ├── photos/                 # Фото от клиентов
│   ├── videos/                 # Видео от клиентов
│   └── models/                 # 3D модели
├── logs/                       # Логи приложения
└── .env                        # Переменные окружения
```

## Обновление бота

```bash
# Останавливаем контейнеры
docker-compose -f docker/docker-compose.yml down

# Обновляем код
git pull

# Пересобираем и запускаем
docker-compose -f docker/docker-compose.yml up -d --build
```

## Резервное копирование

### Резервное копирование медиафайлов

```bash
# Создаем архив медиафайлов
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/

# Восстановление
tar -xzf media_backup_YYYYMMDD.tar.gz
```

### Резервное копирование Redis (если используется для хранения состояния)

```bash
# Redis данные хранятся в volume redis_data
docker volume inspect bambu_service_bot_redis_data
```

## Мониторинг

### Просмотр логов

```bash
# Все логи
docker-compose -f docker/docker-compose.yml logs

# Только логи бота
docker-compose -f docker/docker-compose.yml logs bot

# Логи в реальном времени
docker-compose -f docker/docker-compose.yml logs -f bot
```

### Мониторинг ресурсов

```bash
# Использование ресурсов контейнерами
docker stats

# Проверка дискового пространства
df -h
du -sh media/
```

## Решение проблем

### Бот не запускается

1. Проверьте логи: `docker-compose -f docker/docker-compose.yml logs bot`
2. Проверьте переменные окружения в `.env`
3. Убедитесь, что токен бота правильный

### Медиафайлы не доступны

1. Проверьте, что nginx запущен: `docker-compose -f docker/docker-compose.yml ps`
2. Проверьте доступность порта 8000: `curl http://localhost:8000/health`
3. Проверьте права доступа к директории `media/`

### Проблемы с Redis

1. Проверьте логи Redis: `docker-compose -f docker/docker-compose.yml logs redis`
2. Перезапустите Redis: `docker-compose -f docker/docker-compose.yml restart redis`

## Безопасность

1. **Не коммитьте `.env` файл** - он уже в `.gitignore`
2. **Используйте HTTPS** для `BASE_URL` в продакшене
3. **Ограничьте доступ** к порту 8000 только для инженеров
4. **Регулярно обновляйте** Docker образы

## Масштабирование

Для высоких нагрузок можно:

1. Использовать внешний Redis (например, Redis Cloud)
2. Использовать внешнее хранилище для медиафайлов (S3, MinIO)
3. Настроить балансировщик нагрузки для нескольких экземпляров бота

