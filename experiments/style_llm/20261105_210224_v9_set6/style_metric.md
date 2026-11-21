# 스타일 지표, 목표 동작 기준 (20261105_210224_v9_set6, 프롬프트 v9)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 펭귄처럼 걸어 | Penguin | 0.25 | 32 | 2.11 | 7.9 | LeanLeft 0.54, Quail 0.50, OnToesCrouched 0.50 | s 0.3, c 15, m_arm 0.4, m_torso 10, m_knee 0.4, m_elbow 0, head_pitch 25, shoulder_abduction -15, stance_width 10, toe_out -15 |
| N2 | 닭처럼 걸어 | Chicken | 0.45 | 7 | 1.15 | 6.6 | ArmsBySide 0.55, LeftHop 0.51, DragLeftLeg 0.49 | s 0.3, n 1.45, c 15, m_arm 0, m_torso 0, m_knee 0.8, m_elbow 0, head_pitch 30, shoulder_abduction -15, toe_out 30 |
| N3 | 고양이처럼 걸어 | Cat | -0.02 | 59 | 1.55 | 6.9 | HighKnees 0.77, Kick 0.67, FlickLegs 0.61 | s 0.3, n 1.45, c 15, m_arm 0.4, m_torso 0, m_knee 1.5, head_pitch 25, shoulder_abduction -15 |
| N4 | 공룡처럼 걸어 | Dinosaur | 0.15 | 16 | 0.48 | 3.5 | ArmsBehindBack 0.62, CrossOver 0.48, Lunge 0.38 | s 1.8, n 0.55, m_arm 0.4, m_torso 3, m_knee 0.8, m_elbow 0, torso_pitch 15, head_pitch -15, shoulder_abduction -15, elbow_flexion -30, toe_out -15 |
| N5 | 새처럼 날개를 퍼덕이며 걸어 | Flapping | 0.16 | 55 | 2.69 | 11.2 | Chicken 0.73, March 0.70, Roadrunner 0.68 | s 0.3, n 1.45, c 30, m_arm 1.8, m_torso 0, m_knee 1.5, torso_pitch 15, shoulder_abduction 85, elbow_flexion 60, toe_out 30 |
| N6 | 오리처럼 뒤뚱뒤뚱 걸어 | Penguin | 0.17 | 64 | 2.28 | 8.5 | Teapot 0.65, Balance 0.59, Superman 0.54 | s 0.6, n 0.55, c 15, m_arm 1.8, m_torso 10, m_knee 0.4, m_elbow 0, head_pitch 30, shoulder_abduction 85, toe_out 30 |
| P1 | 좀비처럼 걸어 | Zombie | 0.29 | 25 | 2.33 | 13.8 | BentKnees 0.81, Dinosaur 0.72, Lunge 0.67 | s 1.8, n 0.55, c 30, m_arm 0.4, m_torso 10, m_knee 0.4, head_pitch 25, shoulder_flexion 85, elbow_flexion -30, toe_out 30 |
| P2 | 로봇처럼 걸어 | Robot | 0.04 | 62 | 1.22 | 5.3 | March 0.81, HighKnees 0.77, Kick 0.73 | c 15, m_arm 1.8, m_torso 0, m_knee 1.5, m_elbow 0, elbow_flexion 45 |
| P3 | 노인처럼 걸어 | Old | 0.20 | 30 | 1.66 | 10.9 | BentKnees 0.90, OnToesCrouched 0.71, Lunge 0.68 | s 0.6, n 0.75, c 30, m_arm 0.4, m_torso 6, m_knee 0.4, torso_pitch 15, head_pitch 25, shoulder_abduction -15, toe_out -15 |
| P4 | 수도승처럼 걸어 | Monk | 0.23 | 35 | 1.19 | 5.3 | ArmsAboveHead 0.87, BeatChest 0.75, WalkingStickRight 0.75 | s 1.4, n 0.75, m_arm 1.8, m_torso 0, m_knee 0.8, torso_pitch 15, head_pitch -15, shoulder_flexion 85, elbow_flexion 45 |
| P5 | 술 취한 사람처럼 걸어 | Drunk | 0.27 | 30 | 3.95 | 14.0 | BentKnees 0.80, Dinosaur 0.74, ShieldedLeft 0.69 | s 1.8, n 0.75, c 30, m_arm 1.8, m_torso 10, m_knee 0.4, head_pitch 30, shoulder_flexion 85, toe_out 30 |
| P6 | 슈퍼맨처럼 걸어 | Superman | 0.23 | 30 | 2.03 | 8.7 | Roadrunner 0.60, RaisedRightArm 0.56, RaisedLeftArm 0.53 | s 1.8, n 1.45, c 15, m_arm 1.8, m_torso 0, m_knee 1.5, torso_pitch -10, head_pitch -15, shoulder_abduction 85 |
| F1 | 팔자걸음으로 걸어 | DuckFoot | 0.04 | 63 | 2.64 | 12.5 | Roadrunner 0.74, BentKnees 0.70, Chicken 0.62 | s 1.8, n 0.75, c 30, m_arm 1.8, m_torso 3, m_knee 1.5, m_elbow 0, torso_pitch -10, head_pitch -15, shoulder_abduction 85, toe_out 30 |
| F2 | 안짱걸음으로 걸어 | PigeonToed | -0.07 | 87 | 2.68 | 13.7 | BentKnees 0.81, Crouched 0.69, Dinosaur 0.68 | s 1.8, n 0.75, c 30, m_arm 1.8, m_torso 10, m_knee 0.4, m_elbow 0, torso_pitch 15, head_pitch -15, shoulder_abduction 85, toe_out 30 |
| F3 | 다리를 넓게 벌리고 걸어 | WideLegs | 0.15 | 44 | 1.56 | 11.4 | Roadrunner 0.71, BentKnees 0.69, Dinosaur 0.64 | s 1.8, c 30, m_arm 1.8, m_torso 10, m_knee 1.5, stance_width 10, toe_out 30 |
| F4 | 무릎을 높이 들고 걸어 | HighKnees | 0.75 | 1 | 2.07 | 10.0 | HighKnees 0.75, Kick 0.70, Roadrunner 0.64 | s 0.3, n 0.55, c 30, m_arm 0.4, m_torso 0, m_knee 1.5, m_elbow 0, torso_pitch -10, head_pitch -15, elbow_flexion -30 |
| F5 | 까치발로 걸어 | Tiptoe | 0.04 | 68 | 9.42 | 11.0 | HighKnees 0.69, Roadrunner 0.68, Chicken 0.67 | s 0.3, c 30, m_arm 1.8, m_torso 10, m_knee 1.5, torso_pitch 15, head_pitch -15, shoulder_abduction 85 |
| F6 | 몸을 웅크리고 걸어 | Crouched | 0.52 | 10 | 2.57 | 11.2 | BentKnees 0.83, OnToesCrouched 0.67, Quail 0.66 | s 0.3, n 0.75, c 30, m_arm 0.4, m_torso 3, m_knee 0.4, m_elbow 0, torso_pitch 15, head_pitch 25, shoulder_abduction -15, elbow_flexion 45, toe_out -15 |
| F7 | 상체를 앞으로 숙이고 걸어 | BentForward | 0.55 | 13 | 2.52 | 10.8 | BentKnees 0.86, Dinosaur 0.80, OnToesCrouched 0.76 | c 30, m_arm 1.8, m_torso 10, m_knee 0.8, torso_pitch 15, head_pitch 25, elbow_flexion 60 |
| F8 | 비행기처럼 팔을 벌리고 걸어 | Aeroplane | 0.17 | 38 | 2.04 | 12.1 | Roadrunner 0.74, BentKnees 0.69, Chicken 0.61 | s 1.8, n 0.75, c 30, m_arm 0, m_torso 3, m_knee 1.3, m_elbow 0, torso_pitch -10, head_pitch -15, shoulder_abduction 85, elbow_flexion -30, stance_width 10, toe_out 30 |
| M1 | 우울하게 걸어 | Depressed | 0.48 | 11 | 1.87 | 6.8 | Zombie 0.74, Monk 0.61, InTheDark 0.61 | s 0.6, n 0.55, m_arm 0.4, m_torso 0, m_knee 0.4, torso_pitch 15, head_pitch 25, shoulder_flexion 85 |
| M2 | 신나게 걸어 | Elated | 0.18 | 38 | 2.70 | 12.5 | Roadrunner 0.74, BentKnees 0.70, Crouched 0.66 | s 1.8, n 1.45, c 30, m_arm 1.8, m_torso 10, m_knee 1.5, torso_pitch 15, head_pitch -15, toe_out 30 |
| M3 | 화가 나서 쿵쿵 걸어 | Angry | 0.38 | 24 | 4.37 | 12.7 | BentKnees 0.80, OnToesCrouched 0.75, Crouched 0.70 | s 1.4, n 1.25, c 30, m_arm 1.8, m_torso 10, m_knee 0.4, torso_pitch 15, head_pitch 25, shoulder_flexion 85, elbow_flexion -30 |
| M4 | 당당하게 걸어 | Proud | 0.28 | 22 | 1.37 | 2.4 | Rushed 0.69, SwingShoulders 0.60, SwingArmsRound 0.51 | s 1.4, m_arm 1.8, m_torso 0, torso_pitch 15, head_pitch -15 |
| M5 | 뻣뻣하게 걸어 | Stiff | 0.13 | 50 | 2.87 | 6.2 | ArmsAboveHead 0.75, Punch 0.66, BeatChest 0.65 | s 0.6, n 0.55, m_arm 0.4, m_torso 0, m_knee 0.4, m_elbow 0, shoulder_flexion 85, elbow_flexion 45 |

점수를 낸 25개: 유사도 평균 0.24, 1위 1개, 5위 이내 1개, 순위 중앙값 32, 크기 평균 2.45
