import streamlit as st
from PIL import Image
import numpy as np

# Fungsi untuk menyembunyikan pesan dalam gambar
def encrypt_image(image, message):
    # Ubah pesan menjadi biner
    message_bin = ''.join(format(ord(i), '08b') for i in message) + '00000000'  # Menambahkan terminator
    data_index = 0
    img_data = np.array(image)

    for i in range(img_data.shape[0]):
        for j in range(img_data.shape[1]):
            # Ambil pixel
            pixel = list(img_data[i][j])
            # Ganti bit terakhir dengan bit dari pesan
            for k in range(3):  # R, G, B
                if data_index < len(message_bin):
                    pixel[k] = pixel[k] & ~1 | int(message_bin[data_index])
                    data_index += 1
            img_data[i][j] = tuple(pixel)
            if data_index >= len(message_bin):
                break

    encrypted_image = Image.fromarray(img_data)
    return encrypted_image

# Fungsi untuk mengambil pesan dari gambar
def decrypt_image(image):
    img_data = np.array(image)
    message_bin = ""

    for i in range(img_data.shape[0]):
        for j in range(img_data.shape[1]):
            pixel = img_data[i][j]
            for k in range(3):  # R, G, B
                message_bin += str(pixel[k] & 1)

    # Pisahkan biner menjadi karakter
    message = ""
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i+8]
        if byte == "00000000":
            break
        message += chr(int(byte, 2))

    return message

# Halaman Utama
st.title("Rnh HideNSeek")

# Pilihan menu untuk pengguna
menu = st.sidebar.selectbox("Pilih Halaman:", ["Home", "Encrypt", "Decrypt"])

if menu == "Home":
    # Hanya menampilkan deskripsi di halaman utama
    st.write("""
        Selamat datang di **Rnh HideNSeek**, aplikasi steganografi yang cerdas dan aman! 
        Apakah Anda pernah merasa perlu menyembunyikan pesan rahasia dalam gambar? Kini, Anda dapat melakukannya dengan mudah di sini. 
        Dengan teknologi **Least Significant Bit (LSB)**, kami memberikan solusi aman dan tersembunyi untuk menyematkan pesan pribadi Anda ke dalam gambar yang tampak biasa.

        Jelajahi fitur **Encrypt** untuk menyembunyikan pesan rahasia atau gunakan **Decrypt** untuk membuka pesan tersembunyi dari gambar. 
        Rahasia Anda, aman bersama kami!
    """)

elif menu == "Encrypt":
    st.subheader("Halaman Enkripsi")
    st.write("Tuliskan pesan yang ingin Anda sembunyikan.")
    
    # Input untuk enkripsi
    message = st.text_area("Pesan:")
    uploaded_file = st.file_uploader("Input File (jpg/png)", type=["jpg", "png"])
    
    if uploaded_file and message:
        image = Image.open(uploaded_file)
        if st.button("Encrypt"):
            encrypted_image = encrypt_image(image, message)
            st.subheader("Hasil Enkripsi")
            st.image(encrypted_image, caption="Gambar yang Sudah Dienkripsi", use_column_width=True)

            # Menyimpan gambar yang dienkripsi
            encrypted_image_path = "encrypted_image.png"
            encrypted_image.save(encrypted_image_path)
            st.download_button("Download Gambar yang Dienkripsi", data=open(encrypted_image_path, "rb"), file_name="encrypted_image.png")
            st.write("Pesan yang dienkripsi:", message)

elif menu == "Decrypt":
    st.subheader("Halaman Dekripsi")
    
    uploaded_file = st.file_uploader("Input Gambar untuk Dekripsi (jpg/png)", type=["jpg", "png"], key="decrypt_file")
    if uploaded_file:
        image = Image.open(uploaded_file)
    if st.button("Decrypt"):
        decrypted_message = decrypt_image(image)
        st.write("Plaintext (hasil dekripsi):", decrypted_message)
