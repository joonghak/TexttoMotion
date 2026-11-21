# 파라미터로 닿을 수 있는 100STYLE 스타일 (무작위 1500개, 목표 동작 기준)

가장 높은 유사도 순서이다. 주요 특징은 그 스타일이 Neutral에서 가장 크게 바뀐 특징(같은 단위)이다.

| 스타일 | 최고 유사도 | 주요 특징 | 그때의 값 |
| --- | --- | --- | --- |
| BentKnees | 0.96 | pelvis_height -2.8, knee_bend +2.3, arm_swing -0.4, hand_forward -0.4 | s 1.63, n 0.64, c 25.31, m_arm 0.16, m_knee 0.72, m_elbow 0.88, torso_pitch -9.85, head_pitch 1.57, elbow_flexion -6.14, stance_width 0.8, toe_out -2.78 |
| RaisedRightArm | 0.93 | hand_out +2.0, hand_height +1.1, toe_out -0.7, torso_lean +0.3 | shoulder_abduction 36.5, toe_out -2.38 |
| RaisedLeftArm | 0.92 | hand_out +2.2, hand_height +1.1, toe_out -0.7, head_pitch +0.5 | shoulder_abduction 36.5, toe_out -2.38 |
| OnPhoneRight | 0.91 | elbow_bend +2.0, hand_height +1.7, toe_out +0.8, hand_out -0.7 | m_elbow 0.65, torso_pitch 7.5, head_pitch 1.73, elbow_flexion 59.38, toe_out 16.19 |
| ArmsFolded | 0.91 | hand_out -2.7, elbow_bend +2.5, hand_height +1.6, toe_out +1.0 | m_elbow 0.65, torso_pitch 7.5, head_pitch 1.73, elbow_flexion 59.38, toe_out 16.19 |
| LeanRight | 0.90 | head_pitch +3.2, toe_out -1.0, head_sway +0.8, pelvis_sway +0.7 | s 0.97, n 1.45, m_knee 0.94, head_pitch 19.31, toe_out -2.98 |
| Zombie | 0.89 | hand_forward +4.3, hand_height +2.2, head_sway +2.1, cadence -1.5 | s 1.72, n 0.63, m_torso 9.15, m_knee 0.59, torso_pitch 15.79, shoulder_flexion 75.69, elbow_flexion -8.59 |
| LawnMower | 0.89 | elbow_bend +2.4, hand_out -2.0, hand_forward +1.7, hand_height +1.4 | n 0.98, c 1.96, m_knee 0.79, m_elbow 0.36, torso_pitch 15.52, elbow_flexion 51.8, toe_out -1.25 |
| HighKnees | 0.89 | foot_lift +4.2, knee_bend +1.8, toe_out -1.0, head_sway +0.6 | c 10.58, m_torso 0.41, m_knee 1.44, m_elbow 0.85, head_pitch 6.01 |
| ArmsAboveHead | 0.88 | hand_height +5.8, hand_forward +2.3, elbow_bend +1.0, stance_width -0.6 | s 1.14, n 0.76, c 6.66, m_elbow 0.49, shoulder_flexion 74.95, elbow_flexion 51.66 |
| SwingArmsRound | 0.88 | arm_swing +2.9, cadence -1.1, hand_out -0.9, hand_height +0.7 | n 0.88, m_arm 1.76, m_torso 0.36, m_elbow 0.12 |
| Balance | 0.88 | hand_out +3.6, head_sway +2.1, torso_side +1.8, hand_height +1.7 | s 0.77, n 0.98, c 3.06, m_torso 8.51, m_knee 0.86, m_elbow 0.69, head_pitch 10.96, shoulder_abduction 42.73 |
| Flapping | 0.88 | hand_out +3.0, hand_height +2.3, toe_out -1.0, arm_swing +0.7 | shoulder_abduction 36.5, toe_out -2.38 |
| Monk | 0.88 | head_pitch +3.5, cadence -1.8, hand_out -1.2, step_length +1.1 | n 0.93, m_elbow 0.18, head_pitch 28.66, shoulder_abduction -4.01, elbow_flexion 30.91, toe_out 7.35 |
| Star | 0.88 | stance_width +4.5, pelvis_sway +4.1, hand_out +3.7, toe_out +2.5 | s 1.45, n 1.36, torso_pitch -4.48, shoulder_abduction 32.53, stance_width 9.53 |
| Swat | 0.88 | elbow_bend +3.3, hand_height +2.7, hand_forward +2.2, pelvis_height -2.0 | s 1.2, c 8.3, m_arm 1.64, shoulder_abduction 27.28, elbow_flexion 59.91 |
| Aeroplane | 0.87 | head_sway +3.4, hand_out +3.4, torso_side +2.1, hand_height +1.7 | s 0.77, n 0.98, c 3.06, m_torso 8.51, m_knee 0.86, m_elbow 0.69, head_pitch 10.96, shoulder_abduction 42.73 |
| Teapot | 0.87 | hand_out +2.2, hand_height +1.8, head_pitch +1.3, elbow_bend +1.3 | m_torso 0.47, m_knee 0.94, torso_pitch -4.23, head_pitch 28.3, shoulder_abduction 84.76, elbow_flexion -6.2, toe_out 8.28 |
| OnPhoneLeft | 0.87 | elbow_bend +2.1, hand_height +1.8, hand_out -0.8, head_pitch +0.4 | n 1.04, m_elbow 0.18, head_pitch 12.17, shoulder_abduction 10.98, elbow_flexion 59.39 |
| Superman | 0.87 | head_pitch +3.1, hand_height +2.2, torso_lean +1.0, pelvis_sway +0.8 | s 0.97, n 1.21, c 3.27, m_knee 0.98, m_elbow 0.88, torso_pitch 26.94, head_pitch 29.29, shoulder_abduction 60.5, elbow_flexion 42.35, stance_width 5.62 |
| ShieldedRight | 0.86 | elbow_bend +2.6, hand_height +2.4, pelvis_height -2.0, hand_forward +2.0 | s 1.2, c 8.3, m_arm 1.64, shoulder_abduction 27.28, elbow_flexion 59.91 |
| Dinosaur | 0.86 | pelvis_height -3.8, elbow_bend +3.2, knee_bend +3.1, cadence -1.9 | s 1.29, n 0.75, c 10.59, m_knee 0.85, m_elbow 0.57, shoulder_flexion 23.2, elbow_flexion 42.55, stance_width 0.51 |
| Roadrunner | 0.86 | knee_bend +3.3, pelvis_height -2.9, torso_lean +2.2, hand_forward -1.8 | s 0.99, c 20.57, m_torso 2.36, m_knee 0.83, torso_pitch 37.33, head_pitch -13.38 |
| StartStop | 0.85 | head_pitch +1.6, pelvis_sway -1.6, head_sway +1.1, foot_lift -1.0 | s 0.55, m_arm 0.95, m_torso 8.45, m_knee 0.74, torso_pitch 22.2, head_pitch 10.75, toe_out -5.2 |
| Kick | 0.84 | foot_lift +3.4, cadence -1.1, knee_bend +0.8, pelvis_sway -0.8 | n 0.9, c 5.93, m_knee 1.34, m_elbow 0.71, torso_pitch 15.34, head_pitch -8.57, shoulder_flexion 4.17, toe_out 2.31 |
| WildArms | 0.84 | arm_swing +4.4, hand_height +2.7, hand_forward +0.8, torso_side +0.7 | n 0.88, m_arm 1.76, m_torso 0.36, m_elbow 0.12 |
| Depressed | 0.84 | head_pitch +3.1, head_sway +1.0, pelvis_height +0.8, torso_lean +0.7 | n 1.3, m_torso 1.24, torso_pitch 28.64, head_pitch 26.31 |
| InTheDark | 0.83 | hand_forward +3.2, hand_height +2.0, step_length -1.2, pelvis_sway +0.8 | n 1.41, m_arm 0.96, m_knee 0.72, shoulder_flexion 71.15, elbow_flexion -17.68, toe_out 15.08 |
| LeanLeft | 0.83 | head_pitch +2.3, toe_out -1.3, torso_lean +0.9, knee_bend +0.8 | n 1.22, m_torso 3.17, m_knee 1.22, m_elbow 0.81, head_pitch 25.23, elbow_flexion -2.91, stance_width 1, toe_out -16.55 |
| LegsApart | 0.83 | stance_width +4.6, pelvis_sway +4.1, head_sway +3.0, toe_out +2.0 | s 1.52, n 1.07, m_torso 6.71, head_pitch -5.53, shoulder_abduction 14, stance_width 5.63 |
| OnToesCrouched | 0.82 | knee_bend +2.6, pelvis_height -2.4, torso_lean +1.9, head_sway +1.7 | c 12.57, m_arm 1.11, m_torso 9.95, m_knee 0.59, shoulder_abduction 3.87, elbow_flexion 37.24 |
| Chicken | 0.82 | knee_bend +3.1, torso_lean +2.5, pelvis_height -2.5, elbow_bend +1.7 | s 0.99, c 20.57, m_torso 2.36, m_knee 0.83, torso_pitch 37.33, head_pitch -13.38 |
| Followed | 0.82 | head_sway +2.5, toe_out +1.0, pelvis_sway +1.0, arm_swing +0.9 | s 1.48, m_arm 1.26, m_torso 7.62, m_knee 0.87, m_elbow 0.13, shoulder_flexion 4.74, elbow_flexion -27.81 |
| ShieldedLeft | 0.82 | elbow_bend +2.6, hand_height +2.4, hand_forward +2.3, pelvis_height -2.0 | c 15.09, m_arm 0.56, m_torso 1.5, m_knee 0.49, m_elbow 0.59, head_pitch 1.33, shoulder_flexion 24.34, elbow_flexion 42.85, stance_width 4.61, toe_out 11.12 |
| BeatChest | 0.81 | elbow_bend +3.9, hand_height +2.6, hand_forward +1.2, toe_out +0.6 | n 1.04, m_elbow 0.18, head_pitch 12.17, shoulder_abduction 10.98, elbow_flexion 59.39 |
| WideLegs | 0.81 | stance_width +4.8, pelvis_sway +4.0, head_sway +2.4, toe_out +1.9 | s 1.31, torso_pitch -4.53, stance_width 3.56 |
| PendulumHands | 0.81 | elbow_bend +1.9, step_length -1.7, knee_bend +1.4, hand_out +1.3 | s 0.59, n 1.28, c 16.97, m_arm 1.28, m_knee 0.41, m_elbow 0.57, torso_pitch 30.52, head_pitch 0.52, shoulder_abduction 36.31, elbow_flexion 39.09, toe_out 2 |
| Lunge | 0.80 | pelvis_height -3.9, bounce +2.9, knee_bend +1.5, cadence -1.1 | s 1.33, n 0.55, c 26.23, m_torso 1.72, toe_out -4.7 |
| WildLegs | 0.80 | cadence -2.1, foot_lift +1.8, head_sway +1.4, toe_out +1.1 | s 1.59, n 0.66, m_arm 1.34, m_knee 1.29, torso_pitch -4.63, stance_width 2.78 |
| Crouched | 0.80 | pelvis_height -2.0, torso_lean +1.9, knee_bend +1.9, head_sway +1.8 | c 12.57, m_arm 1.11, m_torso 9.95, m_knee 0.59, shoulder_abduction 3.87, elbow_flexion 37.24 |
| CrowdAvoidance | 0.80 | head_sway +1.7, arm_swing +1.7, head_pitch +1.4, torso_side +0.5 | m_arm 1.13, m_torso 7.76, torso_pitch 20.51, shoulder_flexion 10.32, elbow_flexion -5.78, toe_out -0.21 |
| Sweep | 0.80 | head_sway +4.1, torso_side +4.0, torso_lean +3.9, head_pitch +3.0 | m_arm 1.13, m_torso 7.76, torso_pitch 20.51, shoulder_flexion 10.32, elbow_flexion -5.78, toe_out -0.21 |
| Waving | 0.80 | arm_swing +1.3, head_sway +0.6, stance_width -0.5, elbow_bend +0.5 | n 0.88, m_arm 1.76, m_torso 0.36, m_elbow 0.12 |
| BentForward | 0.79 | torso_lean +2.7, head_pitch +1.9, torso_side +1.5, head_sway +1.5 | c 2.93, m_arm 0.15, m_torso 7.58, torso_pitch 28.25, elbow_flexion 18.6 |
| LimpLeft | 0.78 | head_sway +1.0, foot_lift -0.8, toe_out +0.7, stance_width -0.5 | s 0.92, m_torso 6.43, m_knee 0.53, m_elbow 0.4, shoulder_abduction -10.96, toe_out 24.51 |
| March | 0.78 | elbow_bend +1.8, foot_lift +1.5, knee_bend +1.4, hand_height +0.9 | s 1.2, c 8.3, m_arm 1.64, shoulder_abduction 27.28, elbow_flexion 59.91 |
| Old | 0.78 | head_sway +3.8, torso_side +2.6, head_pitch +2.5, cadence -1.9 | m_arm 0.79, m_torso 9.38, m_knee 0.76, torso_pitch 13.66, head_pitch 8.02, shoulder_flexion 7.77, toe_out 11.11 |
| FlickLegs | 0.78 | foot_lift +4.4, cadence -1.9, stance_width +1.7, knee_bend +1.5 | s 1.37, n 0.66, m_arm 1.02, m_torso 5.18, m_knee 1.44, torso_pitch 12.06, head_pitch 1.1, shoulder_flexion 25.55, stance_width 7.21 |
| SpinClock | 0.77 | head_sway +3.2, head_pitch -2.1, arm_swing +2.1, torso_side +1.3 | n 1.32, m_torso 9.39, m_knee 0.44, m_elbow 0.89, head_pitch -14.09, stance_width 0.3 |
| WalkingStickLeft | 0.76 | elbow_bend +0.9, head_pitch +0.6, hand_forward +0.5, stance_width -0.4 | n 1.04, m_elbow 0.18, head_pitch 12.17, shoulder_abduction 10.98, elbow_flexion 59.39 |
| Quail | 0.75 | knee_bend +1.6, step_length -1.5, pelvis_height -1.4, torso_lean +1.2 | s 0.59, n 1.28, c 16.97, m_arm 1.28, m_knee 0.41, m_elbow 0.57, torso_pitch 30.52, head_pitch 0.52, shoulder_abduction 36.31, elbow_flexion 39.09, toe_out 2 |
| SpinAntiClock | 0.75 | head_sway +2.2, head_pitch -1.6, arm_swing +1.6, foot_lift -1.1 | n 1.32, m_torso 9.39, m_knee 0.44, m_elbow 0.89, head_pitch -14.09, stance_width 0.3 |
| WhirlArms | 0.75 | arm_swing +4.2, hand_height +2.5, torso_side +1.9, cadence -1.6 | n 0.88, m_arm 1.76, m_torso 0.36, m_elbow 0.12 |
| Robot | 0.74 | step_length -2.8, elbow_bend +2.4, foot_lift -1.1, hand_height +1.0 | s 0.33, m_elbow 0.83, head_pitch 6.27, shoulder_abduction 2.67, elbow_flexion 54.16, toe_out 6.39 |
| Rocket | 0.74 | torso_lean +3.1, hand_forward -2.5, hand_height +2.4, head_pitch +1.4 | n 1.15, c 1.26, m_knee 0.86, m_elbow 0.63, torso_pitch 33.9, elbow_flexion -12.32, toe_out 8.74 |
| DuckFoot | 0.74 | toe_out +3.6, cadence -1.6, head_sway +1.4, pelvis_sway +1.2 | s 1.55, m_torso 1.07, m_knee 0.47, m_elbow 0.1, torso_pitch 8.68, head_pitch -12.7, elbow_flexion -14.18, stance_width 7.95, toe_out 29.63 |
| Swimming | 0.74 | hand_forward +2.8, hand_height +2.1, elbow_bend +1.6, arm_swing +1.6 | n 0.84, m_arm 1.65, m_torso 0.78, torso_pitch 4.06, head_pitch -0.99, shoulder_flexion 42.95 |
| GracefulArms | 0.73 | hand_height +2.2, elbow_bend +2.0, arm_swing +1.5, hand_out +1.4 | n 1.01, shoulder_abduction 16.99, elbow_flexion 26.63 |
| Strutting | 0.73 | toe_out +1.2, head_pitch -1.1, pelvis_sway +0.8, stance_width +0.5 | s 1.55, m_torso 1.07, m_knee 0.47, m_elbow 0.1, torso_pitch 8.68, head_pitch -12.7, elbow_flexion -14.18, stance_width 7.95, toe_out 29.63 |
| Angry | 0.73 | head_pitch +1.7, arm_swing +1.2, toe_out +0.8, bounce +0.8 | s 1.54, n 1.01, m_arm 1.74, m_knee 0.69, head_pitch 25.89, toe_out 23.95 |
| HandsInPockets | 0.73 | elbow_bend +1.6, arm_swing -0.5, stance_width -0.5, toe_out -0.5 | n 0.98, c 1.96, m_knee 0.79, m_elbow 0.36, torso_pitch 15.52, elbow_flexion 51.8, toe_out -1.25 |
| Punch | 0.72 | elbow_bend +2.7, hand_height +2.6, hand_forward +1.9, arm_swing +1.5 | s 1.14, n 0.76, c 6.66, m_elbow 0.49, shoulder_flexion 74.95, elbow_flexion 51.66 |
| FairySteps | 0.72 | toe_out -3.1, pelvis_sway -1.5, cadence -1.3, head_pitch +1.2 | n 0.7, m_arm 1.09, m_knee 0.56, head_pitch 27.62, stance_width 0.82, toe_out -17.69 |
| PigeonToed | 0.72 | toe_out -3.2, head_sway +2.3, cadence -1.4, arm_swing +1.3 | m_torso 7.36, m_knee 0.81, head_pitch -0.39, shoulder_abduction 34.21, elbow_flexion 8.48, toe_out -15.93 |
| OnToesBentForward | 0.72 | torso_lean +3.5, torso_side +2.1, head_sway +2.0, knee_bend +1.4 | n 1.12, c 0.2, m_arm 0.49, m_torso 9.54, torso_pitch 28.43, shoulder_flexion 2.29, elbow_flexion 22.89 |
| WalkingStickRight | 0.72 | elbow_bend +0.8, hand_forward +0.7, hand_height +0.4, pelvis_sway -0.3 | s 1.14, n 0.76, c 6.66, m_elbow 0.49, shoulder_flexion 74.95, elbow_flexion 51.66 |
| Drunk | 0.71 | arm_swing +2.4, head_sway +1.6, torso_side +1.0, head_pitch +1.0 | s 1.13, n 1.4, m_arm 1.65, m_torso 7.59, m_elbow 0.57, torso_pitch 10.89, head_pitch 23.18, shoulder_flexion 15.65, stance_width 5.57, toe_out 1.92 |
| Akimbo | 0.71 | elbow_bend +2.0, toe_out +0.9, hand_height +0.7, torso_lean +0.5 | m_elbow 0.65, torso_pitch 7.5, head_pitch 1.73, elbow_flexion 59.38, toe_out 16.19 |
| WiggleHips | 0.71 | elbow_bend +2.1, cadence -2.1, head_sway +1.2, step_length +1.0 | n 0.74, m_torso 7.59, torso_pitch -10.66, head_pitch 4.17, shoulder_abduction -0.77, elbow_flexion 59.02 |
| SlideFeet | 0.70 | cadence -2.0, step_length +1.0, foot_lift -0.9, head_pitch +0.9 | s 1.44, n 0.61, m_arm 0.64, m_torso 6.53, m_knee 0.84, head_pitch 24.84, shoulder_abduction 4.13 |
| BigSteps | 0.70 | pelvis_height -2.9, bounce +2.4, step_length +1.2, knee_bend +0.7 | s 1.62, c 27.5, m_arm 1.08, m_torso 1.77, m_knee 0.47, m_elbow 0.85, toe_out 27.58 |
| Rushed | 0.70 | arm_swing +2.0, pelvis_sway +1.6, pelvis_height -1.4, knee_bend +1.1 | s 1.59, m_arm 1.76, m_knee 0.85, m_elbow 1, torso_pitch -0.8, elbow_flexion -2.73 |
| Skip | 0.70 | bounce +3.6, foot_lift +2.8, knee_bend +1.9, arm_swing +1.2 | n 0.9, c 5.93, m_knee 1.34, m_elbow 0.71, torso_pitch 15.34, head_pitch -8.57, shoulder_flexion 4.17, toe_out 2.31 |
| KarateChop | 0.69 | elbow_bend +2.9, hand_height +2.3, hand_forward +1.8, arm_swing +1.7 | s 1.14, n 0.76, c 6.66, m_elbow 0.49, shoulder_flexion 74.95, elbow_flexion 51.66 |
| ArmsBySide | 0.69 | stance_width -0.7, toe_out +0.6, arm_swing -0.5, hand_out -0.4 | s 0.95, m_arm 0.16, m_torso 1.12, toe_out 20.19 |
| LimpRight | 0.68 | foot_lift -1.0, head_sway +0.8, torso_lean +0.5, torso_side +0.4 | n 1.32, m_torso 9.39, m_knee 0.44, m_elbow 0.89, head_pitch -14.09, stance_width 0.3 |
| Elated | 0.68 | arm_swing +3.0, bounce +2.6, hand_height +1.2, elbow_bend +1.0 | n 1.04, c 1.04, m_arm 1.65, m_knee 1.02, shoulder_flexion 2.74, stance_width 1.38 |
| LeftHop | 0.68 | knee_bend +3.8, elbow_bend +3.1, bounce +2.4, step_length -2.3 | s 0.3, c 14.97, m_arm 0.52, m_knee 0.55, torso_pitch 27.79, head_pitch -6.99, shoulder_flexion 62.02, elbow_flexion 53.61, stance_width 7, toe_out 22.03 |
| CrossOver | 0.68 | toe_out -3.0, cadence -2.0, step_length +1.3, head_pitch +1.3 | n 0.7, m_arm 1.09, m_knee 0.56, head_pitch 27.62, stance_width 0.82, toe_out -17.69 |
| HandsBetweenLegs | 0.67 | torso_side +8.4, torso_lean +5.7, pelvis_sway +4.5, stance_width +3.7 | c 9.54, m_torso 8.7, m_knee 0.87, torso_pitch 36.19, head_pitch -8.49, shoulder_flexion 40.29, shoulder_abduction -3.73, elbow_flexion -23.07, stance_width 8.34, toe_out 1.91 |
| SwingShoulders | 0.67 | arm_swing +2.5, cadence -1.7, step_length +1.5, elbow_bend +1.3 | n 0.88, m_arm 1.76, m_torso 0.36, m_elbow 0.12 |
| Penguin | 0.67 | step_length -2.9, foot_lift -1.8, toe_out +0.9, knee_bend -0.8 | s 0.47, n 1.18, m_arm 0.41, m_torso 0.22, m_knee 0.54, m_elbow 0.2, shoulder_abduction 6.57 |
| Cat | 0.66 | pelvis_height -1.9, step_length +1.9, cadence -1.9, arm_swing +1.6 | n 0.6, c 14.97, m_arm 1.27, m_knee 0.85, m_elbow 0.65, head_pitch 23.11, stance_width 0.05 |
| RightHop | 0.66 | elbow_bend +2.8, knee_bend +2.4, step_length -2.2, bounce +2.0 | s 0.5, n 1.26, c 9.5, m_arm 1.25, m_knee 0.63, m_elbow 0.74, head_pitch 16.53, elbow_flexion 29.93 |
| Tiptoe | 0.66 | toe_out -0.7, knee_bend +0.5, step_length -0.4, foot_lift -0.3 | s 0.6, n 1.22, m_arm 0.83, m_knee 0.93, m_elbow 0.15, toe_out -19.39 |
| Heavyset | 0.64 | elbow_bend +1.5, hand_out +0.7, pelvis_sway +0.5, hand_height +0.5 | s 1.2, c 8.3, m_arm 1.64, shoulder_abduction 27.28, elbow_flexion 59.91 |
| LeanBack | 0.61 | torso_lean -1.7, knee_bend +1.4, torso_side +1.4, pelvis_height -1.3 | n 1.37, c 27.13, m_arm 0.94, m_torso 8.98, m_knee 0.49, head_pitch -9.42 |
| Proud | 0.59 | arm_swing +1.0, elbow_bend +0.9, toe_out -0.5, bounce +0.4 | n 0.88, m_arm 1.76, m_torso 0.36, m_elbow 0.12 |
| Stiff | 0.58 | foot_lift -1.3, knee_bend -1.0, step_length -0.8, arm_swing +0.6 | s 0.82, m_torso 1.96, m_knee 0.45, torso_pitch 21.22, shoulder_flexion 29.92, elbow_flexion -27.71, stance_width 1.36 |
| Morris | 0.56 | bounce +2.8, elbow_bend +2.2, hand_height +1.6, toe_out -1.3 | n 1.19, m_torso 1.9, m_elbow 0.2, shoulder_abduction 79.61, elbow_flexion 59.64, toe_out -16.15 |
| OnHeels | 0.55 | foot_lift -1.6, step_length -1.3, knee_bend -1.3, arm_swing +0.9 | s 0.82, m_torso 1.96, m_knee 0.45, torso_pitch 21.22, shoulder_flexion 29.92, elbow_flexion -27.71, stance_width 1.36 |
| TwoFootJump | 0.54 | bounce +5.8, knee_bend +2.3, step_length -2.1, cadence +1.9 | s 0.56, n 1.23, c 17.65, m_arm 1.31, m_torso 1.91, torso_pitch 34.44, head_pitch 16.33, shoulder_flexion 14.91, elbow_flexion -0.31, toe_out 5.61 |
| LookUp | 0.54 | head_pitch -2.1, step_length -0.9, torso_lean -0.8, pelvis_sway +0.7 | m_arm 0.51, m_elbow 0.17, torso_pitch -9.61, head_pitch -14.32, toe_out -17.29 |
| TogetherStep | 0.53 | step_length -3.5, cadence +3.2, head_sway +1.8, arm_swing +1.5 | s 0.62, n 1.24, m_arm 1.42, m_torso 4.52, head_pitch 24.33 |
| ArmsBehindBack | 0.49 | hand_forward -1.7, hand_out -1.6, toe_out -1.5, arm_swing -0.9 | m_arm 0.31, m_torso 2.65, m_elbow 0.93, torso_pitch 16.25, head_pitch -12.11, stance_width 3.35, toe_out -5.46 |
| DragLeftLeg | 0.46 | step_length -2.8, cadence +2.1, foot_lift -1.2, head_pitch +0.9 | s 0.97, n 1.45, m_knee 0.94, head_pitch 19.31, toe_out -2.98 |
| DragRightLeg | 0.40 | step_length -2.9, cadence +2.1, foot_lift -1.4, stance_width -1.0 | s 0.92, m_torso 6.43, m_knee 0.53, m_elbow 0.4, shoulder_abduction -10.96, toe_out 24.51 |
| BouncyLeft | 0.31 | bounce +2.8, pelvis_height +0.7, toe_out -0.6, cadence +0.5 | n 0.91, m_knee 1.36, m_elbow 0.66, torso_pitch -3.6, stance_width 7.8, toe_out -13.61 |
| BouncyRight | 0.29 | bounce +3.2, pelvis_height +1.0, toe_out -0.7, cadence +0.5 | n 0.91, m_knee 1.36, m_elbow 0.66, torso_pitch -3.6, stance_width 7.8, toe_out -13.61 |

최고 유사도 0.7 이상 71종, 0.5~0.7 23종, 0.5 미만 5종 (99종)
