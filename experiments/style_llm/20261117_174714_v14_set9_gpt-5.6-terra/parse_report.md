# LLM 스타일 파라미터 1단계 결과 (20261117_174714_v14_set9_gpt-5.6-terra)

openai/gpt-5.6-terra, 프롬프트 v14, 생각 예산 4096토큰, test_commands_9.json, 시드 42, 1단계 통과 10/10, 0.5분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| S1 | 오른쪽 다리를 절뚝거리며 걸어 | walk | right_m_knee 0.4 | 통과 | 1.26 |
| S2 | 왼손을 번쩍 들고 걸어 | walk | left_m_arm 0.3, left_shoulder_abduction 160 | 통과 | 1.26 |
| S3 | 오른손으로 전화를 받으면서 걸어 | walk | right_m_arm 0.3, right_shoulder_abduction 70, right_shoulder_rotation -20, right_elbow_flexion 60 | 통과 | 1.26 |
| S4 | 왼쪽 다리를 질질 끌면서 걸어 | walk | s 0.75, n 0.8, m_arm 0.6, torso_roll -12, left_m_knee 0.4, left_toe_out -10 | 통과 | 0.76 |
| S5 | 오른손에 지팡이를 짚고 걸어 | walk | s 0.75, n 0.7, m_arm 0.4, m_knee 0.8, torso_pitch 15, torso_roll 10, right_m_arm 0, right_m_elbow 0, right_shoulder_flexion -20, right_elbow_flexion 35 | 통과 | 0.66 |
| S6 | 몸을 오른쪽으로 기울인 채 걸어 | walk | torso_roll 20 | 통과 | 1.26 |
| S7 | 다친 왼팔을 감싸 쥐고 걸어 | walk | n 0.8, m_arm 0.5, right_m_arm 0.3, right_shoulder_flexion 35, right_shoulder_rotation 45, right_elbow_flexion 60, left_m_arm 0, left_shoulder_flexion 45, left_shoulder_rotation 45, left_elbow_flexion 60 | 통과 | 1.01 |
| S8 | 무거운 가방을 왼쪽 어깨에 메고 걸어 | walk | s 0.85, n 0.85, m_arm 0.7, stance_width 5, torso_roll -15, left_m_arm 0.1, left_shoulder_flexion 20, left_elbow_flexion 60 | 통과 | 0.91 |
| S9 | 고개를 왼쪽으로 갸웃한 채 걸어 | walk | head_roll -20 | 통과 | 1.26 |
| S10 | 한쪽 다리가 나무 의족인 해적처럼 걸어 | walk | s 0.8, n 0.75, m_arm 0.8, m_torso 5, torso_pitch -10, head_pitch -10, stance_width 6, right_m_knee 0.4, right_toe_out 15 | 통과 | 0.76 |
