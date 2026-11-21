# 스핀킥 학습 횟수 비교

```bash
bash /home/jong/TexttoMotion/experiments/spinkick/run.sh
```

백그라운드에서 한 모델을 처음부터 연속 학습한다. 사전학습 모델을 불러오지 않으며,
각 지점에서 다시 시작하지 않는다. Isaac Lab, 환경 1,024개, seed 42,
기본 스핀킥 모션·보상·PPO 설정을 사용하고 GUI는 띄우지 않는다.

실행마다 `MimicKit/output/spinkick_날짜_시간_고유번호/`에 새 결과 폴더를 만든다.
동일 스크립트의 중복 실행은 막고 기존 결과는 덮어쓰지 않는다.
Ubuntu 사용자 서비스 `texttomotion-spinkick`으로 실행하므로 터미널·SSH를 닫아도 계속된다.
컴퓨터가 꺼지거나 절전 상태가 되면 진행되지 않으며, 자동 재시작·자동 재개는 하지 않는다.
수동 중단 명령은 `systemctl --user stop texttomotion-spinkick.service`이다.

| 완료한 학습 반복 | 학습 샘플 수 (32스텝/회 기준) | 저장 파일 |
| ---: | ---: | --- |
| 100 | 3,276,800 | `model_000100.pt` |
| 500 | 16,384,000 | `model_000500.pt` |
| 2,000 | 65,536,000 | `model_002000.pt` |
| 5,000 | 163,840,000 | `model_005000.pt` |

5,000회까지 학습하면 종료한다. `model.pt`는 기본 주기로 갱신되는 최신 모델이며,
이름에 횟수가 붙은 네 모델은 해당 시점의 비교용 사본이다.
`.pt`는 재생용 정책·정규화 상태이며, 옵티마이저까지 포함한 완전한 재시작 파일은 아니다.

- `console.log`: 실행 출력·오류·체크포인트 저장 안내
- `log.txt`: MimicKit 기본 학습 지표 (반복 번호는 0부터 시작)
- `milestones.tsv`: 실제 완료 횟수·샘플 수·파일명 대응표
- `command.txt`, `*_config.yaml`: 실행 명령과 기본 설정 사본
- `status.txt`: `running`, `completed`, 또는 실패 종료 코드
- `train.pid`: 학습 프로세스 번호

체크포인트 번호는 완료한 반복 수이므로 기본 로그의 `Iteration`보다 1 크다.
학습 샘플 수에는 기본 평가 에피소드가 포함되지 않는다.
추가한 `--checkpoint_iters` 옵션을 지정하지 않으면 기존 학습·저장 동작은 그대로다.
