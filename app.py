"""Main Code for the app"""
import os
import shutil
import uuid
from pathlib import Path

import streamlit as st
from PIL import Image

from wallpaper.wallpaper import wallpaper

session_id = st.session_state.session_id if "session_id" in st.session_state else None
if session_id is None:
    session_id = str(uuid.uuid4())
    st.session_state.session_id = session_id


def zipfolder(folder_path, zip_path):
    shutil.make_archive(zip_path, "zip", folder_path)


def wall_page():
    if "wall" not in st.session_state:
        st.session_state.wall = False

    with st.sidebar:
        st.header("Wallpaper keyword")
        keyword = st.text_input("Keyword", value="cars")
        button = st.button("submit")
    if button:
        folder_path = Path(os.path.join(os.getcwd(), "wallpapers"))
        wall_obj = wallpaper(main_tag=keyword)
        data = wall_obj.get_wallpaper()
        with st.spinner("Downloading Wallpaper"):
            progress_placeholder = st.empty()
            progress_bar = st.progress(0)
            progress_generator = wall_obj.download_wallpaper(data=data)
            for progress_message, progress_percentage in progress_generator:
                progress_placeholder.text(progress_message)
                progress_bar.progress(progress_percentage)
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                image = Image.open(file_path)
                st.image(image, caption="wallpaper", use_column_width=True)
        zipfolder(folder_path, "wallpaper")
        with open("wallpaper.zip", "rb") as f:
            download=st.sidebar.download_button(
                label="Download Wallpapers",
                data=f,
                file_name="Wallpapaer.zip",
                mime="application/zip",
            )
            if download:
                shutil.rmtree(folder_path)
                if os.remove('wallpaper.zip'):
                    st.sidebar.success("File deleted")


menu = ["wallpaper"]
choice = st.sidebar.selectbox("Menu", menu)
if choice == "wallpaper":
    wall_page()
