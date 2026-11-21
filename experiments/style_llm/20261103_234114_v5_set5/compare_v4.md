| ID | 명령 | 값 기준 | v4 답 | v4 기준 | v5 답 | v5 기준 |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | 기운 없이 축 처져서 달려 | torso_pitch >= 15 and head_pitch >= 25 and s * n < 1 | run: s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | run: s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 |
| A2 | 고개를 깊이 숙인 채로 점프해 | head_pitch >= 25 | jump: head_pitch 25 | 통과 | jump: head_pitch 25 | 통과 |
| A3 | 자세를 낮추고 무릎을 굽힌 채 점프해 | c >= 15 | jump: c 20, torso_pitch 20 | 통과 | jump: n 1.25, c 20 | 통과 |
| A4 | 피곤한 몸으로 느릿느릿 돌려차기해 | torso_pitch >= 15 and head_pitch >= 25 and n <= 0.8 | spinkick: n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 25 | 통과 | spinkick: s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 |
| A5 | 허리를 뒤로 젖히고 발차기해 | torso_pitch <= -15 | kick: torso_pitch -12 | 실패 | kick: torso_pitch -12 | 실패 |
| A6 | 좀비처럼 두 팔을 앞으로 내밀고 달려 | shoulder_flexion >= 70 | run: s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 | 통과 | run: s 0.85, n 0.6, m_arm 0.3, m_torso 5, torso_pitch 10, shoulder_flexion 85, elbow_flexion -30 | 통과 |
| B1 | 술 취한 사람처럼 비틀비틀 달려 | m_torso >= 5 | run: m_torso 5, torso_pitch 10, head_pitch 20 | 통과 | run: n 0.6, m_torso 10 | 통과 |
| B2 | 당당하게 가슴을 펴고 달려 | torso_pitch <= -10 and m_arm > 1 | run: s 1.15, m_arm 1.4, torso_pitch -12, head_pitch -10 | 통과 | run: s 1.15, m_arm 1.4, torso_pitch -12, head_pitch -10 | 통과 |
| B3 | 로봇처럼 뻣뻣하게 달려 | m_torso == 0 and m_elbow == 0 | run: m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 | 통과 | run: m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 | 통과 |
| B4 | 두 팔을 앞으로 쭉 뻗은 채 점프해 | shoulder_flexion >= 70 | jump: m_arm 0.3, shoulder_flexion 85 | 통과 | jump: shoulder_flexion 85, elbow_flexion -30 (m_arm 1 -> 0.3 (팔을 85° 듦)) | 통과 |
| B5 | 허리가 굽은 노인처럼 점프해 | torso_pitch >= 15 | jump: s 0.6, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 30, head_pitch -10 | 통과 | jump: s 0.6, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 30, head_pitch -10 | 통과 |
| B6 | 두 팔을 옆으로 벌린 채 발차기해 | shoulder_abduction >= 45 | kick: m_arm 0.3, shoulder_abduction 80 | 통과 | kick: shoulder_abduction 80 (m_arm 1 -> 0.3 (팔을 80° 듦)) | 통과 |
| W1 | 다리를 넓게 벌리고 걸어 | stance_width >= 10 | 거절 (not_expressible) [1단계 실패] | 실패 | stance_width 10 | 통과 |
| W2 | 아기처럼 다리를 벌리고 아장아장 걸어 | stance_width >= 10 and s <= 0.7 | s 0.7, n 0.8, c 5, m_arm 0.4, m_torso 10, m_knee 0.7, head_pitch -10 | 실패 | n 0.6, m_torso 10, stance_width 10 | 실패 |
| W3 | 카우보이처럼 다리를 벌리고 느긋하게 걸어 | stance_width >= 10 and n < 1 | n 0.8, c 10, m_arm 0.6, m_knee 0.8, torso_pitch 5, head_pitch -5 | 실패 | s 0.8, n 0.6, stance_width 10 | 통과 |
| W4 | 기진맥진해서 터덜터덜 걸어 | torso_pitch >= 15 and head_pitch >= 25 | s 0.7, n 0.7, m_arm 0.4, m_knee 0.8, torso_pitch 20, head_pitch 25 | 통과 | s 0.8, n 0.75, m_arm 0.4, m_torso 10, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 |
| C1 | 다리를 45도로 쫙 벌리고 걸어 | - | 거절 (not_expressible) | - | 거절 (not_expressible) | - |
| C2 | 옆으로 게걸음으로 걸어 | - | 거절 (not_expressible) | - | 거절 (not_expressible) | - |
| C3 | 물구나무 서서 걸어 | - | s 0.8, n 0.75, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 [1단계 실패] | - | s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 [1단계 실패] | - |
| C4 | 점프한 다음에 바로 발차기해 | - | 거절 (not_expressible) | - | 거절 (not_expressible) | - |

- v4: 1단계 통과 18/20, 값 기준 통과 12/16, 생성 34분, 가장 긴 답 4180토큰, 생각 예산을 다 쓴 답 4개 (폴더 20261103_230713_v4_set5)
- v5: 1단계 통과 19/20, 값 기준 통과 14/16, 생성 31분, 가장 긴 답 4173토큰, 생각 예산을 다 쓴 답 3개 (폴더 20261103_234114_v5_set5)
