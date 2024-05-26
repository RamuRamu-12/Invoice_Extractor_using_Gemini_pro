## Invoice Extractor

from dotenv import load_dotenv
load_dotenv() ##load all the variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configuring the api kkey
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## Function to load the gemini pro vision model and get response
def get_gemini_response(input,image,prompt):
    # Loading the gemini model
    model=genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([input,image[0],prompt])
    return response.text    #Getting the response in the form of text


# Function for the image_setup 
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
       
           "mime_type":uploaded_file.type,  # Get the mime type of the uploaded file
           "data":bytes_data
        }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file Uploaded")
    

## Initialise our streamlit app
st.set_page_config(page_title="Invoice Extractor")

st.header("Gemini Image Info Extractor")
input=st.text_input("Input Prompt:",key="input")
uploaded_file=st.file_uploader("Choose an Image....",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("Tell me aboutt the Invoice")

# Default instruction for the Gemini model to behave like this.
input_prompt="""
 You are an expert in the understanding invoices.You will receive input images as invoices and you will have to answer the questions based on the input image.

"""

# if submit button is clicked
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)

    st.subheader("The Response is:")
    st.write(response)





