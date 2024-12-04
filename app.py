import streamlit as st
import requests
from datetime import datetime
import pytz

# Данные забаненных пользователей
banned_users = {
    "Banned": {
        "reason": "Test Reason",
        "unban_date": "10-12-24 10:00",
        "moderator_note": "Test Mod note..",
    },
    "MkSeven1": {
        "reason": "No root Access!?!?",
        "unban_date": "30-12-24 10:00",
        "moderator_note": "Wrong Admin account.",
    },
}

# Логин и пароли пользователей
users = {
    "MkSeven1": "9872",
    "penisbobra3": "izudoner667",
    "Banned": "1",
    "какой то пидор": "",
    "root": "9872",
}

# Функция для проверки логина
def login(username, password):
    return users.get(username) == password

# Проверка забаненного пользователя
def check_ban(username):
    banned_player = banned_users.get(username)
    if banned_player:
        # Текущее время в Чикагской временной зоне
        current_time = datetime.now(pytz.timezone('America/Chicago'))
        unban_time = datetime.strptime(banned_player["unban_date"], "%d-%m-%y %H:%M")
        unban_time = pytz.timezone('America/Chicago').localize(unban_time)
        if current_time < unban_time:
            return banned_player
    return None

# Обработка cookies
def set_cookie(key, value):
    st.experimental_set_query_params(**{key: value})

def get_cookie(key):
    params = st.experimental_get_query_params()
    return params.get(key, [None])[0]

# Проверка состояния авторизации
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Авторизация
if not st.session_state['logged_in']:
    st.title("Авторизация")
    username = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")
    
    if st.button("Войти"):
        if login(username, password):
            ban_info = check_ban(username)
            if ban_info:
                st.error(f"Вы забанены до {ban_info['unban_date']}. Причина: {ban_info['reason']}.")
            else:
                st.session_state['logged_in'] = True
                set_cookie("logged_in", "true")
                st.success("Вы успешно вошли в систему!")
                st.rerun()  # Перезагружаем страницу после успешного входа
        else:
            st.error("Неверный логин или пароль.")
    st.stop()

# Панель управления
st.sidebar.title("Панель управления")
if st.sidebar.button("Выйти"):
    st.session_state['logged_in'] = False
    set_cookie("logged_in", "false")
    st.rerun()  # Перезагружаем страницу после выхода
    st.stop()

# Основной контент
st.title("AI Фильтр текста")
user_input = st.text_area("Введите текст для анализа:", placeholder="Введите текст здесь... (Только на английском языке)")

api_user = "43464075"
api_secret = "vJ2XKNu732mFPqGrEvRzX5SgyLoGdPqr"

if not api_user or not api_secret:
    st.error("Отсутствуют данные API. Добавьте их для продолжения.")
else:
    if st.button("Анализировать текст"):
        if not user_input.strip():
            st.warning("Введите текст для анализа.")
        else:
            try:
                data = {
                    'text': user_input,
                    'mode': 'ml',
                    'lang': 'en',
                    'models': 'general,self-harm',
                    'api_user': api_user,
                    'api_secret': api_secret
                }
                response = requests.post('https://api.sightengine.com/1.0/text/check.json', data=data)
                if response.status_code == 200:
                    output = response.json()
                    flagged_classes = [
                        cls for cls, score in output.get("moderation_classes", {}).items()
                        if isinstance(score, (int, float)) and score > 0.1
                    ]
                    if flagged_classes:
                        st.warning(f"Обнаружены проблемные категории: {', '.join(flagged_classes)}")
                    else:
                        st.success("Текст не содержит проблемного контента.")
                    st.json(output)
                else:
                    st.error(f"Ошибка API: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Произошла ошибка: {str(e)}")
