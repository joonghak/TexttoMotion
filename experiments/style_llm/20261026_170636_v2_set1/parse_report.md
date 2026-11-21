# LLM 스타일 파라미터 1단계 결과 (20261026_170636_v2_set1)

Qwen/Qwen3-4B-Thinking-2507, 프롬프트 v2, 생각 예산 4096토큰, test_commands.json, 시드 42, 1단계 통과 24/25, 42.0분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| A1 | 들키지 않게 몸을 낮추고 조용히 걸어 | 수락 | n 0.6, c 20, m_arm 0.3, m_knee 0.8, torso_pitch 15, head_pitch 20 | 통과 | 0.76 |
| A2 | 미끄러운 빙판 위를 걷듯이 조심스럽게 걸어 | 수락 | n 0.6, c 20, m_arm 0.3, m_knee 0.8, torso_pitch 15, shoulder_flexion 20, elbow_flexion 40 | 통과 | 0.76 |
| A3 | 기운차게 팔을 크게 흔들면서 걸어 | 수락 | s 1.2, n 1.15, m_arm 1.8 | 통과 | 1.74 |
| A4 | 무릎을 높이 들어 올리면서 걸어 | 수락 | c 15, m_knee 1.5 | 통과 | 1.26 |
| A5 | 하루 종일 일해서 녹초가 된 사람처럼 걸어 | 수락 | s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 0.76 |
| A6 | 가슴을 펴고 자신감 있게 걸어 | 수락 | s 1.15, m_arm 1.4, torso_pitch -12, head_pitch -10 | 통과 | 1.45 |
| A7 | 보폭을 아주 좁게 해서 총총 걸어 | 수락 | s 0.5, m_torso 0 | 통과 | 0.63 |
| A8 | 다리를 쭉쭉 뻗어서 큰 보폭으로 걸어 | 수락 | s 1.5 | 통과 | 1.89 |
| A9 | 기계처럼 뻣뻣하게 걸어 | 수락 | m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 | 통과 | 1.26 |
| A10 | 허리가 굽은 할머니처럼 걸어 | 수락 | s 0.6, n 0.8, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 30, head_pitch -10 | 통과 | 0.60 |
| B1 | 화가 나서 씩씩거리며 걸어 | 수락 | s 1.2, n 1.15, m_arm 0.4, torso_pitch 15, head_pitch 25 | 통과 | 1.74 |
| B2 | 슬퍼서 고개를 떨구고 걸어 | 수락 | s 0.8, n 0.75, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 0.76 |
| B3 | 신이 나서 경쾌하게 걸어 | 수락 | s 1.2, n 1.15, m_arm 1.5, torso_pitch -5, head_pitch -10, elbow_flexion 45 | 통과 | 1.74 |
| B4 | 추워서 몸을 잔뜩 웅크리고 걸어 | 수락 | c 15, m_arm 0.4, m_knee 0.8, torso_pitch 25, head_pitch 10 | 통과 | 1.26 |
| B5 | 늦어서 급하게 서둘러 걸어 | 수락 | s 1.3, n 1.2, m_arm 1.5, torso_pitch -5 | 통과 | 1.97 |
| B6 | 공원을 산책하듯 느긋하게 걸어 | 수락 | n 0.75, c 10, m_arm 0.4, m_knee 0.8, torso_pitch 10 | 통과 | 0.94 |
| B7 | 군인처럼 절도 있게 행진해 | 수락 | s 0.8, n 0.8, c 15, m_arm 0.5, m_torso 0, m_knee 0.8, torso_pitch 5, elbow_flexion 40 | 통과 | 0.81 |
| B8 | 무거운 짐을 짊어진 것처럼 힘겹게 걸어 | 수락 | s 0.8, n 0.75, c 15, m_arm 0.4, m_knee 0.8, torso_pitch 15, head_pitch 25 | 통과 | 0.76 |
| B9 | 양손을 앞으로 공손하게 모으고 걸어 | 수락 | shoulder_flexion 20 | 통과 | 1.26 |
| B10 | 시속 3 km로 걸어 | 수락 | s 0.6, n 1.1 | 통과 | 0.83 |
| C1 | 양팔을 머리 위로 들고 걸어 | 거절 | 거절 (not_expressible) | 통과 | - |
| C2 | 왼쪽 다리를 절뚝거리며 걸어 | 거절 | 거절 (not_expressible) | 통과 | - |
| C3 | 두 발을 모아 콩콩 뛰면서 앞으로 가 | 거절 | s 0.8, n 1.2, c 15, m_arm 1.5, m_knee 1.5 | 실패 | 1.21 |
| C4 | 뒤로 걸어 | 거절 | 거절 (not_expressible) | 통과 | - |
| C5 | 전속력으로 달려 | 거절 | 거절 (not_walking) | 통과 | - |
