# LLM 스타일 파라미터 1단계 결과 (20261103_234114_v5_set5)

Qwen/Qwen3-4B-Thinking-2507, 프롬프트 v5, 생각 예산 4096토큰, test_commands_5.json, 시드 42, 1단계 통과 19/20, 31.3분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| A1 | 기운 없이 축 처져서 달려 | run | run: s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 2.14 |
| A2 | 고개를 깊이 숙인 채로 점프해 | jump | jump: head_pitch 25 | 통과 | 0.61 |
| A3 | 자세를 낮추고 무릎을 굽힌 채 점프해 | jump | jump: n 1.25, c 20 | 통과 | 0.76 |
| A4 | 피곤한 몸으로 느릿느릿 돌려차기해 | spinkick | spinkick: s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 0.23 |
| A5 | 허리를 뒤로 젖히고 발차기해 | kick | kick: torso_pitch -12 | 통과 | 0.73 |
| A6 | 좀비처럼 두 팔을 앞으로 내밀고 달려 | run | run: s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 | 통과 | 1.82 |
| B1 | 술 취한 사람처럼 비틀비틀 달려 | run | run: n 0.6, m_torso 10 | 통과 | 2.14 |
| B2 | 당당하게 가슴을 펴고 달려 | run | run: s 1.15, m_arm 1.4, torso_pitch -12, head_pitch -10 | 통과 | 4.09 |
| B3 | 로봇처럼 뻣뻣하게 달려 | run | run: m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 | 통과 | 3.56 |
| B4 | 두 팔을 앞으로 쭉 뻗은 채 점프해 | jump | jump: shoulder_flexion 85, elbow_flexion -30 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 0.61 |
| B5 | 허리가 굽은 노인처럼 점프해 | jump | jump: s 0.6, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 30, head_pitch -10 | 통과 | 0.29 |
| B6 | 두 팔을 옆으로 벌린 채 발차기해 | kick | kick: shoulder_abduction 80 (m_arm 1 -> 0.3 (팔을 80° 듦)) | 통과 | 0.73 |
| W1 | 다리를 넓게 벌리고 걸어 | walk | stance_width 10 | 통과 | 1.26 |
| W2 | 아기처럼 다리를 벌리고 아장아장 걸어 | walk | n 0.6, m_torso 10, stance_width 10 | 통과 | 0.76 |
| W3 | 카우보이처럼 다리를 벌리고 느긋하게 걸어 | walk | s 0.8, n 0.6, stance_width 10 | 통과 | 0.60 |
| W4 | 기진맥진해서 터덜터덜 걸어 | walk | s 0.8, n 0.75, m_arm 0.4, m_torso 10, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 0.76 |
| C1 | 다리를 45도로 쫙 벌리고 걸어 | 거절 | 거절 (not_expressible) | 통과 | - |
| C2 | 옆으로 게걸음으로 걸어 | 거절 | 거절 (not_expressible) | 통과 | - |
| C3 | 물구나무 서서 걸어 | 거절 | s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 실패 | 0.76 |
| C4 | 점프한 다음에 바로 발차기해 | 거절 | 거절 (not_expressible) | 통과 | - |
