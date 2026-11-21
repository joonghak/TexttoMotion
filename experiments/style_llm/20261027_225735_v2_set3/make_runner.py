"""The v2 parser of commit 51ff297 run on test set 3: only the module location and the test set table change."""
import sys
src = open(sys.argv[1]).read()
subs = [
    ('HERE = Path(__file__).resolve().parent', 'HERE = Path("/home/jong/TexttoMotion/experiments/style_llm")'),
    ('TEST_SETS = {"1": HERE / "test_commands.json", "2": HERE / "test_commands_2.json"}',
     'TEST_SETS = {"1": HERE / "test_commands.json", "2": HERE / "test_commands_2.json", "3": HERE / "test_commands_3.json"}'),
]
for old, new in subs:
    assert src.count(old) == 1, old
    src = src.replace(old, new)
open(sys.argv[2], "w").write(src)
