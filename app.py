import streamlit as st
import json
import requests

# Пользователи и пароли
users = {
    "MkSeven1": "9872",
    # Добавьте больше пользователей здесь, если нужно
}

# Сохранение сессии с помощью Streamlit Session State и cookies
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Функция для логина
def login(username, password):
    return users.get(username) == password

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
            st.session_state['logged_in'] = True
            st.success("Вы успешно вошли в систему!")
            st.experimental_set_query_params(logged_in="true")  # Сохранение состояния
        else:
            st.error("Неверный логин или пароль.")
    st.stop()

# Логика после успешного входа
st.sidebar.title("Панель управления")
if st.sidebar.button("Выйти"):
    st.session_state['logged_in'] = False
    st.experimental_set_query_params()  # Очистка параметров
    st.experimental_rerun()

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
