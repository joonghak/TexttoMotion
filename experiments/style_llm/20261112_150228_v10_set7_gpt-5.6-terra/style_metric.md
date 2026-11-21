# 스타일 지표, 목표 동작 기준 (20261112_150228_v10_set7_gpt-5.6-terra, 프롬프트 v10)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 메추라기처럼 종종 걸어 | Quail | 0.70 | 2 | 1.41 | 4.7 | Chicken 0.72, Quail 0.70, BentKnees 0.67 | s 0.5, n 1.5, c 12, m_arm 0.3, m_knee 0.8, torso_pitch 15, shoulder_abduction -15, bounce 10 |
| N2 | 고릴라처럼 가슴을 두드리며 걸어 | BeatChest | 0.29 | 36 | 1.76 | 8.8 | Dinosaur 0.80, BentKnees 0.76, OnToesCrouched 0.73 | s 0.7, n 0.75, c 25, m_arm 1.6, m_torso 7, m_knee 0.8, torso_pitch 25, shoulder_flexion 35, elbow_flexion 60, stance_width 10, shoulder_rotation 45 |
| N3 | 펭귄 흉내를 내면서 걸어 | Penguin | 0.44 | 4 | 1.43 | 5.3 | LawnMower 0.53, Robot 0.50, ArmsFolded 0.45 | s 0.6, n 0.8, m_arm 0.3, m_torso 6, m_knee 0.7, shoulder_abduction -15, elbow_flexion 40, stance_width 10, toe_out 20 |
| N4 | 티라노사우루스처럼 걸어 | Dinosaur | 0.77 | 1 | 0.80 | 5.8 | Dinosaur 0.77, Swat 0.73, ShieldedRight 0.72 | s 1.5, n 0.75, c 12, m_arm 0, m_torso 5, m_knee 1.3, torso_pitch 20, shoulder_flexion 25, shoulder_abduction -15, elbow_flexion 60, stance_width 7, toe_out 15 |
| N5 | 수탉처럼 걸어 | Chicken | 0.43 | 7 | 1.08 | 6.2 | HighKnees 0.65, Kick 0.61, March 0.59 | s 0.7, n 1.2, c 15, m_arm 0.3, m_knee 1.5, torso_pitch -12, head_pitch -15, shoulder_abduction -15, stance_width 5, toe_out 25 |
| N6 | 고양이처럼 조심스럽게 걸어 | Cat | 0.52 | 13 | 1.76 | 7.8 | BentKnees 0.82, Dinosaur 0.76, OnToesCrouched 0.71 | s 0.6, n 0.75, c 25, m_arm 0.3, m_knee 0.7, torso_pitch 20, head_pitch 10, shoulder_flexion 20, elbow_flexion 40, stance_width -4 |
| P1 | 어둠 속에서 손으로 더듬으며 걸어 | InTheDark | 0.46 | 20 | 1.56 | 6.7 | ShieldedLeft 0.75, Dinosaur 0.75, ShieldedRight 0.73 | n 0.6, c 15, m_arm 0.3, m_knee 0.8, torso_pitch 15, head_pitch 20, shoulder_flexion 60, elbow_flexion 35 |
| P2 | 군인처럼 행진하며 걸어 | March | 0.52 | 7 | 1.68 | 5.1 | HighKnees 0.81, Kick 0.75, Roadrunner 0.68 | n 1.1, c 15, m_arm 1.5, m_torso 0, m_knee 1.5, m_elbow 0, elbow_flexion -20 |
| P3 | 요정처럼 사뿐사뿐 걸어 | FairySteps | 0.48 | 2 | 0.38 | 1.7 | Penguin 0.51, FairySteps 0.48, StartStop 0.48 | s 0.85, n 0.9, m_arm 0.5, m_torso 2, m_knee 0.7 |
| P4 | 덩치 큰 사람처럼 걸어 | Heavyset | 0.15 | 22 | 1.64 | 3.3 | WideLegs 0.72, LegsApart 0.72, Star 0.56 | s 1.25, n 0.8, m_arm 1.2, m_torso 5, stance_width 10 |
| P5 | 패션모델처럼 뽐내며 걸어 | Strutting | 0.44 | 5 | 1.40 | 3.1 | SpinClock 0.70, SpinAntiClock 0.67, LookUp 0.56 | s 1.4, n 0.9, m_arm 1.5, m_torso 5, torso_pitch -12, head_pitch -15 |
| P6 | 특공대원처럼 총을 겨눈 자세로 걸어 | Swat | 0.78 | 3 | 1.10 | 6.7 | ShieldedRight 0.81, ShieldedLeft 0.78, Swat 0.78 | c 15, m_arm 0.3, m_torso 0, m_knee 0.8, shoulder_flexion 85, elbow_flexion 20, stance_width 6, shoulder_rotation 30 |
| F1 | 뒷짐을 지고 걸어 | ArmsBehindBack | 0.68 | 5 | 0.89 | 2.7 | HandsInPockets 0.77, Akimbo 0.72, OnPhoneLeft 0.71 | shoulder_flexion -45, elbow_flexion 60 |
| F2 | 팔짱을 끼고 걸어 | ArmsFolded | 0.91 | 1 | 0.98 | 4.3 | ArmsFolded 0.91, LawnMower 0.84, OnPhoneLeft 0.78 | m_arm 0, shoulder_flexion 35, elbow_flexion 60, shoulder_rotation 60 |
| F3 | 양손을 허리에 짚고 걸어 | Akimbo | 0.73 | 2 | 1.11 | 2.8 | HandsInPockets 0.80, Akimbo 0.73, ArmsFolded 0.66 | m_arm 0.3, shoulder_flexion -25, shoulder_abduction 35, elbow_flexion 60, shoulder_rotation 45 |
| F4 | 두 팔을 머리 위로 들고 걸어 | ArmsAboveHead | 0.88 | 1 | 0.78 | 5.0 | ArmsAboveHead 0.88, InTheDark 0.79, Zombie 0.73 | m_arm 0.3, shoulder_flexion 85 |
| F5 | 발뒤꿈치로 걸어 | OnHeels | 0.51 | 3 | 0.35 | 1.1 | Stiff 0.57, LimpRight 0.53, OnHeels 0.51 | m_knee 0.7 |
| F6 | 무릎을 굽힌 채로 걸어 | BentKnees | 0.96 | 1 | 1.48 | 5.4 | BentKnees 0.96, Roadrunner 0.76, Lunge 0.74 | c 20, m_knee 0.8 |
| F7 | 상체를 뒤로 젖히고 걸어 | LeanBack | 0.25 | 10 | 0.32 | 1.1 | LookUp 0.59, InTheDark 0.42, Strutting 0.36 | torso_pitch -15 |
| F8 | 발을 바닥에 끌면서 걸어 | SlideFeet | 0.23 | 17 | 0.58 | 1.8 | Stiff 0.58, OnHeels 0.51, LimpRight 0.48 | m_knee 0.4 |
| M1 | 급하게 서둘러 걸어 | Rushed | 0.73 | 1 | 0.51 | 1.9 | Rushed 0.73, Followed 0.54, Drunk 0.54 | s 1.2, n 1.3, m_arm 1.5 |
| M2 | 누가 따라오는 것 같아 뒤를 살피며 걸어 | Followed | -0.33 | 94 | 1.13 | 3.7 | WalkingStickRight 0.74, BeatChest 0.61, WiggleHips 0.57 | n 0.6, m_arm 0.3, m_knee 0.8, torso_pitch 10, head_pitch -15, shoulder_flexion 20, elbow_flexion 40 |
| M3 | 우아하게 걸어 | GracefulArms | -0.03 | 44 | 0.47 | 1.8 | LookUp 0.65, Strutting 0.41, SpinClock 0.28 | s 1.2, n 0.9, m_arm 0.8, torso_pitch -10, head_pitch -10 |
| M4 | 외줄을 타듯 균형을 잡으며 걸어 | Balance | 0.76 | 3 | 1.08 | 6.2 | RaisedRightArm 0.79, Flapping 0.76, Balance 0.76 | s 0.7, n 0.65, m_arm 0.3, m_torso 0, m_knee 0.7, shoulder_abduction 80, elbow_flexion -15, stance_width -8, toe_out -10 |
| M5 | 엉덩이를 씰룩거리며 걸어 | WiggleHips | 0.35 | 25 | 0.82 | 3.3 | Followed 0.81, SpinClock 0.70, Old 0.67 | m_torso 10 |

점수를 낸 25개: 유사도 평균 0.50, 1위 5개, 5위 이내 14개, 순위 중앙값 5, 크기 평균 1.06
