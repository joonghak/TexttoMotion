# 스타일 지표, 목표 동작 기준 (20261111_153036_v10_set6_gpt-5.6-sol, 프롬프트 v10)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 펭귄처럼 걸어 | Penguin | 0.32 | 19 | 1.64 | 6.1 | Aeroplane 0.53, Balance 0.49, Crouched 0.43 | s 0.55, n 0.8, c 10, m_arm 0.3, m_torso 10, m_knee 0.7, m_elbow 0, shoulder_abduction 35, elbow_flexion -20, stance_width 8, toe_out 30 |
| N2 | 닭처럼 걸어 | Chicken | 0.69 | 2 | 1.30 | 7.5 | March 0.73, Chicken 0.69, LeftHop 0.65 | s 0.5, n 1.4, c 15, m_arm 0.3, m_torso 3, m_knee 1.4, torso_pitch 20, shoulder_abduction 35, elbow_flexion 60, stance_width 6, toe_out 30, bounce 10 |
| N3 | 고양이처럼 걸어 | Cat | 0.49 | 14 | 1.40 | 6.2 | Dinosaur 0.77, BentKnees 0.76, OnToesCrouched 0.69 | s 0.65, n 0.75, c 20, m_arm 0.3, m_torso 2, m_knee 0.7, torso_pitch 20, shoulder_flexion 20, elbow_flexion 40, stance_width -8 |
| N4 | 공룡처럼 걸어 | Dinosaur | 0.80 | 1 | 1.40 | 10.2 | Dinosaur 0.80, Lunge 0.69, Chicken 0.68 | s 1.3, n 0.7, c 15, m_arm 0.3, m_torso 7, m_knee 1.3, m_elbow 0, torso_pitch 25, head_pitch 10, shoulder_flexion 35, elbow_flexion 60, stance_width 10, toe_out 25, shoulder_rotation 30, bounce 20 |
| N5 | 새처럼 날개를 퍼덕이며 걸어 | Flapping | 0.67 | 1 | 1.56 | 6.5 | Flapping 0.67, RaisedLeftArm 0.65, Teapot 0.65 | s 0.6, n 1.4, m_arm 1.8, m_torso 5, m_knee 0.8, shoulder_abduction 80, elbow_flexion -30, stance_width -4, toe_out 20, bounce 10 |
| N6 | 오리처럼 뒤뚱뒤뚱 걸어 | Penguin | 0.20 | 52 | 1.64 | 6.1 | Crouched 0.67, ShieldedRight 0.62, ShieldedLeft 0.61 | s 0.6, n 0.85, c 15, m_arm 0.3, m_torso 10, m_knee 0.7, elbow_flexion 50, stance_width 10, toe_out 30 |
| P1 | 좀비처럼 걸어 | Zombie | 0.80 | 1 | 0.88 | 5.2 | Zombie 0.80, InTheDark 0.63, ArmsAboveHead 0.57 | s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 |
| P2 | 로봇처럼 걸어 | Robot | 0.70 | 12 | 0.56 | 2.4 | LawnMower 0.88, BeatChest 0.87, OnPhoneLeft 0.85 | m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 |
| P3 | 노인처럼 걸어 | Old | 0.24 | 23 | 0.54 | 3.5 | Chicken 0.61, Quail 0.61, Roadrunner 0.49 | s 0.6, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 30, head_pitch -10 |
| P4 | 수도승처럼 걸어 | Monk | 0.72 | 1 | 1.20 | 5.4 | Monk 0.72, ArmsFolded 0.71, WalkingStickLeft 0.67 | s 0.7, n 0.65, m_arm 0.3, m_torso 0, m_knee 0.7, head_pitch 25, shoulder_flexion 20, elbow_flexion 50, stance_width -4, shoulder_rotation 45 |
| P5 | 술 취한 사람처럼 걸어 | Drunk | 0.36 | 18 | 1.46 | 5.2 | Aeroplane 0.59, Balance 0.59, DuckFoot 0.52 | s 0.8, n 0.65, m_arm 1.4, m_torso 10, m_knee 0.8, shoulder_abduction 35, elbow_flexion 20, stance_width 8, toe_out 20 |
| P6 | 슈퍼맨처럼 걸어 | Superman | -0.25 | 82 | 0.86 | 3.7 | Strutting 0.48, BeatChest 0.48, WideLegs 0.47 | s 1.5, n 0.9, m_arm 1.8, torso_pitch -15, head_pitch -15, elbow_flexion 30, stance_width 6 |
| F1 | 팔자걸음으로 걸어 | DuckFoot | 0.72 | 1 | 0.58 | 2.8 | DuckFoot 0.72, ArmsBySide 0.54, Strutting 0.53 | toe_out 30 |
| F2 | 안짱걸음으로 걸어 | PigeonToed | 0.64 | 3 | 0.54 | 2.7 | CrossOver 0.66, FairySteps 0.66, PigeonToed 0.64 | toe_out -30 |
| F3 | 다리를 넓게 벌리고 걸어 | WideLegs | 0.66 | 1 | 0.45 | 3.3 | WideLegs 0.66, LegsApart 0.63, Star 0.56 | stance_width 10 |
| F4 | 무릎을 높이 들고 걸어 | HighKnees | 0.85 | 1 | 1.01 | 4.9 | HighKnees 0.85, Kick 0.79, Roadrunner 0.69 | c 15, m_knee 1.5 |
| F5 | 까치발로 걸어 | Tiptoe | 0.31 | 11 | 2.65 | 3.1 | Quail 0.53, LeftHop 0.49, RightHop 0.44 | s 0.6, n 0.8, c 10, m_arm 0.3, m_knee 0.7 |
| F6 | 몸을 웅크리고 걸어 | Crouched | 0.58 | 12 | 1.98 | 8.7 | BentKnees 0.84, Dinosaur 0.75, ShieldedLeft 0.69 | c 25, m_knee 0.75, torso_pitch 25, head_pitch 25, shoulder_flexion 20, elbow_flexion 40 |
| F7 | 상체를 앞으로 숙이고 걸어 | BentForward | 0.70 | 3 | 0.34 | 1.5 | Depressed 0.72, Rocket 0.72, BentForward 0.70 | torso_pitch 20 |
| F8 | 비행기처럼 팔을 벌리고 걸어 | Aeroplane | 0.53 | 6 | 0.96 | 5.7 | RaisedRightArm 0.82, RaisedLeftArm 0.82, Flapping 0.79 | m_arm 0.3, shoulder_abduction 80, elbow_flexion -30 |
| M1 | 우울하게 걸어 | Depressed | 0.73 | 3 | 1.13 | 4.1 | StartStop 0.76, Monk 0.74, Depressed 0.73 | s 0.8, n 0.7, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 |
| M2 | 신나게 걸어 | Elated | 0.55 | 4 | 0.52 | 2.4 | Rushed 0.78, Drunk 0.62, Skip 0.59 | s 1.15, n 1.25, m_arm 1.7, m_knee 1.2, bounce 10 |
| M3 | 화가 나서 쿵쿵 걸어 | Angry | 0.55 | 11 | 1.46 | 4.3 | Skip 0.72, March 0.72, Dinosaur 0.69 | s 1.15, n 1.25, m_arm 1.7, m_knee 1.4, torso_pitch 15, elbow_flexion 45, bounce 20 |
| M4 | 당당하게 걸어 | Proud | 0.21 | 14 | 1.10 | 1.9 | LookUp 0.70, Strutting 0.57, SpinClock 0.49 | s 1.15, m_arm 1.4, torso_pitch -12, head_pitch -10 |
| M5 | 뻣뻣하게 걸어 | Stiff | -0.24 | 80 | 0.61 | 1.3 | ArmsBySide 0.45, HandsInPockets 0.24, LimpRight 0.23 | m_arm 0.3, m_torso 0, m_elbow 0 |

점수를 낸 25개: 유사도 평균 0.50, 1위 7개, 5위 이내 12개, 순위 중앙값 6, 크기 평균 1.11
