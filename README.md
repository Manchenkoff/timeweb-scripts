# TimeWeb Deploy Manager script

## Установка

Для установки скрипта на хостинг нужно выполнить

```
git clone https://github.com/manchenkoff/timeweb-manager ./bin
mv ./bin/manager.py ./manager.py
rm -r ./bin
```

После чего можно использовать скрипт:

```
python manager.py [тип операции]
```

## Доступные операции

- **help**: показать справку по командам
- **node**: выполнить установку Node.js и зарегистрировать alias для запуска node, npm
- **clone**: загрузить проект из репозитория Github
- **link**: привязать проект Github к сайту TimeWeb
- **update**: загрузить обновления из репозитория Github