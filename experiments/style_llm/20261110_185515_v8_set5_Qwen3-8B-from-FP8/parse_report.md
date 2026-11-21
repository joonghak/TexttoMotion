# LLM 스타일 파라미터 1단계 결과 (20261110_185515_v8_set5_Qwen3-8B-from-FP8)

/home/jong/models/Qwen3-8B-from-FP8, 프롬프트 v8, 생각 예산 4096토큰, test_commands_5.json, 시드 42, 1단계 통과 16/20, 7.4분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| A1 | 기운 없이 축 처져서 달려 | run | run: s 0.6, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 1.60 |
| A2 | 고개를 깊이 숙인 채로 점프해 | jump | jump: head_pitch 25 | 통과 | 0.61 |
| A3 | 자세를 낮추고 무릎을 굽힌 채 점프해 | jump | jump: c 30, torso_pitch 15 | 통과 | 0.61 |
| A4 | 피곤한 몸으로 느릿느릿 돌려차기해 | spinkick | spinkick: s 0.6, n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 25 | 통과 | 0.17 |
| A5 | 허리를 뒤로 젖히고 발차기해 | kick | kick: torso_pitch -15 | 통과 | 0.73 |
| A6 | 좀비처럼 두 팔을 앞으로 내밀고 달려 | run | run: s 0.6, n 0.75, m_knee 0.8, m_elbow 0, torso_pitch 15, shoulder_flexion 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 1.60 |
| B1 | 술 취한 사람처럼 비틀비틀 달려 | run | run: s 0.6, n 0.75, m_arm 1.5, m_torso 6, m_knee 0.8, m_elbow 0, torso_pitch 15, head_pitch 25, stance_width 10 | 통과 | 1.60 |
| B2 | 당당하게 가슴을 펴고 달려 | run | run: s 1.4, m_arm 1.5, torso_pitch -15, head_pitch -15 | 통과 | 4.98 |
| B3 | 로봇처럼 뻣뻣하게 달려 | run | 거절 (invalid_output) | 실패 | - |
| B4 | 두 팔을 앞으로 쭉 뻗은 채 점프해 | jump | jump: shoulder_flexion 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 0.61 |
| B5 | 허리가 굽은 노인처럼 점프해 | jump | jump: n 0.75, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 35 | 통과 | 0.46 |
| B6 | 두 팔을 옆으로 벌린 채 발차기해 | kick | kick: shoulder_abduction 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | 0.73 |
| W1 | 다리를 넓게 벌리고 걸어 | walk | stance_width 10 | 통과 | 1.26 |
| W2 | 아기처럼 다리를 벌리고 아장아장 걸어 | walk | m_torso 6, stance_width 10 | 통과 | 1.26 |
| W3 | 카우보이처럼 다리를 벌리고 느긋하게 걸어 | walk | s 1.4, n 0.75, m_arm 1.5, stance_width 10 | 통과 | 1.32 |
| W4 | 기진맥진해서 터덜터덜 걸어 | walk | s 0.6, n 0.75, m_arm 0.4, m_torso 6, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 0.57 |
| C1 | 다리를 45도로 쫙 벌리고 걸어 | 거절 | stance_width 10 | 실패 | 1.26 |
| C2 | 옆으로 게걸음으로 걸어 | 거절 | m_torso 6, stance_width 10 | 실패 | 1.26 |
| C3 | 물구나무 서서 걸어 | 거절 | m_torso 6, stance_width 10, toe_out 30 | 실패 | 1.26 |
| C4 | 점프한 다음에 바로 발차기해 | 거절 | 거절 (not_expressible) | 통과 | - |
