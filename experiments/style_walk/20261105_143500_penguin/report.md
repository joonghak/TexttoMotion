# 보상 수식의 숫자만 바꾼 비교 (레퍼런스 고정)

- 폴더: /home/jong/TexttoMotion/experiments/style_walk/20261105_143500_penguin
- 레퍼런스: humanoid_walk.pkl 원본 (모두 같음), 보상 수식의 배율만 다름
- 재생: `./experiments/style_walk/play_compare.py experiments/style_walk/20261105_143500_penguin`

| 변형 | 배율 | 속도 | 팔 흔들기 폭 | 발 들기 높이 | 상체 기울기 | 완주 | 스텝당 보상 | 학습 |
|---|---|---|---|---|---|---|---|---|
| 기본 걷기 | 추적만 | 1.26 m/s | 0.36 m | 0.13 m | 3.3° | 100% | 0.98 | 2000회 27분 |
| 펭귄 A: 지금 파라미터만 (s 0.4, n 1.2, m_arm 0.3, m_knee 0.7, 팔꿈치 신전 30, 다리 벌림 10, m_torso 5) | 보폭 0.4, 걸음 수 1.2, 팔 0.3, 흔들림 배율 (torso 5, right_shin 0.7, left_shin 0.7), 자세 이동 (right_lower_arm [0, 0, -30], left_lower_arm [0, 0, 30], right_thigh [-10, 0, 0], left_thigh [10, 0, 0], right_foot [10, 0, 0], left_foot [-10, 0, 0]) | 0.61 m/s | 0.26 m | 0.13 m | 3.1° | 100% | 0.95 | 2000회 32분 |
| 펭귄 B: A + 발끝 벌림 30 + 팔 흔들기 0 | 보폭 0.4, 걸음 수 1.2, 팔 0, 흔들림 배율 (torso 5, right_shin 0.7, left_shin 0.7), 자세 이동 (right_lower_arm [0, 0, -30], left_lower_arm [0, 0, 30], right_thigh [-10, 0, -30], left_thigh [10, 0, 30], right_foot [10, 0, 0], left_foot [-10, 0, 0]) | 0.60 m/s | 0.21 m | 0.12 m | 3.6° | 100% | 0.94 | 2000회 34분 |
| 펭귄 C: B + 상체 흔들림 10 (뒤뚱거림 과장) | 보폭 0.4, 걸음 수 1.2, 팔 0, 흔들림 배율 (torso 10, right_shin 0.7, left_shin 0.7), 자세 이동 (right_lower_arm [0, 0, -30], left_lower_arm [0, 0, 30], right_thigh [-10, 0, -30], left_thigh [10, 0, 30], right_foot [10, 0, 0], left_foot [-10, 0, 0]) | 0.61 m/s | 0.21 m | 0.12 m | 6.3° | 100% | 0.93 | 2000회 32분 |
| 펭귄 D: s 0.3, n 1.3, m_knee 0.4 (발 끌기), m_arm 0, 팔꿈치 신전 30, 어깨 안쪽 15 (팔을 몸에 붙임), 발끝 벌림 30, 다리 벌림 5, m_torso 10 | 보폭 0.3, 걸음 수 1.3, 팔 0, 흔들림 배율 (torso 10, right_shin 0.4, left_shin 0.4), 자세 이동 (right_lower_arm [0, 0, -30], left_lower_arm [0, 0, 30], right_upper_arm [15, 0, 0], left_upper_arm [-15, 0, 0], right_thigh [-5, 0, -30], left_thigh [5, 0, 30], right_foot [5, 0, 0], left_foot [-5, 0, 0]) | 0.49 m/s | 0.21 m | 0.07 m | 6.5° | 100% | 0.92 | 2000회 33분 |
| 펭귄 E: D에서 다리 벌림 없이 (뒤뚱거림은 흔들림과 발끝 벌림으로) | 보폭 0.3, 걸음 수 1.3, 팔 0, 흔들림 배율 (torso 10, right_shin 0.4, left_shin 0.4), 자세 이동 (right_lower_arm [0, 0, -30], left_lower_arm [0, 0, 30], right_upper_arm [15, 0, 0], left_upper_arm [-15, 0, 0], right_thigh [0, 0, -30], left_thigh [0, 0, 30]) | 0.49 m/s | 0.21 m | 0.06 m | 6.3° | 100% | 0.93 | 2000회 33분 |
| (레퍼런스 원본) | - | 1.26 m/s | 0.32 m | 0.17 m | 3.0° | - | - | - |

속도: 10초 동안 간 거리 ÷ 시간. 팔 흔들기 폭: 골반 기준 손의 앞뒤 이동 범위(양손 평균).
발 들기 높이: 발이 가장 낮을 때 대비 최고 높이. 상체 기울기: 골반→머리 선이 수직에서 기운 평균 각도.
모두 10초 재생 한 번(처음부터, 결정적 정책)으로 측정.
