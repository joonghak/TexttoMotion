# 보상 수식의 숫자만 바꾼 비교 (레퍼런스 고정)

- 폴더: /home/jong/TexttoMotion/experiments/style_walk/20261112_221819_terra_v11_set9_trained
- 레퍼런스: humanoid_walk.pkl 원본 (모두 같음), 보상 수식의 배율만 다름
- 재생: `./experiments/style_walk/play_compare.py experiments/style_walk/20261112_221819_terra_v11_set9_trained`

| 변형 | 배율 | 속도 | 팔 흔들기 폭 | 발 들기 높이 | 상체 기울기 | 완주 | 스텝당 보상 | 학습 |
|---|---|---|---|---|---|---|---|---|
| 기본 걷기 | 추적만 | 1.26 m/s | 0.36 m | 0.13 m | 3.3° | 100% | 0.98 | 2000회 27분 |
| 오른쪽 다리를 절뚝거리며 걸어: gpt-5.6-terra, 프롬프트 v11이 정한 값 (right_m_knee 0.4) | 흔들림 배율 (right_shin 0.4) | 1.26 m/s | 0.39 m | 0.11 m | 3.3° | 100% | 0.98 | 2000회 30분 |
| 왼손을 번쩍 들고 걸어: gpt-5.6-terra, 프롬프트 v11이 정한 값 (left_m_arm 0.3, left_shoulder_flexion 85) | 흔들림 배율 (left_upper_arm 0.3, left_lower_arm 0.3), 자세 이동 (left_upper_arm [0.0, -85.0, -0.0]) | 1.26 m/s | 0.29 m | 0.15 m | 3.4° | 100% | 0.98 | 2000회 31분 |
| 무거운 가방을 왼쪽 어깨에 메고 걸어: gpt-5.6-terra, 프롬프트 v11이 정한 값 (s 0.85, n 0.8, torso_roll 15, head_roll 12, left_m_arm 0.3, left_shoulder_flexion 45, left_elbow_flexion 60) | 보폭 0.85, 걸음 수 0.8, 흔들림 배율 (left_upper_arm 0.3, left_lower_arm 0.3), 자세 이동 (torso [15.0, 0.0, 0.0], head [12.0, 0.0, 0.0], left_upper_arm [0.0, -45.0, -0.0], left_lower_arm [0, 0, -60.0]) | 0.86 m/s | 0.25 m | 0.12 m | 6.5° | 100% | 0.98 | 2000회 34분 |
| 까치발 걸음을 노린 새 항 확인 (사람이 정한 값): 발끝 세우기 25° | 발끝 세우기 25 | 1.26 m/s | 0.35 m | 0.19 m | 3.7° | 100% | 0.90 | 2000회 32분 |
| (레퍼런스 원본) | - | 1.26 m/s | 0.32 m | 0.17 m | 3.0° | - | - | - |

속도: 10초 동안 간 거리 ÷ 시간. 팔 흔들기 폭: 골반 기준 손의 앞뒤 이동 범위(양손 평균).
발 들기 높이: 발이 가장 낮을 때 대비 최고 높이. 상체 기울기: 골반→머리 선이 수직에서 기운 평균 각도.
모두 10초 재생 한 번(처음부터, 결정적 정책)으로 측정.
