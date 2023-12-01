Данный проект настроен для запуска с помощью Docker Compose, 
оформлены файлы Dockerfile и docker-compose.yaml.

Для запуска проекта в Docker нужно:
- создать файл .env
- указать значения переменных окружения в файле .env (набор необходимых перменных указан в файле .env.sample)
- собрать образы командой docker-compose build
- запустить контейнеры командой docker-compose up