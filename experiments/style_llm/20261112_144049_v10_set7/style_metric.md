# 스타일 지표, 목표 동작 기준 (20261112_144049_v10_set7, 프롬프트 v10)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 메추라기처럼 종종 걸어 | Quail | 0.17 | 19 | 0.81 | 2.7 | Penguin 0.51, RightHop 0.51, Robot 0.51 | s 0.5, n 1.5, m_arm 0.6 |
| N2 | 고릴라처럼 가슴을 두드리며 걸어 | BeatChest | 0.75 | 2 | 0.81 | 4.0 | ArmsAboveHead 0.82, BeatChest 0.75, OnPhoneRight 0.74 | m_arm 1.5, shoulder_flexion 45, elbow_flexion 40 |
| N3 | 펭귄 흉내를 내면서 걸어 | Penguin | 0.07 | 59 | 1.24 | 4.6 | LegsApart 0.76, WideLegs 0.72, Star 0.56 | m_torso 10, stance_width 10 |
| N4 | 티라노사우루스처럼 걸어 | Dinosaur | 0.53 | 8 | 0.99 | 7.2 | BentKnees 0.76, Chicken 0.63, Lunge 0.58 | s 0.8, n 0.75, c 20, m_arm 0.4, m_knee 0.8, torso_pitch 25, head_pitch 20, stance_width 10 |
| N5 | 수탉처럼 걸어 | Chicken | -0.09 | 64 | 0.44 | 2.6 | LookUp 0.75, Strutting 0.55, SpinClock 0.35 | s 1.2, m_torso 0, m_elbow 0, torso_pitch -15, head_pitch -15 |
| N6 | 고양이처럼 조심스럽게 걸어 | Cat | 0.54 | 7 | 1.00 | 4.5 | Dinosaur 0.77, WalkingStickRight 0.65, ShieldedRight 0.64 | n 0.5, c 10, m_arm 0.3, m_knee 0.8, torso_pitch 10, shoulder_flexion 20, elbow_flexion 40 |
| P1 | 어둠 속에서 손으로 더듬으며 걸어 | InTheDark | 0.20 | 47 | 1.25 | 5.3 | Dinosaur 0.84, BentKnees 0.71, ShieldedRight 0.66 | n 0.5, c 15, m_arm 0.3, m_knee 0.8, torso_pitch 15, shoulder_flexion 20, elbow_flexion 40 |
| P2 | 군인처럼 행진하며 걸어 | March | 0.36 | 12 | 1.75 | 5.3 | InTheDark 0.67, ArmsAboveHead 0.62, Zombie 0.61 | c 10, m_arm 0.3, m_torso 0, torso_pitch 5, head_pitch -10, shoulder_flexion 85, elbow_flexion -30 |
| P3 | 요정처럼 사뿐사뿐 걸어 | FairySteps | 0.11 | 56 | 0.73 | 3.3 | LawnMower 0.74, ShieldedRight 0.69, Swat 0.67 | m_arm 0.4, m_torso 5, m_knee 0.75, torso_pitch 10, head_pitch -5, shoulder_flexion 20, elbow_flexion 40 |
| P4 | 덩치 큰 사람처럼 걸어 | Heavyset | 0.12 | 37 | 2.35 | 4.7 | BentKnees 0.75, Chicken 0.63, Roadrunner 0.62 | s 0.8, n 0.8, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 15, stance_width 8 |
| P5 | 패션모델처럼 뽐내며 걸어 | Strutting | -0.02 | 62 | 2.32 | 5.1 | ArmsAboveHead 0.84, InTheDark 0.77, Zombie 0.70 | m_arm 1.4, head_pitch -10, shoulder_flexion 85 |
| P6 | 특공대원처럼 총을 겨눈 자세로 걸어 | Swat | 0.62 | 10 | 0.62 | 3.8 | ArmsAboveHead 0.71, InTheDark 0.70, LawnMower 0.68 | m_arm 0.3, m_elbow 0, torso_pitch 10, head_pitch -10, shoulder_flexion 45, elbow_flexion 30 |
| F1 | 뒷짐을 지고 걸어 | ArmsBehindBack | 0.21 | 31 | 0.36 | 1.1 | Depressed 0.72, Rocket 0.70, BentForward 0.70 | torso_pitch 15 |
| F2 | 팔짱을 끼고 걸어 | ArmsFolded | 0.20 | 28 | 1.07 | 4.8 | InTheDark 0.78, ArmsAboveHead 0.74, Zombie 0.74 | shoulder_flexion 85, elbow_flexion -30 |
| F3 | 양손을 허리에 짚고 걸어 | Akimbo | 0.63 | 15 | 1.12 | 2.8 | BeatChest 0.90, OnPhoneLeft 0.89, ArmsFolded 0.89 | elbow_flexion 60 |
| F4 | 두 팔을 머리 위로 들고 걸어 | ArmsAboveHead | 0.57 | 3 | 0.81 | 5.2 | Zombie 0.80, InTheDark 0.63, ArmsAboveHead 0.57 | s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 |
| F5 | 발뒤꿈치로 걸어 | OnHeels | -0.59 | 98 | 1.78 | 5.3 | BentKnees 0.91, Roadrunner 0.79, Lunge 0.72 | c 20 |
| F6 | 무릎을 굽힌 채로 걸어 | BentKnees | 0.91 | 1 | 1.46 | 5.3 | BentKnees 0.91, Roadrunner 0.79, Lunge 0.72 | c 20 |
| F7 | 상체를 뒤로 젖히고 걸어 | LeanBack | 0.24 | 10 | 0.25 | 0.9 | LookUp 0.59, InTheDark 0.42, Strutting 0.36 | torso_pitch -12 |
| F8 | 발을 바닥에 끌면서 걸어 | SlideFeet | 0.41 | 5 | 0.90 | 2.7 | StartStop 0.53, FairySteps 0.52, Penguin 0.51 | s 0.8, n 0.75, m_arm 0.4, m_knee 0.4 |
| M1 | 급하게 서둘러 걸어 | Rushed | 0.70 | 1 | 0.53 | 2.0 | Rushed 0.70, LegsApart 0.53, Followed 0.53 | s 1.3, n 1.2, m_arm 1.4 |
| M2 | 누가 따라오는 것 같아 뒤를 살피며 걸어 | Followed | 0.12 | 41 | 1.10 | 3.6 | LeanRight 0.82, Depressed 0.75, Monk 0.74 | m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 |
| M3 | 우아하게 걸어 | GracefulArms | 0.08 | 47 | 0.36 | 1.4 | Roadrunner 0.83, Chicken 0.70, BentKnees 0.63 | c 5, m_arm 1.2, m_torso 0.8, torso_pitch 10, head_pitch -10 |
| M4 | 외줄을 타듯 균형을 잡으며 걸어 | Balance | 0.18 | 26 | 0.34 | 1.9 | LeanRight 0.71, Monk 0.67, Depressed 0.63 | m_arm 0.4, m_torso 0, torso_pitch 10, head_pitch 10 |
| M5 | 엉덩이를 씰룩거리며 걸어 | WiggleHips | 0.35 | 25 | 0.82 | 3.3 | Followed 0.81, SpinClock 0.70, Old 0.67 | m_torso 10 |

점수를 낸 25개: 유사도 평균 0.30, 1위 2개, 5위 이내 5개, 순위 중앙값 25, 크기 평균 1.01
