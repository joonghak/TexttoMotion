# 한쪽 동작 확인 (20261112_211507_v11_set9_gpt-5.6-terra, 학습 없이 목표 동작으로)

값이 기준 이상이면 통과이다. 기본 걷기 열은 같은 식을 보통 걸음의 목표 동작에 적용한 값이다.

| ID | 명령 | 답 | 확인 식 | 기준 | 값 | 기본 걷기 | 결과 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | 오른쪽 다리를 절뚝거리며 걸어 | right_m_knee 0.4 | `legs` | 1 | 3.98 | 1.13 | 통과 |
| S2 | 왼손을 번쩍 들고 걸어 | left_m_arm 0.3, left_shoulder_flexion 85 | `l_hand_height - r_hand_height` | 0.4 | 0.96 | -0.01 | 통과 |
| S3 | 오른손으로 전화를 받으면서 걸어 | right_m_arm 0.3, right_shoulder_flexion 35, right_shoulder_abduction 45, right_elbow_flexion 60 | `r_elbow_bend - l_elbow_bend` | 25 | 63.12 | 3.07 | 통과 |
| S4 | 왼쪽 다리를 질질 끌면서 걸어 | left_m_knee 0.4 | `r_knee_range - l_knee_range` | 10 | 37.58 | -1.47 | 통과 |
| S5 | 오른손에 지팡이를 짚고 걸어 | s 0.7, n 0.7, m_arm 0.4, m_knee 0.8, torso_pitch 15, torso_roll 20, right_m_arm 0, right_m_elbow 0, right_shoulder_flexion 20, right_elbow_flexion 40 | `arms` | 1 | 5.53 | 0.36 | 통과 |
| S6 | 몸을 오른쪽으로 기울인 채 걸어 | torso_roll 20 | `torso_roll` | 8 | 9.70 | 0.00 | 통과 |
| S7 | 다친 왼팔을 감싸 쥐고 걸어 | right_m_arm 0, right_m_elbow 0, right_shoulder_flexion 55, right_shoulder_rotation 45, right_elbow_flexion 60, left_m_arm 0, left_m_elbow 0, left_shoulder_flexion 25, left_shoulder_rotation 30, left_elbow_flexion 50 | `r_arm_swing - l_arm_swing` | 0.15 | 0.03 | -0.03 | 실패 |
| S8 | 무거운 가방을 왼쪽 어깨에 메고 걸어 | s 0.85, n 0.8, torso_roll 15, head_roll 12, left_m_arm 0.3, left_shoulder_flexion 45, left_elbow_flexion 60 | `max(abs(torso_roll) / 5, arms)` | 1 | 7.64 | 0.36 | 통과 |
| S9 | 고개를 왼쪽으로 갸웃한 채 걸어 | head_roll -20 | `-head_roll` | 8 | 19.93 | -0.00 | 통과 |
| S10 | 한쪽 다리가 나무 의족인 해적처럼 걸어 | s 0.8, n 0.75, m_torso 6, stance_width 6, right_m_knee 0.4 | `legs` | 1 | 3.97 | 1.13 | 통과 |

통과 9/10
