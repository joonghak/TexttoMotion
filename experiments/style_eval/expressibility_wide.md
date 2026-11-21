# 파라미터로 닿을 수 있는 100STYLE 스타일 (무작위 1500개, 목표 동작 기준)

가장 높은 유사도 순서이다. 주요 특징은 그 스타일이 Neutral에서 가장 크게 바뀐 특징(같은 단위)이다.

| 스타일 | 최고 유사도 | 주요 특징 | 그때의 값 |
| --- | --- | --- | --- |
| BentKnees | 0.95 | pelvis_height -2.8, knee_bend +2.3, arm_swing -0.4, hand_forward -0.4 | s 1.77, c 29.41, m_arm 0.04, m_knee 0.58, m_elbow 0.94, torso_pitch 15.08, shoulder_abduction -6.05 |
| Followed | 0.92 | head_sway +2.5, toe_out +1.0, pelvis_sway +1.0, arm_swing +0.9 | s 1.07, n 1.41, m_arm 1.2, m_torso 8.25, m_elbow 0.96, toe_out 21.71 |
| Lunge | 0.92 | pelvis_height -3.9, bounce +2.9, knee_bend +1.5, cadence -1.1 | s 1.02, n 0.65, c 19, m_arm 0.91, shoulder_flexion -28.94, stance_width -2.84, toe_out 0.41, bounce 21.84 |
| RaisedLeftArm | 0.91 | hand_out +2.2, hand_height +1.1, toe_out -0.7, head_pitch +0.5 | n 1.15, m_arm 1.04, m_torso 1.71, shoulder_abduction 40.96 |
| Aeroplane | 0.90 | head_sway +3.4, hand_out +3.4, torso_side +2.1, hand_height +1.7 | m_torso 9.45, m_elbow 0.14, shoulder_abduction 27.79 |
| RaisedRightArm | 0.90 | hand_out +2.0, hand_height +1.1, toe_out -0.7, torso_lean +0.3 | n 1.15, m_arm 1.04, m_torso 1.71, shoulder_abduction 40.96 |
| BigSteps | 0.89 | pelvis_height -2.9, bounce +2.4, step_length +1.2, knee_bend +0.7 | s 1.35, c 21.24, m_arm 1.48, m_knee 0.77, m_elbow 0.01, torso_pitch 34.09, head_pitch 7.3, elbow_flexion 23.16, stance_width -7.39, toe_out -10.47, bounce 29.36 |
| ArmsFolded | 0.89 | hand_out -2.7, elbow_bend +2.5, hand_height +1.6, toe_out +1.0 | s 1.04, m_knee 1.14, torso_pitch -1.37, shoulder_abduction -14.1, elbow_flexion 58.07, stance_width 0.89, toe_out 24.47, shoulder_rotation 43.98 |
| Superman | 0.89 | head_pitch +3.1, hand_height +2.2, torso_lean +1.0, pelvis_sway +0.8 | s 0.97, n 1.21, c 3.27, m_knee 0.98, m_elbow 0.88, torso_pitch 26.94, head_pitch 29.29, shoulder_abduction 60.5, elbow_flexion 42.35, stance_width 2.11 |
| HighKnees | 0.87 | foot_lift +4.2, knee_bend +1.8, toe_out -1.0, head_sway +0.6 | s 0.69, n 0.73, c 12.05, m_arm 1.11, m_torso 6.65, m_knee 1.49, m_elbow 0.46, torso_pitch 2.6, head_pitch -6.51, elbow_flexion -9.63, stance_width -7.61, toe_out -26.8, shoulder_rotation -23.97 |
| Roadrunner | 0.87 | knee_bend +3.3, pelvis_height -2.9, torso_lean +2.2, hand_forward -1.8 | n 1.17, c 18.83, m_arm 1.74, m_elbow 0.74, torso_pitch 30.71, head_pitch -13.91, shoulder_abduction 11.47, elbow_flexion 10.67, bounce 7.62 |
| Flapping | 0.87 | hand_out +3.0, hand_height +2.3, toe_out -1.0, arm_swing +0.7 | n 1.15, m_arm 1.04, m_torso 1.71, shoulder_abduction 40.96 |
| Swat | 0.87 | elbow_bend +3.3, hand_height +2.7, hand_forward +2.2, pelvis_height -2.0 | n 1.1, m_arm 1.01, torso_pitch 10.85, elbow_flexion 53.04, bounce 15.32 |
| ArmsAboveHead | 0.86 | hand_height +5.8, hand_forward +2.3, elbow_bend +1.0, stance_width -0.6 | m_arm 0.44, head_pitch 19.47, shoulder_flexion 72.37, elbow_flexion 23.74 |
| LeanLeft | 0.86 | head_pitch +2.3, toe_out -1.3, torso_lean +0.9, knee_bend +0.8 | n 0.95, c 9.48, m_elbow 0.54, torso_pitch 24.93, head_pitch 25.29, shoulder_abduction 19.13, elbow_flexion 2.47, toe_out -31.16 |
| OnToesCrouched | 0.86 | knee_bend +2.6, pelvis_height -2.4, torso_lean +1.9, head_sway +1.7 | c 18.76, m_arm 0.77, m_torso 9.32, m_knee 0.5, head_pitch -0.19, shoulder_flexion 9.65, stance_width -3.84, shoulder_rotation 21.88 |
| FairySteps | 0.85 | toe_out -3.1, pelvis_sway -1.5, cadence -1.3, head_pitch +1.2 | n 0.72, m_torso 5.6, m_elbow 0.99, torso_pitch -4.59, head_pitch 13.54, toe_out -31.76 |
| Monk | 0.85 | head_pitch +3.5, cadence -1.8, hand_out -1.2, step_length +1.1 | n 0.68, m_torso 3.01, m_elbow 0.82, torso_pitch 23.9, head_pitch 19.16, shoulder_flexion 16.9, elbow_flexion 13.1 |
| OnPhoneRight | 0.84 | elbow_bend +2.0, hand_height +1.7, toe_out +0.8, hand_out -0.7 | n 0.78, m_arm 1.29, m_elbow 0.21, torso_pitch -11.03, head_pitch 16.39, elbow_flexion 59.49, toe_out 12.28, bounce 8.4 |
| ShieldedRight | 0.84 | elbow_bend +2.6, hand_height +2.4, pelvis_height -2.0, hand_forward +2.0 | n 1.1, m_arm 1.01, torso_pitch 10.85, elbow_flexion 53.04, bounce 15.32 |
| ArmsBehindBack | 0.84 | hand_forward -1.7, hand_out -1.6, toe_out -1.5, arm_swing -0.9 | m_arm 0.27, m_elbow 0.57, shoulder_flexion -38.82, elbow_flexion 15.51, toe_out -27.2, bounce 4.25 |
| Depressed | 0.84 | head_pitch +3.1, head_sway +1.0, pelvis_height +0.8, torso_lean +0.7 | s 0.54, m_torso 9.01, m_knee 0.94, torso_pitch 22.8, head_pitch 19.86, stance_width -3.39, shoulder_rotation 28.26, bounce 1.45 |
| Teapot | 0.84 | hand_out +2.2, hand_height +1.8, head_pitch +1.3, elbow_bend +1.3 | n 1.39, c 4.21, m_arm 0.8, m_knee 0.86, m_elbow 0.62, torso_pitch 11.18, head_pitch 18.85, shoulder_abduction 67.24, elbow_flexion 7.57, stance_width -3.85, shoulder_rotation -33.69, bounce 7.74 |
| Zombie | 0.83 | hand_forward +4.3, hand_height +2.2, head_sway +2.1, cadence -1.5 | m_arm 1.08, m_torso 6.7, shoulder_flexion 40.14, shoulder_rotation 25.59, bounce 3.73 |
| LeanRight | 0.83 | head_pitch +3.2, toe_out -1.0, head_sway +0.8, pelvis_sway +0.7 | n 1.06, m_arm 1.16, m_torso 1.72, m_elbow 0.76, torso_pitch 18.59, head_pitch 11.27, shoulder_flexion -12.3, shoulder_abduction 11.34, elbow_flexion 13.8, stance_width 0.54, bounce 3.2 |
| Dinosaur | 0.83 | pelvis_height -3.8, elbow_bend +3.2, knee_bend +3.1, cadence -1.9 | c 15.94, m_torso 0.73, m_elbow 0.96, torso_pitch -7.56, elbow_flexion 51.86, bounce 2.94 |
| Balance | 0.83 | hand_out +3.6, head_sway +2.1, torso_side +1.8, hand_height +1.7 | s 0.64, n 0.61, c 0.64, m_torso 4.98, m_knee 0.6, torso_pitch 36.65, head_pitch 16.61, shoulder_abduction 56.35, elbow_flexion -7.23, toe_out -22.73, shoulder_rotation -5.8 |
| Chicken | 0.83 | knee_bend +3.1, torso_lean +2.5, pelvis_height -2.5, elbow_bend +1.7 | c 21.58, torso_pitch 21.79, shoulder_flexion -21.59, elbow_flexion 38.73, shoulder_rotation 6.17 |
| InTheDark | 0.82 | hand_forward +3.2, hand_height +2.0, step_length -1.2, pelvis_sway +0.8 | n 0.99, m_knee 0.82, m_elbow 0.82, shoulder_flexion 32.01 |
| BeatChest | 0.82 | elbow_bend +3.9, hand_height +2.6, hand_forward +1.2, toe_out +0.6 | m_arm 1.01, torso_pitch -4.55, elbow_flexion 54.93, toe_out 19.39, shoulder_rotation -32.01 |
| ShieldedLeft | 0.82 | elbow_bend +2.6, hand_height +2.4, hand_forward +2.3, pelvis_height -2.0 | c 21.89, m_knee 0.8, torso_pitch 26.77, head_pitch 0.3, shoulder_flexion 82.24, elbow_flexion 39.66, shoulder_rotation 44.43 |
| Rocket | 0.82 | torso_lean +3.1, hand_forward -2.5, hand_height +2.4, head_pitch +1.4 | m_arm 1.31, torso_pitch 34, head_pitch 0.34, shoulder_flexion -19.34, toe_out -3.19 |
| Star | 0.82 | stance_width +4.5, pelvis_sway +4.1, hand_out +3.7, toe_out +2.5 | n 1.17, m_elbow 0.12, head_pitch -0.62, shoulder_abduction 4.32, stance_width 2.75 |
| StartStop | 0.81 | head_pitch +1.6, pelvis_sway -1.6, head_sway +1.1, foot_lift -1.0 | s 0.54, m_torso 9.01, m_knee 0.94, torso_pitch 22.8, head_pitch 19.86, stance_width -3.39, shoulder_rotation 28.26, bounce 1.45 |
| CrowdAvoidance | 0.81 | head_sway +1.7, arm_swing +1.7, head_pitch +1.4, torso_side +0.5 | m_arm 1.33, m_torso 9.41, m_elbow 0.21, torso_pitch 7.85, head_pitch 16.19, shoulder_abduction 17.41 |
| March | 0.81 | elbow_bend +1.8, foot_lift +1.5, knee_bend +1.4, hand_height +0.9 | c 9.4, m_elbow 0.16, shoulder_flexion -5.95, elbow_flexion 53.77, shoulder_rotation 1.41 |
| FlickLegs | 0.81 | foot_lift +4.4, cadence -1.9, stance_width +1.7, knee_bend +1.5 | s 1.37, n 0.66, m_arm 1.02, m_torso 5.18, m_knee 1.44, torso_pitch 12.06, head_pitch 1.1, shoulder_flexion -5.93, stance_width 4.99, shoulder_rotation 42.15, bounce 0.58 |
| LawnMower | 0.81 | elbow_bend +2.4, hand_out -2.0, hand_forward +1.7, hand_height +1.4 | n 1.33, torso_pitch 23.58, head_pitch 4.42, shoulder_flexion 80.48, elbow_flexion 48.52, toe_out 8.71, shoulder_rotation 13.98 |
| Old | 0.81 | head_sway +3.8, torso_side +2.6, head_pitch +2.5, cadence -1.9 | s 1.14, n 0.76, m_torso 9.77, m_knee 0.94, head_pitch 27.3, shoulder_abduction 0.36, stance_width -5.52, toe_out -8.94 |
| CrossOver | 0.80 | toe_out -3.0, cadence -2.0, step_length +1.3, head_pitch +1.3 | n 0.72, m_torso 5.6, m_elbow 0.99, torso_pitch -4.59, head_pitch 13.54, toe_out -31.76 |
| PigeonToed | 0.80 | toe_out -3.2, head_sway +2.3, cadence -1.4, arm_swing +1.3 | s 1.07, n 1.09, m_arm 1.65, m_torso 4.42, m_elbow 0.01, torso_pitch 8.77, shoulder_flexion -11.45, shoulder_abduction 13.33, toe_out -30.23, shoulder_rotation -22.29 |
| LeftHop | 0.80 | knee_bend +3.8, elbow_bend +3.1, bounce +2.4, step_length -2.3 | s 0.44, m_arm 1.31, m_torso 0.85, head_pitch 5.57, shoulder_flexion -8.7, elbow_flexion 32.29, toe_out 7.96, bounce 23.15 |
| OnPhoneLeft | 0.80 | elbow_bend +2.1, hand_height +1.8, hand_out -0.8, head_pitch +0.4 | n 0.78, m_arm 1.29, m_elbow 0.21, torso_pitch -11.03, head_pitch 16.39, elbow_flexion 59.49, toe_out 12.28, bounce 8.4 |
| Crouched | 0.80 | pelvis_height -2.0, torso_lean +1.9, knee_bend +1.9, head_sway +1.8 | c 18.76, m_arm 0.77, m_torso 9.32, m_knee 0.5, head_pitch -0.19, shoulder_flexion 9.65, stance_width -3.84, shoulder_rotation 21.88 |
| Kick | 0.79 | foot_lift +3.4, cadence -1.1, knee_bend +0.8, pelvis_sway -0.8 | s 0.69, n 0.73, c 12.05, m_arm 1.11, m_torso 6.65, m_knee 1.49, m_elbow 0.46, torso_pitch 2.6, head_pitch -6.51, elbow_flexion -9.63, stance_width -7.61, toe_out -26.8, shoulder_rotation -23.97 |
| Akimbo | 0.79 | elbow_bend +2.0, toe_out +0.9, hand_height +0.7, torso_lean +0.5 | m_arm 1.01, torso_pitch -4.55, elbow_flexion 54.93, toe_out 19.39, shoulder_rotation -32.01 |
| WalkingStickLeft | 0.79 | elbow_bend +0.9, head_pitch +0.6, hand_forward +0.5, stance_width -0.4 | n 1.04, m_arm 1.04, m_knee 0.78, torso_pitch 20.68, head_pitch 11.49, shoulder_flexion 39.25, elbow_flexion 56.93, stance_width -1.76, toe_out 27.6, shoulder_rotation -40.5 |
| Angry | 0.78 | head_pitch +1.7, arm_swing +1.2, toe_out +0.8, bounce +0.8 | s 1.76, m_arm 1.75, torso_pitch 18.54, head_pitch 23.4, elbow_flexion 30.21, toe_out 4.12, shoulder_rotation -24.97, bounce 13.93 |
| WalkingStickRight | 0.78 | elbow_bend +0.8, hand_forward +0.7, hand_height +0.4, pelvis_sway -0.3 | n 0.55, m_arm 0.49, m_knee 1.04, shoulder_flexion 56.74, elbow_flexion 36.97, shoulder_rotation 18.41 |
| ArmsBySide | 0.78 | stance_width -0.7, toe_out +0.6, arm_swing -0.5, hand_out -0.4 | c 5.35, m_arm 0.27, m_elbow 0.52, shoulder_flexion -0.2, shoulder_abduction -9.01, toe_out 22.62, shoulder_rotation 30.34 |
| Rushed | 0.77 | arm_swing +2.0, pelvis_sway +1.6, pelvis_height -1.4, knee_bend +1.1 | s 1.59, m_arm 1.76, m_knee 0.85, m_elbow 1, torso_pitch -0.8, elbow_flexion -2.73, shoulder_rotation 19.82, bounce 11.83 |
| BentForward | 0.77 | torso_lean +2.7, head_pitch +1.9, torso_side +1.5, head_sway +1.5 | c 0.23, m_torso 4.84, m_knee 0.84, m_elbow 0.43, torso_pitch 35.97, head_pitch 2.87, shoulder_abduction 8.8, shoulder_rotation 56.32 |
| HandsInPockets | 0.77 | elbow_bend +1.6, arm_swing -0.5, stance_width -0.5, toe_out -0.5 | n 1.28, m_torso 2.88, m_knee 1.13, m_elbow 0.9, head_pitch 3.6, elbow_flexion 58.58, stance_width -7.2, toe_out -10.87 |
| TwoFootJump | 0.77 | bounce +5.8, knee_bend +2.3, step_length -2.1, cadence +1.9 | s 0.49, m_arm 1.39, m_elbow 0.88, torso_pitch 23.11, shoulder_flexion 4.1, stance_width -4.16, toe_out -8.15, shoulder_rotation -29.38, bounce 22.89 |
| SpinClock | 0.76 | head_sway +3.2, head_pitch -2.1, arm_swing +2.1, torso_side +1.3 | n 1.09, m_arm 1.09, m_torso 7.06, head_pitch -11.43, toe_out -15.21, shoulder_rotation 32.38 |
| Sweep | 0.75 | head_sway +4.1, torso_side +4.0, torso_lean +3.9, head_pitch +3.0 | m_torso 5.99, m_knee 0.78, torso_pitch 24.08, elbow_flexion 4.73, shoulder_rotation 9.89 |
| LegsApart | 0.75 | stance_width +4.6, pelvis_sway +4.1, head_sway +3.0, toe_out +2.0 | s 1.6, c 2.54, m_arm 0.89, m_torso 8.32, m_knee 1.01, m_elbow 0.75, shoulder_abduction -3.09, stance_width 4.45 |
| RightHop | 0.75 | elbow_bend +2.8, knee_bend +2.4, step_length -2.2, bounce +2.0 | s 0.69, n 1.11, torso_pitch -4.29, shoulder_abduction -13.26, elbow_flexion 18.7, stance_width -1.26, shoulder_rotation -27.79, bounce 8.57 |
| WideLegs | 0.74 | stance_width +4.8, pelvis_sway +4.0, head_sway +2.4, toe_out +1.9 | n 1.26, m_elbow 0.05, head_pitch -0.75, stance_width 5.12, toe_out -2.5 |
| LimpLeft | 0.74 | head_sway +1.0, foot_lift -0.8, toe_out +0.7, stance_width -0.5 | s 0.86, c 1.86, m_arm 0.97, m_torso 9.47, m_knee 0.79, head_pitch 11.09, shoulder_abduction 8.41, elbow_flexion 22.98, toe_out 29.14, shoulder_rotation 1.17 |
| SlideFeet | 0.74 | cadence -2.0, step_length +1.0, foot_lift -0.9, head_pitch +0.9 | s 1.3, n 0.63, m_torso 5.21, m_elbow 0.39, torso_pitch 3.65, head_pitch 15.54 |
| WiggleHips | 0.73 | elbow_bend +2.1, cadence -2.1, head_sway +1.2, step_length +1.0 | n 0.59, m_torso 3.95, m_knee 0.43, torso_pitch -13.31, head_pitch 6.67, elbow_flexion 46.54, toe_out 11.56 |
| Skip | 0.73 | bounce +3.6, foot_lift +2.8, knee_bend +1.9, arm_swing +1.2 | s 0.65, c 8.97, m_torso 2.62, m_knee 1.34, m_elbow 0.01, head_pitch 2.57, shoulder_abduction 6.86, elbow_flexion 7.67, stance_width 1.7, toe_out 12.3, bounce 26.75 |
| DuckFoot | 0.72 | toe_out +3.6, cadence -1.6, head_sway +1.4, pelvis_sway +1.2 | s 1.59, m_knee 0.41, torso_pitch 4.86, head_pitch 4.17, toe_out 21.59 |
| Cat | 0.72 | pelvis_height -1.9, step_length +1.9, cadence -1.9, arm_swing +1.6 | s 1.53, n 0.59, c 5.23, torso_pitch -1.4, shoulder_rotation 11.25, bounce 1.43 |
| LimpRight | 0.72 | foot_lift -1.0, head_sway +0.8, torso_lean +0.5, torso_side +0.4 | n 0.74, m_torso 7.84, m_knee 0.46, m_elbow 0.55, elbow_flexion -3.22 |
| Quail | 0.71 | knee_bend +1.6, step_length -1.5, pelvis_height -1.4, torso_lean +1.2 | s 0.46, n 0.84, c 20.86, m_arm 0.71, m_torso 6.73, m_knee 0.45, m_elbow 0.1, torso_pitch 20.21, head_pitch -11.58, shoulder_abduction 18.46, elbow_flexion 54.81, stance_width 0.95, toe_out -8.62, bounce 4.79 |
| SpinAntiClock | 0.71 | head_sway +2.2, head_pitch -1.6, arm_swing +1.6, foot_lift -1.1 | s 0.94, m_torso 9.82, m_knee 0.5, m_elbow 0.93, torso_pitch -4.27, elbow_flexion -17.78, toe_out -4.67, shoulder_rotation -29.73, bounce 0.32 |
| GracefulArms | 0.71 | hand_height +2.2, elbow_bend +2.0, arm_swing +1.5, hand_out +1.4 | shoulder_abduction 37.83, elbow_flexion 39.98, stance_width 2.39 |
| Punch | 0.70 | elbow_bend +2.7, hand_height +2.6, hand_forward +1.9, arm_swing +1.5 | n 1.41, m_arm 1.74, torso_pitch -12.41, elbow_flexion 35.54, stance_width -0.32, toe_out 5.32 |
| PendulumHands | 0.69 | elbow_bend +1.9, step_length -1.7, knee_bend +1.4, hand_out +1.3 | n 1.29, c 10.66, m_arm 0.02, m_torso 5.98, m_knee 0.67, m_elbow 0.65, torso_pitch 15, shoulder_abduction 76.26, elbow_flexion 27.85, shoulder_rotation -10.97 |
| Heavyset | 0.69 | elbow_bend +1.5, hand_out +0.7, pelvis_sway +0.5, hand_height +0.5 | s 1.55, n 0.94, m_torso 1.22, m_knee 1, shoulder_flexion -44.25, shoulder_abduction 47.92, elbow_flexion 59.02, bounce 8.4 |
| Robot | 0.69 | step_length -2.8, elbow_bend +2.4, foot_lift -1.1, hand_height +1.0 | s 0.73, head_pitch 8.02, shoulder_flexion 21.65, elbow_flexion 51.68, stance_width 0.17 |
| Drunk | 0.69 | arm_swing +2.4, head_sway +1.6, torso_side +1.0, head_pitch +1.0 | m_arm 1.33, m_torso 9.41, m_elbow 0.21, torso_pitch 7.85, head_pitch 16.19, shoulder_abduction 17.41 |
| Swimming | 0.69 | hand_forward +2.8, hand_height +2.1, elbow_bend +1.6, arm_swing +1.6 | n 1.33, torso_pitch 23.58, head_pitch 4.42, shoulder_flexion 80.48, elbow_flexion 48.52, toe_out 8.71, shoulder_rotation 13.98 |
| KarateChop | 0.68 | elbow_bend +2.9, hand_height +2.3, hand_forward +1.8, arm_swing +1.7 | s 0.95, n 0.65, m_arm 1.67, m_torso 6.15, m_knee 0.88, m_elbow 0.75, shoulder_abduction 36.64, elbow_flexion 53.66 |
| Tiptoe | 0.68 | toe_out -0.7, knee_bend +0.5, step_length -0.4, foot_lift -0.3 | s 0.39, m_knee 0.48, m_elbow 0.38, torso_pitch 9.96, stance_width -1, toe_out -22.4, shoulder_rotation 40.65, bounce 16.97 |
| Strutting | 0.68 | toe_out +1.2, head_pitch -1.1, pelvis_sway +0.8, stance_width +0.5 | m_elbow 0.29, torso_pitch -11.43, elbow_flexion -21.03, toe_out 13.22 |
| WildLegs | 0.66 | cadence -2.1, foot_lift +1.8, head_sway +1.4, toe_out +1.1 | m_arm 1.6, m_torso 7.86, m_knee 1.28, m_elbow 0.68, head_pitch 11.47, toe_out 10.41 |
| Stiff | 0.66 | foot_lift -1.3, knee_bend -1.0, step_length -0.8, arm_swing +0.6 | s 0.9, m_arm 1.59, m_torso 3.09, m_knee 0.61, toe_out 7.7 |
| OnToesBentForward | 0.66 | torso_lean +3.5, torso_side +2.1, head_sway +2.0, knee_bend +1.4 | m_torso 5.99, m_knee 0.78, torso_pitch 24.08, elbow_flexion 4.73, shoulder_rotation 9.89 |
| Morris | 0.62 | bounce +2.8, elbow_bend +2.2, hand_height +1.6, toe_out -1.3 | m_knee 1.15, torso_pitch -5.1, shoulder_abduction 26.22, elbow_flexion 44.9, toe_out -29.14 |
| HandsBetweenLegs | 0.62 | torso_side +8.4, torso_lean +5.7, pelvis_sway +4.5, stance_width +3.7 | s 1.26, m_torso 7.43, m_knee 0.83, m_elbow 0.1, torso_pitch 8.64, head_pitch 18.52, elbow_flexion -1.75, stance_width 5.11, shoulder_rotation 54.54, bounce 6.23 |
| OnHeels | 0.62 | foot_lift -1.6, step_length -1.3, knee_bend -1.3, arm_swing +0.9 | s 0.58, m_torso 6.3, m_knee 0.49 |
| LeanBack | 0.62 | torso_lean -1.7, knee_bend +1.4, torso_side +1.4, pelvis_height -1.3 | s 1.56, n 1.28, c 23.53, m_arm 0.02, m_knee 0.64, shoulder_flexion -23.54, shoulder_abduction -5.58, stance_width -6.24, toe_out 27.76 |
| SwingArmsRound | 0.61 | arm_swing +2.9, cadence -1.1, hand_out -0.9, hand_height +0.7 | n 0.82, c 1.13, m_arm 1.78, m_elbow 0.41, head_pitch 23.44, shoulder_abduction -6.28, elbow_flexion -8.58, stance_width -1.54 |
| Penguin | 0.60 | step_length -2.9, foot_lift -1.8, toe_out +0.9, knee_bend -0.8 | s 0.58, m_torso 6.3, m_knee 0.49 |
| Waving | 0.58 | arm_swing +1.3, head_sway +0.6, stance_width -0.5, elbow_bend +0.5 | s 1.32, n 0.7, m_arm 1.5, m_torso 9.96, m_knee 0.99, torso_pitch -8.3, elbow_flexion 16.87 |
| BouncyRight | 0.56 | bounce +3.2, pelvis_height +1.0, toe_out -0.7, cadence +0.5 | s 0.52, m_elbow 0.58, head_pitch 10.97, stance_width 2.83, toe_out -20.04, shoulder_rotation 23.85, bounce 26.72 |
| TogetherStep | 0.55 | step_length -3.5, cadence +3.2, head_sway +1.8, arm_swing +1.5 | s 0.31, n 1.39, m_arm 1.51, m_torso 6.8, m_elbow 0.45, shoulder_flexion 15.87, stance_width -5.94, shoulder_rotation -16, bounce 25.28 |
| BouncyLeft | 0.55 | bounce +2.8, pelvis_height +0.7, toe_out -0.6, cadence +0.5 | s 0.52, m_elbow 0.58, head_pitch 10.97, stance_width 2.83, toe_out -20.04, shoulder_rotation 23.85, bounce 26.72 |
| DragRightLeg | 0.53 | step_length -2.9, cadence +2.1, foot_lift -1.4, stance_width -1.0 | s 0.66, m_torso 6.36, m_knee 0.45, m_elbow 0.23, elbow_flexion 12.56, stance_width -6.86, shoulder_rotation -16.68, bounce 18.66 |
| WhirlArms | 0.53 | arm_swing +4.2, hand_height +2.5, torso_side +1.9, cadence -1.6 | m_arm 1.33, m_torso 9.41, m_elbow 0.21, torso_pitch 7.85, head_pitch 16.19, shoulder_abduction 17.41 |
| LookUp | 0.52 | head_pitch -2.1, step_length -0.9, torso_lean -0.8, pelvis_sway +0.7 | s 1.56, n 0.84, m_arm 0.61, m_torso 4.81, torso_pitch -13.1, head_pitch -14.04, elbow_flexion 6.61 |
| SwingShoulders | 0.51 | arm_swing +2.5, cadence -1.7, step_length +1.5, elbow_bend +1.3 | s 1.59, m_arm 1.76, m_knee 0.85, m_elbow 1, torso_pitch -0.8, elbow_flexion -2.73, shoulder_rotation 19.82, bounce 11.83 |
| DragLeftLeg | 0.51 | step_length -2.8, cadence +2.1, foot_lift -1.2, head_pitch +0.9 | n 1.38, m_knee 0.7, shoulder_flexion 6.71, stance_width -5.23, toe_out 5.66, shoulder_rotation 13.68, bounce 2.38 |
| Elated | 0.50 | arm_swing +3.0, bounce +2.6, hand_height +1.2, elbow_bend +1.0 | s 1.15, m_arm 1.65, m_torso 0.6, m_elbow 0.01, head_pitch 15.04, shoulder_flexion 27.75, stance_width 0.72, toe_out -9.8, bounce 28.09 |
| WildArms | 0.48 | arm_swing +4.4, hand_height +2.7, hand_forward +0.8, torso_side +0.7 | c 0.45, m_arm 1.47, m_torso 2.17, m_knee 0.86, torso_pitch 9.76, shoulder_flexion 9.13, stance_width -0.08, shoulder_rotation 20.79 |
| Proud | 0.48 | arm_swing +1.0, elbow_bend +0.9, toe_out -0.5, bounce +0.4 | n 1.28, m_arm 1.08, m_elbow 0.36, torso_pitch 1.58, elbow_flexion 42.64, toe_out -22.87, bounce 9.78 |

최고 유사도 0.7 이상 69종, 0.5~0.7 27종, 0.5 미만 3종 (99종)
