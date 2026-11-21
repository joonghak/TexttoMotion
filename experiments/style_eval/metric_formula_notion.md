# 스타일 유사도 지표 (100STYLE 기준)

노션: 빈 줄에서 /수식 → 수식 블록 → 아래 한 줄을 그대로 붙여 넣는다.

**① 기본 걸음과의 차이와 정규화**

$$
d_k=\begin{cases}\ln\dfrac{f_k^{\text{스타일}}}{f_k^{\text{기본}}} & k\in\{\text{보폭},\ \text{박자}\}\\[6pt] f_k^{\text{스타일}}-f_k^{\text{기본}} & \text{나머지 16개 특징}\end{cases}\qquad z_k=\dfrac{d_k}{\sigma_k}\ \ (k=1,\dots,18)
$$

**② 유사도, 순위, 크기**

$$
\begin{aligned}\text{유사도}&=\dfrac{\sum_{k=1}^{18}\bar{z}_k\,z_k}{\lVert\bar{\mathbf{z}}\rVert\,\lVert\mathbf{z}\rVert}\\[6pt]\text{순위}&=1+\left|\left\{s:\cos(\bar{\mathbf{z}},\mathbf{z}_s)>\cos(\bar{\mathbf{z}},\mathbf{z})\right\}\right|\\[6pt]\text{크기}&=\dfrac{\lVert\bar{\mathbf{z}}\rVert}{\lVert\mathbf{z}\rVert}\end{aligned}
$$

**기호**

- f_k: 걸음 특징 k의 값이다. 보폭, 박자, 상체 앞 기울기, 상체 좌우 기울기 폭, 고개 숙임, 팔 흔들기 폭, 손의 앞 위치, 손 높이, 손의 바깥 위치, 팔꿈치 굽힘, 무릎 굽힘, 골반 높이, 발 들림, 두 발 간격, 골반 좌우 흔들림, 머리 좌우 흔들림, 골반 위아래 움직임, 발끝 바깥 각도의 18개를 곧게 걷는 구간에서 진행 방향 기준으로 재며, 길이는 다리나 팔 길이로 나눈다.
- 스타일, 기본: 우리 쪽은 학습한 정책과 우리 기본 걷기 정책, 100STYLE 쪽은 그 스타일 클립과 Neutral 클립이다. 발끝 각도만 100개 클립의 중앙값을 기본으로 쓴다.
- σ_k: 100STYLE 99종(Neutral 제외)에서 d_k의 표준편차이다.
- z̄ (바): 우리 정책의 z_k 18개를 모은 벡터이다. z: 목표로 정한 100STYLE 스타일의 벡터이다. z_s: 100STYLE 스타일 s의 벡터이다.
- s: 100STYLE 99종 각각이다. 순위 1은 99종 가운데 목표 스타일이 가장 비슷하다는 뜻이다.
