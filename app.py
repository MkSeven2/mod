import streamlit as st
import json
import requests

# Функция для сериализации вывода
def serialize(obj):
    """Рекурсивно обходит объект."""
    if isinstance(obj, (bool, int, float, str)):
        return obj
    elif isinstance(obj, dict):
        obj = obj.copy()
        for key in obj:
            obj[key] = serialize(obj[key])
        return obj
    elif isinstance(obj, list):
        return [serialize(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(serialize(item) for item in obj)
    elif hasattr(obj, '__dict__'):
        return serialize(obj.__dict__)
    else:
        return repr(obj)  # Преобразует неизвестные типы в строку

# Доступ к пользовательским данным API
api_user = "43464075"
api_secret = "vJ2XKNu732mFPqGrEvRzX5SgyLoGdPqr"
if not api_user or not api_secret:
    st.error("Данные пользователя API не найдены в Streamlit secrets. Добавьте их для продолжения.")
    st.stop()

# Компоненты интерфейса Streamlit
st.title("Обнаружение языка ненависти")
st.subheader("Анализируйте текст с помощью API Sightengine.")
user_input = st.text_area("Введите текст для анализа:", placeholder="Введите текст здесь...")

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
                'models': 'general,self-harm,toxic',
                'api_user': api_user,
                'api_secret': api_secret
            }
            
            # Отправка запроса в API Sightengine
            response = requests.post('https://api.sightengine.com/1.0/text/check.json', data=data)
            
            # Проверка ответа
            if response.status_code == 200:
                output = response.json()
                serialized_output = serialize(output)
                
                # Анализ классов модерации
                moderation_classes = output.get("moderation_classes", {})
                flagged_classes = [
                    cls for cls, score in moderation_classes.items()
                    if isinstance(score, (int, float)) and score > 0.3
                ]
                
                if flagged_classes:
                    flagged_text = ", ".join(flagged_classes)
                    st.warning(f"Текст отфильтрован. Обнаружены следующие категории: {flagged_text}.")
                else:
                    st.success("Все в порядке. Текст не содержит проблемного контента.")
                
                # Отображение полных результатов
                json_output = json.dumps(serialized_output, indent=2, ensure_ascii=False)
                st.subheader("Полные результаты анализа")
                st.json(json_output)
            else:
                st.error(f"Ошибка API: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Произошла ошибка при обработке запроса: {str(e)}")
