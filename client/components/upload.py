import streamlit as st
from utils.api import upload_pdfs_api

def render_uploader():
    st.sidebar.header("Upload Documents (.PDF)")
    uploaded_files = st.sidebar.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    
    if st.sidebar.button("Upload to Vector DB") and uploaded_files:
        response = upload_pdfs_api(uploaded_files)
        if response.status_code == 200:
            st.sidebar.success("Uploaded successfully")
        else:
            st.sidebar.error(f"Error: {response.text}")
