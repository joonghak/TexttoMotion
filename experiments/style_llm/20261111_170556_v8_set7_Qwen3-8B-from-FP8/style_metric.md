# 스타일 지표, 목표 동작 기준 (20261111_170556_v8_set7_Qwen3-8B-from-FP8, 프롬프트 v8)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 메추라기처럼 종종 걸어 | Quail | -0.07 | 72 | 2.00 | 6.7 | Star 0.69, InTheDark 0.64, Zombie 0.60 | s 1.4, n 1.25, m_torso 3, m_knee 0.8, torso_pitch 15, head_pitch -15, shoulder_flexion 85, elbow_flexion -30, stance_width 10, toe_out 30 |
| N2 | 고릴라처럼 가슴을 두드리며 걸어 | BeatChest | 0.29 | 36 | 2.50 | 12.5 | Swat 0.75, ShieldedLeft 0.75, ShieldedRight 0.75 | s 1.8, n 1.25, c 30, m_arm 1.8, m_torso 0, torso_pitch 15, head_pitch 25, shoulder_flexion 85, elbow_flexion 45, stance_width 10, toe_out 30 |
| N3 | 펭귄 흉내를 내면서 걸어 | Penguin | -0.08 | 88 | 2.10 | 7.8 | Teapot 0.70, Superman 0.69, ShieldedLeft 0.55 | c 15, m_torso 6, torso_pitch 15, head_pitch 25, shoulder_abduction 85, stance_width 10, toe_out 30 |
| N4 | 티라노사우루스처럼 걸어 | Dinosaur | 0.06 | 43 | 0.81 | 5.9 | DuckFoot 0.70, Depressed 0.58, Monk 0.54 | s 1.8, n 0.55, m_arm 0.4, m_torso 6, torso_pitch 15, head_pitch 25, elbow_flexion -30, stance_width 10, toe_out 30 |
| N5 | 수탉처럼 걸어 | Chicken | 0.05 | 44 | 0.97 | 5.6 | Strutting 0.53, BeatChest 0.47, Akimbo 0.46 | s 0.6, n 1.25, m_arm 1.5, torso_pitch -15, head_pitch -15, elbow_flexion 45, stance_width 10, toe_out 30 |
| N6 | 고양이처럼 조심스럽게 걸어 | Cat | 0.16 | 46 | 1.36 | 6.0 | BentForward 0.52, ArmsBySide 0.51, Chicken 0.50 | s 0.6, n 0.75, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25, toe_out 30 |
| P1 | 어둠 속에서 손으로 더듬으며 걸어 | InTheDark | 0.64 | 3 | 1.52 | 6.5 | Zombie 0.69, Superman 0.65, InTheDark 0.64 | s 0.6, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25, shoulder_flexion 85 |
| P2 | 군인처럼 행진하며 걸어 | March | 0.44 | 11 | 1.94 | 5.9 | ShieldedRight 0.60, ShieldedLeft 0.58, Swat 0.57 | s 1.4, n 1.25, c 15, m_arm 1.5, m_torso 0, torso_pitch -15, shoulder_flexion 30, stance_width 10, toe_out 30 |
| P3 | 요정처럼 사뿐사뿐 걸어 | FairySteps | -0.26 | 91 | 1.92 | 8.5 | March 0.63, LeftHop 0.57, HighKnees 0.53 | s 0.3, n 1.45, c 15, m_arm 1.5, m_knee 1.5, torso_pitch 15, shoulder_flexion 85, stance_width 10, toe_out 30 |
| P4 | 덩치 큰 사람처럼 걸어 | Heavyset | 0.27 | 22 | 2.39 | 4.8 | WideLegs 0.56, BeatChest 0.50, LegsApart 0.49 | s 1.4, m_arm 1.5, torso_pitch -15, head_pitch -15, elbow_flexion 45, stance_width 10 |
| P5 | 패션모델처럼 뽐내며 걸어 | Strutting | 0.36 | 21 | 3.21 | 7.0 | ArmsAboveHead 0.68, BeatChest 0.61, Swat 0.55 | s 1.4, n 1.25, m_arm 1.8, m_torso 0, torso_pitch -15, head_pitch -15, shoulder_flexion 85, elbow_flexion 45, stance_width 10 |
| P6 | 특공대원처럼 총을 겨눈 자세로 걸어 | Swat | 0.55 | 3 | 1.15 | 7.1 | ArmsAboveHead 0.68, BeatChest 0.61, Swat 0.55 | s 1.4, n 1.25, m_arm 1.5, torso_pitch -15, head_pitch -15, shoulder_flexion 85, elbow_flexion 45, stance_width 10 |
| F1 | 뒷짐을 지고 걸어 | ArmsBehindBack | 0.24 | 24 | 0.85 | 2.6 | Rocket 0.77, BentForward 0.72, Depressed 0.71 | torso_pitch 35 |
| F2 | 팔짱을 끼고 걸어 | ArmsFolded | -0.04 | 32 | 0.52 | 2.3 | ArmsBehindBack 0.52, ArmsBySide 0.50, Rocket 0.20 | m_arm 0, shoulder_abduction -15, elbow_flexion -30 |
| F3 | 양손을 허리에 짚고 걸어 | Akimbo | -0.10 | 82 | 0.48 | 1.2 | ArmsFolded 0.59, ArmsBehindBack 0.52, LawnMower 0.47 | shoulder_abduction -15 |
| F4 | 두 팔을 머리 위로 들고 걸어 | ArmsAboveHead | 0.88 | 1 | 0.78 | 5.0 | ArmsAboveHead 0.88, InTheDark 0.79, Zombie 0.73 | m_arm 1.5, shoulder_flexion 85 |
| F5 | 발뒤꿈치로 걸어 | OnHeels | 0.19 | 22 | 0.46 | 1.4 | FairySteps 0.67, CrossOver 0.66, PigeonToed 0.64 | toe_out -15 |
| F6 | 무릎을 굽힌 채로 걸어 | BentKnees | 0.89 | 1 | 1.01 | 3.7 | BentKnees 0.89, Roadrunner 0.79, Chicken 0.71 | c 15 |
| F7 | 상체를 뒤로 젖히고 걸어 | LeanBack | 0.25 | 10 | 0.32 | 1.1 | LookUp 0.59, InTheDark 0.42, Strutting 0.36 | torso_pitch -15 |
| F8 | 발을 바닥에 끌면서 걸어 | SlideFeet | 0.59 | 1 | 0.45 | 1.4 | SlideFeet 0.59, StartStop 0.57, FairySteps 0.54 | n 0.75, m_knee 0.8 |
| M1 | 급하게 서둘러 걸어 | Rushed | 0.68 | 1 | 0.68 | 2.6 | Rushed 0.68, LegsApart 0.54, Followed 0.52 | s 1.4, n 1.25, m_arm 1.5 |
| M2 | 누가 따라오는 것 같아 뒤를 살피며 걸어 | Followed | -0.09 | 68 | 1.36 | 4.4 | StartStop 0.72, Depressed 0.70, Monk 0.61 | s 0.6, n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 25 |
| M3 | 우아하게 걸어 | GracefulArms | 0.45 | 18 | 1.64 | 6.2 | ArmsAboveHead 0.78, OnPhoneRight 0.77, ShieldedRight 0.70 | s 1.4, m_arm 1.5, m_torso 0, torso_pitch 15, head_pitch -15, shoulder_flexion 85, elbow_flexion 45, toe_out 30 |
| M4 | 외줄을 타듯 균형을 잡으며 걸어 | Balance | 0.02 | 54 | 0.61 | 3.5 | DuckFoot 0.49, Depressed 0.48, Penguin 0.42 | s 0.6, n 1.25, m_arm 1.5, m_torso 3, torso_pitch 15, toe_out 30 |
| M5 | 엉덩이를 씰룩거리며 걸어 | WiggleHips | 0.14 | 40 | 1.16 | 4.6 | LegsApart 0.76, WideLegs 0.72, Star 0.56 | m_torso 10, stance_width 10 |

점수를 낸 25개: 유사도 평균 0.26, 1위 4개, 5위 이내 6개, 순위 중앙값 24, 크기 평균 1.29
