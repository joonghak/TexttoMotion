# v1 프롬프트를 2세트로 실행

v2와 같은 명령에서 비교하기 위해 v1 파서(커밋 fe52856의 `style_parser.py`)를 2세트로 실행하였다. `make_runner.py`는 git의 그 파일에서 위치(HERE), 입력 파일(test_commands_2.json), 결과 폴더 이름, 요약의 키만 바꾼 실행본을 만든다. 모델, 시드, 생각 예산(2,048토큰), 프롬프트는 v1 그대로이다.

    git show fe52856:experiments/style_llm/style_parser.py > /tmp/v1.py
    python3 make_runner.py /tmp/v1.py /tmp/v1_set2.py
    /home/jong/isaaclab/.venv/bin/python /tmp/v1_set2.py --test --offline
