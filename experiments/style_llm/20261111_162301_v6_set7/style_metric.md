# 스타일 지표, 목표 동작 기준 (20261111_162301_v6_set7, 프롬프트 v6)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 메추라기처럼 종종 걸어 | Quail | 0.21 | 22 | 1.14 | 3.8 | TogetherStep 0.63, StartStop 0.59, Penguin 0.54 | s 0.35, n 1.45, m_torso 6 |
| N2 | 고릴라처럼 가슴을 두드리며 걸어 | BeatChest | 0.54 | 9 | 1.02 | 5.1 | ArmsAboveHead 0.85, Zombie 0.75, InTheDark 0.74 | n 0.75, m_arm 0.4, shoulder_flexion 85 |
| N3 | 펭귄 흉내를 내면서 걸어 | Penguin | 0.09 | 63 | 1.21 | 4.5 | Old 0.83, StartStop 0.80, Sweep 0.66 | n 0.55, m_torso 10, torso_pitch 35 |
| N4 | 티라노사우루스처럼 걸어 | Dinosaur | 0.65 | 6 | 1.31 | 9.6 | BentKnees 0.89, Lunge 0.72, Roadrunner 0.72 | s 0.6, n 0.55, c 30, m_arm 0, m_knee 0.8, m_elbow 0, torso_pitch 15, head_pitch -15, stance_width 10 |
| N5 | 수탉처럼 걸어 | Chicken | -0.16 | 59 | 0.49 | 2.8 | LookUp 0.53, SpinAntiClock 0.38, RightHop 0.36 | s 0.6, n 1.25, m_torso 0, m_elbow 0, torso_pitch -10, head_pitch -15 |
| N6 | 고양이처럼 조심스럽게 걸어 | Cat | -0.40 | 89 | 0.82 | 3.6 | Penguin 0.39, LookUp 0.38, Robot 0.34 | s 0.6, n 0.75, m_arm 0.4, m_torso 3, m_knee 0.8, torso_pitch -10, head_pitch -15 |
| P1 | 어둠 속에서 손으로 더듬으며 걸어 | InTheDark | 0.62 | 3 | 1.51 | 6.5 | Zombie 0.68, Superman 0.65, InTheDark 0.62 | s 0.6, n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 25, shoulder_flexion 85 |
| P2 | 군인처럼 행진하며 걸어 | March | 0.17 | 29 | 1.28 | 3.9 | InTheDark 0.56, Swimming 0.47, ArmsAboveHead 0.47 | s 1.4, n 1.25, m_arm 1.5, m_torso 0, torso_pitch -10, head_pitch -15, shoulder_flexion 30 |
| P3 | 요정처럼 사뿐사뿐 걸어 | FairySteps | 0.42 | 9 | 0.93 | 4.1 | OnHeels 0.60, SpinAntiClock 0.56, TogetherStep 0.55 | s 0.35, n 1.25, m_arm 1.8, m_torso 6, m_knee 0.7, torso_pitch 15, head_pitch -15 |
| P4 | 덩치 큰 사람처럼 걸어 | Heavyset | 0.21 | 28 | 4.88 | 9.8 | BentKnees 0.91, Roadrunner 0.75, Lunge 0.74 | c 30, stance_width 10 |
| P5 | 패션모델처럼 뽐내며 걸어 | Strutting | 0.58 | 2 | 1.34 | 2.9 | LookUp 0.66, Strutting 0.58, SpinClock 0.44 | s 1.4, m_arm 1.5, torso_pitch -15, head_pitch -15 |
| P6 | 특공대원처럼 총을 겨눈 자세로 걸어 | Swat | 0.18 | 29 | 0.86 | 5.3 | RaisedRightArm 0.85, Flapping 0.81, RaisedLeftArm 0.76 | m_arm 0.4, m_elbow 0, torso_pitch 15, head_pitch -15, shoulder_abduction 85 |
| F1 | 뒷짐을 지고 걸어 | ArmsBehindBack | 0.16 | 22 | 1.14 | 3.5 | WideLegs 0.65, LegsApart 0.64, Star 0.53 | torso_pitch 15, stance_width 10 |
| F2 | 팔짱을 끼고 걸어 | ArmsFolded | 0.41 | 17 | 1.13 | 5.0 | ArmsAboveHead 0.88, InTheDark 0.79, Zombie 0.73 | m_arm 0.4, shoulder_flexion 85 |
| F3 | 양손을 허리에 짚고 걸어 | Akimbo | -0.00 | 53 | 0.84 | 2.1 | InTheDark 0.82, Zombie 0.79, Swimming 0.68 | shoulder_flexion 30 |
| F4 | 두 팔을 머리 위로 들고 걸어 | ArmsAboveHead | 0.87 | 1 | 0.78 | 5.0 | ArmsAboveHead 0.87, InTheDark 0.79, Zombie 0.73 | m_arm 0, shoulder_flexion 85 |
| F5 | 발뒤꿈치로 걸어 | OnHeels | -0.58 | 99 | 0.44 | 1.3 | Kick 0.80, HighKnees 0.77, FlickLegs 0.74 | m_knee 1.3 |
| F6 | 무릎을 굽힌 채로 걸어 | BentKnees | 0.89 | 1 | 1.01 | 3.7 | BentKnees 0.89, Roadrunner 0.79, Chicken 0.71 | c 15 |
| F7 | 상체를 뒤로 젖히고 걸어 | LeanBack | 0.25 | 10 | 0.32 | 1.1 | LookUp 0.59, InTheDark 0.42, Strutting 0.36 | torso_pitch -15 |
| F8 | 발을 바닥에 끌면서 걸어 | SlideFeet | 0.20 | 16 | 0.93 | 2.8 | StartStop 0.64, FairySteps 0.57, Penguin 0.54 | s 0.6, n 0.75, m_knee 0.7 |
| M1 | 급하게 서둘러 걸어 | Rushed | 0.73 | 1 | 0.81 | 3.1 | Rushed 0.73, Followed 0.54, Drunk 0.53 | s 1.4, n 1.45, m_arm 1.8 |
| M2 | 누가 따라오는 것 같아 뒤를 살피며 걸어 | Followed | 0.20 | 30 | 0.76 | 2.5 | LeanRight 0.85, Depressed 0.84, Monk 0.78 | head_pitch 25 |
| M3 | 우아하게 걸어 | GracefulArms | 0.14 | 36 | 0.56 | 2.1 | Rushed 0.65, SwingShoulders 0.51, Strutting 0.44 | s 1.4, m_arm 1.5, m_torso 0, torso_pitch 15, head_pitch -15 |
| M4 | 외줄을 타듯 균형을 잡으며 걸어 | Balance | -0.14 | 88 | 1.65 | 9.5 | BentKnees 0.96, Lunge 0.78, Roadrunner 0.75 | c 30, m_torso 0, m_knee 0.8 |
| M5 | 엉덩이를 씰룩거리며 걸어 | WiggleHips | 0.35 | 25 | 0.82 | 3.3 | Followed 0.81, SpinClock 0.70, Old 0.67 | m_torso 10 |

점수를 낸 25개: 유사도 평균 0.26, 1위 3개, 5위 이내 5개, 순위 중앙값 22, 크기 평균 1.12
