# LLM 스타일 파라미터 1단계 결과 (20261031_221501_v4_set4)

Qwen/Qwen3-4B-Thinking-2507, 프롬프트 v4, 생각 예산 4096토큰, test_commands_4.json, 시드 42, 1단계 통과 22/22, 22.9분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| A1 | 상체를 앞으로 기울인 채 뛰어 | run | run: torso_pitch 20 | 통과 | 3.56 |
| A2 | 최대한 빠르게 달려 | run | run: s 2, n 1.5 | 통과 | 10.68 |
| A3 | 앞으로 멀리 점프해 | jump | jump: s 1.25 | 통과 | 0.76 |
| A4 | 양팔을 쫙 펴고 점프해 | jump | jump: shoulder_abduction 80 (m_arm 1 -> 0.3 (팔을 80° 듦)) | 통과 | 0.61 |
| A5 | 그 자리에서 발차기해 | kick | kick: 기본값 | 통과 | 0.73 |
| A6 | 천천히 달려 | run | run: n 0.75 | 통과 | 2.67 |
| A7 | 한 바퀴 돌면서 발차기해 | spinkick | spinkick: 기본값 | 통과 | 0.38 |
| A8 | 무릎을 굽히고 낮은 자세로 달려 | run | run: c 20 | 통과 | 3.56 |
| A9 | 몸을 좌우로 흔들면서 달려 | run | run: m_torso 2 | 통과 | 3.56 |
| A10 | 1분에 180걸음 속도로 달려 | run | run: n 1.2 | 통과 | 4.27 |
| B1 | 지쳐서 터벅터벅 달려 | run | run: s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 2.14 |
| B2 | 좀비처럼 팔을 앞으로 뻗고 달려 | run | run: s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 | 통과 | 1.82 |
| B3 | 고개를 푹 숙이고 점프해 | jump | jump: head_pitch 25 | 통과 | 0.61 |
| B4 | 팔꿈치를 굽히고 힘차게 발차기해 | kick | kick: s 1.2, n 1.15, c 20 | 통과 | 1.01 |
| B5 | 상체를 뒤로 젖힌 채 발차기해 | kick | kick: torso_pitch -10 | 통과 | 0.73 |
| B6 | 무릎을 굽히고 낮게 점프해 | jump | jump: n 1.25, c 20 | 통과 | 0.76 |
| W1 | 팔을 크게 흔들며 걸어 | walk | m_arm 1.5 | 통과 | 1.26 |
| W2 | 느릿느릿 걸어 | walk | n 0.75 | 통과 | 0.94 |
| C1 | 수영해 | 거절 | 거절 (not_supported) | 통과 | - |
| C2 | 뒤로 공중제비 돌아 | 거절 | 거절 (not_supported) | 통과 | - |
| C3 | 오른발로만 깡충깡충 뛰어 | 거절 | 거절 (not_expressible) | 통과 | - |
| C4 | 달리다가 점프해 | 거절 | 거절 (not_expressible) | 통과 | - |
