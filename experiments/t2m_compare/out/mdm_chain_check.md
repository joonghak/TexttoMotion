# 연속 동작 순서 확인, mdm

동작마다 그 동작으로 판정된 프레임들의 가운데 시각(초)이다. 요청한 동작이 모두 나오고 이 순서이면 통과이다.

| ID | 명령 | 요청 순서 | 동작의 시각 (달리기, 걷기, 점프, 차기, 돌기) | 통과 |
| --- | --- | --- | --- | --- |
| C1 | 천천히 걷다가 갑자기 막 뛰어 | walk → run | run 2.2, walk 7.0; walk 2.4; walk 3.1 | 0/3 |
| C2 | 뛰어가다가 앞으로 크게 점프해 | run → jump | walk 4.0, jump 6.8, kick 6.8; run 6.2, walk 2.5, jump 6.4, kick 6.4; walk 3.7, jump 1.6, kick 0.8 | 1/3 |
| C3 | 걸어가다가 앞차기 한 번 해 | walk → kick | walk 4.8, jump 1.3, kick 1.4; walk 1.1, jump 3.4, kick 4.8; walk 2.2, jump 1.6, kick 7.5 | 2/3 |
| C4 | 점프 두 번 하고 나서 걸어 | jump → walk | run 1.8, walk 4.5, jump 3.6, kick 3.8; walk 3.1, jump 1.9; walk 3.3, jump 6.1 | 2/3 |
| C5 | 걷다가 돌려차기 해 | walk → spinkick | walk 1.1, jump 2.5, kick 7.8, spin 3.1; walk 4.2, jump 2.3, kick 2.3; walk 4.5, kick 1.1, spin 3.3 | 1/3 |
| C6 | 달리다가 멈춰서 발차기해 | run → kick | run 0.5; run 0.4, walk 4.7; run 0.3, walk 3.8 | 0/3 |
| C7 | 걷다가 뛰다가 마지막에 점프해 | walk → run → jump | run 7.4, walk 3.5, jump 2.7, kick 0.7; walk 4.0, jump 4.8, kick 4.9; walk 4.0, jump 0.7, kick 0.5 | 0/3 |
| C8 | 지쳐서 터벅터벅 걷다가 힘을 내서 달려 | walk → run | walk 3.9, jump 7.8; run 0.8, walk 4.2, jump 0.8, kick 0.7; walk 3.7, spin 5.1 | 0/3 |

통과 6/24
