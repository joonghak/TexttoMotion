# 스타일 지표, 목표 동작 기준 (20261116_120656_v13_set6_gpt-5.6-sol, 프롬프트 v13)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 펭귄처럼 걸어 | Penguin | 0.48 | 5 | 1.71 | 6.4 | Star 0.53, Aeroplane 0.52, Balance 0.51 | s 0.5, n 0.9, m_arm 0.3, m_torso 10, m_knee 0.5, m_elbow 0, shoulder_abduction 30, elbow_flexion -30, stance_width 8, toe_out 30 |
| N2 | 닭처럼 걸어 | Chicken | 0.64 | 2 | 1.30 | 7.5 | March 0.64, Chicken 0.64, LeftHop 0.62 | s 0.55, n 1.4, c 10, m_arm 0.3, m_torso 5, m_knee 1.3, torso_pitch 20, head_pitch 25, shoulder_abduction 45, elbow_flexion 60, stance_width 6, toe_out 25, bounce 15 |
| N3 | 고양이처럼 걸어 | Cat | 0.37 | 32 | 1.29 | 5.7 | ShieldedRight 0.72, ShieldedLeft 0.72, Dinosaur 0.71 | s 0.7, n 0.75, c 15, m_arm 0.3, m_torso 3, m_knee 0.8, torso_pitch 15, shoulder_flexion 45, elbow_flexion 60, stance_width -4, toe_out -10, shoulder_rotation 20, foot_pitch 20 |
| N4 | 공룡처럼 걸어 | Dinosaur | 0.80 | 1 | 1.04 | 7.6 | Dinosaur 0.80, ShieldedRight 0.69, ShieldedLeft 0.67 | s 1.4, n 0.75, c 10, m_arm 0.3, m_torso 7, m_knee 1.3, torso_pitch 30, head_pitch -10, shoulder_flexion 35, elbow_flexion 60, stance_width 10, toe_out 25, shoulder_rotation 30, bounce 15 |
| N5 | 새처럼 날개를 퍼덕이며 걸어 | Flapping | 0.77 | 1 | 1.46 | 6.1 | Flapping 0.77, Teapot 0.72, RaisedLeftArm 0.71 | s 0.6, n 1.3, m_arm 1.8, m_knee 0.8, torso_pitch 10, shoulder_abduction 80, elbow_flexion -30, toe_out 15 |
| N6 | 오리처럼 뒤뚱뒤뚱 걸어 | Penguin | 0.26 | 49 | 1.61 | 6.0 | LeftHop 0.60, ShieldedRight 0.57, ShieldedLeft 0.57 | s 0.6, n 0.75, c 10, m_arm 0.3, m_torso 10, m_knee 0.8, shoulder_abduction 30, elbow_flexion 60, stance_width 10, toe_out 30 |
| P1 | 좀비처럼 걸어 | Zombie | 0.80 | 1 | 0.88 | 5.2 | Zombie 0.80, InTheDark 0.63, ArmsAboveHead 0.57 | s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 |
| P2 | 로봇처럼 걸어 | Robot | 0.70 | 12 | 0.56 | 2.4 | LawnMower 0.88, BeatChest 0.87, OnPhoneLeft 0.85 | m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 |
| P3 | 노인처럼 걸어 | Old | 0.24 | 23 | 0.54 | 3.5 | Chicken 0.61, Quail 0.61, Roadrunner 0.49 | s 0.6, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 30, head_pitch -10 |
| P4 | 수도승처럼 걸어 | Monk | 0.71 | 2 | 1.23 | 5.5 | ArmsFolded 0.76, Monk 0.71, WalkingStickLeft 0.66 | s 0.75, n 0.65, m_arm 0, m_torso 0, m_knee 0.75, head_pitch 25, shoulder_flexion 20, elbow_flexion 60, stance_width -4, shoulder_rotation 60 |
| P5 | 술 취한 사람처럼 걸어 | Drunk | 0.79 | 1 | 1.36 | 4.8 | Drunk 0.79, CrowdAvoidance 0.74, WhirlArms 0.74 | s 0.75, n 0.65, m_arm 1.4, m_torso 10, shoulder_abduction 30, stance_width 7, head_roll 15, weave 0.35 |
| P6 | 슈퍼맨처럼 걸어 | Superman | -0.16 | 77 | 0.98 | 4.2 | Strutting 0.60, WideLegs 0.58, LegsApart 0.54 | s 1.4, m_arm 1.7, m_torso 3, torso_pitch -12, head_pitch -15, elbow_flexion 35, stance_width 7, toe_out 15 |
| F1 | 팔자걸음으로 걸어 | DuckFoot | 0.72 | 1 | 0.58 | 2.8 | DuckFoot 0.72, ArmsBySide 0.54, Strutting 0.53 | toe_out 30 |
| F2 | 안짱걸음으로 걸어 | PigeonToed | 0.56 | 4 | 0.57 | 2.9 | CrossOver 0.72, FairySteps 0.70, Tiptoe 0.61 | stance_width -4, toe_out -30 |
| F3 | 다리를 넓게 벌리고 걸어 | WideLegs | 0.66 | 1 | 0.45 | 3.3 | WideLegs 0.66, LegsApart 0.63, Star 0.56 | stance_width 10 |
| F4 | 무릎을 높이 들고 걸어 | HighKnees | 0.85 | 1 | 1.01 | 4.9 | HighKnees 0.85, Kick 0.79, Roadrunner 0.69 | c 15, m_knee 1.5 |
| F5 | 까치발로 걸어 | Tiptoe | -0.43 | 96 | 1.01 | 1.2 | DuckFoot 0.69, Strutting 0.45, ArmsBySide 0.44 | foot_pitch 20 |
| F6 | 몸을 웅크리고 걸어 | Crouched | 0.51 | 14 | 1.50 | 6.6 | BentKnees 0.84, Chicken 0.65, Lunge 0.65 | c 20, m_knee 0.75, torso_pitch 20, head_pitch 25 |
| F7 | 상체를 앞으로 숙이고 걸어 | BentForward | 0.70 | 3 | 0.34 | 1.5 | Depressed 0.72, Rocket 0.72, BentForward 0.70 | torso_pitch 20 |
| F8 | 비행기처럼 팔을 벌리고 걸어 | Aeroplane | 0.53 | 6 | 0.96 | 5.7 | RaisedRightArm 0.82, RaisedLeftArm 0.82, Flapping 0.79 | m_arm 0.3, shoulder_abduction 80, elbow_flexion -30 |
| M1 | 우울하게 걸어 | Depressed | 0.74 | 1 | 1.09 | 4.0 | Depressed 0.74, Monk 0.70, StartStop 0.70 | s 0.8, n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 25 |
| M2 | 신나게 걸어 | Elated | 0.59 | 4 | 0.49 | 2.3 | Rushed 0.87, Drunk 0.67, Angry 0.60 | s 1.15, n 1.25, m_arm 1.8, bounce 10 |
| M3 | 화가 나서 쿵쿵 걸어 | Angry | 0.56 | 10 | 1.49 | 4.3 | Skip 0.71, March 0.70, Dinosaur 0.68 | s 1.2, n 1.25, m_arm 1.8, m_knee 1.4, torso_pitch 15, elbow_flexion 45, bounce 20 |
| M4 | 당당하게 걸어 | Proud | 0.21 | 14 | 1.10 | 1.9 | LookUp 0.70, Strutting 0.57, SpinClock 0.49 | s 1.15, m_arm 1.4, torso_pitch -12, head_pitch -10 |
| M5 | 뻣뻣하게 걸어 | Stiff | 0.30 | 5 | 0.96 | 2.1 | LimpRight 0.53, Penguin 0.40, Quail 0.37 | m_arm 0.3, m_torso 0, m_knee 0.5, m_elbow 0 |

점수를 낸 25개: 유사도 평균 0.52, 1위 8개, 5위 이내 15개, 순위 중앙값 4, 크기 평균 1.02
