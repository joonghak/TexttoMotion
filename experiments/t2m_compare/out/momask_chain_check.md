# 연속 동작 순서 확인, momask

동작마다 그 동작으로 판정된 프레임들의 가운데 시각(초)이다. 요청한 동작이 모두 나오고 이 순서이면 통과이다.

| ID | 명령 | 요청 순서 | 동작의 시각 (달리기, 걷기, 점프, 차기, 돌기) | 통과 |
| --- | --- | --- | --- | --- |
| C1 | 천천히 걷다가 갑자기 막 뛰어 | walk → run | run 4.0, walk 3.4; walk 3.6; run 4.1, walk 5.2, jump 3.8 | 1/3 |
| C2 | 뛰어가다가 앞으로 크게 점프해 | run → jump | run 4.5, walk 6.5, jump 4.4; walk 5.0, jump 2.5; walk 4.8, jump 3.0, kick 1.6 | 0/3 |
| C3 | 걸어가다가 앞차기 한 번 해 | walk → kick | walk 4.8, kick 5.7; walk 4.6, kick 5.8; walk 4.5, kick 2.0 | 2/3 |
| C4 | 점프 두 번 하고 나서 걸어 | jump → walk | walk 5.5, jump 1.5; walk 5.5, jump 5.5; walk 5.5 | 1/3 |
| C5 | 걷다가 돌려차기 해 | walk → spinkick | walk 3.7, jump 6.2, kick 6.0, spin 5.2; walk 4.9, jump 6.2, kick 5.7, spin 5.9; walk 5.0, jump 5.5, kick 2.4, spin 6.4 | 2/3 |
| C6 | 달리다가 멈춰서 발차기해 | run → kick | run 4.1, walk 6.5, jump 4.6, kick 5.5; run 5.7, walk 3.4, kick 0.5; run 5.5, walk 3.1, jump 0.4, kick 0.1 | 1/3 |
| C7 | 걷다가 뛰다가 마지막에 점프해 | walk → run → jump | run 5.5, walk 2.5, jump 5.3; run 5.9, walk 2.6, jump 5.5, kick 6.2; run 6.0, walk 2.6, jump 5.2, kick 6.1 | 0/3 |
| C8 | 지쳐서 터벅터벅 걷다가 힘을 내서 달려 | walk → run | walk 4.8, jump 2.0; walk 4.2, jump 1.6; walk 4.3 | 0/3 |

통과 7/24
