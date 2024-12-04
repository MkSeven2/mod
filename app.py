import streamlit as st
import json
import requests
import base64
from datetime import datetime
import pytz

# Список забаненных пользователей с датой разбана
banned_users = {
    "MkSeven1": {
        "reason": "Cheating",
        "unban_date": "15-12-24 10:00",  # Дата и время (чикагоское время)
        "moderator_note": "Detected using unauthorized tools.",
    },
    # Добавьте других забаненных пользователей здесь
}

# Пользователи и пароли
users = {
    "MkSeven1": "9872", 
    "penisbobra3": "izudoner667",
    # Добавьте больше пользователей здесь, если нужно
}

# Функция для логина
def login(username, password):
    return users.get(username) == password

# Функция для чтения cookies
def get_cookie(key):
    # Используем st.query_params вместо устаревшего st.experimental_get_query_params
    cookie_value = st.query_params.get(key, [None])[0]
    return cookie_value


# Функция для записи cookies через query_params
def set_cookie(key, value):
    current_params = st.experimental_get_query_params()  # Читаем текущие параметры
    current_params[key] = value
    st.experimental_set_query_params(**current_params)  # Обновляем параметры

# Проверка забанен ли игрок
def check_ban(username):
    banned_player = banned_users.get(username)
    if banned_player:
        # Текущее время с временной зоной
        current_time = datetime.now(pytz.timezone('America/Chicago'))
        # Время разбана
        unban_time_naive = datetime.strptime(banned_player["unban_date"], "%d-%m-%y %H:%M")
        # Добавляем временную зону к unban_time
        timezone = pytz.timezone('America/Chicago')
        unban_time = timezone.localize(unban_time_naive)
        # Сравниваем два offset-aware времени
        if current_time < unban_time:
            return banned_player
    return None

# Сохранение сессии с помощью Streamlit Session State и cookies
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Чтение cookie
cookie_logged_in = get_cookie("logged_in")

# Если cookie существует и равно "true", то считаем пользователя авторизованным
if cookie_logged_in == "true":
    st.session_state['logged_in'] = True

# Проверка сессии и логина
if not st.session_state['logged_in']:
    st.title("Авторизация")
    st.subheader("Введите логин и пароль, чтобы продолжить.")
    
    # Форма авторизации
    username = st.text_input("Логин", placeholder="Введите ваш логин")
    password = st.text_input("Пароль", placeholder="Введите ваш пароль", type="password")
    login_btn = st.button("Войти")
    
    if login_btn:
        if login(username, password):
            # Проверка на бан
            ban_info = check_ban(username)
            if ban_info:
                # Если забанен, перенаправляем на страницу с баном
                st.session_state['logged_in'] = False
                st.session_state['ban_info'] = ban_info
                set_cookie("logged_in", "false")  # Сбрасываем состояние
                st.experimental_rerun()
            else:
                st.session_state['logged_in'] = True
                set_cookie("logged_in", "true")  # Устанавливаем cookie на "true"
                st.success("Вы успешно вошли в систему!")
        else:
            st.error("Неверный логин или пароль.")
    st.stop()  # Останавливаем выполнение, пока не произошел вход

# Логика после успешного входа
st.sidebar.title("Панель управления")
if st.sidebar.button("Выйти"):
    st.session_state['logged_in'] = False
    set_cookie("logged_in", "false")  # Убираем cookie
    st.experimental_set_query_params()  # Очистка параметров
    st.stop()  # Остановка выполнения скрипта после выхода

# Если игрок забанен, показываем бан-страницу
if 'ban_info' in st.session_state:
    ban_info = st.session_state['ban_info']
    st.title("Вы забанены!")
    st.subheader(f"Причина: {ban_info['reason']}")
    st.write(f"Срок до разбана: {ban_info['unban_date']} (Чикагоское время)")
    st.write(f"Заметка модератора: {ban_info['moderator_note']}")
    st.write("Вы не можете использовать этот сервис до указанной даты и времени.")
    st.write("Пожалуйста, обратитесь к модератору, если у вас есть вопросы.")
    st.markdown("![Ban Image](https://example.com/banned-image.png)")  # Ссылка на изображение с баном
    st.stop()  # Останавливаем выполнение после показа сообщения о бане

# Основной функционал после входа
st.title("AI Фильтр текста")
st.subheader("Анализируйте текст с помощью искуственного интеллекта. | By MkSeven1.")

# Поле для ввода текста
user_input = st.text_area("Введите текст для анализа:", placeholder="Введите текст здесь... (Только английский язык)")

# Доступ к пользовательским данным API
api_user = "43464075"
api_secret = "vJ2XKNu732mFPqGrEvRzX5SgyLoGdPqr"

if not api_user or not api_secret:
    st.error("Данные пользователя API не найдены. Добавьте их для продолжения.")
    st.stop()

# Кнопка для запуска анализа
if st.button("Анализировать текст"):
    if not user_input.strip():
        st.warning("Введите текст для анализа.")
    else:
        try:
            # Подготовка данных для запроса
            data = {
                'text': user_input,
                'mode': 'ml',
                'lang': 'en',  # Измените на нужный язык, если требуется
                'models': 'general,self-harm',
                'api_user': api_user,
                'api_secret': api_secret
            }
            
            # Отправка запроса в API Sightengine
            response = requests.post('https://api.sightengine.com/1.0/text/check.json', data=data)
            
            # Проверка ответа
            if response.status_code == 200:
                output = response.json()
                # Анализ классов модерации
                moderation_classes = output.get("moderation_classes", {})
                flagged_classes = [
                    cls for cls, score in moderation_classes.items()
                    if isinstance(score, (int, float)) and score > 0.1
                ]
                
                if flagged_classes:
                    flagged_text = ", ".join(flagged_classes)
                    st.warning(f"Текст отфильтрован. Обнаружены следующие категории: {flagged_text}.")
                else:
                    st.success("Все в порядке. Текст не содержит проблемного контента.")
                
                # Отображение полных результатов
                st.json(output)
            else:
                st.error(f"Ошибка API: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Произошла ошибка при обработке запроса: {str(e)}")
