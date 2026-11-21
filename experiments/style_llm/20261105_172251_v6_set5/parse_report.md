# LLM 스타일 파라미터 1단계 결과 (20261105_172251_v6_set5)

Qwen/Qwen3-4B-Thinking-2507, 프롬프트 v6, 생각 예산 4096토큰, test_commands_5.json, 시드 42, 1단계 통과 17/20, 25.5분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| A1 | 기운 없이 축 처져서 달려 | run | run: s 0.6, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 35, head_pitch 25 | 통과 | 1.60 |
| A2 | 고개를 깊이 숙인 채로 점프해 | jump | jump: head_pitch 25 | 통과 | 0.61 |
| A3 | 자세를 낮추고 무릎을 굽힌 채 점프해 | jump | jump: c 30, torso_pitch 35 | 통과 | 0.61 |
| A4 | 피곤한 몸으로 느릿느릿 돌려차기해 | spinkick | spinkick: n 0.55, c 15, m_arm 0.4, m_torso 6, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 0.21 |
| A5 | 허리를 뒤로 젖히고 발차기해 | kick | kick: torso_pitch -15 | 통과 | 0.73 |
| A6 | 좀비처럼 두 팔을 앞으로 내밀고 달려 | run | run: s 0.6, n 0.55, m_torso 6, torso_pitch 15, shoulder_flexion 85, elbow_flexion -30 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 1.18 |
| B1 | 술 취한 사람처럼 비틀비틀 달려 | run | run: n 0.75, m_torso 10, head_pitch 25 | 통과 | 2.67 |
| B2 | 당당하게 가슴을 펴고 달려 | run | run: torso_pitch -15 | 통과 | 3.56 |
| B3 | 로봇처럼 뻣뻣하게 달려 | run | run: m_torso 0, m_knee 0.8, m_elbow 0, elbow_flexion 45 | 통과 | 3.56 |
| B4 | 두 팔을 앞으로 쭉 뻗은 채 점프해 | jump | jump: shoulder_flexion 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 0.61 |
| B5 | 허리가 굽은 노인처럼 점프해 | jump | jump: torso_pitch 35 | 통과 | 0.61 |
| B6 | 두 팔을 옆으로 벌린 채 발차기해 | kick | kick: shoulder_abduction 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 0.73 |
| W1 | 다리를 넓게 벌리고 걸어 | walk | stance_width 10 | 통과 | 1.26 |
| W2 | 아기처럼 다리를 벌리고 아장아장 걸어 | walk | m_torso 10, stance_width 10 | 통과 | 1.26 |
| W3 | 카우보이처럼 다리를 벌리고 느긋하게 걸어 | walk | n 0.75, stance_width 10 | 통과 | 0.94 |
| W4 | 기진맥진해서 터덜터덜 걸어 | walk | s 0.6, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 0.57 |
| C1 | 다리를 45도로 쫙 벌리고 걸어 | 거절 | stance_width 10 | 실패 | 1.26 |
| C2 | 옆으로 게걸음으로 걸어 | 거절 | m_torso 10 | 실패 | 1.26 |
| C3 | 물구나무 서서 걸어 | 거절 | c 15, m_torso 0, m_knee 0.8, m_elbow 0 | 실패 | 1.26 |
| C4 | 점프한 다음에 바로 발차기해 | 거절 | 거절 (not_expressible) | 통과 | - |
