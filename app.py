import streamlit as st
import openai
import json

# Function to serialize the output
def serialize(obj):
    """Recursively walk object's hierarchy."""
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
        return repr(obj)  # Convert unknown types to string

# Access the OpenAI API key from Streamlit secrets
api_key = st.secrets.get("openai_secret")
if not api_key:
    st.error("API key not found in Streamlit secrets. Please add it to proceed.")
    st.stop()

# Initialize OpenAI client
openai.api_key = api_key

# Streamlit UI components
st.title("Hate Speech Detection")
st.subheader("Detect potentially harmful or hateful content using OpenAI's Moderation API.")
user_input = st.text_area("Enter text to analyze:", placeholder="Type your text here...")

# Button to trigger hate speech detection
if st.button("Detect Hate"):
    if not user_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        try:
            # API call to OpenAI Moderation endpoint
            response = openai.Moderation.create(
                model="text-moderation-latest",
                input=user_input
            )

            # Extract and serialize the response
            output = response['results'][0]
            serialized_output = serialize(output)
            json_output = json.dumps(serialized_output, indent=2, ensure_ascii=False)
            
            # Display the results
            st.subheader("Detection Results")
            st.json(json_output)

        except Exception as e:
            st.error(f"An error occurred while processing the request: {str(e)}")
