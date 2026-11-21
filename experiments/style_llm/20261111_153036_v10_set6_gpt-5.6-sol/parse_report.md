# LLM 스타일 파라미터 1단계 결과 (20261111_153036_v10_set6_gpt-5.6-sol)

openai/gpt-5.6-sol, 프롬프트 v10, 생각 예산 4096토큰, test_commands_6.json, 시드 42, 1단계 통과 25/25, 10.8분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| N1 | 펭귄처럼 걸어 | walk | s 0.55, n 0.8, c 10, m_arm 0.3, m_torso 10, m_knee 0.7, m_elbow 0, shoulder_abduction 35, elbow_flexion -20, stance_width 8, toe_out 30 | 통과 | 0.55 |
| N2 | 닭처럼 걸어 | walk | s 0.5, n 1.4, c 15, m_arm 0.3, m_torso 3, m_knee 1.4, torso_pitch 20, shoulder_abduction 35, elbow_flexion 60, stance_width 6, toe_out 30, bounce 10 | 통과 | 0.88 |
| N3 | 고양이처럼 걸어 | walk | s 0.65, n 0.75, c 20, m_arm 0.3, m_torso 2, m_knee 0.7, torso_pitch 20, shoulder_flexion 20, elbow_flexion 40, stance_width -8 | 통과 | 0.61 |
| N4 | 공룡처럼 걸어 | walk | s 1.3, n 0.7, c 15, m_arm 0.3, m_torso 7, m_knee 1.3, m_elbow 0, torso_pitch 25, head_pitch 10, shoulder_flexion 35, elbow_flexion 60, stance_width 10, toe_out 25, shoulder_rotation 30, bounce 20 | 통과 | 1.15 |
| N5 | 새처럼 날개를 퍼덕이며 걸어 | walk | s 0.6, n 1.4, m_arm 1.8, m_torso 5, m_knee 0.8, shoulder_abduction 80, elbow_flexion -30, stance_width -4, toe_out 20, bounce 10 (m_arm 1.8 -> 0.3 (팔을 80° 듦)) | 통과 | 1.06 |
| N6 | 오리처럼 뒤뚱뒤뚱 걸어 | walk | s 0.6, n 0.85, c 15, m_arm 0.3, m_torso 10, m_knee 0.7, elbow_flexion 50, stance_width 10, toe_out 30 | 통과 | 0.64 |
| P1 | 좀비처럼 걸어 | walk | s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 | 통과 | 0.64 |
| P2 | 로봇처럼 걸어 | walk | m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 | 통과 | 1.26 |
| P3 | 노인처럼 걸어 | walk | s 0.6, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 30, head_pitch -10 | 통과 | 0.60 |
| P4 | 수도승처럼 걸어 | walk | s 0.7, n 0.65, m_arm 0.3, m_torso 0, m_knee 0.7, head_pitch 25, shoulder_flexion 20, elbow_flexion 50, stance_width -4, shoulder_rotation 45 | 통과 | 0.57 |
| P5 | 술 취한 사람처럼 걸어 | walk | s 0.8, n 0.65, m_arm 1.4, m_torso 10, m_knee 0.8, shoulder_abduction 35, elbow_flexion 20, stance_width 8, toe_out 20 | 통과 | 0.66 |
| P6 | 슈퍼맨처럼 걸어 | walk | s 1.5, n 0.9, m_arm 1.8, torso_pitch -15, head_pitch -15, elbow_flexion 30, stance_width 6 | 통과 | 1.70 |
| F1 | 팔자걸음으로 걸어 | walk | toe_out 30 | 통과 | 1.26 |
| F2 | 안짱걸음으로 걸어 | walk | toe_out -30 | 통과 | 1.26 |
| F3 | 다리를 넓게 벌리고 걸어 | walk | stance_width 10 | 통과 | 1.26 |
| F4 | 무릎을 높이 들고 걸어 | walk | c 15, m_knee 1.5 | 통과 | 1.26 |
| F5 | 까치발로 걸어 | walk | s 0.6, n 0.8, c 10, m_arm 0.3, m_knee 0.7 | 통과 | 0.60 |
| F6 | 몸을 웅크리고 걸어 | walk | c 25, m_knee 0.75, torso_pitch 25, head_pitch 25, shoulder_flexion 20, elbow_flexion 40 | 통과 | 1.26 |
| F7 | 상체를 앞으로 숙이고 걸어 | walk | torso_pitch 20 | 통과 | 1.26 |
| F8 | 비행기처럼 팔을 벌리고 걸어 | walk | m_arm 0.3, shoulder_abduction 80, elbow_flexion -30 | 통과 | 1.26 |
| M1 | 우울하게 걸어 | walk | s 0.8, n 0.7, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 0.71 |
| M2 | 신나게 걸어 | walk | s 1.15, n 1.25, m_arm 1.7, m_knee 1.2, bounce 10 | 통과 | 1.81 |
| M3 | 화가 나서 쿵쿵 걸어 | walk | s 1.15, n 1.25, m_arm 1.7, m_knee 1.4, torso_pitch 15, elbow_flexion 45, bounce 20 | 통과 | 1.81 |
| M4 | 당당하게 걸어 | walk | s 1.15, m_arm 1.4, torso_pitch -12, head_pitch -10 | 통과 | 1.45 |
| M5 | 뻣뻣하게 걸어 | walk | m_arm 0.3, m_torso 0, m_elbow 0 | 통과 | 1.26 |
