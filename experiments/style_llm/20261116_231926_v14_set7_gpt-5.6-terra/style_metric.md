# 스타일 지표, 목표 동작 기준 (20261116_231926_v14_set7_gpt-5.6-terra, 프롬프트 v14)

학습 없이, 생성한 값의 목표 동작(보상이 요구하는 동작)을 100STYLE과 비교한 값이다. 학습한 정책은 목표를 대부분 따르므로 이 값과 비슷하게 나온다(기존 걷기 정책 10개에서 유사도 상관 0.90).

| ID | 명령 | 목표 | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 | 값 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | 메추라기처럼 종종 걸어 | Quail | 0.53 | 4 | 1.09 | 3.6 | LeftHop 0.63, RightHop 0.62, TwoFootJump 0.58 | s 0.45, n 1.5, m_arm 0.2, m_knee 0.75, torso_pitch 12, shoulder_abduction -15, bounce 15 |
| N2 | 고릴라처럼 가슴을 두드리며 걸어 | BeatChest | 0.33 | 35 | 1.61 | 8.0 | ShieldedLeft 0.72, Dinosaur 0.72, Swat 0.70 | s 0.7, n 0.75, c 20, m_arm 1.5, m_torso 6, m_knee 0.8, torso_pitch 25, head_pitch 15, shoulder_flexion 45, elbow_flexion 60, stance_width 10, shoulder_rotation 60 |
| N3 | 펭귄 흉내를 내면서 걸어 | Penguin | 0.34 | 10 | 1.23 | 4.6 | Crouched 0.53, LeftHop 0.47, OnToesCrouched 0.46 | s 0.65, n 0.8, c 10, m_arm 0.4, m_torso 7, m_knee 0.7, shoulder_abduction -15, stance_width 10, toe_out 25 |
| N4 | 티라노사우루스처럼 걸어 | Dinosaur | 0.60 | 5 | 0.88 | 6.5 | ShieldedLeft 0.65, March 0.65, Swat 0.63 | s 0.75, n 0.8, c 12, m_arm 0, m_knee 1.3, torso_pitch 20, head_pitch 15, shoulder_flexion 35, elbow_flexion 60, stance_width 8 |
| N5 | 수탉처럼 걸어 | Chicken | 0.45 | 7 | 1.12 | 6.4 | HighKnees 0.67, Kick 0.63, FlickLegs 0.56 | s 0.65, n 1.25, c 15, m_arm 0.3, m_torso 5, m_knee 1.5, torso_pitch -10, head_pitch -15, shoulder_abduction -15, toe_out 25 |
| N6 | 고양이처럼 조심스럽게 걸어 | Cat | 0.43 | 18 | 1.36 | 6.0 | Dinosaur 0.74, Chicken 0.67, BentKnees 0.66 | s 0.65, n 0.7, c 20, m_arm 0.3, m_knee 0.7, torso_pitch 20, shoulder_flexion 20, elbow_flexion 40, stance_width -5, foot_pitch 20 |
| P1 | 어둠 속에서 손으로 더듬으며 걸어 | InTheDark | 0.47 | 19 | 1.45 | 6.2 | ShieldedLeft 0.71, ShieldedRight 0.69, Dinosaur 0.68 | s 0.7, n 0.6, c 15, m_arm 0.3, m_knee 0.75, torso_pitch 15, head_pitch 15, shoulder_flexion 55, elbow_flexion 35 |
| P2 | 군인처럼 행진하며 걸어 | March | 0.53 | 1 | 0.82 | 2.5 | March 0.53, HighKnees 0.46, Kick 0.42 | s 1.1, n 1.05, m_arm 0.35, m_torso 0, m_knee 1.35, m_elbow 0, torso_pitch -3, head_pitch -8, elbow_flexion 20 |
| P3 | 요정처럼 사뿐사뿐 걸어 | FairySteps | 0.11 | 43 | 0.62 | 2.7 | PendulumHands 0.50, RightHop 0.49, LeftHop 0.49 | s 0.75, n 0.9, m_arm 0.5, m_knee 0.7, torso_pitch -5, head_pitch -8, shoulder_abduction 20, elbow_flexion 20, bounce 8 |
| P4 | 덩치 큰 사람처럼 걸어 | Heavyset | 0.20 | 38 | 1.90 | 3.8 | LegsApart 0.58, WideLegs 0.57, Lunge 0.46 | s 1.3, n 0.75, m_arm 1.2, m_torso 5, m_knee 0.8, stance_width 10, bounce 12 |
| P5 | 패션모델처럼 뽐내며 걸어 | Strutting | 0.73 | 1 | 1.43 | 3.1 | Strutting 0.73, LookUp 0.56, WideLegs 0.45 | s 1.4, n 0.9, m_arm 1.4, torso_pitch -15, head_pitch -15, stance_width 4, toe_out 12 |
| P6 | 특공대원처럼 총을 겨눈 자세로 걸어 | Swat | 0.63 | 11 | 0.86 | 5.2 | ArmsAboveHead 0.92, InTheDark 0.75, Zombie 0.68 | m_arm 0.3, shoulder_flexion 85, elbow_flexion 15, shoulder_rotation 25 |
| F1 | 뒷짐을 지고 걸어 | ArmsBehindBack | 0.69 | 3 | 0.98 | 3.0 | HandsInPockets 0.77, Akimbo 0.69, ArmsBehindBack 0.69 | m_arm 0.3, shoulder_flexion -45, elbow_flexion 60 |
| F2 | 팔짱을 끼고 걸어 | ArmsFolded | 0.91 | 1 | 0.96 | 4.2 | ArmsFolded 0.91, LawnMower 0.83, OnPhoneLeft 0.78 | m_arm 0, shoulder_flexion 30, elbow_flexion 60, shoulder_rotation 60 |
| F3 | 양손을 허리에 짚고 걸어 | Akimbo | 0.73 | 2 | 1.11 | 2.8 | HandsInPockets 0.80, Akimbo 0.73, ArmsFolded 0.66 | m_arm 0.3, shoulder_flexion -25, shoulder_abduction 35, elbow_flexion 60, shoulder_rotation 45 |
| F4 | 두 팔을 머리 위로 들고 걸어 | ArmsAboveHead | 0.89 | 1 | 0.97 | 6.3 | ArmsAboveHead 0.89, OnPhoneLeft 0.59, OnPhoneRight 0.55 | m_arm 0.3, shoulder_abduction 155 |
| F5 | 발뒤꿈치로 걸어 | OnHeels | -0.02 | 67 | 0.17 | 0.5 | BouncyRight 0.81, BouncyLeft 0.81, TwoFootJump 0.67 | foot_pitch -20 |
| F6 | 무릎을 굽힌 채로 걸어 | BentKnees | 0.97 | 1 | 1.49 | 5.5 | BentKnees 0.97, Lunge 0.75, Roadrunner 0.74 | c 20, m_knee 0.75 |
| F7 | 상체를 뒤로 젖히고 걸어 | LeanBack | 0.25 | 10 | 0.32 | 1.1 | LookUp 0.59, InTheDark 0.42, Strutting 0.36 | torso_pitch -15 |
| F8 | 발을 바닥에 끌면서 걸어 | SlideFeet | 0.23 | 17 | 0.58 | 1.8 | Stiff 0.58, OnHeels 0.51, LimpRight 0.48 | m_knee 0.4 |
| M1 | 급하게 서둘러 걸어 | Rushed | 0.72 | 1 | 0.43 | 1.6 | Rushed 0.72, Followed 0.54, Drunk 0.53 | s 1.1, n 1.35, m_arm 1.4 |
| M2 | 누가 따라오는 것 같아 뒤를 살피며 걸어 | Followed | -0.40 | 88 | 0.41 | 1.3 | ArmsBySide 0.37, FairySteps 0.33, SlideFeet 0.32 | n 0.8, m_arm 0.5, head_yaw 60 |
| M3 | 우아하게 걸어 | GracefulArms | 0.23 | 24 | 0.55 | 2.1 | BeatChest 0.64, WalkingStickRight 0.58, HandsInPockets 0.54 | s 1.2, n 0.9, m_arm 0.8, m_torso 0.5, torso_pitch -8, head_pitch -8, elbow_flexion 25 |
| M4 | 외줄을 타듯 균형을 잡으며 걸어 | Balance | 0.61 | 5 | 1.27 | 7.3 | Teapot 0.74, RaisedLeftArm 0.65, RaisedRightArm 0.64 | s 0.7, n 0.6, c 15, m_arm 0.3, m_knee 0.7, torso_pitch 15, head_pitch 25, shoulder_abduction 80, stance_width -8 |
| M5 | 엉덩이를 씰룩거리며 걸어 | WiggleHips | 0.20 | 28 | 0.77 | 3.1 | LegsApart 0.63, WideLegs 0.59, Followed 0.53 | n 0.85, m_torso 8, stance_width 6 |

점수를 낸 25개: 유사도 평균 0.45, 1위 6개, 5위 이내 11개, 순위 중앙값 10, 크기 평균 0.98
