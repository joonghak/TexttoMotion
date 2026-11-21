# 파라미터로 닿을 수 있는 100STYLE 스타일 (무작위 1500개, 목표 동작 기준)

가장 높은 유사도 순서이다. 주요 특징은 그 스타일이 Neutral에서 가장 크게 바뀐 특징(같은 단위)이다.

| 스타일 | 최고 유사도 | 주요 특징 | 그때의 값 |
| --- | --- | --- | --- |
| BentKnees | 0.95 | pelvis_height -2.8, knee_bend +2.3, arm_swing -0.4, hand_forward -0.4 | c 18.34, m_knee 0.8, torso_pitch -6.62, elbow_flexion -7.22 |
| ArmsAboveHead | 0.95 | hand_height +5.8, hand_forward +2.3, elbow_bend +1.0, stance_width -0.6 | m_arm 1.73, torso_pitch 0.69, shoulder_flexion 82.98, elbow_flexion 45.93 |
| LawnMower | 0.93 | elbow_bend +2.4, hand_out -2.0, hand_forward +1.7, hand_height +1.4 | n 1.1, m_arm 1.14, torso_pitch 10.85, elbow_flexion 53.04 |
| RaisedLeftArm | 0.92 | hand_out +2.2, hand_height +1.1, toe_out -0.7, head_pitch +0.5 | m_arm 1.23, m_torso 1.4, m_elbow 0.73, head_pitch 5.21, shoulder_abduction 26.04, elbow_flexion -9.47 |
| ArmsFolded | 0.90 | hand_out -2.7, elbow_bend +2.5, hand_height +1.6, toe_out +1.0 | n 1.1, m_arm 1.14, torso_pitch 10.85, elbow_flexion 53.04 |
| Aeroplane | 0.90 | head_sway +3.4, hand_out +3.4, torso_side +2.1, hand_height +1.7 | m_torso 7.71, m_elbow 0.71, shoulder_abduction 34.54 |
| CrowdAvoidance | 0.89 | head_sway +1.7, arm_swing +1.7, head_pitch +1.4, torso_side +0.5 | s 1.05, m_arm 1.42, m_torso 7.97, m_elbow 0.57, head_pitch 17.05, stance_width 0.22 |
| BeatChest | 0.89 | elbow_bend +3.9, hand_height +2.6, hand_forward +1.2, toe_out +0.6 | n 1.05, m_torso 0.48, shoulder_abduction 5.72, elbow_flexion 26.87 |
| HighKnees | 0.89 | foot_lift +4.2, knee_bend +1.8, toe_out -1.0, head_sway +0.6 | s 0.58, c 9.78, m_knee 1.44 |
| OnPhoneRight | 0.89 | elbow_bend +2.0, hand_height +1.7, toe_out +0.8, hand_out -0.7 | n 1.1, m_arm 1.14, torso_pitch 10.85, elbow_flexion 53.04 |
| RaisedRightArm | 0.89 | hand_out +2.0, hand_height +1.1, toe_out -0.7, torso_lean +0.3 | m_arm 0.97, m_knee 1.08, m_elbow 0.67, torso_pitch -5.95, shoulder_abduction 41.13 |
| Kick | 0.88 | foot_lift +3.4, cadence -1.1, knee_bend +0.8, pelvis_sway -0.8 | s 1.13, n 0.56, c 7.95, m_arm 0.86, m_knee 1.47, m_elbow 0.23, torso_pitch 9.25, head_pitch -9.06, shoulder_flexion 0.4, elbow_flexion -2.76 |
| LeanRight | 0.88 | head_pitch +3.2, toe_out -1.0, head_sway +0.8, pelvis_sway +0.7 | n 1.3, m_arm 0.88, m_torso 3.97, m_elbow 0.44, torso_pitch -2.58, head_pitch 29.68, shoulder_abduction 7.35 |
| Balance | 0.87 | hand_out +3.6, head_sway +2.1, torso_side +1.8, hand_height +1.7 | s 0.67, m_arm 0.31, m_torso 9.79, m_knee 1.09, m_elbow 0.91, torso_pitch 31.61, shoulder_abduction 84.12, elbow_flexion -14.58 |
| OnPhoneLeft | 0.87 | elbow_bend +2.1, hand_height +1.8, hand_out -0.8, head_pitch +0.4 | n 1.1, m_arm 1.14, torso_pitch 10.85, elbow_flexion 53.04 |
| Followed | 0.87 | head_sway +2.5, toe_out +1.0, pelvis_sway +1.0, arm_swing +0.9 | n 1.24, m_torso 8.16, head_pitch 11.71 |
| Teapot | 0.87 | hand_out +2.2, hand_height +1.8, head_pitch +1.3, elbow_bend +1.3 | n 1.06, head_pitch 22.4, shoulder_abduction 65.47, stance_width 1.59 |
| Zombie | 0.86 | hand_forward +4.3, hand_height +2.2, head_sway +2.1, cadence -1.5 | m_torso 6.69, m_knee 0.85, m_elbow 0.38, torso_pitch 8.48, shoulder_flexion 60.22 |
| Roadrunner | 0.86 | knee_bend +3.3, pelvis_height -2.9, torso_lean +2.2, hand_forward -1.8 | s 0.94, c 18.45, m_arm 0.68, m_elbow 0.16, torso_pitch 28.64, head_pitch -6.55 |
| Dinosaur | 0.86 | pelvis_height -3.8, elbow_bend +3.2, knee_bend +3.1, cadence -1.9 | s 1.52, n 0.62, c 24.62, m_arm 0.55, m_elbow 0.69, head_pitch -1.1, elbow_flexion 56.16, stance_width 5.45 |
| Superman | 0.85 | head_pitch +3.1, hand_height +2.2, torso_lean +1.0, pelvis_sway +0.8 | m_arm 1.24, m_elbow 0.73, torso_pitch 39.32, head_pitch 24.08, shoulder_abduction 53.05, elbow_flexion 49.23, stance_width 0.39 |
| Chicken | 0.85 | knee_bend +3.1, torso_lean +2.5, pelvis_height -2.5, elbow_bend +1.7 | c 7.86, m_arm 1.25, torso_pitch 22.87, head_pitch -9.32, shoulder_flexion 2.98, elbow_flexion 11.8 |
| ShieldedLeft | 0.85 | elbow_bend +2.6, hand_height +2.4, hand_forward +2.3, pelvis_height -2.0 | c 18.13, m_knee 0.87, m_elbow 0.51, torso_pitch 25.92, shoulder_flexion 55.24, elbow_flexion 46.55, stance_width 0.45 |
| ShieldedRight | 0.85 | elbow_bend +2.6, hand_height +2.4, pelvis_height -2.0, hand_forward +2.0 | c 18.13, m_knee 0.87, m_elbow 0.51, torso_pitch 25.92, shoulder_flexion 55.24, elbow_flexion 46.55, stance_width 0.45 |
| Swat | 0.85 | elbow_bend +3.3, hand_height +2.7, hand_forward +2.2, pelvis_height -2.0 | s 1.3, n 1.44, c 12.01, m_knee 1.1, m_elbow 0.26, torso_pitch 13.5, head_pitch -11.1, shoulder_flexion 53.07, elbow_flexion 55.19, stance_width 2.86 |
| WildArms | 0.84 | arm_swing +4.4, hand_height +2.7, hand_forward +0.8, torso_side +0.7 | m_arm 1.3, m_elbow 0.63 |
| Flapping | 0.84 | hand_out +3.0, hand_height +2.3, toe_out -1.0, arm_swing +0.7 | m_arm 0.97, m_knee 1.08, m_elbow 0.67, torso_pitch -5.95, shoulder_abduction 41.13 |
| GracefulArms | 0.84 | hand_height +2.2, elbow_bend +2.0, arm_swing +1.5, hand_out +1.4 | m_arm 1.4, m_knee 0.97, shoulder_abduction 42.77, elbow_flexion 36.35 |
| Depressed | 0.84 | head_pitch +3.1, head_sway +1.0, pelvis_height +0.8, torso_lean +0.7 | m_arm 1.28, m_torso 3.32, head_pitch 15.87 |
| LegsApart | 0.84 | stance_width +4.6, pelvis_sway +4.1, head_sway +3.0, toe_out +2.0 | s 1.75, m_torso 5.14, m_elbow 0.77, head_pitch 6.88, stance_width 6.44 |
| SwingArmsRound | 0.84 | arm_swing +2.9, cadence -1.1, hand_out -0.9, hand_height +0.7 | m_arm 1.49 |
| Old | 0.84 | head_sway +3.8, torso_side +2.6, head_pitch +2.5, cadence -1.9 | s 0.83, n 0.7, m_arm 1.74, m_torso 8.02, m_knee 0.92, torso_pitch 20.87, elbow_flexion 20.1 |
| InTheDark | 0.84 | hand_forward +3.2, hand_height +2.0, step_length -1.2, pelvis_sway +0.8 | n 1.32, m_knee 0.71, head_pitch 4.36, shoulder_flexion 72.12 |
| March | 0.83 | elbow_bend +1.8, foot_lift +1.5, knee_bend +1.4, hand_height +0.9 | s 0.86, c 12.09, m_arm 0.88, m_knee 1.29, m_elbow 0.87, torso_pitch -12.76, elbow_flexion 34.69 |
| Sweep | 0.83 | head_sway +4.1, torso_side +4.0, torso_lean +3.9, head_pitch +3.0 | s 0.99, m_arm 1.42, m_torso 8.66, m_knee 1.06, torso_pitch 27.89, head_pitch -0.05, shoulder_abduction 9.26, elbow_flexion 12.9 |
| WideLegs | 0.83 | stance_width +4.8, pelvis_sway +4.0, head_sway +2.4, toe_out +1.9 | s 1.26, n 1.04, m_torso 3.54, m_knee 0.98, m_elbow 0.83, shoulder_flexion 6.84, stance_width 7.16 |
| Monk | 0.82 | head_pitch +3.5, cadence -1.8, hand_out -1.2, step_length +1.1 | s 1.09, n 0.69, c 0.74, head_pitch 18.19 |
| FlickLegs | 0.81 | foot_lift +4.4, cadence -1.9, stance_width +1.7, knee_bend +1.5 | m_arm 0.89, m_knee 1.36, m_elbow 0.44, stance_width 2.95 |
| SpinClock | 0.81 | head_sway +3.2, head_pitch -2.1, arm_swing +2.1, torso_side +1.3 | n 0.94, m_torso 5.43, m_knee 0.83, m_elbow 0.9, head_pitch -13.68 |
| Star | 0.80 | stance_width +4.5, pelvis_sway +4.1, hand_out +3.7, toe_out +2.5 | n 1.16, m_arm 1.31, m_elbow 0.91, shoulder_abduction 13.25, stance_width 1.48 |
| SpinAntiClock | 0.80 | head_sway +2.2, head_pitch -1.6, arm_swing +1.6, foot_lift -1.1 | n 0.94, m_torso 5.43, m_knee 0.83, m_elbow 0.9, head_pitch -13.68 |
| Robot | 0.80 | step_length -2.8, elbow_bend +2.4, foot_lift -1.1, hand_height +1.0 | s 0.47, n 1.28, c 2.47, m_arm 0.52, m_torso 2, m_knee 0.9, m_elbow 0.59, torso_pitch 2.88, elbow_flexion 54.47 |
| Swimming | 0.79 | hand_forward +2.8, hand_height +2.1, elbow_bend +1.6, arm_swing +1.6 | m_arm 1.03, m_elbow 0.39 |
| LeanLeft | 0.79 | head_pitch +2.3, toe_out -1.3, torso_lean +0.9, knee_bend +0.8 | n 1.26, c 2.75, m_arm 0.37, m_knee 0.86, torso_pitch 29.77, head_pitch 28.8, shoulder_flexion 18.09, elbow_flexion -6.96, stance_width 4.47 |
| Lunge | 0.79 | pelvis_height -3.9, bounce +2.9, knee_bend +1.5, cadence -1.1 | n 0.58, c 29.56, m_torso 1.76, m_knee 0.86, torso_pitch 12.8, shoulder_abduction 20.21, stance_width 1.71 |
| WalkingStickRight | 0.79 | elbow_bend +0.8, hand_forward +0.7, hand_height +0.4, pelvis_sway -0.3 | m_torso 0.83, elbow_flexion 20.08 |
| OnToesCrouched | 0.78 | knee_bend +2.6, pelvis_height -2.4, torso_lean +1.9, head_sway +1.7 | s 0.79, c 16.88, m_arm 1.76, m_torso 8.78, m_knee 0.73, torso_pitch -13.75, elbow_flexion 8.73 |
| Rocket | 0.77 | torso_lean +3.1, hand_forward -2.5, hand_height +2.4, head_pitch +1.4 | m_torso 1.69, torso_pitch 38.97, elbow_flexion -15.46 |
| BentForward | 0.77 | torso_lean +2.7, head_pitch +1.9, torso_side +1.5, head_sway +1.5 | m_torso 5.99, m_knee 0.97, torso_pitch 24.08, elbow_flexion 4.73 |
| Punch | 0.76 | elbow_bend +2.7, hand_height +2.6, hand_forward +1.9, arm_swing +1.5 | m_torso 0.83, elbow_flexion 20.08 |
| WalkingStickLeft | 0.76 | elbow_bend +0.9, head_pitch +0.6, hand_forward +0.5, stance_width -0.4 | s 0.98, n 0.71, m_arm 0.82, torso_pitch 30.73, head_pitch 12.99, shoulder_flexion 38.08, elbow_flexion 43.58 |
| Rushed | 0.76 | arm_swing +2.0, pelvis_sway +1.6, pelvis_height -1.4, knee_bend +1.1 | s 1.21, n 1.44, m_arm 1.71, m_torso 0.35 |
| StartStop | 0.76 | head_pitch +1.6, pelvis_sway -1.6, head_sway +1.1, foot_lift -1.0 | s 0.83, n 0.7, m_arm 1.74, m_torso 8.02, m_knee 0.92, torso_pitch 20.87, elbow_flexion 20.1 |
| WhirlArms | 0.75 | arm_swing +4.2, hand_height +2.5, torso_side +1.9, cadence -1.6 | m_arm 1.03, m_elbow 0.39 |
| HandsInPockets | 0.75 | elbow_bend +1.6, arm_swing -0.5, stance_width -0.5, toe_out -0.5 | n 1.1, m_arm 1.14, torso_pitch 10.85, elbow_flexion 53.04 |
| WiggleHips | 0.74 | elbow_bend +2.1, cadence -2.1, head_sway +1.2, step_length +1.0 | s 1.01, n 0.61, m_arm 0.7, m_torso 6.22, torso_pitch 14.23, shoulder_flexion 6.23, elbow_flexion 55.96, stance_width 1.35 |
| Angry | 0.74 | head_pitch +1.7, arm_swing +1.2, toe_out +0.8, bounce +0.8 | n 1, c 2.51, m_arm 1.69, head_pitch 26.87 |
| Waving | 0.74 | arm_swing +1.3, head_sway +0.6, stance_width -0.5, elbow_bend +0.5 | m_arm 1.3, m_elbow 0.63 |
| Crouched | 0.73 | pelvis_height -2.0, torso_lean +1.9, knee_bend +1.9, head_sway +1.8 | c 18.15, m_arm 0.86, m_torso 9.98, m_elbow 0.93, elbow_flexion 46.28, stance_width 3.8 |
| Drunk | 0.73 | arm_swing +2.4, head_sway +1.6, torso_side +1.0, head_pitch +1.0 | s 1.05, m_arm 1.42, m_torso 7.97, m_elbow 0.57, head_pitch 17.05, stance_width 0.22 |
| Quail | 0.72 | knee_bend +1.6, step_length -1.5, pelvis_height -1.4, torso_lean +1.2 | s 0.69, c 16.95, m_arm 0.38, m_knee 0.81, torso_pitch 27.95, head_pitch -13.6, shoulder_abduction 0.45, elbow_flexion 10.4, stance_width 2.3 |
| BigSteps | 0.72 | pelvis_height -2.9, bounce +2.4, step_length +1.2, knee_bend +0.7 | s 1.62, c 27.5, m_arm 1.2, m_torso 1.77, m_knee 0.75, m_elbow 0.85 |
| SlideFeet | 0.72 | cadence -2.0, step_length +1.0, foot_lift -0.9, head_pitch +0.9 | s 1.42, n 0.59, m_torso 4.02, m_elbow 0.76, shoulder_flexion 7.2 |
| RightHop | 0.72 | elbow_bend +2.8, knee_bend +2.4, step_length -2.2, bounce +2.0 | s 0.47, n 1.28, c 2.47, m_arm 0.52, m_torso 2, m_knee 0.9, m_elbow 0.59, torso_pitch 2.88, elbow_flexion 54.47 |
| Cat | 0.70 | pelvis_height -1.9, step_length +1.9, cadence -1.9, arm_swing +1.6 | s 1.1, n 0.86, c 12.46, m_arm 1.6, m_torso 4, torso_pitch 9.34, head_pitch 7.69, shoulder_flexion 1.72, elbow_flexion 6.05 |
| OnToesBentForward | 0.68 | torso_lean +3.5, torso_side +2.1, head_sway +2.0, knee_bend +1.4 | s 0.99, m_arm 1.42, m_torso 8.66, m_knee 1.06, torso_pitch 27.89, head_pitch -0.05, shoulder_abduction 9.26, elbow_flexion 12.9 |
| Skip | 0.68 | bounce +3.6, foot_lift +2.8, knee_bend +1.9, arm_swing +1.2 | c 1.35, m_arm 1.79, m_knee 1.44, m_elbow 0.83, torso_pitch -14.78 |
| HandsBetweenLegs | 0.68 | torso_side +8.4, torso_lean +5.7, pelvis_sway +4.5, stance_width +3.7 | s 1.41, n 1.28, c 9.06, m_torso 8.57, m_knee 1.13, m_elbow 0.14, torso_pitch 23, shoulder_flexion 15.51, stance_width 5.27 |
| LeftHop | 0.67 | knee_bend +3.8, elbow_bend +3.1, bounce +2.4, step_length -2.3 | s 0.32, c 13.57, m_arm 0.69, m_knee 1.14, m_elbow 0.57, torso_pitch 16.15, head_pitch -5.68, shoulder_flexion 55.72, elbow_flexion 50.82 |
| PendulumHands | 0.67 | elbow_bend +1.9, step_length -1.7, knee_bend +1.4, hand_out +1.3 | c 7.71, m_arm 1.44, m_knee 0.83, m_elbow 0.99, torso_pitch 22.85, shoulder_abduction 22.67, elbow_flexion 30.02, stance_width 3.81 |
| KarateChop | 0.67 | elbow_bend +2.9, hand_height +2.3, hand_forward +1.8, arm_swing +1.7 | m_torso 0.83, elbow_flexion 20.08 |
| Elated | 0.67 | arm_swing +3.0, bounce +2.6, hand_height +1.2, elbow_bend +1.0 | m_arm 1.3, m_elbow 0.63 |
| WildLegs | 0.66 | cadence -2.1, foot_lift +1.8, head_sway +1.4, toe_out +1.1 | s 0.92, m_torso 9.27, m_knee 1.39, m_elbow 0.02 |
| SwingShoulders | 0.66 | arm_swing +2.5, cadence -1.7, step_length +1.5, elbow_bend +1.3 | m_arm 1.3, m_elbow 0.63 |
| Heavyset | 0.63 | elbow_bend +1.5, hand_out +0.7, pelvis_sway +0.5, hand_height +0.5 | m_arm 1.4, m_knee 0.97, shoulder_abduction 42.77, elbow_flexion 36.35 |
| Akimbo | 0.63 | elbow_bend +2.0, toe_out +0.9, hand_height +0.7, torso_lean +0.5 | s 1.11, m_torso 1.69, m_elbow 0.68, torso_pitch -4.49, shoulder_abduction 64.44, elbow_flexion 59.13 |
| Proud | 0.62 | arm_swing +1.0, elbow_bend +0.9, toe_out -0.5, bounce +0.4 | m_arm 1.3, m_elbow 0.63 |
| Penguin | 0.61 | step_length -2.9, foot_lift -1.8, toe_out +0.9, knee_bend -0.8 | s 0.37, n 1.45, m_torso 3.55, m_knee 0.73, shoulder_flexion 16.57, stance_width 1.61 |
| LimpRight | 0.61 | foot_lift -1.0, head_sway +0.8, torso_lean +0.5, torso_side +0.4 | n 0.94, m_torso 5.43, m_knee 0.83, m_elbow 0.9, head_pitch -13.68 |
| TogetherStep | 0.60 | step_length -3.5, cadence +3.2, head_sway +1.8, arm_swing +1.5 | s 0.68, n 1.33, m_torso 6.51, torso_pitch 18.4, head_pitch 0.94 |
| LimpLeft | 0.60 | head_sway +1.0, foot_lift -0.8, toe_out +0.7, stance_width -0.5 | n 0.99, m_arm 0.84, m_torso 8.65, m_elbow 0.27, torso_pitch 27.89, elbow_flexion -3.84 |
| FairySteps | 0.59 | toe_out -3.1, pelvis_sway -1.5, cadence -1.3, head_pitch +1.2 | s 0.35, n 0.6, m_arm 0.34, m_torso 5.03, m_elbow 0, torso_pitch -3.33, head_pitch 11.22, elbow_flexion -28.2 |
| LeanBack | 0.58 | torso_lean -1.7, knee_bend +1.4, torso_side +1.4, pelvis_height -1.3 | s 0.79, c 16.88, m_arm 1.76, m_torso 8.78, m_knee 0.73, torso_pitch -13.75, elbow_flexion 8.73 |
| PigeonToed | 0.58 | toe_out -3.2, head_sway +2.3, cadence -1.4, arm_swing +1.3 | m_arm 1.21, m_torso 8.53, torso_pitch 21.8, shoulder_abduction 16.22, elbow_flexion 11.8 |
| Morris | 0.55 | bounce +2.8, elbow_bend +2.2, hand_height +1.6, toe_out -1.3 | m_arm 1.4, m_knee 0.97, shoulder_abduction 42.77, elbow_flexion 36.35 |
| LookUp | 0.55 | head_pitch -2.1, step_length -0.9, torso_lean -0.8, pelvis_sway +0.7 | n 0.94, m_torso 5.43, m_knee 0.83, m_elbow 0.9, head_pitch -13.68 |
| Strutting | 0.55 | toe_out +1.2, head_pitch -1.1, pelvis_sway +0.8, stance_width +0.5 | n 1.29, m_arm 1.57, m_elbow 0.99, torso_pitch -12.79, shoulder_abduction 16.26, stance_width 2.59 |
| TwoFootJump | 0.54 | bounce +5.8, knee_bend +2.3, step_length -2.1, cadence +1.9 | s 0.56, n 1.23, c 17.65, m_arm 1.39, m_torso 1.91, torso_pitch 34.44, head_pitch 16.33, shoulder_flexion 14.91, elbow_flexion -0.31 |
| OnHeels | 0.53 | foot_lift -1.6, step_length -1.3, knee_bend -1.3, arm_swing +0.9 | s 0.37, n 1.45, m_torso 3.55, m_knee 0.73, shoulder_flexion 16.57, stance_width 1.61 |
| CrossOver | 0.51 | toe_out -3.0, cadence -2.0, step_length +1.3, head_pitch +1.3 | s 1.09, n 0.69, c 0.74, head_pitch 18.19 |
| DuckFoot | 0.51 | toe_out +3.6, cadence -1.6, head_sway +1.4, pelvis_sway +1.2 | s 1.75, m_torso 5.14, m_elbow 0.77, head_pitch 6.88, stance_width 6.44 |
| ArmsBySide | 0.47 | stance_width -0.7, toe_out +0.6, arm_swing -0.5, hand_out -0.4 | m_arm 0.36, m_elbow 0.89, head_pitch 15.57 |
| Tiptoe | 0.45 | toe_out -0.7, knee_bend +0.5, step_length -0.4, foot_lift -0.3 | s 0.37, n 1.45, m_torso 3.55, m_knee 0.73, shoulder_flexion 16.57, stance_width 1.61 |
| DragRightLeg | 0.42 | step_length -2.9, cadence +2.1, foot_lift -1.4, stance_width -1.0 | s 0.37, n 1.45, m_torso 3.55, m_knee 0.73, shoulder_flexion 16.57, stance_width 1.61 |
| DragLeftLeg | 0.41 | step_length -2.8, cadence +2.1, foot_lift -1.2, head_pitch +0.9 | s 0.68, n 1.33, m_torso 6.51, torso_pitch 18.4, head_pitch 0.94 |
| Stiff | 0.40 | foot_lift -1.3, knee_bend -1.0, step_length -0.8, arm_swing +0.6 | s 0.37, n 1.45, m_torso 3.55, m_knee 0.73, shoulder_flexion 16.57, stance_width 1.61 |
| ArmsBehindBack | 0.34 | hand_forward -1.7, hand_out -1.6, toe_out -1.5, arm_swing -0.9 | n 1.02, m_knee 0.98, m_elbow 0.53, torso_pitch 29.82, head_pitch -12.79, elbow_flexion 22.54, stance_width 5.86 |
| BouncyRight | 0.29 | bounce +3.2, pelvis_height +1.0, toe_out -0.7, cadence +0.5 | s 1.19, n 0.71, c 2.68, m_knee 1.35, shoulder_flexion 4.81, stance_width 8 |
| BouncyLeft | 0.29 | bounce +2.8, pelvis_height +0.7, toe_out -0.6, cadence +0.5 | s 1.19, n 0.71, c 2.68, m_knee 1.35, shoulder_flexion 4.81, stance_width 8 |

최고 유사도 0.7 이상 64종, 0.5~0.7 27종, 0.5 미만 8종 (99종)
