# LLM 스타일 파라미터 1단계 결과 (20261105_161101_v6_set6)

Qwen/Qwen3-4B-Thinking-2507, 프롬프트 v6, 생각 예산 4096토큰, test_commands_6.json, 시드 42, 1단계 통과 25/25, 30.5분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| N1 | 펭귄처럼 걸어 | walk | n 0.55, m_torso 10, stance_width 10 | 통과 | 0.69 |
| N2 | 닭처럼 걸어 | walk | n 0.55, m_torso 10 | 통과 | 0.69 |
| N3 | 고양이처럼 걸어 | walk | s 0.6, n 1.25, c 30, m_arm 0.4, m_torso 3, m_knee 0.8, torso_pitch 15, head_pitch -15 | 통과 | 0.94 |
| N4 | 공룡처럼 걸어 | walk | n 0.75, c 30, torso_pitch 35, head_pitch 25, stance_width 10 | 통과 | 0.94 |
| N5 | 새처럼 날개를 퍼덕이며 걸어 | walk | n 1.25, m_arm 1.8, shoulder_abduction 85 (m_arm 1.8 -> 0.3 (팔을 85° 듦)) | 통과 | 1.57 |
| N6 | 오리처럼 뒤뚱뒤뚱 걸어 | walk | m_torso 10, stance_width 10 | 통과 | 1.26 |
| P1 | 좀비처럼 걸어 | walk | s 0.6, n 0.55, m_torso 6, torso_pitch 15, shoulder_flexion 85, elbow_flexion -30 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 0.42 |
| P2 | 로봇처럼 걸어 | walk | m_torso 0, m_knee 0.8, m_elbow 0, elbow_flexion 45 | 통과 | 1.26 |
| P3 | 노인처럼 걸어 | walk | s 0.6, n 0.75, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 35, head_pitch -15 | 통과 | 0.57 |
| P4 | 수도승처럼 걸어 | walk | s 0.6, n 0.75, c 15, m_arm 0.4, m_knee 0.8, head_pitch 25 | 통과 | 0.57 |
| P5 | 술 취한 사람처럼 걸어 | walk | s 0.6, n 0.55, m_torso 10, torso_pitch 15, head_pitch 25, elbow_flexion -30 | 통과 | 0.42 |
| P6 | 슈퍼맨처럼 걸어 | walk | s 1.8, n 1.25, m_arm 1.8, m_torso 0, torso_pitch 15, head_pitch -15 | 통과 | 2.83 |
| F1 | 팔자걸음으로 걸어 | walk | shoulder_abduction 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 1.26 |
| F2 | 안짱걸음으로 걸어 | walk | n 0.55, m_torso 10 | 통과 | 0.69 |
| F3 | 다리를 넓게 벌리고 걸어 | walk | stance_width 10 | 통과 | 1.26 |
| F4 | 무릎을 높이 들고 걸어 | walk | c 30 | 통과 | 1.26 |
| F5 | 까치발로 걸어 | walk | m_knee 0.7 | 통과 | 1.26 |
| F6 | 몸을 웅크리고 걸어 | walk | torso_pitch 35 | 통과 | 1.26 |
| F7 | 상체를 앞으로 숙이고 걸어 | walk | torso_pitch 15 | 통과 | 1.26 |
| F8 | 비행기처럼 팔을 벌리고 걸어 | walk | shoulder_abduction 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 1.26 |
| M1 | 우울하게 걸어 | walk | s 0.6, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 35, head_pitch 25 | 통과 | 0.57 |
| M2 | 신나게 걸어 | walk | s 1.4, n 1.25, m_arm 1.8, torso_pitch 15 | 통과 | 2.21 |
| M3 | 화가 나서 쿵쿵 걸어 | walk | n 1.25, c 15, m_arm 1.5, m_knee 1.5 | 통과 | 1.57 |
| M4 | 당당하게 걸어 | walk | s 1.4, m_arm 1.5, torso_pitch -15, head_pitch -15 | 통과 | 1.76 |
| M5 | 뻣뻣하게 걸어 | walk | m_torso 0, m_elbow 0 | 통과 | 1.26 |
