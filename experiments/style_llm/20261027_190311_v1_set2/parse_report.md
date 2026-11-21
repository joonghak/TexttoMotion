# LLM 스타일 파라미터 1단계 결과 (20261027_190311_v1_set2)

Qwen/Qwen3-4B-Thinking-2507, 프롬프트 v1 (fe52856), 생각 예산 2048토큰, test_commands_2.json, 시드 42, 1단계 통과 24/25, 19.1분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| A1 | 발소리가 나지 않게 몰래 걸어 | 수락 | s 0.6, n 0.7, c 15, m_arm 0.3, m_torso 0, m_knee 0.8, m_elbow 0 | 통과 | 0.53 |
| A2 | 넘어지지 않게 한 발 한 발 신중하게 걸어 | 수락 | n 0.5, c 15, m_arm 0.3, m_knee 0.8, torso_pitch 15, shoulder_flexion 20, elbow_flexion 40 | 통과 | 0.63 |
| A3 | 활기차고 씩씩하게 걸어 | 수락 | s 1.2, n 0.8, m_arm 1.5, m_torso 10 | 통과 | 1.21 |
| A4 | 허벅지를 높이 들면서 걸어 | 수락 | c 5, m_knee 0.7 | 통과 | 1.26 |
| A5 | 기진맥진해서 축 처진 채로 걸어 | 수락 | s 0.65, n 0.65, c 20, m_arm 0.3, m_knee 0.75, torso_pitch 25, head_pitch 30 | 통과 | 0.53 |
| A6 | 턱을 치켜들고 거만하게 걸어 | 수락 | n 0.7, m_arm 0.4, m_torso 0, head_pitch -10 | 통과 | 0.88 |
| A7 | 잰걸음으로 바쁘게 걸어 | 수락 | s 1.2, n 1.15, m_arm 1.4, torso_pitch -10 | 통과 | 1.74 |
| A8 | 한 걸음 한 걸음 크게 내디디며 걸어 | 수락 | s 1.5 | 통과 | 1.89 |
| A9 | 몸을 좌우로 크게 흔들면서 걸어 | 수락 | n 0.6, m_torso 10 | 통과 | 0.76 |
| A10 | 두 팔을 앞으로 나란히 뻗고 천천히 걸어 | 수락 | n 0.75, shoulder_flexion 85 | 통과 | 0.94 |
| B1 | 긴장해서 몸이 굳은 채로 걸어 | 수락 | m_arm 0.3, m_torso 0, m_elbow 0, elbow_flexion 50 | 통과 | 1.26 |
| B2 | 우아하게 천천히 걸어 | 수락 | n 0.8, c 15, m_arm 0.6, m_torso 5, m_knee 0.8 | 통과 | 1.01 |
| B3 | 배가 아파서 배를 움켜쥐고 걸어 | 수락 | s 0.8, n 0.75, m_arm 0.4, torso_pitch 15, head_pitch 10, shoulder_flexion 20, elbow_flexion 40 | 통과 | 0.76 |
| B4 | 졸려서 꾸벅꾸벅 졸면서 걸어 | 수락 | s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 0.76 |
| B5 | 운동하듯 파워 워킹해 | 수락 | s 1.2, n 1.15, m_arm 1.5, m_knee 1.2, torso_pitch -5 | 통과 | 1.74 |
| B6 | 펭귄처럼 뒤뚱뒤뚱 걸어 | 수락 | n 0.6, m_torso 10 | 통과 | 0.76 |
| B7 | 고양이처럼 사뿐사뿐 걸어 | 수락 | s 0.8, n 1.1, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 10, head_pitch -5 | 통과 | 1.11 |
| B8 | 어깨를 움츠리고 소심하게 걸어 | 수락 | n 0.5, c 15, m_arm 0.3, m_knee 0.8, torso_pitch 15, shoulder_flexion 25, elbow_flexion 40 | 통과 | 0.63 |
| B9 | 비를 맞으며 고개를 숙이고 서둘러 걸어 | 수락 | s 1.3, n 0.9, torso_pitch 5, head_pitch 15 | 통과 | 1.47 |
| B10 | 1분에 140걸음 걷는 빠르기로 걸어 | 수락 | n 1.21 | 통과 | 1.52 |
| C1 | 만세를 부르면서 걸어 | 거절 | m_arm 1.5, torso_pitch -15, head_pitch -15, shoulder_flexion 85 | 실패 | 1.26 |
| C2 | 오른발만 질질 끌면서 걸어 | 거절 | 거절 (not_expressible) | 통과 | - |
| C3 | 제자리에서 깡충깡충 뛰어 | 거절 | 거절 (not_walking) | 통과 | - |
| C4 | 옆으로 게걸음으로 걸어 | 거절 | 거절 (not_expressible) | 통과 | - |
| C5 | 한 바퀴 빙글 돌면서 걸어 | 거절 | 거절 (not_expressible) | 통과 | - |
