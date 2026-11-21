# v2 프롬프트를 3세트로 실행

v3와 같은 명령에서 비교하기 위해 v2 파서(커밋 51ff297의 `style_parser.py`)를 3세트로 실행하였다. `make_runner.py`는 git의 그 파일에서 위치(HERE)와 테스트 세트 표만 바꾼 실행본을 만든다. 모델, 시드, 생각 예산(4,096토큰), 프롬프트는 v2 그대로이다.

    git show 51ff297:experiments/style_llm/style_parser.py > /tmp/v2.py
    python3 make_runner.py /tmp/v2.py /tmp/v2_set3.py
    /home/jong/isaaclab/.venv/bin/python /tmp/v2_set3.py --test 3 --offline
