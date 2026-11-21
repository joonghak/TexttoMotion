# LLM 스타일 파라미터 1단계 결과 (20261112_213225_v12_set10_gpt-5.6-sol)

openai/gpt-5.6-sol, 프롬프트 v12, 생각 예산 4096토큰, test_commands_10.json, 시드 42, 1단계 통과 12/12, 0.0분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| C1 | 천천히 걷다가 갑자기 막 뛰어 | 수락 | walk 3s -> run 3s: n 0.75 | 통과 | 0.94 |
| C2 | 뛰어가다가 앞으로 크게 점프해 | 수락 | run 2.4s -> jump 1.77s: s 1.4 | 통과 | 4.98 |
| C3 | 걸어가다가 앞차기 한 번 해 | 수락 | walk 3s -> kick 1.53s: 기본값 | 통과 | 1.26 |
| C4 | 점프 두 번 하고 나서 걸어 | 수락 | jump 3.54s -> walk 3s: 기본값 | 통과 | 0.61 |
| C5 | 걷다가 돌려차기 해 | 수락 | walk 3s -> spinkick 1.28s: 기본값 | 통과 | 1.26 |
| C6 | 달리다가 멈춰서 발차기해 | 수락 | run 2.4s -> kick 1.53s: 기본값 | 통과 | 3.56 |
| C7 | 걷다가 뛰다가 마지막에 점프해 | 수락 | walk 3s -> run 3s -> jump 3.54s: 기본값 | 통과 | 1.26 |
| C8 | 지쳐서 터벅터벅 걷다가 힘을 내서 달려 | 수락 | walk 3s -> run 3s: 기본값 | 통과 | 1.26 |
| T1 | 까치발을 들고 사뿐사뿐 걸어 | walk | s 0.8, n 0.8, m_arm 0.4, m_knee 0.7, foot_pitch 25 | 통과 | 0.81 |
| T2 | 발뒤꿈치로만 걸어 | walk | foot_pitch -20 | 통과 | 1.26 |
| T3 | 하이힐을 신은 것처럼 걸어 | walk | s 0.65, n 0.85, m_torso 5, m_knee 0.8, stance_width -6, foot_pitch 25 | 통과 | 0.70 |
| T4 | 발레리나처럼 발끝으로 걸어 | walk | s 0.6, n 0.85, m_arm 0.3, m_torso 0, m_knee 0.7, torso_pitch -10, head_pitch -10, shoulder_abduction 55, elbow_flexion 40, stance_width -8, toe_out 30, foot_pitch 30 | 통과 | 0.64 |
