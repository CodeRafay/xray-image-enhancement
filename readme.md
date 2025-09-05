# Chest X-Ray Image Enhancement using Point Processing Techniques

## 📌 Introduction

Medical imaging often suffers from low contrast, making it difficult for radiologists and automated systems to detect abnormalities such as **pneumonia in chest X-rays**. Enhancing these images can reveal hidden details, improve visibility of anatomical structures, and support more accurate diagnosis.

This project focuses on improving **the visibility of bone and lung structures in low-contrast X-ray images** using **point processing transformations** and histogram-based techniques.

---

## 📂 Dataset

**Source**: [Kaggle – Chest X-Ray Pneumonia Dataset](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)

- The dataset is organized into **3 folders**: `train`, `test`, and `val`, each containing subfolders for categories **Pneumonia** and **Normal**.
- Contains **5,863 anterior-posterior (AP) chest X-Ray images** (JPEG).
- Patient group: **pediatric patients aged 1–5 years**, collected at Guangzhou Women and Children’s Medical Center.
- Quality control: Low-quality/unreadable scans were removed. Diagnoses were graded by **two expert physicians**, with an additional third review on the evaluation set for consistency.

---

## ⚙️ Prerequisites

Before running the project, install the following dependencies:

```bash
pip install opencv-python matplotlib numpy
```

If running on **Google Colab**, you only need to upload your notebook and dataset.

---

## 🔬 Methodology & Justification

### 1. **Gamma (Power-Law) Transformation**

- **Justification**: Enhances visibility in darker regions while compressing bright areas. Useful for lung field details.
- **Function**:

  $$
  s = c \cdot r^\gamma
  $$

  where `c` is a scaling constant and `γ` controls brightness/contrast.

---

### 2. **Histogram Equalization**

- **Justification**: Spreads out pixel intensities, improving global contrast.
- **Function**: Redistributes histogram values so intensities are more evenly spread across 0–255.

---

### 3. **Contrast Stretching**

- **Justification**: Expands a narrow range of intensity values to cover the full spectrum, improving image clarity.
- **Function**:

  $$
  s = \frac{(r - r_{min})}{(r_{max} - r_{min})} \times (L-1)
  $$

---

### 4. **Gamma + Histogram Equalization (Combination)**

- **Justification**: Gamma first enhances darker lung regions, while histogram equalization redistributes contrast globally. This gives the most balanced and clinically useful result.

---

## 📊 Results & Analysis

- **Gamma Transformation**: Improved darker details but limited global contrast.
- **Histogram Equalization**: Strong global contrast improvement, but sometimes introduced noise in bright regions.
- **Contrast Stretching**: Helped when intensity range was narrow but less effective in varied datasets.
- **Combination (Gamma + Histogram Equalization)**: Provided the **best overall enhancement**, balancing detail visibility with global contrast.

### Histogram Behavior Summary (Quick Guide)

- **Gamma (<1)**: Histogram shifts right (brighter image).
- **Gamma (>1)**: Histogram shifts left (darker image).
- **Histogram Equalization**: Histogram flattens and spreads across full range.
- **Contrast Stretching**: Histogram expands from compressed/narrow range to full 0–255.
- **Combination**: Histogram shows both spread and adjusted distribution for balanced enhancement.

---

## Conclusion

- The combination of **Gamma Transformation + Histogram Equalization** gave the **most diagnostically useful results**.
- This combination enhanced subtle lung details while also redistributing global contrast effectively.
- **Recommendation**: For medical image enhancement tasks, particularly chest X-rays, apply **Gamma → Histogram Equalization** for optimal clarity.

---

## 💻 Usage

1. Run the Jupyter Notebook / Colab Notebook.
2. Upload a chest X-ray image (`.jpg`, `.jpeg`, `.png`).
3. Select a transformation (Gamma, Histogram Equalization, Contrast Stretching, or Combination).
4. View **original vs enhanced image** side by side with their histograms.
5. Optionally **save the enhanced image** to your local machine.

---

## 📂 Appendix (Code)

The full well-commented code is available in the project notebook:

- Check the attached `.ipynb` file in this repository.

---

👨‍💻 **Author**: Rafay Adeel

📧 Contact: [Rafay Adeel](mailto:rafayadeel1999@gmail.com)
