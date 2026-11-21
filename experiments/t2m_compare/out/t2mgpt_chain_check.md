# 연속 동작 순서 확인, t2mgpt

동작마다 그 동작으로 판정된 프레임들의 가운데 시각(초)이다. 요청한 동작이 모두 나오고 이 순서이면 통과이다.

| ID | 명령 | 요청 순서 | 동작의 시각 (달리기, 걷기, 점프, 차기, 돌기) | 통과 |
| --- | --- | --- | --- | --- |
| C1 | 천천히 걷다가 갑자기 막 뛰어 | walk → run | walk 2.6; walk 2.4; walk 2.4 | 0/3 |
| C2 | 뛰어가다가 앞으로 크게 점프해 | run → jump | jump 1.5; walk 3.3, jump 3.2; walk 3.5, jump 3.0 | 0/3 |
| C3 | 걸어가다가 앞차기 한 번 해 | walk → kick | kick 3.7; -; walk 1.1, kick 1.0 | 0/3 |
| C4 | 점프 두 번 하고 나서 걸어 | jump → walk | jump 8.1, kick 8.2; walk 0.6, jump 3.6, kick 6.0; walk 0.6, jump 8.4, kick 8.6 | 0/3 |
| C5 | 걷다가 돌려차기 해 | walk → spinkick | walk 1.1, jump 1.8, kick 3.4, spin 2.0; walk 3.2, kick 2.0, spin 1.2; kick 4.2, spin 6.0 | 1/3 |
| C6 | 달리다가 멈춰서 발차기해 | run → kick | walk 0.6; -; walk 0.5 | 0/3 |
| C7 | 걷다가 뛰다가 마지막에 점프해 | walk → run → jump | walk 3.8, jump 3.7; jump 1.8; jump 1.4 | 0/3 |
| C8 | 지쳐서 터벅터벅 걷다가 힘을 내서 달려 | walk → run | walk 7.5, jump 7.2, spin 7.1; run 5.1, walk 6.1; run 3.5, walk 8.1, spin 6.9 | 0/3 |

통과 1/24
