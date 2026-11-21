| ID | 명령 | 값 기준 | v5 답 | v5 기준 | v8 답 | v8 기준 | v8 답 | v8 기준 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | 기운 없이 축 처져서 달려 | torso_pitch >= 15 and head_pitch >= 25 and s * n < 1 | run: s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | run: s 0.6, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | run: s 0.6, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 |
| A2 | 고개를 깊이 숙인 채로 점프해 | head_pitch >= 25 | jump: head_pitch 25 | 통과 | jump: head_pitch 25 | 통과 | jump: head_pitch 25 | 통과 |
| A3 | 자세를 낮추고 무릎을 굽힌 채 점프해 | c >= 15 | jump: n 1.25, c 20 | 통과 | jump: c 30 | 통과 | jump: c 30, torso_pitch 15 | 통과 |
| A4 | 피곤한 몸으로 느릿느릿 돌려차기해 | torso_pitch >= 15 and head_pitch >= 25 and n <= 0.8 | spinkick: s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | spinkick: s 0.6, n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 25 | 통과 | spinkick: s 0.6, n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 25 | 통과 |
| A5 | 허리를 뒤로 젖히고 발차기해 | torso_pitch <= -15 | kick: torso_pitch -12 | 실패 | kick: torso_pitch -15 | 통과 | kick: torso_pitch -15 | 통과 |
| A6 | 좀비처럼 두 팔을 앞으로 내밀고 달려 | shoulder_flexion >= 70 | run: s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 | 통과 | run: s 0.6, n 0.55, m_torso 6, torso_pitch 15, shoulder_flexion 85, elbow_flexion -30 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | run: s 0.6, n 0.75, m_knee 0.8, m_elbow 0, torso_pitch 15, shoulder_flexion 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 |
| B1 | 술 취한 사람처럼 비틀비틀 달려 | m_torso >= 5 | run: n 0.6, m_torso 10 | 통과 | run: s 0.6, n 0.75, m_torso 10, torso_pitch 15 | 통과 | run: s 0.6, n 0.75, m_arm 1.5, m_torso 6, m_knee 0.8, m_elbow 0, torso_pitch 15, head_pitch 25, stance_width 10 | 통과 |
| B2 | 당당하게 가슴을 펴고 달려 | torso_pitch <= -10 and m_arm > 1 | run: s 1.15, m_arm 1.4, torso_pitch -12, head_pitch -10 | 통과 | run: s 1.4, m_arm 1.5, torso_pitch -15, head_pitch -15 | 통과 | run: s 1.4, m_arm 1.5, torso_pitch -15, head_pitch -15 | 통과 |
| B3 | 로봇처럼 뻣뻣하게 달려 | m_torso == 0 and m_elbow == 0 | run: m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 | 통과 | run: m_torso 0, m_knee 0.8, m_elbow 0, elbow_flexion 45 | 통과 | 거절 (invalid_output) [1단계 실패] | 실패 |
| B4 | 두 팔을 앞으로 쭉 뻗은 채 점프해 | shoulder_flexion >= 70 | jump: shoulder_flexion 85, elbow_flexion -30 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | jump: shoulder_flexion 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | jump: shoulder_flexion 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 |
| B5 | 허리가 굽은 노인처럼 점프해 | torso_pitch >= 15 | jump: s 0.6, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 30, head_pitch -10 | 통과 | jump: s 0.6, n 0.75, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 35, head_pitch -15 | 통과 | jump: n 0.75, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 35 | 통과 |
| B6 | 두 팔을 옆으로 벌린 채 발차기해 | shoulder_abduction >= 45 | kick: shoulder_abduction 80 (m_arm 1 -> 0.3 (팔을 80° 듦)) | 통과 | kick: shoulder_abduction 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 | kick: shoulder_abduction 85 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 |
| W1 | 다리를 넓게 벌리고 걸어 | stance_width >= 10 | stance_width 10 | 통과 | stance_width 10 | 통과 | stance_width 10 | 통과 |
| W2 | 아기처럼 다리를 벌리고 아장아장 걸어 | stance_width >= 10 and s <= 0.7 | n 0.6, m_torso 10, stance_width 10 | 실패 | n 0.55, m_torso 10, stance_width 10 | 실패 | m_torso 6, stance_width 10 | 실패 |
| W3 | 카우보이처럼 다리를 벌리고 느긋하게 걸어 | stance_width >= 10 and n < 1 | s 0.8, n 0.6, stance_width 10 | 통과 | s 1.4, n 0.75, stance_width 10 | 통과 | s 1.4, n 0.75, m_arm 1.5, stance_width 10 | 통과 |
| W4 | 기진맥진해서 터덜터덜 걸어 | torso_pitch >= 15 and head_pitch >= 25 | s 0.8, n 0.75, m_arm 0.4, m_torso 10, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | s 0.6, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | s 0.6, n 0.75, m_arm 0.4, m_torso 6, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 |
| C1 | 다리를 45도로 쫙 벌리고 걸어 | - | 거절 (not_expressible) | - | stance_width 10 [1단계 실패] | - | stance_width 10 [1단계 실패] | - |
| C2 | 옆으로 게걸음으로 걸어 | - | 거절 (not_expressible) | - | stance_width 10 [1단계 실패] | - | m_torso 6, stance_width 10 [1단계 실패] | - |
| C3 | 물구나무 서서 걸어 | - | s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 [1단계 실패] | - | n 0.55, m_torso 10 [1단계 실패] | - | m_torso 6, stance_width 10, toe_out 30 [1단계 실패] | - |
| C4 | 점프한 다음에 바로 발차기해 | - | 거절 (not_expressible) | - | 거절 (not_expressible) | - | 거절 (not_expressible) | - |

- v5: 1단계 통과 19/20, 값 기준 통과 14/16, 생성 31분, 가장 긴 답 4173토큰, 생각 예산을 다 쓴 답 3개 (폴더 20261103_234114_v5_set5)
- v8: 1단계 통과 17/20, 값 기준 통과 15/16, 생성 28분, 가장 긴 답 4174토큰, 생각 예산을 다 쓴 답 3개 (폴더 20261105_203223_v8_set5)
- v8: 1단계 통과 16/20, 값 기준 통과 14/16, 생성 7분, 가장 긴 답 1988토큰, 생각 예산을 다 쓴 답 0개 (폴더 20261110_185515_v8_set5_Qwen3-8B-from-FP8)
