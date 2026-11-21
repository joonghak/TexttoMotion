# 스타일 지표, 목표 동작 기준 (20261105_161101_v6_set6_remap, 프롬프트 v6)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 펭귄처럼 걸어 | Penguin | 0.06 | 60 | 1.25 | 4.7 | FlickLegs 0.50, SpinClock 0.50, LegsApart 0.48 | n 0.55, m_torso 10, stance_width 10 |
| N2 | 닭처럼 걸어 | Chicken | 0.12 | 44 | 0.65 | 3.7 | Old 0.74, SpinClock 0.61, StartStop 0.60 | n 0.55, m_torso 10 |
| N3 | 고양이처럼 걸어 | Cat | 0.39 | 14 | 2.00 | 8.9 | BentKnees 0.93, Roadrunner 0.79, Chicken 0.74 | s 0.6, n 1.25, c 30, m_arm 0.4, m_torso 3, m_knee 0.8, torso_pitch 15, head_pitch -15 |
| N4 | 공룡처럼 걸어 | Dinosaur | 0.63 | 6 | 1.49 | 10.9 | BentKnees 0.85, Lunge 0.71, Roadrunner 0.69 | n 0.75, c 30, torso_pitch 35, head_pitch 25, stance_width 10 |
| N5 | 새처럼 날개를 퍼덕이며 걸어 | Flapping | 0.84 | 2 | 1.27 | 5.3 | RaisedRightArm 0.85, Flapping 0.84, RaisedLeftArm 0.82 | n 1.25, m_arm 0.3, shoulder_abduction 85 |
| N6 | 오리처럼 뒤뚱뒤뚱 걸어 | Penguin | 0.06 | 65 | 1.24 | 4.6 | LegsApart 0.75, WideLegs 0.71, Star 0.55 | m_torso 10, stance_width 10 |
| P1 | 좀비처럼 걸어 | Zombie | 0.77 | 1 | 0.96 | 5.7 | Zombie 0.77, InTheDark 0.58, Balance 0.50 | s 0.6, n 0.55, m_arm 0.3, m_torso 6, torso_pitch 15, shoulder_flexion 85, elbow_flexion -30 |
| P2 | 로봇처럼 걸어 | Robot | 0.70 | 11 | 0.52 | 2.3 | LawnMower 0.88, BeatChest 0.85, ArmsFolded 0.84 | m_torso 0, m_knee 0.8, m_elbow 0, elbow_flexion 45 |
| P3 | 노인처럼 걸어 | Old | 0.17 | 31 | 0.68 | 4.5 | Chicken 0.75, Quail 0.68, Roadrunner 0.68 | s 0.6, n 0.75, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 35, head_pitch -15 |
| P4 | 수도승처럼 걸어 | Monk | 0.42 | 10 | 1.05 | 4.7 | BentKnees 0.59, Chicken 0.51, Quail 0.47 | s 0.6, n 0.75, c 15, m_arm 0.4, m_knee 0.8, head_pitch 25 |
| P5 | 술 취한 사람처럼 걸어 | Drunk | 0.30 | 23 | 1.59 | 5.7 | StartStop 0.85, Depressed 0.76, Old 0.67 | s 0.6, n 0.55, m_torso 10, torso_pitch 15, head_pitch 25, elbow_flexion -30 |
| P6 | 슈퍼맨처럼 걸어 | Superman | 0.05 | 51 | 1.05 | 4.5 | Rushed 0.66, LegsApart 0.48, WideLegs 0.47 | s 1.8, n 1.25, m_arm 1.8, m_torso 0, torso_pitch 15, head_pitch -15 |
| F1 | 팔자걸음으로 걸어 | DuckFoot | -0.01 | 63 | 1.11 | 5.3 | RaisedRightArm 0.85, Flapping 0.83, RaisedLeftArm 0.81 | m_arm 0.3, shoulder_abduction 85 |
| F2 | 안짱걸음으로 걸어 | PigeonToed | 0.40 | 17 | 0.73 | 3.7 | Old 0.74, SpinClock 0.61, StartStop 0.60 | n 0.55, m_torso 10 |
| F3 | 다리를 넓게 벌리고 걸어 | WideLegs | 0.64 | 1 | 0.45 | 3.3 | WideLegs 0.64, LegsApart 0.61, Star 0.54 | stance_width 10 |
| F4 | 무릎을 높이 들고 걸어 | HighKnees | 0.38 | 17 | 1.92 | 9.3 | BentKnees 0.93, Roadrunner 0.77, Lunge 0.76 | c 30 |
| F5 | 까치발로 걸어 | Tiptoe | 0.20 | 23 | 1.48 | 1.7 | Stiff 0.60, LimpRight 0.49, OnHeels 0.48 | m_knee 0.4 |
| F6 | 몸을 웅크리고 걸어 | Crouched | 0.13 | 44 | 0.59 | 2.6 | Rocket 0.77, BentForward 0.72, Depressed 0.71 | torso_pitch 35 |
| F7 | 상체를 앞으로 숙이고 걸어 | BentForward | 0.70 | 3 | 0.26 | 1.1 | Depressed 0.72, Rocket 0.70, BentForward 0.70 | torso_pitch 15 |
| F8 | 비행기처럼 팔을 벌리고 걸어 | Aeroplane | 0.55 | 7 | 0.89 | 5.3 | RaisedRightArm 0.85, Flapping 0.83, RaisedLeftArm 0.81 | m_arm 0.3, shoulder_abduction 85 |
| M1 | 우울하게 걸어 | Depressed | 0.77 | 1 | 1.52 | 5.6 | Depressed 0.77, StartStop 0.76, LeanRight 0.68 | s 0.6, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 35, head_pitch 25 |
| M2 | 신나게 걸어 | Elated | 0.31 | 22 | 0.66 | 3.1 | Rushed 0.76, Drunk 0.62, Angry 0.60 | s 1.4, n 1.25, m_arm 1.8, torso_pitch 15 |
| M3 | 화가 나서 쿵쿵 걸어 | Angry | 0.31 | 17 | 1.72 | 5.0 | HighKnees 0.80, Kick 0.73, Roadrunner 0.68 | n 1.25, c 15, m_arm 1.5, m_knee 1.5 |
| M4 | 당당하게 걸어 | Proud | 0.15 | 20 | 1.68 | 2.9 | LookUp 0.66, Strutting 0.55, SpinClock 0.45 | s 1.4, m_arm 1.5, torso_pitch -15, head_pitch -15 |
| M5 | 뻣뻣하게 걸어 | Stiff | 0.06 | 66 | 0.12 | 0.3 | Old 0.66, HandsBetweenLegs 0.65, Sweep 0.62 | m_torso 0, m_elbow 0 |

점수를 낸 25개: 유사도 평균 0.36, 1위 3개, 5위 이내 5개, 순위 중앙값 17, 크기 평균 1.08
