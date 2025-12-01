# Инструкция по подключению к GitHub

## Шаг 1: Создайте репозиторий на GitHub

1. Перейдите на https://github.com/new
2. Заполните форму:
   - **Repository name**: `aberhol_service_bot`
   - **Description**: "Telegram bot for Bambu Lab service center"
   - Выберите **Public** или **Private**
   - **НЕ** добавляйте README, .gitignore или лицензию (они уже есть в проекте)
3. Нажмите "Create repository"

## Шаг 2: Подключите локальный репозиторий к GitHub

После создания репозитория на GitHub, выполните следующие команды:

```bash
cd /Users/sergej/StudioProjects/Aberhol/aberhol_service_bot

# Добавьте удаленный репозиторий (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/aberhol_service_bot.git

# Отправьте код на GitHub
git push -u origin main
```

## Альтернативный вариант: Использование SSH

Если вы используете SSH ключи:

```bash
git remote add origin git@github.com:YOUR_USERNAME/aberhol_service_bot.git
git push -u origin main
```

## Дальнейшая работа

После подключения, для фиксации изменений используйте:

```bash
# Добавить все изменения
git add .

# Создать коммит
git commit -m "Описание изменений"

# Отправить на GitHub
git push
```
