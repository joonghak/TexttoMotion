# LLM 스타일 파라미터 1단계 결과 (20261116_120656_v13_set6_gpt-5.6-sol)

openai/gpt-5.6-sol, 프롬프트 v13, 생각 예산 4096토큰, test_commands_6.json, 시드 42, 1단계 통과 25/25, 1.3분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| N1 | 펭귄처럼 걸어 | walk | s 0.5, n 0.9, m_arm 0.3, m_torso 10, m_knee 0.5, m_elbow 0, shoulder_abduction 30, elbow_flexion -30, stance_width 8, toe_out 30 | 통과 | 0.57 |
| N2 | 닭처럼 걸어 | walk | s 0.55, n 1.4, c 10, m_arm 0.3, m_torso 5, m_knee 1.3, torso_pitch 20, head_pitch 25, shoulder_abduction 45, elbow_flexion 60, stance_width 6, toe_out 25, bounce 15 | 통과 | 0.97 |
| N3 | 고양이처럼 걸어 | walk | s 0.7, n 0.75, c 15, m_arm 0.3, m_torso 3, m_knee 0.8, torso_pitch 15, shoulder_flexion 45, elbow_flexion 60, stance_width -4, toe_out -10, shoulder_rotation 20, foot_pitch 20 | 통과 | 0.66 |
| N4 | 공룡처럼 걸어 | walk | s 1.4, n 0.75, c 10, m_arm 0.3, m_torso 7, m_knee 1.3, torso_pitch 30, head_pitch -10, shoulder_flexion 35, elbow_flexion 60, stance_width 10, toe_out 25, shoulder_rotation 30, bounce 15 | 통과 | 1.32 |
| N5 | 새처럼 날개를 퍼덕이며 걸어 | walk | s 0.6, n 1.3, m_arm 1.8, m_knee 0.8, torso_pitch 10, shoulder_abduction 80, elbow_flexion -30, toe_out 15 (m_arm 1.8 -> 0.3 (팔을 80° 듦)) | 통과 | 0.98 |
| N6 | 오리처럼 뒤뚱뒤뚱 걸어 | walk | s 0.6, n 0.75, c 10, m_arm 0.3, m_torso 10, m_knee 0.8, shoulder_abduction 30, elbow_flexion 60, stance_width 10, toe_out 30 | 통과 | 0.57 |
| P1 | 좀비처럼 걸어 | walk | s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 | 통과 | 0.64 |
| P2 | 로봇처럼 걸어 | walk | m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 | 통과 | 1.26 |
| P3 | 노인처럼 걸어 | walk | s 0.6, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 30, head_pitch -10 | 통과 | 0.60 |
| P4 | 수도승처럼 걸어 | walk | s 0.75, n 0.65, m_arm 0, m_torso 0, m_knee 0.75, head_pitch 25, shoulder_flexion 20, elbow_flexion 60, stance_width -4, shoulder_rotation 60 | 통과 | 0.61 |
| P5 | 술 취한 사람처럼 걸어 | walk | s 0.75, n 0.65, m_arm 1.4, m_torso 10, shoulder_abduction 30, stance_width 7, head_roll 15, weave 0.35 | 통과 | 0.61 |
| P6 | 슈퍼맨처럼 걸어 | walk | s 1.4, m_arm 1.7, m_torso 3, torso_pitch -12, head_pitch -15, elbow_flexion 35, stance_width 7, toe_out 15 | 통과 | 1.76 |
| F1 | 팔자걸음으로 걸어 | walk | toe_out 30 | 통과 | 1.26 |
| F2 | 안짱걸음으로 걸어 | walk | stance_width -4, toe_out -30 | 통과 | 1.26 |
| F3 | 다리를 넓게 벌리고 걸어 | walk | stance_width 10 | 통과 | 1.26 |
| F4 | 무릎을 높이 들고 걸어 | walk | c 15, m_knee 1.5 | 통과 | 1.26 |
| F5 | 까치발로 걸어 | walk | foot_pitch 20 | 통과 | 1.26 |
| F6 | 몸을 웅크리고 걸어 | walk | c 20, m_knee 0.75, torso_pitch 20, head_pitch 25 | 통과 | 1.26 |
| F7 | 상체를 앞으로 숙이고 걸어 | walk | torso_pitch 20 | 통과 | 1.26 |
| F8 | 비행기처럼 팔을 벌리고 걸어 | walk | m_arm 0.3, shoulder_abduction 80, elbow_flexion -30 | 통과 | 1.26 |
| M1 | 우울하게 걸어 | walk | s 0.8, n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 25 | 통과 | 0.76 |
| M2 | 신나게 걸어 | walk | s 1.15, n 1.25, m_arm 1.8, bounce 10 | 통과 | 1.81 |
| M3 | 화가 나서 쿵쿵 걸어 | walk | s 1.2, n 1.25, m_arm 1.8, m_knee 1.4, torso_pitch 15, elbow_flexion 45, bounce 20 | 통과 | 1.89 |
| M4 | 당당하게 걸어 | walk | s 1.15, m_arm 1.4, torso_pitch -12, head_pitch -10 | 통과 | 1.45 |
| M5 | 뻣뻣하게 걸어 | walk | m_arm 0.3, m_torso 0, m_knee 0.5, m_elbow 0 | 통과 | 1.26 |
