from pydantic_settings import BaseSettings
import streamlit as st
import google.generativeai as genai

class Settings(BaseSettings):
    gemini_api_key: str
    class Config:
        env_file = ".env"

settings = Settings()

genai.configure(api_key=settings.gemini_api_key)
model=genai.GenerativeModel("models/gemini-2.5-pro")

def get_gemini_response(question):
    response=model.generate_content(question)
    return response.text

#Initialize streamlit app

st.set_page_config(page_title="Gemini Copilot")
st.header("Gemini LLM App")
input=st.text_input("Input: ",key="Input")
submit=st.button("Ask Any Prompt")

if submit:
    response=get_gemini_response(input)
    st.subheader("The Response is")
    st.write(response)