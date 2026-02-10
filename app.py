import streamlit as st
import cv2
import numpy as np

st.title("📷 QR Code Scanner")

uploaded_file = st.file_uploader("Upload an image with a QR code", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert uploaded file to OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Uploaded Image", use_column_width=True)

    # Initialize QRCode detector
    qr_detector = cv2.QRCodeDetector()

    # Detect and decode
    data, bbox, _ = qr_detector.detectAndDecode(image)

    if bbox is not None:
        # Draw bounding box
        n_lines = len(bbox)
        for i in range(n_lines):
            pt1 = tuple(bbox[i][0])
            pt2 = tuple(bbox[(i+1) % n_lines][0])
            cv2.line(image, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), (255, 0, 0), 2)

        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Detected QR Code", use_column_width=True)

    if data:
        st.success(f"Decoded Data: {data}")
    else:
        st.warning("No QR code detected in the image.")
