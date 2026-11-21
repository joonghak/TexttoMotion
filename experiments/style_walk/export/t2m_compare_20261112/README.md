# 우리와 공개 T2M 모델 비교 영상 (2026-11-12)

GIF마다 화면이 여덟 개이다. 윗줄은 옆에서, 아랫줄은 정면(캐릭터가 카메라 쪽으로 걸어옴)에서 찍었고, 왼쪽부터 다음과 같다. 6초이며, 카메라가 각 캐릭터를 따라간다.

1. 파랑, 우리: gpt-5.6-terra(프롬프트 v10)가 명령에서 정한 스타일 파라미터로 학습한 정책을 Isaac Lab 물리 시뮬레이션에서 실행한 것.
2. 보라, MoMask (CVPR 2024)
3. 노랑, T2M-GPT (CVPR 2023)
4. 빨강, MDM (ICLR 2023)

비교 모델은 공개된 사전학습 가중치(HumanML3D)에 명령의 영어 번역을 넣어 만든 관절 위치를 우리 캐릭터의 관절 각도로 옮겨 그대로 재생한 것이다(물리 없음, 시드별 세 개 가운데 첫 번째). 높이는 클립 전체에 한 번만 맞추었으므로 비교 모델의 떠 있음과 발 미끄러짐이 그대로 보인다. 영어 문장은 `experiments/t2m_compare/commands_en.json`에 있다.

| 파일 | 명령 | 우리 쪽 값 (LLM이 정함) |
| --- | --- | --- |
| dinosaur.gif | 공룡처럼 걸어 | s 1.4, n 0.7, c 20, m_arm 0.3, m_torso 6, m_knee 1.2, torso_pitch 15, head_pitch -10, shoulder_flexion 35, elbow_flexion 60, stance_width 8, toe_out 20 |
| chicken.gif | 닭처럼 걸어 | s 0.5, n 1.5, m_arm 0.3, m_knee 1.3, torso_pitch 15, shoulder_abduction -15, elbow_flexion 50, toe_out 25, bounce 20 |
| penguin.gif | 펭귄처럼 걸어 | s 0.6, n 0.8, m_arm 0.3, m_torso 7, m_knee 0.7, shoulder_abduction 45, elbow_flexion 20, stance_width 10, toe_out 20 |
| cat.gif | 고양이처럼 걸어 | s 0.65, n 0.8, c 20, m_arm 0.3, m_knee 0.7, torso_pitch 15, head_pitch 10, shoulder_flexion 15, elbow_flexion 35, stance_width -5, toe_out -10 |
| angry.gif | 화가 나서 쿵쿵 걸어 | s 1.2, n 1.2, c 15, m_arm 1.5, m_knee 1.4, torso_pitch 10, head_pitch 15, elbow_flexion 45, bounce 20 |
| drunk.gif | 술 취한 사람처럼 걸어 | s 0.75, n 0.65, m_arm 0.6, m_torso 8, m_knee 0.8, torso_pitch 10, head_pitch 15, stance_width 8, toe_out 15 |

같은 명령의 값: 100STYLE 유사도(학습한 정책)는 공룡 0.84, 닭 0.53, 펭귄 0.35, 고양이 0.51, 화남 0.57, 술 취함 0.27이고, 비교 모델의 6세트 평균은 MoMask 0.05, T2M-GPT 0.31, MDM 0.13이다(`experiments/t2m_compare/README.md`).
