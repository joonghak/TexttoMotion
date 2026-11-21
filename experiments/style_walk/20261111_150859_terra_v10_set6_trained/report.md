# 보상 수식의 숫자만 바꾼 비교 (레퍼런스 고정)

- 폴더: /home/jong/TexttoMotion/experiments/style_walk/20261111_150859_terra_v10_set6_trained
- 레퍼런스: humanoid_walk.pkl 원본 (모두 같음), 보상 수식의 배율만 다름
- 재생: `./experiments/style_walk/play_compare.py experiments/style_walk/20261111_150859_terra_v10_set6_trained`

| 변형 | 배율 | 속도 | 팔 흔들기 폭 | 발 들기 높이 | 상체 기울기 | 완주 | 스텝당 보상 | 학습 |
|---|---|---|---|---|---|---|---|---|
| 기본 걷기 | 추적만 | 1.26 m/s | 0.36 m | 0.13 m | 3.3° | 100% | 0.98 | 2000회 27분 |
| 공룡처럼 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 1.4, n 0.7, c 20, m_arm 0.3, m_torso 6, m_knee 1.2, torso_pitch 15, head_pitch -10, shoulder_flexion 35, elbow_flexion 60, stance_width 8, toe_out 20) | 보폭 1.4, 걸음 수 0.7, 팔 0.3, 다리 굽힘 20, 흔들림 배율 (torso 6, right_shin 1.2, left_shin 1.2), 자세 이동 (torso [0, 15.0, 0], head [0, -10.0, 0], right_upper_arm [-0.0, -35.0, 0.0], left_upper_arm [0.0, -35.0, -0.0], right_lower_arm [0, 0, 60.0], left_lower_arm [0, 0, -60.0], right_thigh [-8.0, 0, -20.0], left_thigh [8.0, 0, 20.0], right_foot [8.0, 0, 0], left_foot [-8.0, 0, 0]) | 1.24 m/s | 0.28 m | 0.25 m | 6.3° | 100% | 0.92 | 2000회 37분 |
| 고양이처럼 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 0.65, n 0.8, c 20, m_arm 0.3, m_knee 0.7, torso_pitch 15, head_pitch 10, shoulder_flexion 15, elbow_flexion 35, stance_width -5, toe_out -10) | 보폭 0.65, 걸음 수 0.8, 팔 0.3, 다리 굽힘 20, 흔들림 배율 (right_shin 0.7, left_shin 0.7), 자세 이동 (torso [0, 15.0, 0], head [0, 10.0, 0], right_upper_arm [-0.0, -15.0, 0.0], left_upper_arm [0.0, -15.0, -0.0], right_lower_arm [0, 0, 35.0], left_lower_arm [0, 0, -35.0], right_thigh [5.0, 0, 10.0], left_thigh [-5.0, 0, -10.0], right_foot [-5.0, 0, 0], left_foot [5.0, 0, 0]) | 0.66 m/s | 0.22 m | 0.18 m | 6.6° | 100% | 0.97 | 2000회 38분 |
| 술 취한 사람처럼 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 0.75, n 0.65, m_arm 0.6, m_torso 8, m_knee 0.8, torso_pitch 10, head_pitch 15, stance_width 8, toe_out 15) | 보폭 0.75, 걸음 수 0.65, 팔 0.6, 흔들림 배율 (torso 8, right_shin 0.8, left_shin 0.8), 자세 이동 (torso [0, 10.0, 0], head [0, 15.0, 0], right_thigh [-8.0, 0, -15.0], left_thigh [8.0, 0, 15.0], right_foot [8.0, 0, 0], left_foot [-8.0, 0, 0]) | 0.62 m/s | 0.28 m | 0.10 m | 6.1° | 100% | 0.96 | 2000회 33분 |
| 화가 나서 쿵쿵 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 1.2, n 1.2, c 15, m_arm 1.5, m_knee 1.4, torso_pitch 10, head_pitch 15, elbow_flexion 45, bounce 20) | 보폭 1.2, 걸음 수 1.2, 팔 1.5, 다리 굽힘 15, 위아래 출렁임 20, 흔들림 배율 (right_shin 1.4, left_shin 1.4), 자세 이동 (torso [0, 10.0, 0], head [0, 15.0, 0], right_lower_arm [0, 0, 45.0], left_lower_arm [0, 0, -45.0]) | 1.82 m/s | 0.36 m | 0.25 m | 5.2° | 100% | 0.89 | 2000회 36분 |
| 펭귄처럼 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 0.6, n 0.8, m_arm 0.3, m_torso 7, m_knee 0.7, shoulder_abduction 45, elbow_flexion 20, stance_width 10, toe_out 20) | 보폭 0.6, 걸음 수 0.8, 팔 0.3, 흔들림 배율 (torso 7, right_shin 0.7, left_shin 0.7), 자세 이동 (right_upper_arm [-45.0, -0.0, 0.0], left_upper_arm [45.0, -0.0, -0.0], right_lower_arm [0, 0, 20.0], left_lower_arm [0, 0, -20.0], right_thigh [-10.0, 0, -20.0], left_thigh [10.0, 0, 20.0], right_foot [10.0, 0, 0], left_foot [-10.0, 0, 0]) | 0.61 m/s | 0.23 m | 0.13 m | 4.9° | 100% | 0.95 | 2000회 32분 |
| 닭처럼 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 0.5, n 1.5, m_arm 0.3, m_knee 1.3, torso_pitch 15, shoulder_abduction -15, elbow_flexion 50, toe_out 25, bounce 20) | 보폭 0.5, 걸음 수 1.5, 팔 0.3, 위아래 출렁임 20, 흔들림 배율 (right_shin 1.3, left_shin 1.3), 자세 이동 (torso [0, 15.0, 0], right_upper_arm [15.0, -0.0, 0.0], left_upper_arm [-15.0, -0.0, -0.0], right_lower_arm [0, 0, 50.0], left_lower_arm [0, 0, -50.0], right_thigh [-0.0, 0, -25.0], left_thigh [0.0, 0, 25.0]) | 0.94 m/s | 0.22 m | 0.30 m | 8.6° | 100% | 0.89 | 2000회 38분 |
| (레퍼런스 원본) | - | 1.26 m/s | 0.32 m | 0.17 m | 3.0° | - | - | - |

속도: 10초 동안 간 거리 ÷ 시간. 팔 흔들기 폭: 골반 기준 손의 앞뒤 이동 범위(양손 평균).
발 들기 높이: 발이 가장 낮을 때 대비 최고 높이. 상체 기울기: 골반→머리 선이 수직에서 기운 평균 각도.
모두 10초 재생 한 번(처음부터, 결정적 정책)으로 측정.
