import streamlit as st
import openai
import json

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

# Доступ к ключу API OpenAI из Streamlit secrets
api_key = st.secrets.get("openai_secret")
if not api_key:
    st.error("Ключ API не найден в Streamlit secrets. Добавьте его для продолжения.")
    st.stop()

# Инициализация клиента OpenAI
client = openai.Client(api_key=api_key)

# Компоненты интерфейса Streamlit
st.title("Обнаружение языка ненависти")
st.subheader("Анализируйте текст с помощью API модерации OpenAI.")
user_input = st.text_area("Введите текст для анализа:", placeholder="Введите текст здесь...")

# Кнопка для запуска анализа
if st.button("Анализировать текст"):
    if not user_input.strip():
        st.warning("Введите текст для анализа.")
    else:
        try:
            # Вызов метода модерации
            response = client.moderations.create(
            model="omni-moderation-2024-09-26",
            input=user_input,
            )
            print(response)
            # Извлечение и сериализация ответа
            output = response['results'][0]
            serialized_output = serialize(output)
            json_output = json.dumps(serialized_output, indent=2, ensure_ascii=False)
            
            # Отображение результатов
            st.subheader("Результаты анализа")
            st.json(json_output)

        except Exception as e:
            st.error(f"Произошла ошибка при обработке запроса: {str(e)}")
