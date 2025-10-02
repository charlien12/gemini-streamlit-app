from pydantic_settings import BaseSettings
import streamlit as st
import google.generativeai as genai
from PIL import Image

class Settings(BaseSettings):
    gemini_api_key: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()

# Prefer st.secrets on Streamlit Cloud
api_key = st.secrets.get("gemini_api_key", settings.gemini_api_key)

if not api_key:
    st.error("❌ No GEMINI_API_KEY found. Please set it in `.env` (local) or `Secrets Manager` (Streamlit Cloud).")
else:
    genai.configure(api_key=api_key)

model=genai.GenerativeModel("models/gemini-2.5-pro")

def get_gemini_response(question,image):
    if question!="" and image!="":
        response=model.generate_content([question,image])
    elif image=="" and question!="":
        response=model.generate_content(question)
    else:
        response=model.generate_content(image)
    return response.text

#Initialize streamlit app

st.set_page_config(page_title="Gemini Copilot")
st.header("Gemini LLM App")
input=st.text_input("Input: ",key="Input")
uploaded_file=st.file_uploader("Choose an Image.....",type=["jpg","png","jpeg"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_container_width=True)
submit=st.button("Ask Any Prompt")

if submit:
    response=get_gemini_response(input,image)
    st.subheader("The Response is")
    st.write(response)