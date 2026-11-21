# LLM 스타일 파라미터 1단계 결과 (20261027_225735_v2_set3)

Qwen/Qwen3-4B-Thinking-2507, 프롬프트 v2, 생각 예산 4096토큰, test_commands_3.json, 시드 42, 1단계 통과 22/25, 41.9분

| ID | 명령 | 기대 | 결과 | 1단계 | 속도 (m/s) |
| --- | --- | --- | --- | --- | --- |
| A1 | 도둑처럼 몸을 숙이고 숨죽여 걸어 | 수락 | n 0.6, c 20, m_arm 0.3, m_knee 0.8, torso_pitch 20, head_pitch 20 | 통과 | 0.76 |
| A2 | 기세 좋게 팔을 휘저으며 걸어 | 수락 | s 1.2, n 1.15, m_arm 1.8, torso_pitch -5, elbow_flexion 45 | 통과 | 1.74 |
| A3 | 다리를 번쩍번쩍 들어 올리며 걸어 | 수락 | n 1.2, c 15, m_arm 1.5, m_knee 1.5 | 통과 | 1.51 |
| A4 | 왕처럼 위엄 있게 걸어 | 수락 | s 1.2, m_arm 1.5, m_torso 0, torso_pitch -15, head_pitch -12 | 통과 | 1.51 |
| A5 | 발을 조금씩 바삐 옮기며 걸어 | 수락 | s 1.05, n 1.05 | 통과 | 1.39 |
| A6 | 보폭을 넓게 해서 시원시원하게 걸어 | 수락 | s 1.2, n 0.9 | 통과 | 1.36 |
| A7 | 태엽 인형처럼 딱딱하게 걸어 | 수락 | m_torso 0, m_knee 0.85, m_elbow 0, elbow_flexion 50 | 통과 | 1.26 |
| A8 | 나이 많은 어르신처럼 구부정하게 천천히 걸어 | 수락 | s 0.6, n 0.75, c 10, m_arm 0.4, m_torso 0, m_knee 0.8, torso_pitch 30, head_pitch 25 | 통과 | 0.57 |
| A9 | 상체를 좌우로 기우뚱거리며 걸어 | 수락 | m_torso 10 | 통과 | 1.26 |
| A10 | 되살아난 시체처럼 걸어 | 수락 | s 0.7, n 0.7, c 10, m_arm 0.3, m_torso 0, m_knee 0.8, m_elbow 0, torso_pitch 10, head_pitch 15, elbow_flexion -30 | 통과 | 0.62 |
| B1 | 모델처럼 런웨이를 걷듯이 걸어 | 수락 | m_torso 5, torso_pitch -10, head_pitch -10 | 통과 | 1.26 |
| B2 | 겁에 질려서 움츠린 채로 걸어 | 수락 | s 0.8, n 0.7, c 15, m_arm 0.3, m_torso 0, m_knee 0.8, torso_pitch 20, head_pitch 30, elbow_flexion 45 | 통과 | 0.71 |
| B3 | 주머니에 손을 넣고 건들건들 걸어 | 수락 | n 1.2, c 15, m_arm 1.5, m_knee 1.5, shoulder_flexion 20, elbow_flexion 40 | 통과 | 1.51 |
| B4 | 휴대폰을 들여다보면서 걸어 | 수락 | torso_pitch 10, head_pitch 15, shoulder_flexion 20, elbow_flexion 30 | 통과 | 1.26 |
| B5 | 등산하듯 몸을 앞으로 숙이고 힘차게 걸어 | 수락 | s 1.2, n 1.15, m_arm 1.5, m_knee 0.8, torso_pitch 20, elbow_flexion 45 | 통과 | 1.74 |
| B6 | 아기처럼 아장아장 걸어 | 수락 | n 0.6, m_torso 10 | 통과 | 0.76 |
| B7 | 경보 선수처럼 빠르게 걸어 | 수락 | s 1.3, n 1.2, m_arm 1.5, torso_pitch 10 | 통과 | 1.97 |
| B8 | 무릎을 굽힌 채 엉거주춤하게 걸어 | 수락 | n 0.6, c 20, m_torso 10, m_knee 0.8 | 통과 | 0.76 |
| B9 | 외줄 타듯이 두 팔을 양옆으로 벌리고 걸어 | 수락 | shoulder_abduction 45 | 통과 | 1.26 |
| B10 | 보폭을 평소의 절반으로 줄여서 걸어 | 수락 | s 0.5 | 통과 | 0.63 |
| C1 | 두 팔을 하늘로 쭉 뻗은 채로 걸어 | 거절 | shoulder_flexion 85, elbow_flexion -30 | 실패 | 1.26 |
| C2 | 왼팔만 크게 휘두르며 걸어 | 거절 | m_arm 1.5 | 실패 | 1.26 |
| C3 | 엎드려서 네 발로 기어가 | 거절 | 거절 (not_walking) | 통과 | - |
| C4 | 스케이트 타듯이 미끄러지며 가 | 거절 | s 0.8, n 0.85, c 15, m_arm 0.3, torso_pitch 10, head_pitch 14 | 실패 | 0.86 |
| C5 | 지그재그로 걸어 | 거절 | 거절 (not_expressible) | 통과 | - |
