"""The web page (docs/index.html) must give the same answers as the Python engine."""
import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stability_checker import check  # noqa: E402
from stability_checker.checker import CHANGES, CONDITIONS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
NODE = shutil.which("node")

DAYS = (0, 6, 7, 30, 89, 90, 179, 180, 181, 182, 364, 365)
AGES = (40, 54, 55, 65, 72, 80, 90)

JS = r"""
const fs = require('fs');
const html = fs.readFileSync(process.argv[1], "utf8").split(String.fromCharCode(13)).join("");
const plans = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')).plans;
eval(html.match(/function requiredDays[\s\S]*?\n}\nfunction passes[\s\S]*?\n}/)[0]);
const cases = JSON.parse(fs.readFileSync(0, 'utf8'));
console.log(JSON.stringify(cases.map(([d, a, c, ch]) =>
  plans.filter(p => passes(p, d, a, c, ch)).map(p => p.id).sort())));
"""


@unittest.skipUnless(NODE, "node is not installed")
class WebParityTest(unittest.TestCase):
    def test_page_matches_python(self):
        cases = [(d, a, c, ch) for d in DAYS for a in AGES for c in CONDITIONS for ch in CHANGES]
        out = subprocess.run(
            [NODE, "-e", JS, str(ROOT / "docs" / "index.html"), str(ROOT / "data" / "clauses.json")],
            input=json.dumps(cases), capture_output=True, text=True, check=True,
        ).stdout
        js = json.loads(out)
        for case, js_ids in zip(cases, js):
            py_ids = sorted(r.plan_id for r in check(*case) if r.passes)
            self.assertEqual(js_ids, py_ids, msg=f"days, age, condition, change = {case}")

    def test_page_script_parses(self):
        html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        script = re.search(r"<script>([\s\S]*)</script>", html).group(1)
        out = subprocess.run([NODE, "--check", "-"], input=script, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)

    def test_page_has_no_tracking(self):
        html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"google-analytics|gtag\(|document\.cookie|localStorage", html))


if __name__ == "__main__":
    unittest.main()
