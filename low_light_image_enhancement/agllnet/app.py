import streamlit as st
import numpy as np
import cv2
import os
import subprocess
from agllnet import recognize_from_image

# Konfigurasi Streamlit
st.set_page_config(page_title="Low Light Enhancement", layout="centered")

# Fungsi untuk menyimpan sementara gambar yang diunggah
def save_uploaded_file(uploaded_file, save_path="input.png"):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Fungsi untuk memuat gambar
def load_image(image_path):
    return cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

# Halaman utama
st.title("Low Light Enhancement with AGLLNet")
st.write("Unggah gambar dengan pencahayaan rendah, dan lihat hasil gambar yang telah diperbaiki.")

# Upload Gambar
uploaded_file = st.file_uploader("Unggah gambar di sini", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Simpan file yang diunggah sementara
    save_uploaded_file(uploaded_file, "input.png")
    
    # Tampilkan gambar asli
    st.subheader("Gambar Asli")
    original_image = load_image("input.png")
    st.image(original_image, caption="Gambar Asli", use_column_width=True)
    
    # Jalankan model AGLLNet
    st.subheader("Proses Peningkatan Cahaya")
    with st.spinner("Memproses gambar..."):
        # Proses gambar menggunakan subprocess untuk menjalankan AGLLNet dengan argumen input dan output
        input_path = "input.png"
        output_path = "output.png"
        
        # Menjalankan perintah AGLLNet dengan subprocess
        subprocess.run([
            "python", "agllnet.py", "--input", input_path, "--savepath", output_path
        ])
        
        # Membaca hasil gambar yang sudah diproses
        output_image = load_image(output_path)
        
    # Tampilkan gambar hasil
    st.subheader("Gambar Setelah Ditingkatkan")
    st.image(output_image, caption="Gambar Ditingkatkan", use_column_width=True)

    # Unduh hasil gambar
    with open(output_path, "rb") as file:
        st.download_button(
            label="Unduh Gambar",
            data=file,
            file_name="enhanced_image.png",
            mime="image/png"
        )
