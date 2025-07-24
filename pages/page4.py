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
    plt.rcParams['axes.unicode_minus'] = False

# ✅ 정수는 소숫점 생략, 소수는 한 자리까지
def format_number(n):
    return f"{n:.1f}".rstrip('0').rstrip('.') if n % 1 != 0 else str(int(n))

st.title("🔄 일차변환 시각화")
st.markdown("도형과 변환 행렬을 입력하면, 선형변환 결과를 시각화합니다.")

# 도형 선택
shape_type = st.selectbox("도형 종류를 선택하세요", ["삼각형", "사각형", "원", "직선"])

# 도형 정의
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
    center = np.array(st.text_input("원 중심 좌표 (예: 1,1)", "1,1").split(','), dtype=float)
    radius = st.number_input("반지름", value=2.0, step=0.1, format="%.1f")
    theta = np.linspace(0, 2*np.pi, 200)
    shape = np.stack([center[0] + radius * np.cos(theta),
                      center[1] + radius * np.sin(theta)], axis=1)
elif shape_type == "직선":
    st.markdown("직선의 형태: $ax + by = c$")
    a = st.number_input("계수 a", value=1.0, step=0.1, format="%.1f")
    b = st.number_input("계수 b", value=2.0, step=0.1, format="%.1f")
    c = st.number_input("상수 c", value=3.0, step=0.1, format="%.1f")
    x_vals = np.linspace(-5, 5, 400)
    if b != 0:
        y_vals = (c - a * x_vals) / b
    else:
        x_vals = np.full(400, c / a)
        y_vals = np.linspace(-5, 5, 400)
    shape = np.stack([x_vals, y_vals], axis=1)

# 행렬 입력
st.subheader("2×2 변환 행렬 입력")
a11 = st.number_input("a11", value=1, step=1, format="%d")
a12 = st.number_input("a12", value=2, step=1, format="%d")
a21 = st.number_input("a21", value=3, step=1, format="%d")
a22 = st.number_input("a22", value=4, step=1, format="%d")
matrix = np.array([[a11, a12], [a21, a22]])

# 변환 적용
transformed = np.dot(shape, matrix.T)

# 시각화
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')

if shape_type in ["삼각형", "사각형", "원", "직선"]:
    ax.plot(shape[:, 0], shape[:, 1], 'b-', label='원래 도형')
    ax.plot(transformed[:, 0], transformed[:, 1], 'r--', label='변환된 도형')

# 원점 및 축
ax.axhline(0, color='gray')
ax.axvline(0, color='gray')
ax.plot(0, 0, 'ko', markersize=3)

# 축 범위 자동 조절 (1.5배 확장)
all_x = np.concatenate([shape[:, 0], transformed[:, 0]])
all_y = np.concatenate([shape[:, 1], transformed[:, 1]])
x_center = np.mean(all_x)
y_center = np.mean(all_y)
x_range = np.ptp(all_x)
y_range = np.ptp(all_y)
half_range = max(x_range, y_range) * 0.75
if half_range < 1:
    half_range = 2
ax.set_xlim(x_center - half_range, x_center + half_range)
ax.set_ylim(y_center - half_range, y_center + half_range)

# 범례
ax.legend(loc='upper left', prop=font_prop if font_prop else None)
plt.tight_layout()
st.pyplot(fig)

# 수식 출력
st.subheader("수식 표시")
st.latex(rf"""
\text{{입력된 행렬}} = 
\begin{{bmatrix}}
{a11} & {a12} \\
{a21} & {a22}
\end{{bmatrix}}
""")

if shape_type == "원":
    st.latex(rf"(x - {format_number(center[0])})^2 + (y - {format_number(center[1])})^2 = {format_number(radius)}^2")
elif shape_type == "직선":
    st.latex(rf"\text{{입력된 직선:}} \quad {format_number(a)}x + {format_number(b)}y = {format_number(c)}")

    # 변환된 직선 추정
    if b != 0:
        p1 = np.array([0, c / b])
        p2 = np.array([c / a if a != 0 else 1, 0])
    else:
        p1 = np.array([c / a, 0])
        p2 = np.array([c / a, 1])
    points = np.vstack([p1, p2])
    new_points = np.dot(points, matrix.T)
    x1, y1 = new_points[0]
    x2, y2 = new_points[1]

    if x2 != x1:
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        st.latex(rf"\text{{변환된 직선:}} \quad y = {slope:.2f}x + {intercept:.2f}")
    else:
        st.latex(rf"\text{{변환된 직선:}} \quad x = {x1:.2f}")

