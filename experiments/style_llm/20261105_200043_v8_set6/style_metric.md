# 스타일 지표, 목표 동작 기준 (20261105_200043_v8_set6, 프롬프트 v8)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 펭귄처럼 걸어 | Penguin | 0.07 | 59 | 1.24 | 4.6 | LegsApart 0.76, WideLegs 0.72, Star 0.56 | m_torso 10, stance_width 10 |
| N2 | 닭처럼 걸어 | Chicken | 0.13 | 41 | 0.80 | 4.6 | LegsApart 0.76, WideLegs 0.72, Star 0.56 | m_torso 10, stance_width 10 |
| N3 | 고양이처럼 걸어 | Cat | 0.16 | 35 | 0.83 | 3.7 | Chicken 0.74, BentKnees 0.73, Quail 0.72 | s 0.6, n 1.25, c 15, m_arm 0.4, m_torso 3, m_knee 0.8, torso_pitch 15 |
| N4 | 공룡처럼 걸어 | Dinosaur | 0.70 | 5 | 1.44 | 10.5 | BentKnees 0.89, OnToesCrouched 0.77, Lunge 0.75 | n 0.75, c 30, m_torso 10, m_knee 0.8, stance_width 10 |
| N5 | 새처럼 날개를 퍼덕이며 걸어 | Flapping | 0.47 | 10 | 1.28 | 5.3 | BeatChest 0.64, ArmsAboveHead 0.61, GracefulArms 0.56 | s 1.4, n 1.25, m_arm 1.8, torso_pitch -10, head_pitch -15, shoulder_abduction 85, elbow_flexion 60 |
| N6 | 오리처럼 뒤뚱뒤뚱 걸어 | Penguin | 0.07 | 59 | 1.24 | 4.6 | LegsApart 0.76, WideLegs 0.72, Star 0.56 | m_torso 10, stance_width 10 |
| P1 | 좀비처럼 걸어 | Zombie | 0.77 | 1 | 0.96 | 5.7 | Zombie 0.77, InTheDark 0.58, Balance 0.51 | s 0.6, n 0.55, m_torso 6, torso_pitch 15, shoulder_flexion 85, elbow_flexion -30 |
| P2 | 로봇처럼 걸어 | Robot | 0.70 | 10 | 0.52 | 2.3 | LawnMower 0.87, BeatChest 0.84, OnPhoneLeft 0.82 | m_torso 0, m_knee 0.8, m_elbow 0, elbow_flexion 45 |
| P3 | 노인처럼 걸어 | Old | 0.17 | 31 | 0.68 | 4.5 | Chicken 0.75, Quail 0.68, Roadrunner 0.68 | s 0.6, n 0.75, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 35, head_pitch -15 |
| P4 | 수도승처럼 걸어 | Monk | 0.31 | 10 | 0.70 | 3.1 | StartStop 0.71, FairySteps 0.56, Penguin 0.47 | s 0.6, n 0.75, m_knee 0.8, torso_pitch 15, shoulder_abduction -15 |
| P5 | 술 취한 사람처럼 걸어 | Drunk | 0.32 | 24 | 1.52 | 5.4 | StartStop 0.86, Depressed 0.79, Old 0.76 | s 0.6, n 0.55, m_torso 10, torso_pitch 15, head_pitch 25 |
| P6 | 슈퍼맨처럼 걸어 | Superman | -0.45 | 93 | 0.69 | 2.9 | LookUp 0.66, Strutting 0.58, SpinClock 0.44 | s 1.4, m_arm 1.5, torso_pitch -15, head_pitch -15 |
| F1 | 팔자걸음으로 걸어 | DuckFoot | 0.31 | 28 | 0.69 | 3.3 | Followed 0.81, SpinClock 0.70, Old 0.67 | m_torso 10 |
| F2 | 안짱걸음으로 걸어 | PigeonToed | -0.22 | 89 | 1.22 | 6.2 | HighKnees 0.83, Kick 0.72, March 0.65 | s 0.3, n 1.45, c 15, m_knee 1.5 |
| F3 | 다리를 넓게 벌리고 걸어 | WideLegs | 0.66 | 1 | 0.45 | 3.3 | WideLegs 0.66, LegsApart 0.63, Star 0.56 | stance_width 10 |
| F4 | 무릎을 높이 들고 걸어 | HighKnees | 0.38 | 17 | 1.92 | 9.3 | BentKnees 0.93, Roadrunner 0.77, Lunge 0.76 | c 30 |
| F5 | 까치발로 걸어 | Tiptoe | 0.43 | 7 | 3.46 | 4.0 | Penguin 0.65, Robot 0.59, StartStop 0.53 | s 0.3, n 1.45, m_arm 0.4, m_knee 0.8 |
| F6 | 몸을 웅크리고 걸어 | Crouched | 0.13 | 44 | 0.59 | 2.6 | Rocket 0.77, BentForward 0.72, Depressed 0.71 | torso_pitch 35 |
| F7 | 상체를 앞으로 숙이고 걸어 | BentForward | 0.70 | 3 | 0.26 | 1.1 | Depressed 0.72, Rocket 0.70, BentForward 0.70 | torso_pitch 15 |
| F8 | 비행기처럼 팔을 벌리고 걸어 | Aeroplane | 0.55 | 7 | 0.89 | 5.3 | RaisedRightArm 0.85, Flapping 0.83, RaisedLeftArm 0.81 | shoulder_abduction 85 |
| M1 | 우울하게 걸어 | Depressed | 0.70 | 2 | 1.21 | 4.4 | StartStop 0.72, Depressed 0.70, Monk 0.61 | s 0.6, n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 25 |
| M2 | 신나게 걸어 | Elated | 0.28 | 18 | 0.56 | 2.6 | Rushed 0.68, LegsApart 0.54, Followed 0.52 | s 1.4, n 1.25, m_arm 1.5 |
| M3 | 화가 나서 쿵쿵 걸어 | Angry | 0.35 | 17 | 1.88 | 5.5 | HighKnees 0.68, Roadrunner 0.67, Skip 0.61 | s 1.4, n 1.25, c 15, m_arm 1.5, m_knee 1.5 |
| M4 | 당당하게 걸어 | Proud | 0.13 | 23 | 1.69 | 2.9 | LookUp 0.66, Strutting 0.58, SpinClock 0.44 | s 1.4, m_arm 1.5, torso_pitch -15, head_pitch -15 |
| M5 | 뻣뻣하게 걸어 | Stiff | 0.09 | 56 | 1.05 | 2.3 | LawnMower 0.87, BeatChest 0.84, OnPhoneLeft 0.82 | m_torso 0, m_knee 0.8, m_elbow 0, elbow_flexion 45 |

점수를 낸 25개: 유사도 평균 0.32, 1위 2개, 5위 이내 5개, 순위 중앙값 18, 크기 평균 1.11
