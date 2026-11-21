# 스타일 지표, 목표 동작 기준 (20261112_135026_v10_set6, 프롬프트 v10)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 펭귄처럼 걸어 | Penguin | 0.10 | 55 | 0.89 | 3.3 | Old 0.74, SpinClock 0.67, Followed 0.63 | n 0.75, m_torso 10 |
| N2 | 닭처럼 걸어 | Chicken | 0.08 | 56 | 0.80 | 4.6 | StartStop 0.79, Old 0.76, Depressed 0.68 | s 0.8, n 0.6, m_arm 0.4, m_torso 10, head_pitch 25 |
| N3 | 고양이처럼 걸어 | Cat | 0.19 | 29 | 0.81 | 3.6 | BentKnees 0.87, Roadrunner 0.80, Chicken 0.75 | s 0.8, n 1.2, c 15, m_arm 0.3, m_knee 0.8, torso_pitch 10, head_pitch -10 |
| N4 | 공룡처럼 걸어 | Dinosaur | 0.57 | 7 | 0.86 | 6.3 | BentKnees 0.82, Chicken 0.67, Lunge 0.63 | s 0.8, n 0.75, c 20, m_arm 0.4, m_knee 0.7, torso_pitch 20, head_pitch 20 |
| N5 | 새처럼 날개를 퍼덕이며 걸어 | Flapping | 0.42 | 8 | 1.14 | 4.8 | InTheDark 0.78, ArmsAboveHead 0.74, Zombie 0.74 | m_arm 1.5, shoulder_flexion 85, elbow_flexion -30 |
| N6 | 오리처럼 뒤뚱뒤뚱 걸어 | Penguin | 0.07 | 58 | 1.25 | 4.6 | LegsApart 0.53, WideLegs 0.51, FlickLegs 0.51 | n 0.6, m_torso 10, stance_width 10 |
| P1 | 좀비처럼 걸어 | Zombie | 0.80 | 1 | 0.88 | 5.2 | Zombie 0.80, InTheDark 0.63, ArmsAboveHead 0.57 | s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 |
| P2 | 로봇처럼 걸어 | Robot | 0.70 | 12 | 0.56 | 2.4 | LawnMower 0.88, BeatChest 0.87, OnPhoneLeft 0.85 | m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 |
| P3 | 노인처럼 걸어 | Old | 0.24 | 23 | 0.54 | 3.5 | Chicken 0.61, Quail 0.61, Roadrunner 0.49 | s 0.6, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 30, head_pitch -10 |
| P4 | 수도승처럼 걸어 | Monk | 0.39 | 10 | 0.72 | 3.2 | Quail 0.51, Chicken 0.51, BentKnees 0.48 | s 0.7, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 10, head_pitch 10 |
| P5 | 술 취한 사람처럼 걸어 | Drunk | 0.42 | 22 | 1.44 | 5.1 | Depressed 0.83, StartStop 0.81, Old 0.80 | n 0.6, m_torso 10, torso_pitch 20, head_pitch 25 |
| P6 | 슈퍼맨처럼 걸어 | Superman | -0.37 | 93 | 0.51 | 2.2 | LookUp 0.63, Strutting 0.60, SpinClock 0.45 | s 1.2, n 1.15, m_arm 1.5, torso_pitch -10, head_pitch -10 |
| F1 | 팔자걸음으로 걸어 | DuckFoot | -0.06 | 70 | 1.00 | 4.8 | InTheDark 0.78, ArmsAboveHead 0.74, Zombie 0.74 | shoulder_flexion 85, elbow_flexion -30 |
| F2 | 안짱걸음으로 걸어 | PigeonToed | 0.41 | 17 | 0.71 | 3.6 | Old 0.74, SpinClock 0.63, StartStop 0.59 | n 0.6, m_torso 10 |
| F3 | 다리를 넓게 벌리고 걸어 | WideLegs | 0.66 | 1 | 0.45 | 3.3 | WideLegs 0.66, LegsApart 0.63, Star 0.56 | stance_width 10 |
| F4 | 무릎을 높이 들고 걸어 | HighKnees | 0.85 | 1 | 1.01 | 4.9 | HighKnees 0.85, Kick 0.79, Roadrunner 0.69 | c 15, m_knee 1.5 |
| F5 | 까치발로 걸어 | Tiptoe | 0.41 | 8 | 2.31 | 2.7 | Penguin 0.51, RightHop 0.51, Robot 0.51 | s 0.5, n 1.5, m_arm 0.6 |
| F6 | 몸을 웅크리고 걸어 | Crouched | 0.56 | 8 | 1.22 | 5.3 | BentKnees 0.91, Roadrunner 0.79, Lunge 0.72 | c 20 |
| F7 | 상체를 앞으로 숙이고 걸어 | BentForward | 0.70 | 3 | 0.26 | 1.1 | Depressed 0.72, Rocket 0.70, BentForward 0.70 | torso_pitch 15 |
| F8 | 비행기처럼 팔을 벌리고 걸어 | Aeroplane | 0.56 | 6 | 0.86 | 5.1 | RaisedRightArm 0.86, Flapping 0.83, RaisedLeftArm 0.82 | m_arm 0.3, shoulder_abduction 80 |
| M1 | 우울하게 걸어 | Depressed | 0.74 | 2 | 1.10 | 4.0 | StartStop 0.75, Depressed 0.74, Monk 0.71 | s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 |
| M2 | 신나게 걸어 | Elated | 0.30 | 30 | 0.55 | 2.5 | Swat 0.80, OnPhoneRight 0.79, BeatChest 0.77 | s 1.2, n 1.15, m_arm 1.8, torso_pitch -5, elbow_flexion 45 |
| M3 | 화가 나서 쿵쿵 걸어 | Angry | 0.63 | 8 | 0.82 | 2.4 | Swat 0.77, LawnMower 0.76, OnPhoneRight 0.72 | s 1.2, n 1.1, m_arm 1.5, torso_pitch 20, elbow_flexion 40 |
| M4 | 당당하게 걸어 | Proud | 0.21 | 14 | 1.10 | 1.9 | LookUp 0.70, Strutting 0.57, SpinClock 0.49 | s 1.15, m_arm 1.4, torso_pitch -12, head_pitch -10 |
| M5 | 뻣뻣하게 걸어 | Stiff | -0.24 | 80 | 0.61 | 1.3 | ArmsBySide 0.45, HandsInPockets 0.24, LimpRight 0.23 | m_arm 0.3, m_torso 0, m_elbow 0 |

점수를 낸 25개: 유사도 평균 0.37, 1위 3개, 5위 이내 5개, 순위 중앙값 12, 크기 평균 0.90
