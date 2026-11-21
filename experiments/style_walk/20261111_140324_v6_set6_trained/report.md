# 보상 수식의 숫자만 바꾼 비교 (레퍼런스 고정)

- 폴더: /home/jong/TexttoMotion/experiments/style_walk/20261111_140324_v6_set6_trained
- 레퍼런스: humanoid_walk.pkl 원본 (모두 같음), 보상 수식의 배율만 다름
- 재생: `./experiments/style_walk/play_compare.py experiments/style_walk/20261111_140324_v6_set6_trained`

| 변형 | 배율 | 속도 | 팔 흔들기 폭 | 발 들기 높이 | 상체 기울기 | 완주 | 스텝당 보상 | 학습 |
|---|---|---|---|---|---|---|---|---|
| 기본 걷기 | 추적만 | 1.26 m/s | 0.36 m | 0.13 m | 3.3° | 100% | 0.98 | 2000회 27분 |
| 공룡처럼 걸어: Qwen3-4B-Thinking-2507, 프롬프트 v6이 정한 값 (n 0.75, c 30, torso_pitch 35, head_pitch 25, stance_width 10) | 걸음 수 0.75, 다리 굽힘 30, 자세 이동 (torso [0, 35.0, 0], head [0, 25.0, 0], right_thigh [-10.0, 0, -0.0], left_thigh [10.0, 0, 0.0], right_foot [10.0, 0, 0], left_foot [-10.0, 0, 0]) | 0.95 m/s | 0.41 m | 0.31 m | 15.2° | 100% | 0.95 | 2000회 33분 |
| 고양이처럼 걸어: Qwen3-4B-Thinking-2507, 프롬프트 v6이 정한 값 (s 0.6, n 1.25, c 30, m_arm 0.4, m_torso 3, m_knee 0.8, torso_pitch 15, head_pitch -15) | 보폭 0.6, 걸음 수 1.25, 팔 0.4, 다리 굽힘 30, 흔들림 배율 (torso 3, right_shin 0.8, left_shin 0.8), 자세 이동 (torso [0, 15.0, 0], head [0, -15.0, 0]) | 0.94 m/s | 0.25 m | 0.24 m | 7.0° | 100% | 0.96 | 2000회 37분 |
| 술 취한 사람처럼 걸어: Qwen3-4B-Thinking-2507, 프롬프트 v6이 정한 값 (s 0.6, n 0.55, m_torso 10, torso_pitch 15, head_pitch 25, elbow_flexion -30) | 보폭 0.6, 걸음 수 0.55, 흔들림 배율 (torso 10), 자세 이동 (torso [0, 15.0, 0], head [0, 25.0, 0], right_lower_arm [0, 0, -30.0], left_lower_arm [0, 0, 30.0]) | 0.41 m/s | 0.49 m | 0.09 m | 8.2° | 100% | 0.94 | 2000회 34분 |
| 화가 나서 쿵쿵 걸어: Qwen3-4B-Thinking-2507, 프롬프트 v6이 정한 값 (n 1.25, c 15, m_arm 1.5, m_knee 1.5) | 걸음 수 1.25, 팔 1.5, 다리 굽힘 15, 흔들림 배율 (right_shin 1.5, left_shin 1.5) | 1.58 m/s | 0.47 m | 0.35 m | 3.4° | 100% | 0.92 | 2000회 32분 |
| (레퍼런스 원본) | - | 1.26 m/s | 0.32 m | 0.17 m | 3.0° | - | - | - |

속도: 10초 동안 간 거리 ÷ 시간. 팔 흔들기 폭: 골반 기준 손의 앞뒤 이동 범위(양손 평균).
발 들기 높이: 발이 가장 낮을 때 대비 최고 높이. 상체 기울기: 골반→머리 선이 수직에서 기운 평균 각도.
모두 10초 재생 한 번(처음부터, 결정적 정책)으로 측정.
