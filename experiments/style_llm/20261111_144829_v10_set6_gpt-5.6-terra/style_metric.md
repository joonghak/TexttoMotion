# 스타일 지표, 목표 동작 기준 (20261111_144829_v10_set6_gpt-5.6-terra, 프롬프트 v10)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 펭귄처럼 걸어 | Penguin | 0.40 | 8 | 1.54 | 5.7 | Star 0.57, Balance 0.48, Aeroplane 0.47 | s 0.6, n 0.8, m_arm 0.3, m_torso 7, m_knee 0.7, shoulder_abduction 45, elbow_flexion 20, stance_width 10, toe_out 20 |
| N2 | 닭처럼 걸어 | Chicken | 0.54 | 5 | 0.96 | 5.5 | LeftHop 0.74, March 0.67, ArmsFolded 0.57 | s 0.5, n 1.5, m_arm 0.3, m_knee 1.3, torso_pitch 15, shoulder_abduction -15, elbow_flexion 50, toe_out 25, bounce 20 |
| N3 | 고양이처럼 걸어 | Cat | 0.50 | 14 | 1.35 | 6.0 | BentKnees 0.77, Dinosaur 0.73, OnToesCrouched 0.68 | s 0.65, n 0.8, c 20, m_arm 0.3, m_knee 0.7, torso_pitch 15, head_pitch 10, shoulder_flexion 15, elbow_flexion 35, stance_width -5, toe_out -10 |
| N4 | 공룡처럼 걸어 | Dinosaur | 0.86 | 1 | 1.02 | 7.4 | Dinosaur 0.86, ShieldedRight 0.74, ShieldedLeft 0.71 | s 1.4, n 0.7, c 20, m_arm 0.3, m_torso 6, m_knee 1.2, torso_pitch 15, head_pitch -10, shoulder_flexion 35, elbow_flexion 60, stance_width 8, toe_out 20 |
| N5 | 새처럼 날개를 퍼덕이며 걸어 | Flapping | 0.81 | 3 | 1.33 | 5.5 | RaisedRightArm 0.84, RaisedLeftArm 0.83, Flapping 0.81 | m_arm 1.8, shoulder_abduction 80, elbow_flexion -20 |
| N6 | 오리처럼 뒤뚱뒤뚱 걸어 | Penguin | 0.14 | 60 | 1.53 | 5.7 | Crouched 0.67, OnToesCrouched 0.61, LeanBack 0.53 | s 0.7, n 0.7, c 15, m_torso 10, m_knee 0.7, shoulder_abduction -15, stance_width 10, toe_out 30 |
| P1 | 좀비처럼 걸어 | Zombie | 0.80 | 1 | 0.88 | 5.2 | Zombie 0.80, InTheDark 0.63, ArmsAboveHead 0.57 | s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 |
| P2 | 로봇처럼 걸어 | Robot | 0.70 | 12 | 0.56 | 2.4 | LawnMower 0.88, BeatChest 0.87, OnPhoneLeft 0.85 | m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 |
| P3 | 노인처럼 걸어 | Old | 0.24 | 23 | 0.54 | 3.5 | Chicken 0.61, Quail 0.61, Roadrunner 0.49 | s 0.6, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 30, head_pitch -10 |
| P4 | 수도승처럼 걸어 | Monk | 0.31 | 30 | 0.80 | 3.6 | Dinosaur 0.67, ShieldedRight 0.53, LeftHop 0.52 | s 0.8, n 0.65, c 10, m_arm 0.2, m_torso 0.3, m_knee 0.8, m_elbow 0.2, elbow_flexion 35 |
| P5 | 술 취한 사람처럼 걸어 | Drunk | 0.21 | 31 | 1.33 | 4.7 | Depressed 0.60, StartStop 0.53, Old 0.51 | s 0.75, n 0.65, m_arm 0.6, m_torso 8, m_knee 0.8, torso_pitch 10, head_pitch 15, stance_width 8, toe_out 15 |
| P6 | 슈퍼맨처럼 걸어 | Superman | -0.24 | 86 | 0.76 | 3.3 | LookUp 0.58, Strutting 0.49, BeatChest 0.45 | s 1.4, n 1.1, m_arm 1.3, torso_pitch -12, head_pitch -15, elbow_flexion 25 |
| F1 | 팔자걸음으로 걸어 | DuckFoot | 0.72 | 1 | 0.58 | 2.8 | DuckFoot 0.72, ArmsBySide 0.54, Strutting 0.53 | toe_out 30 |
| F2 | 안짱걸음으로 걸어 | PigeonToed | 0.64 | 3 | 0.54 | 2.7 | CrossOver 0.66, FairySteps 0.66, PigeonToed 0.64 | toe_out -30 |
| F3 | 다리를 넓게 벌리고 걸어 | WideLegs | 0.66 | 1 | 0.45 | 3.3 | WideLegs 0.66, LegsApart 0.63, Star 0.56 | stance_width 10 |
| F4 | 무릎을 높이 들고 걸어 | HighKnees | 0.85 | 1 | 1.01 | 4.9 | HighKnees 0.85, Kick 0.79, Roadrunner 0.69 | c 15, m_knee 1.5 |
| F5 | 까치발로 걸어 | Tiptoe | 0.21 | 8 | 1.42 | 1.7 | LimpRight 0.43, Penguin 0.34, Quail 0.32 | m_arm 0.3, m_knee 0.7 |
| F6 | 몸을 웅크리고 걸어 | Crouched | 0.58 | 9 | 2.31 | 10.1 | BentKnees 0.94, Lunge 0.76, BigSteps 0.71 | c 30, m_knee 0.7, torso_pitch 15, head_pitch 20 |
| F7 | 상체를 앞으로 숙이고 걸어 | BentForward | 0.70 | 3 | 0.34 | 1.5 | Depressed 0.72, Rocket 0.72, BentForward 0.70 | torso_pitch 20 |
| F8 | 비행기처럼 팔을 벌리고 걸어 | Aeroplane | 0.56 | 6 | 0.86 | 5.1 | RaisedRightArm 0.86, Flapping 0.83, RaisedLeftArm 0.82 | m_arm 0.3, shoulder_abduction 80 |
| M1 | 우울하게 걸어 | Depressed | 0.74 | 2 | 1.10 | 4.0 | StartStop 0.75, Depressed 0.74, Monk 0.71 | s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 |
| M2 | 신나게 걸어 | Elated | 0.44 | 6 | 0.39 | 1.8 | Rushed 0.72, Drunk 0.60, Angry 0.49 | s 1.15, n 1.2, m_arm 1.6, m_knee 1.2 |
| M3 | 화가 나서 쿵쿵 걸어 | Angry | 0.54 | 15 | 2.93 | 8.6 | Roadrunner 0.75, Dinosaur 0.73, BentKnees 0.72 | s 1.2, n 1.2, c 15, m_arm 1.5, m_knee 1.4, torso_pitch 10, head_pitch 15, elbow_flexion 45, bounce 20 |
| M4 | 당당하게 걸어 | Proud | 0.21 | 14 | 1.10 | 1.9 | LookUp 0.70, Strutting 0.57, SpinClock 0.49 | s 1.15, m_arm 1.4, torso_pitch -12, head_pitch -10 |
| M5 | 뻣뻣하게 걸어 | Stiff | -0.24 | 80 | 0.61 | 1.3 | ArmsBySide 0.45, HandsInPockets 0.24, LimpRight 0.23 | m_arm 0.3, m_torso 0, m_elbow 0 |

점수를 낸 25개: 유사도 평균 0.47, 1위 5개, 5위 이내 10개, 순위 중앙값 8, 크기 평균 1.05
