import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 사용자 지정 한글 폰트 경로 설정
font_path = './fonts/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf'
font_prop = None
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지
else:
    print("❌ 한글 폰트 파일을 찾을 수 없습니다.")

st.title("🔄 일차변환 시각화")
st.markdown("도형과 변환 행렬을 입력하면, 선형변환 결과를 시각화합니다.")

# 1. 도형 선택
shape_type = st.selectbox("도형 종류를 선택하세요", ["삼각형", "사각형", "원", "직선", "평면"])

# 2. 도형 좌표 정의
st.subheader("도형 입력")
if shape_type == "삼각형":
    A = np.array(st.text_input("점 A 좌표 (예: 1,1)", "1,1").split(','), dtype=float)
    B = np.array(st.text_input("점 B 좌표 (예: 1,2)", "1,2").split(','), dtype=float)
    C = np.array(st.text_input("점 C 좌표 (예: 2,1)", "2,1").split(','), dtype=float)
    shape = np.array([A, B, C, A])
elif shape_type == "사각형":
    A = np.array(st.text_input("점 A 좌표 (예: 1,1)", "1,1").split(','), dtype=float)
    B = np.array(st.text_input("점 B 좌표 (예: 1,2)", "1,2").split(','), dtype=float)
    C = np.array(st.text_input("점 C 좌표 (예: 2,2)", "2,2").split(','), dtype=float)
    D = np.array(st.text_input("점 D 좌표 (예: 2,1)", "2,1").split(','), dtype=float)
    shape = np.array([A, B, C, D, A])
elif shape_type == "원":
    center = np.array([1.5, 1.5])
    radius = 0.7
    theta = np.linspace(0, 2*np.pi, 100)
    shape = np.stack([center[0] + radius * np.cos(theta),
                      center[1] + radius * np.sin(theta)], axis=1)
elif shape_type == "직선":
    x = np.linspace(-2, 2, 100)
    y = 0.5 * x + 1
    shape = np.stack([x, y], axis=1)
elif shape_type == "평면":
    grid_x, grid_y = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))
    shape = np.stack([grid_x.flatten(), grid_y.flatten()], axis=1)

# 3. 행렬 입력
st.subheader("2×2 변환 행렬 입력")
a11 = st.number_input("a11", value=1, step=1, format="%d")
a12 = st.number_input("a12", value=2, step=1, format="%d")
a21 = st.number_input("a21", value=3, step=1, format="%d")
a22 = st.number_input("a22", value=4, step=1, format="%d")
matrix = np.array([[a11, a12], [a21, a22]])

# 4. 변환
transformed = np.dot(shape, matrix.T)

# 5. 시각화
fig, ax = plt.subplots(figsize=(2.5, 2.5))

if shape_type in ["삼각형", "사각형", "원", "직선"]:
    ax.plot(shape[:,0], shape[:,1], 'b-', label='원래 도형')
    ax.plot(transformed[:,0], transformed[:,1], 'r--', label='변환된 도형')
elif shape_type == "평면":
    ax.scatter(shape[:,0], shape[:,1], color='blue', s=10, label='원래 평면')
    ax.scatter(transformed[:,0], transformed[:,1], color='red', s=10, label='변환된 평면')

# 자동 축 범위
all_x = np.concatenate([shape[:,0], transformed[:,0], [-1, 1]])
all_y = np.concatenate([shape[:,1], transformed[:,1], [-1, 1]])
margin = 0.5
ax.set_xlim(np.min(all_x) - margin, np.max(all_x) + margin)
ax.set_ylim(np.min(all_y) - margin, np.max(all_y) + margin)

# 축과 원점
ax.axhline(0, color='gray', linewidth=1)
ax.axvline(0, color='gray', linewidth=1)
ax.plot(0, 0, 'ko')
ax.text(0.1, 0.1, '원점', fontsize=8, fontproperties=font_prop)

# 범례
if font_prop:
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1.0), fontsize='small',
              frameon=True, prop=font_prop)
else:
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1.0), fontsize='small',
              frameon=True)

plt.tight_layout(pad=0.3)
st.pyplot(fig)

# 6. 수식 출력
st.latex(rf"""
\text{{입력된 행렬}} = 
\begin{{bmatrix}}
{a11} & {a12} \\
{a21} & {a22}
\end{{bmatrix}}
""")
