"""The v1 parser of commit fe52856 run on test set 2: only the input file, the folder name and the summary keys change."""
import sys
src = open(sys.argv[1]).read()
subs = [
    ('HERE = Path(__file__).resolve().parent', 'HERE = Path("/home/jong/TexttoMotion/experiments/style_llm")'),
    ('TEST_FILE = HERE / "test_commands.json"', 'TEST_FILE = HERE / "test_commands_2.json"'),
    ('out_dir = HERE / datetime.datetime.now().strftime("%Y%m%d_%H%M%S")',
     'out_dir = HERE / (datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_v1_set2")'),
    ('summary = {"model": mp.MODEL_ID, "revision": mp.MODEL_REVISION, "seed": parser.seed,',
     'summary = {"model": mp.MODEL_ID, "revision": mp.MODEL_REVISION, "prompt": "v1 (fe52856)", '
     '"thinking_budget": mp.THINKING_BUDGET, "test_set": TEST_FILE.name, "seed": parser.seed,'),
    ('f"{mp.MODEL_ID}, 시드 {parser.seed},',
     'f"{mp.MODEL_ID}, 프롬프트 v1 (fe52856), 생각 예산 {mp.THINKING_BUDGET}토큰, {TEST_FILE.name}, 시드 {parser.seed},'),
]
for old, new in subs:
    assert src.count(old) == 1, old
    src = src.replace(old, new)
open(sys.argv[2], "w").write(src)
