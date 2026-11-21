# LLM 스타일 파라미터 1단계 결과 (20261116_231926_v14_set7_gpt-5.6-terra)

openai/gpt-5.6-terra, 프롬프트 v14, 생각 예산 4096토큰, test_commands_7.json, 시드 42, 1단계 통과 25/25, 1.6분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| N1 | 메추라기처럼 종종 걸어 | walk | s 0.45, n 1.5, m_arm 0.2, m_knee 0.75, torso_pitch 12, shoulder_abduction -15, bounce 15 | 통과 | 0.85 |
| N2 | 고릴라처럼 가슴을 두드리며 걸어 | walk | s 0.7, n 0.75, c 20, m_arm 1.5, m_torso 6, m_knee 0.8, torso_pitch 25, head_pitch 15, shoulder_flexion 45, elbow_flexion 60, stance_width 10, shoulder_rotation 60 (m_arm 1.5 -> 0.3 (팔을 45° 듦)) | 통과 | 0.66 |
| N3 | 펭귄 흉내를 내면서 걸어 | walk | s 0.65, n 0.8, c 10, m_arm 0.4, m_torso 7, m_knee 0.7, shoulder_abduction -15, stance_width 10, toe_out 25 | 통과 | 0.66 |
| N4 | 티라노사우루스처럼 걸어 | walk | s 0.75, n 0.8, c 12, m_arm 0, m_knee 1.3, torso_pitch 20, head_pitch 15, shoulder_flexion 35, elbow_flexion 60, stance_width 8 | 통과 | 0.76 |
| N5 | 수탉처럼 걸어 | walk | s 0.65, n 1.25, c 15, m_arm 0.3, m_torso 5, m_knee 1.5, torso_pitch -10, head_pitch -15, shoulder_abduction -15, toe_out 25 | 통과 | 1.02 |
| N6 | 고양이처럼 조심스럽게 걸어 | walk | s 0.65, n 0.7, c 20, m_arm 0.3, m_knee 0.7, torso_pitch 20, shoulder_flexion 20, elbow_flexion 40, stance_width -5, foot_pitch 20 | 통과 | 0.57 |
| P1 | 어둠 속에서 손으로 더듬으며 걸어 | walk | s 0.7, n 0.6, c 15, m_arm 0.3, m_knee 0.75, torso_pitch 15, head_pitch 15, shoulder_flexion 55, elbow_flexion 35 | 통과 | 0.53 |
| P2 | 군인처럼 행진하며 걸어 | walk | s 1.1, n 1.05, m_arm 0.35, m_torso 0, m_knee 1.35, m_elbow 0, torso_pitch -3, head_pitch -8, elbow_flexion 20 | 통과 | 1.46 |
| P3 | 요정처럼 사뿐사뿐 걸어 | walk | s 0.75, n 0.9, m_arm 0.5, m_knee 0.7, torso_pitch -5, head_pitch -8, shoulder_abduction 20, elbow_flexion 20, bounce 8 | 통과 | 0.85 |
| P4 | 덩치 큰 사람처럼 걸어 | walk | s 1.3, n 0.75, m_arm 1.2, m_torso 5, m_knee 0.8, stance_width 10, bounce 12 | 통과 | 1.23 |
| P5 | 패션모델처럼 뽐내며 걸어 | walk | s 1.4, n 0.9, m_arm 1.4, torso_pitch -15, head_pitch -15, stance_width 4, toe_out 12 | 통과 | 1.59 |
| P6 | 특공대원처럼 총을 겨눈 자세로 걸어 | walk | m_arm 0.3, shoulder_flexion 85, elbow_flexion 15, shoulder_rotation 25 | 통과 | 1.26 |
| F1 | 뒷짐을 지고 걸어 | walk | m_arm 0.3, shoulder_flexion -45, elbow_flexion 60 | 통과 | 1.26 |
| F2 | 팔짱을 끼고 걸어 | walk | m_arm 0, shoulder_flexion 30, elbow_flexion 60, shoulder_rotation 60 | 통과 | 1.26 |
| F3 | 양손을 허리에 짚고 걸어 | walk | m_arm 0.3, shoulder_flexion -25, shoulder_abduction 35, elbow_flexion 60, shoulder_rotation 45 | 통과 | 1.26 |
| F4 | 두 팔을 머리 위로 들고 걸어 | walk | m_arm 0.3, shoulder_abduction 155 | 통과 | 1.26 |
| F5 | 발뒤꿈치로 걸어 | walk | foot_pitch -20 | 통과 | 1.26 |
| F6 | 무릎을 굽힌 채로 걸어 | walk | c 20, m_knee 0.75 | 통과 | 1.26 |
| F7 | 상체를 뒤로 젖히고 걸어 | walk | torso_pitch -15 | 통과 | 1.26 |
| F8 | 발을 바닥에 끌면서 걸어 | walk | m_knee 0.4 | 통과 | 1.26 |
| M1 | 급하게 서둘러 걸어 | walk | s 1.1, n 1.35, m_arm 1.4 | 통과 | 1.87 |
| M2 | 누가 따라오는 것 같아 뒤를 살피며 걸어 | walk | n 0.8, m_arm 0.5, head_yaw 60 | 통과 | 1.01 |
| M3 | 우아하게 걸어 | walk | s 1.2, n 0.9, m_arm 0.8, m_torso 0.5, torso_pitch -8, head_pitch -8, elbow_flexion 25 | 통과 | 1.36 |
| M4 | 외줄을 타듯 균형을 잡으며 걸어 | walk | s 0.7, n 0.6, c 15, m_arm 0.3, m_knee 0.7, torso_pitch 15, head_pitch 25, shoulder_abduction 80, stance_width -8 | 통과 | 0.53 |
| M5 | 엉덩이를 씰룩거리며 걸어 | walk | n 0.85, m_torso 8, stance_width 6 | 통과 | 1.07 |
