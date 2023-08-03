import streamlit as st
import easyocr
import cv2
from pdf2image import convert_from_path
import os

def ocr_img(img_name):
    reader = easyocr.Reader(['en'], gpu = False)
    result = reader.readtext(img_name)
    return result

def display_result_img(results, img_name):
    img = cv2.imread(img_name)
    text = ''
    for result in results:
        top_left = tuple(result[0][0])
        bottom_right = tuple(result[0][2])
        img = cv2.rectangle(img, top_left, bottom_right, (0,225,0), 2)
        text += result[1]+'\n\n'
    st.image(img)
    st.write(text)
    return


def ocr_pdf(uploaded_file):
    images = convert_from_path(uploaded_file.name)
    results = []
    img_paths = []
    reader = easyocr.Reader(['en'], gpu = False)
    for i in range(len(images)):
        images[i].save('page'+ str(i) +'.jpg')
        img_path = (('page'+ str(i) +'.jpg'))
        img_paths.append(img_path)
        result = reader.readtext(img_path)
        results.append(result)
    return results, img_paths

def display_result_pdf(results, img_paths):
    i = 0
    for img_path in img_paths:
        img = cv2.imread(img_path)
        text = ''
        for result in results[i]:
            top_left = tuple(result[0][0])
            bottom_right = tuple(result[0][2])
            img = cv2.rectangle(img, top_left, bottom_right, (0,225,0), 2)
            text += result[1]+'\n'
        st.image(img)
        st.write(text)
        i += 1
        os.remove(img_path)
    return





def main():
    uploaded_file = st.file_uploader('upload your files here')

    if st.button("Process"):
        with open(os.path.join(uploaded_file.name),"wb") as f:
            f.write(uploaded_file.getbuffer())


        
        if uploaded_file.name.split('.')[1]!='pdf':
            img_name = uploaded_file.name
            result = ocr_img(img_name)
            display_result_img(result, img_name)


        if uploaded_file.name.split('.')[1]=='pdf':
            result, img_paths = ocr_pdf(uploaded_file)
            display_result_pdf(result, img_paths)


        os.remove(uploaded_file.name)


if __name__ == '__main__':
    main()