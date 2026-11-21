# 스타일 지표, 목표 동작 기준 (20261112_144300_v10_set7_gpt-5.6-luna, 프롬프트 v10)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 메추라기처럼 종종 걸어 | Quail | 0.52 | 2 | 1.28 | 4.3 | LeftHop 0.57, Quail 0.52, RightHop 0.51 | s 0.5, n 1.5, c 10, m_arm 0.3, m_torso 5, m_knee 0.7, m_elbow 0, shoulder_abduction -15, stance_width 8, toe_out 10 |
| N2 | 고릴라처럼 가슴을 두드리며 걸어 | BeatChest | 0.36 | 25 | 1.46 | 7.3 | ShieldedLeft 0.75, ShieldedRight 0.74, Dinosaur 0.73 | s 0.7, n 0.8, c 20, m_arm 0.3, m_torso 3, m_knee 0.8, torso_pitch 25, shoulder_flexion 45, elbow_flexion 50, stance_width 10 |
| N3 | 펭귄 흉내를 내면서 걸어 | Penguin | 0.35 | 12 | 1.46 | 5.5 | LegsApart 0.61, WideLegs 0.59, Star 0.58 | s 0.7, n 0.9, m_arm 0.3, m_torso 10, m_knee 0.7, shoulder_abduction 20, stance_width 10, toe_out 20 |
| N4 | 티라노사우루스처럼 걸어 | Dinosaur | 0.60 | 7 | 0.96 | 7.0 | ShieldedLeft 0.78, Swat 0.74, ShieldedRight 0.73 | s 0.7, n 1.2, c 15, m_arm 0.3, m_knee 0.8, torso_pitch 30, head_pitch 25, shoulder_flexion 45, elbow_flexion 60, stance_width 6 |
| N5 | 수탉처럼 걸어 | Chicken | 0.55 | 5 | 1.11 | 6.4 | March 0.70, Roadrunner 0.63, HighKnees 0.58 | s 1.15, c 15, m_arm 0.3, m_knee 1.5, torso_pitch -10, head_pitch -10, shoulder_abduction 45, elbow_flexion 45, stance_width 5, toe_out 20 |
| N6 | 고양이처럼 조심스럽게 걸어 | Cat | 0.46 | 13 | 1.18 | 5.2 | Dinosaur 0.74, ShieldedRight 0.61, OnToesCrouched 0.61 | s 0.7, n 0.6, c 15, m_arm 0.3, m_torso 0, m_knee 0.7, torso_pitch 15, shoulder_flexion 20, elbow_flexion 40, stance_width -5 |
| P1 | 어둠 속에서 손으로 더듬으며 걸어 | InTheDark | 0.51 | 4 | 1.55 | 6.6 | Superman 0.57, Zombie 0.56, ShieldedLeft 0.55 | s 0.7, n 0.6, c 15, m_arm 0.3, m_knee 0.8, torso_pitch 15, head_pitch 20, shoulder_flexion 85, elbow_flexion -30 |
| P2 | 군인처럼 행진하며 걸어 | March | 0.53 | 7 | 1.67 | 5.1 | HighKnees 0.82, Kick 0.75, Roadrunner 0.69 | n 1.1, c 15, m_arm 1.3, m_torso 0, m_knee 1.5, m_elbow 0, elbow_flexion -20 |
| P3 | 요정처럼 사뿐사뿐 걸어 | FairySteps | 0.37 | 5 | 0.45 | 2.0 | Penguin 0.55, Robot 0.47, Tiptoe 0.40 | s 0.7, n 1.2, m_arm 0.3, m_knee 0.7 |
| P4 | 덩치 큰 사람처럼 걸어 | Heavyset | 0.11 | 35 | 1.76 | 3.5 | WideLegs 0.67, LegsApart 0.66, Star 0.53 | s 1.1, n 0.8, m_arm 1.3, m_torso 5, m_knee 0.8, stance_width 10 |
| P5 | 패션모델처럼 뽐내며 걸어 | Strutting | 0.48 | 2 | 1.30 | 2.9 | LookUp 0.48, Strutting 0.48, Waving 0.42 | s 1.4, n 0.9, m_arm 1.5, torso_pitch -10, head_pitch -10, stance_width -5, toe_out 10 |
| P6 | 특공대원처럼 총을 겨눈 자세로 걸어 | Swat | 0.48 | 8 | 0.97 | 6.0 | InTheDark 0.60, ShieldedRight 0.59, ArmsAboveHead 0.58 | s 0.8, n 0.75, c 15, m_arm 0.3, m_torso 0, m_knee 0.8, shoulder_flexion 85, elbow_flexion -30 |
| F1 | 뒷짐을 지고 걸어 | ArmsBehindBack | 0.62 | 1 | 1.14 | 3.5 | ArmsBehindBack 0.62, Rocket 0.52, Roadrunner 0.32 | m_arm 0.3, shoulder_flexion -45 |
| F2 | 팔짱을 끼고 걸어 | ArmsFolded | 0.88 | 1 | 1.02 | 4.5 | ArmsFolded 0.88, LawnMower 0.85, OnPhoneLeft 0.81 | m_arm 0.3, shoulder_flexion 45, elbow_flexion 60, shoulder_rotation 45 |
| F3 | 양손을 허리에 짚고 걸어 | Akimbo | 0.75 | 2 | 0.93 | 2.3 | BeatChest 0.75, Akimbo 0.75, HandsInPockets 0.73 | m_arm 0.3, shoulder_flexion -20, shoulder_abduction 25, elbow_flexion 50 |
| F4 | 두 팔을 머리 위로 들고 걸어 | ArmsAboveHead | 0.88 | 1 | 0.78 | 5.0 | ArmsAboveHead 0.88, InTheDark 0.79, Zombie 0.73 | m_arm 0.3, shoulder_flexion 85 |
| F5 | 발뒤꿈치로 걸어 | OnHeels | 0.00 | 21 | 0.00 | 0.0 | Aeroplane 0.00, ShieldedRight 0.00, ShieldedLeft 0.00 | 기본값 |
| F6 | 무릎을 굽힌 채로 걸어 | BentKnees | 0.96 | 1 | 1.02 | 3.7 | BentKnees 0.96, Roadrunner 0.75, OnToesCrouched 0.73 | c 15, m_knee 0.8 |
| F7 | 상체를 뒤로 젖히고 걸어 | LeanBack | 0.24 | 10 | 0.25 | 0.9 | LookUp 0.59, InTheDark 0.42, Strutting 0.36 | torso_pitch -12 |
| F8 | 발을 바닥에 끌면서 걸어 | SlideFeet | 0.23 | 17 | 0.58 | 1.8 | Stiff 0.58, OnHeels 0.51, LimpRight 0.48 | m_knee 0.4 |
| M1 | 급하게 서둘러 걸어 | Rushed | 0.72 | 1 | 0.37 | 1.4 | Rushed 0.72, Followed 0.54, LegsApart 0.51 | s 1.1, n 1.3, m_arm 1.3 |
| M2 | 누가 따라오는 것 같아 뒤를 살피며 걸어 | Followed | -0.11 | 87 | 1.52 | 5.0 | Dinosaur 0.79, ShieldedRight 0.66, ShieldedLeft 0.65 | s 0.8, n 0.6, c 15, m_arm 0.3, m_knee 0.8, torso_pitch 15, shoulder_flexion 20, elbow_flexion 40 |
| M3 | 우아하게 걸어 | GracefulArms | -0.15 | 65 | 0.37 | 1.4 | Strutting 0.49, LookUp 0.47, LimpRight 0.41 | s 1.1, n 0.9, m_arm 0.7, m_torso 0.5, m_knee 0.8, torso_pitch -3, head_pitch -5, toe_out 8 |
| M4 | 외줄을 타듯 균형을 잡으며 걸어 | Balance | 0.75 | 2 | 1.07 | 6.2 | RaisedRightArm 0.75, Balance 0.75, Flapping 0.73 | s 0.7, n 0.7, m_arm 0.3, m_torso 5, m_knee 0.8, shoulder_abduction 80, elbow_flexion -20, stance_width -8 |
| M5 | 엉덩이를 씰룩거리며 걸어 | WiggleHips | 0.41 | 18 | 0.82 | 3.3 | Old 0.73, Followed 0.69, SpinClock 0.68 | n 0.8, m_torso 10 |

점수를 낸 25개: 유사도 평균 0.46, 1위 5개, 5위 이내 12개, 순위 중앙값 7, 크기 평균 1.00
