import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("📷 QR Code Scanner")

mode = st.radio("Choose mode:", ["Upload Image", "Webcam QR Scan"])

if mode == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        qr_detector = cv2.QRCodeDetector()
        data, bbox, _ = qr_detector.detectAndDecode(cv_image)

        if bbox is not None:
            n_lines = len(bbox)
            for i in range(n_lines):
                pt1 = tuple(bbox[i][0])
                pt2 = tuple(bbox[(i+1) % n_lines][0])
                cv2.line(cv_image, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), (255, 0, 0), 2)
            st.image(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB), caption="Detected QR Code", use_column_width=True)

        if data:
            st.success(f"Decoded Data: {data}")
            if data.startswith("http://") or data.startswith("https://"):
                st.markdown(f"[Open Link]({data})")
        else:
            st.warning("No QR code detected.")

elif mode == "Webcam QR Scan":
    st.write("Click 'Start' to scan QR codes live from your webcam.")
    run = st.checkbox("Start Webcam")

    if run:
        cap = cv2.VideoCapture(0)
        qr_detector = cv2.QRCodeDetector()
        stframe = st.empty()

        while run:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to access webcam.")
                break

            data, bbox, _ = qr_detector.detectAndDecode(frame)
            if bbox is not None:
                n_lines = len(bbox)
                for i in range(n_lines):
                    pt1 = tuple(bbox[i][0])
                    pt2 = tuple(bbox[(i+1) % n_lines][0])
                    cv2.line(frame, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), (0, 255, 0), 2)

            if data:
                st.success(f"Decoded Data: {data}")
                if data.startswith("http://") or data.startswith("https://"):
                    st.markdown(f"[Open Link]({data})")

            stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        cap.release()
