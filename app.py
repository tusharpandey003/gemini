# invoice extractor
import google.generativeai as genai
from PIL import Image
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()


# configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load Gemini Pro vision model and get Response


def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("no file uploaded")


# initialize our streamlit app

st.set_page_config(page_title="Invoice extractor")
st.header("GEMINI Application")
input = st.text_input("Input prompt:", key="input")
submit = st.button('Submit')
uploaded_file = st.file_uploader(
    "choose an image...", type=["jpg", "jpeg", "png"])
image = ''
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="uploaded image", use_column_width=True)


input_prompt = '''
you are expert in uderstanding invoices. you will recieve input images as invoices and you will have to answer questions based on input image.
'''


if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)

    st.subheader("The Response")
    st.write(response)
