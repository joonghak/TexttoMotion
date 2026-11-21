# gpt-5.6-terra v10 답의 학습 (2026-11-11)

유사도: 우리 정책이 기본 걸음에서 달라진 방향과 100STYLE 스타일이 Neutral에서 달라진 방향의 코사인 (특징마다 100STYLE 99종의 차이 분포로 나눈 뒤). 순위: 99종 가운데 목표 스타일의 순위. 크기: 우리 차이의 길이 / 목표 스타일 차이의 길이. 변화: 우리 차이의 길이(같은 단위, 100STYLE 99종의 중앙값 4.2).

| 정책 | 명령 | 목표 (100STYLE) | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| t10_N4 | 공룡처럼 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 1.4, n 0.7, c 20, m_arm 0.3, m_torso 6, m_knee 1.2, torso_pitch 15, head_pitch -10, shoulder_flexion 35, elbow_flexion 60, stance_width 8, toe_out 20) | Dinosaur | 0.84 | 1 | 1.10 | 8.0 | Dinosaur 0.84, ShieldedRight 0.76, ShieldedLeft 0.73 |
| t10_N3 | 고양이처럼 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 0.65, n 0.8, c 20, m_arm 0.3, m_knee 0.7, torso_pitch 15, head_pitch 10, shoulder_flexion 15, elbow_flexion 35, stance_width -5, toe_out -10) | Cat | 0.51 | 13 | 1.43 | 6.3 | BentKnees 0.85, Dinosaur 0.75, OnToesCrouched 0.70 |
| t10_P5 | 술 취한 사람처럼 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 0.75, n 0.65, m_arm 0.6, m_torso 8, m_knee 0.8, torso_pitch 10, head_pitch 15, stance_width 8, toe_out 15) | Drunk | 0.27 | 33 | 1.23 | 4.4 | DuckFoot 0.77, LegsApart 0.70, WideLegs 0.65 |
| t10_M3 | 화가 나서 쿵쿵 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 1.2, n 1.2, c 15, m_arm 1.5, m_knee 1.4, torso_pitch 10, head_pitch 15, elbow_flexion 45, bounce 20) | Angry | 0.57 | 13 | 2.71 | 7.9 | BentKnees 0.85, Dinosaur 0.75, Roadrunner 0.71 |
| t10_N1 | 펭귄처럼 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 0.6, n 0.8, m_arm 0.3, m_torso 7, m_knee 0.7, shoulder_abduction 45, elbow_flexion 20, stance_width 10, toe_out 20) | Penguin | 0.35 | 14 | 1.51 | 5.6 | Star 0.80, LegsApart 0.69, WideLegs 0.68 |
| t10_N2 | 닭처럼 걸어: gpt-5.6-terra, 프롬프트 v10이 정한 값 (s 0.5, n 1.5, m_arm 0.3, m_knee 1.3, torso_pitch 15, shoulder_abduction -15, elbow_flexion 50, toe_out 25, bounce 20) | Chicken | 0.53 | 9 | 0.89 | 5.1 | LeftHop 0.69, ArmsFolded 0.65, March 0.60 |

목표가 있는 6개: 유사도 평균 0.51, 1위 1개, 5위 이내 1개, 크기 평균 1.48
