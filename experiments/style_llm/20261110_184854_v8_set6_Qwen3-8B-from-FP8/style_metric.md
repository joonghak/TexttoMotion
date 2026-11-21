# 스타일 지표, 목표 동작 기준 (20261110_184854_v8_set6_Qwen3-8B-from-FP8, 프롬프트 v8)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 펭귄처럼 걸어 | Penguin | 0.37 | 7 | 1.31 | 4.9 | LegsApart 0.59, DuckFoot 0.59, WideLegs 0.56 | s 0.6, n 1.25, m_torso 6, torso_pitch 15, stance_width 10, toe_out 30 |
| N2 | 닭처럼 걸어 | Chicken | 0.07 | 44 | 1.17 | 6.8 | LeanRight 0.59, LeanLeft 0.57, Depressed 0.56 | s 0.3, n 1.45, m_torso 6, torso_pitch 15, head_pitch 25, shoulder_abduction -15, stance_width 10, toe_out -15 |
| N3 | 고양이처럼 걸어 | Cat | 0.09 | 59 | 1.59 | 7.0 | RightHop 0.64, InTheDark 0.61, LeftHop 0.56 | s 0.3, n 1.45, c 15, m_arm 0.4, m_torso 0, m_knee 0.8, m_elbow 0, torso_pitch 15, shoulder_flexion 85, toe_out -15 |
| N4 | 공룡처럼 걸어 | Dinosaur | 0.69 | 3 | 0.96 | 7.0 | ShieldedRight 0.73, ShieldedLeft 0.71, Dinosaur 0.69 | s 1.8, n 0.75, c 15, m_arm 1.5, m_torso 6, m_knee 0.8, torso_pitch 15, shoulder_abduction 85, elbow_flexion 45, stance_width 10, toe_out 30 |
| N5 | 새처럼 날개를 퍼덕이며 걸어 | Flapping | 0.10 | 51 | 1.86 | 7.7 | ShieldedLeft 0.61, ShieldedRight 0.60, March 0.57 | c 15, m_arm 1.8, m_knee 1.5, torso_pitch 15, shoulder_flexion 85, toe_out 30 |
| N6 | 오리처럼 뒤뚱뒤뚱 걸어 | Penguin | 0.20 | 31 | 1.40 | 5.2 | LegsApart 0.77, WideLegs 0.72, DuckFoot 0.72 | m_torso 10, stance_width 10, toe_out 30 |
| P1 | 좀비처럼 걸어 | Zombie | -0.03 | 49 | 0.71 | 4.2 | StartStop 0.68, FairySteps 0.57, Balance 0.44 | s 0.6, n 0.55, m_arm 0.4, m_torso 6, torso_pitch 15, elbow_flexion -30 |
| P2 | 로봇처럼 걸어 | Robot | 0.70 | 10 | 0.52 | 2.3 | LawnMower 0.87, BeatChest 0.84, OnPhoneLeft 0.82 | m_torso 0, m_knee 0.8, m_elbow 0, elbow_flexion 45 |
| P3 | 노인처럼 걸어 | Old | 0.17 | 31 | 0.68 | 4.5 | Chicken 0.75, Quail 0.68, Roadrunner 0.68 | s 0.6, n 0.75, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 35, head_pitch -15 |
| P4 | 수도승처럼 걸어 | Monk | 0.33 | 33 | 1.33 | 6.0 | ShieldedRight 0.78, ShieldedLeft 0.78, Dinosaur 0.77 | s 1.4, n 0.75, c 15, m_arm 0.4, m_torso 3, m_knee 0.8, torso_pitch 15, shoulder_flexion 30, elbow_flexion 45, stance_width 10, toe_out 30 |
| P5 | 술 취한 사람처럼 걸어 | Drunk | 0.48 | 9 | 1.62 | 5.7 | DuckFoot 0.71, Depressed 0.69, Angry 0.61 | s 1.4, n 0.75, m_arm 1.5, m_torso 6, torso_pitch 15, head_pitch 25, elbow_flexion -30, stance_width 10, toe_out 30 |
| P6 | 슈퍼맨처럼 걸어 | Superman | -0.07 | 66 | 1.21 | 5.2 | WideLegs 0.61, LegsApart 0.56, Star 0.53 | s 1.4, n 1.25, m_arm 1.8, torso_pitch -15, head_pitch -15, elbow_flexion 45, stance_width 10 |
| F1 | 팔자걸음으로 걸어 | DuckFoot | 0.12 | 32 | 1.31 | 6.2 | Flapping 0.71, Teapot 0.68, RaisedRightArm 0.67 | shoulder_abduction 85, stance_width 10 |
| F2 | 안짱걸음으로 걸어 | PigeonToed | 0.44 | 13 | 0.91 | 4.6 | LegsApart 0.76, WideLegs 0.72, Star 0.56 | m_torso 10, stance_width 10 |
| F3 | 다리를 넓게 벌리고 걸어 | WideLegs | 0.66 | 1 | 0.45 | 3.3 | WideLegs 0.66, LegsApart 0.63, Star 0.56 | stance_width 10 |
| F4 | 무릎을 높이 들고 걸어 | HighKnees | 0.85 | 1 | 1.01 | 4.9 | HighKnees 0.85, Kick 0.79, Roadrunner 0.69 | c 15, m_knee 1.5 |
| F5 | 까치발로 걸어 | Tiptoe | -0.60 | 96 | 2.36 | 2.8 | DuckFoot 0.72, ArmsBySide 0.54, Strutting 0.53 | toe_out 30 |
| F6 | 몸을 웅크리고 걸어 | Crouched | 0.61 | 8 | 2.20 | 9.6 | BentKnees 0.97, Lunge 0.77, Roadrunner 0.77 | c 30, m_arm 0.4, m_knee 0.8, torso_pitch 15 |
| F7 | 상체를 앞으로 숙이고 걸어 | BentForward | 0.70 | 3 | 0.26 | 1.1 | Depressed 0.72, Rocket 0.70, BentForward 0.70 | torso_pitch 15 |
| F8 | 비행기처럼 팔을 벌리고 걸어 | Aeroplane | 0.55 | 7 | 0.89 | 5.3 | RaisedRightArm 0.85, Flapping 0.83, RaisedLeftArm 0.81 | shoulder_abduction 85 |
| M1 | 우울하게 걸어 | Depressed | 0.70 | 2 | 1.21 | 4.4 | StartStop 0.72, Depressed 0.70, Monk 0.61 | s 0.6, n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 25 |
| M2 | 신나게 걸어 | Elated | 0.28 | 18 | 0.56 | 2.6 | Rushed 0.68, LegsApart 0.54, Followed 0.52 | s 1.4, n 1.25, m_arm 1.5 |
| M3 | 화가 나서 쿵쿵 걸어 | Angry | -0.11 | 66 | 1.27 | 3.7 | Strutting 0.54, LookUp 0.53, Rushed 0.35 | s 1.4, n 1.25, m_arm 1.5, m_knee 1.3, torso_pitch -15, head_pitch -15 |
| M4 | 당당하게 걸어 | Proud | 0.21 | 16 | 1.75 | 3.0 | LookUp 0.64, Strutting 0.58, SpinClock 0.48 | s 1.4, m_arm 1.8, torso_pitch -15, head_pitch -15 |
| M5 | 뻣뻣하게 걸어 | Stiff | -0.24 | 80 | 0.53 | 1.1 | ArmsBySide 0.45, HandsInPockets 0.24, LimpRight 0.24 | m_arm 0.4, m_torso 0, m_elbow 0 |

점수를 낸 25개: 유사도 평균 0.29, 1위 2개, 5위 이내 5개, 순위 중앙값 18, 크기 평균 1.16
