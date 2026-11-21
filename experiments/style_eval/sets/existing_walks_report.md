# 기존 걷기 정책과 100STYLE (2026-11-05)

유사도: 우리 정책이 기본 걸음에서 달라진 방향과 100STYLE 스타일이 Neutral에서 달라진 방향의 코사인 (특징마다 100STYLE 99종의 차이 분포로 나눈 뒤). 순위: 99종 가운데 목표 스타일의 순위. 크기: 우리 차이의 길이 / 목표 스타일 차이의 길이. 변화: 우리 차이의 길이(같은 단위, 100STYLE 99종의 중앙값 4.2).

| 정책 | 명령 | 목표 (100STYLE) | 유사도 | 순위 | 크기 | 변화 | 가장 가까운 스타일 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| zombie | 좀비처럼 걸어 | Zombie | 0.82 | 1 | 0.84 | 5.0 | Zombie 0.82, InTheDark 0.69, ArmsAboveHead 0.61 |
| old | 노인처럼 걸어 | Old | 0.13 | 40 | 0.52 | 3.4 | Quail 0.76, Chicken 0.75, BentKnees 0.73 |
| proud | 당당하게 걸어 | Proud | 0.25 | 14 | 0.96 | 1.7 | LookUp 0.66, Strutting 0.62, SpinAntiClock 0.46 |
| robot2 | 로봇처럼 걸어 | Robot | 0.63 | 16 | 0.55 | 2.4 | BeatChest 0.90, ArmsFolded 0.86, OnPhoneLeft 0.86 |
| striding | 성큼성큼 걸어 | BigSteps | 0.79 | 1 | 0.55 | 2.3 | BigSteps 0.79, Lunge 0.65, Rushed 0.58 |
| tired | 지쳐서 터벅터벅 걸어 | Depressed | 0.69 | 3 | 0.90 | 3.3 | Monk 0.74, LeanRight 0.70, Depressed 0.69 |
| stance10 | 다리를 벌리고 걸어 | LegsApart | 0.86 | 2 | 0.49 | 3.7 | WideLegs 0.88, LegsApart 0.86, Star 0.75 |
| hip16 | 허벅지를 높이 들며 걸어 (허벅지 진폭 1.6배) | HighKnees | 0.17 | 40 | 0.24 | 1.2 | BigSteps 0.62, Rushed 0.56, LeanBack 0.55 |
| n_walk_zombie | 좀비처럼 걸어 (고정한 수식) | Zombie | 0.80 | 1 | 0.85 | 5.1 | Zombie 0.80, InTheDark 0.67, ArmsAboveHead 0.59 |
| n_walk_tired | 지쳐서 터벅터벅 걸어 (고정한 수식) | Depressed | 0.75 | 2 | 1.08 | 4.0 | Monk 0.77, Depressed 0.75, LeanRight 0.75 |
| sneak_a | 살금살금 걸어 | - | - | - | - | 7.0 | BentKnees 0.87, Dinosaur 0.81, OnToesCrouched 0.72 |
| sneak_c | 조심조심 걸어 | - | - | - | - | 5.7 | Dinosaur 0.84, BentKnees 0.77, ShieldedRight 0.69 |
| power | 힘차게 걸어 | - | - | - | - | 2.4 | OnPhoneRight 0.87, OnPhoneLeft 0.86, ArmsFolded 0.85 |
| bouncy | 껑충껑충 걸어 | - | - | - | - | 4.6 | HighKnees 0.69, Roadrunner 0.67, Kick 0.64 |
| mincing | 종종걸음으로 걸어 | - | - | - | - | 2.3 | Penguin 0.65, Robot 0.57, DragRightLeg 0.47 |
| sway | 흔들흔들 걸어 | - | - | - | - | 3.1 | Old 0.71, SlideFeet 0.62, StartStop 0.57 |
| n_walk_sneak | 살금살금 걸어 (고정한 수식) | - | - | - | - | 6.2 | BentKnees 0.85, Dinosaur 0.84, ShieldedRight 0.74 |

목표가 있는 10개: 유사도 평균 0.59, 1위 3개, 5위 이내 6개, 크기 평균 0.70
