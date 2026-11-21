# 스타일 지표, 목표 동작 기준 (20261111_152002_v10_set7_gpt-5.6-sol, 프롬프트 v10)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 메추라기처럼 종종 걸어 | Quail | 0.59 | 5 | 1.58 | 5.3 | LeftHop 0.70, Chicken 0.66, March 0.60 | s 0.45, n 1.5, c 15, m_arm 0.2, m_torso 0.3, m_knee 0.7, torso_pitch 20, shoulder_abduction -15, elbow_flexion 50, stance_width -4, toe_out 10 |
| N2 | 고릴라처럼 가슴을 두드리며 걸어 | BeatChest | 0.40 | 26 | 1.51 | 7.5 | Dinosaur 0.77, ShieldedLeft 0.74, ShieldedRight 0.73 | s 0.7, n 0.75, c 20, m_arm 1.8, m_torso 7, m_knee 0.8, torso_pitch 25, shoulder_flexion 45, elbow_flexion 60, stance_width 10, toe_out 25, shoulder_rotation 60 |
| N3 | 펭귄 흉내를 내면서 걸어 | Penguin | 0.36 | 11 | 1.71 | 6.4 | Aeroplane 0.53, Balance 0.49, Star 0.42 | s 0.5, n 0.85, c 10, m_arm 0.3, m_torso 10, m_knee 0.6, shoulder_abduction 35, elbow_flexion -30, stance_width 10, toe_out 30 |
| N4 | 티라노사우루스처럼 걸어 | Dinosaur | 0.83 | 1 | 1.57 | 11.4 | Dinosaur 0.83, Lunge 0.78, BigSteps 0.74 | s 1.3, n 0.7, c 20, m_arm 0.3, m_torso 5, m_knee 1.2, torso_pitch 40, head_pitch -15, shoulder_flexion 45, elbow_flexion 60, stance_width 10, toe_out 15, shoulder_rotation 30, bounce 20 |
| N5 | 수탉처럼 걸어 | Chicken | 0.65 | 3 | 1.34 | 7.7 | March 0.76, Roadrunner 0.67, Chicken 0.65 | s 0.65, n 1.2, c 15, m_arm 0.3, m_torso 4, m_knee 1.5, torso_pitch -12, head_pitch -10, shoulder_abduction 45, elbow_flexion 60, stance_width -5, toe_out 20, bounce 10 |
| N6 | 고양이처럼 조심스럽게 걸어 | Cat | 0.52 | 11 | 1.49 | 6.6 | Dinosaur 0.80, BentKnees 0.70, OnToesCrouched 0.69 | s 0.65, n 0.6, c 20, m_arm 0.3, m_torso 0, m_knee 0.7, torso_pitch 15, head_pitch -10, shoulder_flexion 25, elbow_flexion 50, stance_width -8, toe_out -10, shoulder_rotation 20 |
| P1 | 어둠 속에서 손으로 더듬으며 걸어 | InTheDark | 0.48 | 18 | 1.36 | 5.8 | Dinosaur 0.72, ShieldedRight 0.70, ShieldedLeft 0.70 | s 0.7, n 0.6, c 15, m_arm 0.3, m_knee 0.8, torso_pitch 15, shoulder_flexion 55, elbow_flexion 35 |
| P2 | 군인처럼 행진하며 걸어 | March | 0.46 | 8 | 1.72 | 5.2 | HighKnees 0.78, Kick 0.73, Roadrunner 0.67 | n 1.15, c 15, m_arm 1.5, m_torso 0, m_knee 1.5, m_elbow 0, elbow_flexion -30 |
| P3 | 요정처럼 사뿐사뿐 걸어 | FairySteps | -0.00 | 62 | 0.69 | 3.1 | WalkingStickLeft 0.50, PendulumHands 0.49, Robot 0.48 | s 0.7, n 1.2, m_arm 0.5, m_knee 0.7, shoulder_abduction 25, elbow_flexion 30, stance_width -4, toe_out 15 |
| P4 | 덩치 큰 사람처럼 걸어 | Heavyset | 0.26 | 19 | 2.05 | 4.1 | LegsApart 0.73, Star 0.72, WideLegs 0.70 | s 1.4, n 0.75, m_arm 1.3, m_torso 6, shoulder_abduction 20, stance_width 10, toe_out 20 |
| P5 | 패션모델처럼 뽐내며 걸어 | Strutting | 0.29 | 16 | 1.39 | 3.0 | SpinClock 0.61, SpinAntiClock 0.56, LookUp 0.48 | s 1.4, n 0.85, m_arm 1.3, m_torso 5, torso_pitch -12, head_pitch -10, stance_width -8 |
| P6 | 특공대원처럼 총을 겨눈 자세로 걸어 | Swat | 0.74 | 3 | 1.11 | 6.8 | ShieldedRight 0.78, ShieldedLeft 0.78, Swat 0.74 | s 0.7, n 0.75, c 15, m_arm 0.3, m_torso 0, m_knee 0.8, m_elbow 0, torso_pitch 15, shoulder_flexion 85, elbow_flexion 40, stance_width 6, shoulder_rotation 25 |
| F1 | 뒷짐을 지고 걸어 | ArmsBehindBack | 0.79 | 1 | 1.43 | 4.4 | ArmsBehindBack 0.79, ArmsFolded 0.72, HandsInPockets 0.64 | m_arm 0, shoulder_flexion -45, elbow_flexion 60, shoulder_rotation 60 |
| F2 | 팔짱을 끼고 걸어 | ArmsFolded | 0.90 | 1 | 1.02 | 4.5 | ArmsFolded 0.90, LawnMower 0.84, OnPhoneLeft 0.79 | m_arm 0, m_elbow 0, shoulder_flexion 45, elbow_flexion 60, shoulder_rotation 60 |
| F3 | 양손을 허리에 짚고 걸어 | Akimbo | 0.69 | 6 | 1.11 | 2.8 | HandsInPockets 0.81, ArmsFolded 0.80, BeatChest 0.77 | m_arm 0, m_elbow 0, shoulder_abduction 35, elbow_flexion 60, shoulder_rotation 60 |
| F4 | 두 팔을 머리 위로 들고 걸어 | ArmsAboveHead | 0.74 | 2 | 0.74 | 4.8 | InTheDark 0.78, ArmsAboveHead 0.74, Zombie 0.74 | m_arm 0.3, shoulder_flexion 85, elbow_flexion -30 |
| F5 | 발뒤꿈치로 걸어 | OnHeels | 0.43 | 5 | 0.96 | 2.9 | Penguin 0.52, FairySteps 0.49, StartStop 0.47 | s 0.6, n 0.75, m_knee 0.7, torso_pitch -10 |
| F6 | 무릎을 굽힌 채로 걸어 | BentKnees | 0.97 | 1 | 1.49 | 5.5 | BentKnees 0.97, Lunge 0.75, Roadrunner 0.74 | c 20, m_knee 0.75 |
| F7 | 상체를 뒤로 젖히고 걸어 | LeanBack | 0.25 | 10 | 0.32 | 1.1 | LookUp 0.59, InTheDark 0.42, Strutting 0.36 | torso_pitch -15 |
| F8 | 발을 바닥에 끌면서 걸어 | SlideFeet | 0.38 | 8 | 0.90 | 2.7 | StartStop 0.64, FairySteps 0.58, Penguin 0.56 | s 0.7, n 0.75, m_knee 0.4 |
| M1 | 급하게 서둘러 걸어 | Rushed | 0.77 | 1 | 0.63 | 2.4 | Rushed 0.77, Angry 0.67, Drunk 0.61 | s 1.2, n 1.4, m_arm 1.5, torso_pitch 15 |
| M2 | 누가 따라오는 것 같아 뒤를 살피며 걸어 | Followed | -0.07 | 81 | 1.58 | 5.2 | Dinosaur 0.84, BentKnees 0.73, ShieldedRight 0.70 | n 0.6, c 15, m_arm 0.3, m_knee 0.8, torso_pitch 15, shoulder_flexion 20, elbow_flexion 40 |
| M3 | 우아하게 걸어 | GracefulArms | -0.11 | 70 | 0.54 | 2.0 | ArmsBySide 0.56, SlideFeet 0.50, Lunge 0.43 | s 1.25, n 0.8, m_arm 0.6, m_torso 0.5, m_knee 0.8, stance_width -4 |
| M4 | 외줄을 타듯 균형을 잡으며 걸어 | Balance | 0.75 | 2 | 1.07 | 6.2 | RaisedRightArm 0.76, Balance 0.75, Flapping 0.74 | s 0.7, n 0.6, m_arm 0.3, m_torso 0, m_knee 0.8, shoulder_abduction 80, elbow_flexion -20, stance_width -8 |
| M5 | 엉덩이를 씰룩거리며 걸어 | WiggleHips | 0.34 | 24 | 0.62 | 2.5 | Followed 0.80, SpinClock 0.69, Old 0.65 | m_torso 8 |

점수를 낸 25개: 유사도 평균 0.50, 1위 5개, 5위 이내 11개, 순위 중앙값 8, 크기 평균 1.20
