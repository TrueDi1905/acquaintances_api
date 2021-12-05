# acquaintances_api
Сайт знакомств
### Для тестирования:(использовался постман)
- Регистрация(нужно отправить заполенные поля sex, first_name, avatar, last_name, email, password) - https://truedi1905.pythonanywhere.com/api/clients/create/ 
- Аутентификация(нужно отправить email и пароль введенные выше для получения токена, токен вводим в параметры запроса, например Token "token") - https://truedi1905.pythonanywhere.com/api/clients/auth/ 
- Выразить симпатию - https://truedi1905.pythonanywhere.com/api/clients/{id}/match
- поиск людей с фильтрацией https://truedi1905.pythonanywhere.com/api/list/ , для фильтрации по расстоянию, нужно указать параметр distance. В базе данных есть пользователь с Волгограда, для его поиска укажите distance с аргументом 958(https://truedi1905.pythonanywhere.com/api/list/?distance=958)
- 
