# xray_app.py
import cv2
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import io
import datetime

# ----------------------------
# Utility Functions
# ----------------------------

def plot_results(original_img, processed_img, transform_lut=None,
                 original_title="Original Image", processed_title="Processed Image"):
    """Displays original/processed images, transformation curve, and histograms using Matplotlib."""
    st.subheader("Comparison")

    col1, col2 = st.columns(2)
    with col1:
        st.image(original_img, caption=original_title, use_container_width=True, clamp=True, channels="GRAY")
    with col2:
        st.image(processed_img, caption=processed_title, use_container_width=True, clamp=True, channels="GRAY")

    # Transformation curve
    if transform_lut is not None:
        fig, ax = plt.subplots()
        ax.plot(np.arange(256), transform_lut, color="red")
        ax.set_title("Transformation Function s = T(r)")
        ax.set_xlabel("Input Intensity (r)")
        ax.set_ylabel("Output Intensity (s)")
        ax.set_xlim([0, 255])
        ax.set_ylim([0, 255])
        st.pyplot(fig)

    # Histograms
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].hist(original_img.ravel(), bins=256, range=(0, 255), color="blue")
    axes[0].set_title("Original Histogram")
    axes[0].set_xlim([0, 255])

    axes[1].hist(processed_img.ravel(), bins=256, range=(0, 255), color="green")
    axes[1].set_title("Processed Histogram")
    axes[1].set_xlim([0, 255])
    st.pyplot(fig)

# ----------------------------
# Enhancement Functions
# ----------------------------

def apply_gamma(img, gamma):
    lut = np.array([((i / 255.0) ** gamma) * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(img, lut), lut

def apply_hist_eq(img):
    gray = img if len(img.shape) == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.equalizeHist(gray)

def apply_contrast_stretch(img, low, high):
    lut = np.zeros(256, dtype=np.uint8)
    if high > low:
        lut[low:high] = np.linspace(0, 255, high - low).astype("uint8")
        lut[high:] = 255
    return cv2.LUT(img, lut), lut

def apply_gamma_hist(img, gamma):
    gamma_img, _ = apply_gamma(img, gamma)
    return apply_hist_eq(gamma_img)

# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(page_title="X-Ray Enhancement Dashboard", layout="wide")
st.title("🩻 Chest X-Ray Enhancement Dashboard")

uploaded_file = st.file_uploader("Upload a Chest X-Ray Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read uploaded image as grayscale
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    original_image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

    st.sidebar.title("Controls")
    option = st.sidebar.radio(
        "Choose Enhancement Technique",
        ["Gamma Transformation", "Histogram Equalization", "Contrast Stretching", "Gamma + HistEq"]
    )

    if option == "Gamma Transformation":
        gamma_val = st.sidebar.slider("Gamma Value", 0.1, 5.0, 1.0, 0.1)
        processed_img, lut = apply_gamma(original_image, gamma_val)
        plot_results(original_image, processed_img, lut,
                     processed_title=f"Gamma (γ={gamma_val:.2f})")

    elif option == "Histogram Equalization":
        processed_img = apply_hist_eq(original_image)
        plot_results(original_image, processed_img,
                     processed_title="Histogram Equalization")

    elif option == "Contrast Stretching":
        low, high = st.sidebar.slider("Select Intensity Range", 0, 255, (50, 200))
        processed_img, lut = apply_contrast_stretch(original_image, low, high)
        plot_results(original_image, processed_img, lut,
                     processed_title=f"Contrast Stretching ({low}-{high})")

    elif option == "Gamma + HistEq":
        gamma_val = st.sidebar.slider("Gamma Value", 0.1, 5.0, 1.0, 0.1)
        processed_img = apply_gamma_hist(original_image, gamma_val)
        plot_results(original_image, processed_img,
                     processed_title=f"Gamma (γ={gamma_val:.2f}) + Histogram Equalization")

    # Save/download button
    buf = io.BytesIO()
    pil_img = Image.fromarray(processed_img)
    pil_img.save(buf, format="PNG")
    st.download_button(
        label="💾 Download Enhanced Image",
        data=buf.getvalue(),
        file_name=f"enhanced_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        mime="image/png"
    )
else:
    st.info("Please upload an image to get started.")
