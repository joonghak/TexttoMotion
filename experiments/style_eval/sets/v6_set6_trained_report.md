# 4B v6 답의 학습 (2026-11-11, 기준선)

유사도: 우리 정책이 기본 걸음에서 달라진 방향과 100STYLE 스타일이 Neutral에서 달라진 방향의 코사인 (특징마다 100STYLE 99종의 차이 분포로 나눈 뒤). 순위: 99종 가운데 목표 스타일의 순위. 크기: 우리 차이의 길이 / 목표 스타일 차이의 길이. 변화: 우리 차이의 길이(같은 단위, 100STYLE 99종의 중앙값 4.2).

| 정책 | 명령 | 목표 (100STYLE) | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| v6_N4 | 공룡처럼 걸어: Qwen3-4B-Thinking-2507, 프롬프트 v6이 정한 값 (n 0.75, c 30, torso_pitch 35, head_pitch 25, stance_width 10) | Dinosaur | 0.61 | 6 | 1.53 | 11.1 | BentKnees 0.84, Roadrunner 0.69, Chicken 0.68 |
| v6_N3 | 고양이처럼 걸어: Qwen3-4B-Thinking-2507, 프롬프트 v6이 정한 값 (s 0.6, n 1.25, c 30, m_arm 0.4, m_torso 3, m_knee 0.8, torso_pitch 15, head_pitch -15) | Cat | 0.37 | 15 | 2.22 | 9.8 | BentKnees 0.93, Roadrunner 0.74, OnToesCrouched 0.72 |
| v6_P5 | 술 취한 사람처럼 걸어: Qwen3-4B-Thinking-2507, 프롬프트 v6이 정한 값 (s 0.6, n 0.55, m_torso 10, torso_pitch 15, head_pitch 25, elbow_flexion -30) | Drunk | 0.28 | 26 | 1.61 | 5.7 | StartStop 0.87, Depressed 0.74, Old 0.67 |
| v6_M3 | 화가 나서 쿵쿵 걸어: Qwen3-4B-Thinking-2507, 프롬프트 v6이 정한 값 (n 1.25, c 15, m_arm 1.5, m_knee 1.5) | Angry | 0.46 | 13 | 1.54 | 4.5 | Roadrunner 0.70, BentKnees 0.64, Chicken 0.61 |

목표가 있는 4개: 유사도 평균 0.43, 1위 0개, 5위 이내 0개, 크기 평균 1.72
