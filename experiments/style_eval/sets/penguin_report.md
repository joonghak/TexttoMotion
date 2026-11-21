# 펭귄 파라미터 시험 (2026-11-05, 학습한 정책)

유사도: 우리 정책이 기본 걸음에서 달라진 방향과 100STYLE 스타일이 Neutral에서 달라진 방향의 코사인 (특징마다 100STYLE 99종의 차이 분포로 나눈 뒤). 순위: 99종 가운데 목표 스타일의 순위. 크기: 우리 차이의 길이 / 목표 스타일 차이의 길이. 변화: 우리 차이의 길이(같은 단위, 100STYLE 99종의 중앙값 4.2).

| 정책 | 명령 | 목표 (100STYLE) | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| v5 answer (sway) | 펭귄처럼 걸어, v5가 낸 값 (n 0.6, m_torso 10) | Penguin | 0.12 | 49 | 0.83 | 3.1 | Old 0.71, SlideFeet 0.62, StartStop 0.57 |
| pen_a | 지금 파라미터만 (s 0.4, n 1.2, m_arm 0.3, m_knee 0.7, 팔꿈치 신전 30, 다리 벌림 10, m_torso 5) | Penguin | 0.48 | 4 | 1.31 | 4.9 | WideLegs 0.53, LegsApart 0.52, Star 0.51 |
| pen_b | A + 발끝 벌림 30 + 팔 흔들기 0 | Penguin | 0.55 | 5 | 1.54 | 5.8 | LegsApart 0.60, WideLegs 0.60, Star 0.57 |
| pen_c | B + 상체 흔들림 10 | Penguin | 0.51 | 1 | 1.71 | 6.4 | Penguin 0.51, DuckFoot 0.46, LegsApart 0.45 |
| pen_d | s 0.3, n 1.3, m_knee 0.4, m_arm 0, 팔꿈치 신전 30, 어깨 안쪽 15, 발끝 벌림 30, 다리 벌림 5, m_torso 10 | Penguin | 0.67 | 1 | 1.63 | 6.1 | Penguin 0.67, DragRightLeg 0.49, DragLeftLeg 0.40 |
| pen_e | D에서 다리 벌림 없음 | Penguin | 0.74 | 1 | 1.44 | 5.4 | Penguin 0.74, DragRightLeg 0.60, LimpLeft 0.55 |

목표가 있는 6개: 유사도 평균 0.51, 1위 3개, 5위 이내 5개, 크기 평균 1.41
