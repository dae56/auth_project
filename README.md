### Introduction for DEV
* Используется семантическое версионирование приложения `<minor>.<major>.<patch>`
* Методология разработки - базовый gitworkflow
* Пример сообщения коммита: `<type> - <description>`, где `type = init | feat | fix | refactor | 
tests | revert` 

### Пример заполнения переменных окружения:
* `DB_HOST` - Хост СУБД PostgreSQL
* `DB_PORT` - Порт СУБД PostgreSQL
* `DB_USER` - Пользователь СУБД PostgreSQL
* `DB_PASS` - Пароль пользователя СУБД PostgreSQL
* `DB_NAME` - Имя БД СУБД PostgreSQL
* `DB_ECHO` - Трассировка запросов SQLAlchemy
* `APP_DEBUG` - Режим дебага FastAPI
* `REFRESH_TABLE` - Пересоздание всех таблиц
* `JWT_SALT` - Соль для разбавления JWT токена
* `PASS_SALT` - Соль для разбавления паролей