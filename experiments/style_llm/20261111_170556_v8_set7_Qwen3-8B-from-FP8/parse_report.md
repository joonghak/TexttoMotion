# LLM 스타일 파라미터 1단계 결과 (20261111_170556_v8_set7_Qwen3-8B-from-FP8)

/home/jong/models/Qwen3-8B-from-FP8, 프롬프트 v8, 생각 예산 4096토큰, test_commands_7.json, 시드 42, 1단계 통과 25/25, 7.5분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| N1 | 메추라기처럼 종종 걸어 | walk | s 1.4, n 1.25, m_torso 3, m_knee 0.8, torso_pitch 15, head_pitch -15, shoulder_flexion 85, elbow_flexion -30, stance_width 10, toe_out 30 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 2.21 |
| N2 | 고릴라처럼 가슴을 두드리며 걸어 | walk | s 1.8, n 1.25, c 30, m_arm 1.8, m_torso 0, torso_pitch 15, head_pitch 25, shoulder_flexion 85, elbow_flexion 45, stance_width 10, toe_out 30 (m_arm 1.8 -> 0.3 (팔을 85° 듦)) | 통과 | 2.83 |
| N3 | 펭귄 흉내를 내면서 걸어 | walk | c 15, m_torso 6, torso_pitch 15, head_pitch 25, shoulder_abduction 85, stance_width 10, toe_out 30 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 1.26 |
| N4 | 티라노사우루스처럼 걸어 | walk | s 1.8, n 0.55, m_arm 0.4, m_torso 6, torso_pitch 15, head_pitch 25, elbow_flexion -30, stance_width 10, toe_out 30 | 통과 | 1.25 |
| N5 | 수탉처럼 걸어 | walk | s 0.6, n 1.25, m_arm 1.5, torso_pitch -15, head_pitch -15, elbow_flexion 45, stance_width 10, toe_out 30 | 통과 | 0.94 |
| N6 | 고양이처럼 조심스럽게 걸어 | walk | s 0.6, n 0.75, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25, toe_out 30 | 통과 | 0.57 |
| P1 | 어둠 속에서 손으로 더듬으며 걸어 | walk | s 0.6, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25, shoulder_flexion 85 (m_arm 0.4 -> 0.3 (팔을 85° 듦)) | 통과 | 0.57 |
| P2 | 군인처럼 행진하며 걸어 | walk | s 1.4, n 1.25, c 15, m_arm 1.5, m_torso 0, torso_pitch -15, shoulder_flexion 30, stance_width 10, toe_out 30 | 통과 | 2.21 |
| P3 | 요정처럼 사뿐사뿐 걸어 | walk | s 0.3, n 1.45, c 15, m_arm 1.5, m_knee 1.5, torso_pitch 15, shoulder_flexion 85, stance_width 10, toe_out 30 (m_arm 1.5 -> 0.3 (팔을 85° 듦)) | 통과 | 0.55 |
| P4 | 덩치 큰 사람처럼 걸어 | walk | s 1.4, m_arm 1.5, torso_pitch -15, head_pitch -15, elbow_flexion 45, stance_width 10 | 통과 | 1.76 |
| P5 | 패션모델처럼 뽐내며 걸어 | walk | s 1.4, n 1.25, m_arm 1.8, m_torso 0, torso_pitch -15, head_pitch -15, shoulder_flexion 85, elbow_flexion 45, stance_width 10 (m_arm 1.8 -> 0.3 (팔을 85° 듦)) | 통과 | 2.21 |
| P6 | 특공대원처럼 총을 겨눈 자세로 걸어 | walk | s 1.4, n 1.25, m_arm 1.5, torso_pitch -15, head_pitch -15, shoulder_flexion 85, elbow_flexion 45, stance_width 10 (m_arm 1.5 -> 0.3 (팔을 85° 듦)) | 통과 | 2.21 |
| F1 | 뒷짐을 지고 걸어 | walk | torso_pitch 35 | 통과 | 1.26 |
| F2 | 팔짱을 끼고 걸어 | walk | m_arm 0, shoulder_abduction -15, elbow_flexion -30 | 통과 | 1.26 |
| F3 | 양손을 허리에 짚고 걸어 | walk | shoulder_abduction -15 | 통과 | 1.26 |
| F4 | 두 팔을 머리 위로 들고 걸어 | walk | m_arm 1.5, shoulder_flexion 85 (m_arm 1.5 -> 0.3 (팔을 85° 듦)) | 통과 | 1.26 |
| F5 | 발뒤꿈치로 걸어 | walk | toe_out -15 | 통과 | 1.26 |
| F6 | 무릎을 굽힌 채로 걸어 | walk | c 15 | 통과 | 1.26 |
| F7 | 상체를 뒤로 젖히고 걸어 | walk | torso_pitch -15 | 통과 | 1.26 |
| F8 | 발을 바닥에 끌면서 걸어 | walk | n 0.75, m_knee 0.8 | 통과 | 0.94 |
| M1 | 급하게 서둘러 걸어 | walk | s 1.4, n 1.25, m_arm 1.5 | 통과 | 2.21 |
| M2 | 누가 따라오는 것 같아 뒤를 살피며 걸어 | walk | s 0.6, n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 25 | 통과 | 0.57 |
| M3 | 우아하게 걸어 | walk | s 1.4, m_arm 1.5, m_torso 0, torso_pitch 15, head_pitch -15, shoulder_flexion 85, elbow_flexion 45, toe_out 30 (m_arm 1.5 -> 0.3 (팔을 85° 듦)) | 통과 | 1.76 |
| M4 | 외줄을 타듯 균형을 잡으며 걸어 | walk | s 0.6, n 1.25, m_arm 1.5, m_torso 3, torso_pitch 15, toe_out 30 | 통과 | 0.94 |
| M5 | 엉덩이를 씰룩거리며 걸어 | walk | m_torso 10, stance_width 10 | 통과 | 1.26 |
