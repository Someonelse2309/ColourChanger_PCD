import streamlit as st
import cv2
import numpy as np
from program import replacingColor

st.session_state.colorReplace = replacingColor()

if "status" not in st.session_state:
    st.session_state.status = False

uploaded_file = st.file_uploader("Upload Gambar Anda", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    st.image(img, channels='BGR', caption="Gambar Sebelum")
else:
    st.write("Belum ada gambar di-upload.")

tab1, tab2 = st.tabs(["Pengaturan Warna", "Pengaturan Threshold"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        colorAwal = st.color_picker("Warna yang ingin diganti",
                                    help="Warna yang ingin diganti dari gambar.")

    with col2:
        colorAkhir = st.color_picker("Ganti dengan warna ini",
                                     help="Warna dari gambar akan diganti dengan warna ini.")



with tab2:
    col1T, col2T, col3T = st.columns(3)
    hTol, sTol, vTol = st.session_state.colorReplace.getThreshold()
    with col1T:
        hTolInp = st.number_input(
            label="Toleransi H",
            max_value=255,
            min_value=0,
            value=hTol,
            placeholder="Masukan Toleransi H Ada",
            help="Seberapa banyak variasi \'jenis\' warna yang masih Anda anggap sama, misalnya seberapa jauh sebuah warna bisa bergeser dari \'merah murni\' tapi tetap dianggap merah (bukan oranye atau pink).",
        )

    with col2T:
        sTolInp = st.number_input(
            label="Toleransi S",
            max_value=255,
            min_value=0,
            value=sTol,
            placeholder="Masukan Toleransi S Ada",
            help="Seberapa pudar atau seberapa mencolok sebuah warna yang masih Anda terima, misalnya apakah merah yang sedikit pudar masih dianggap sama dengan merah yang sangat pekat."
        )

    with col3T:
        sTolInp = st.number_input(
            label="Toleransi V",
            max_value=255,
            min_value=0,
            value=vTol,
            placeholder="Masukan Toleransi V Ada",
            help="Seberapa terang atau gelap sebuah warna yang masih Anda anggap cocok, misalnya apakah merah yang agak gelap masih sama dengan merah yang sangat terang di bawah sinar matahari."
        )


if st.button("Ubah Warna"):
    st.session_state.colorReplace.changeThreshold(hTolInp,sTolInp,sTolInp)
    st.session_state.colorReplace.inputImage(img, colorAwal,colorAkhir)
    st.session_state.status = True

if st.session_state.get("status", False) and st.session_state.colorReplace.getMasking() != None and st.session_state.colorReplace.getResult() != None:
    col1Result, col2Result = st.columns(2)
    with col1Result:
        st.image(st.session_state.colorReplace.getMasking(), channels='GRAY', caption="Hasil Masking")
    with col2Result:
        st.image(st.session_state.colorReplace.getResult(), channels='BGR', caption="Hasil Akhir")
else:
    pass
