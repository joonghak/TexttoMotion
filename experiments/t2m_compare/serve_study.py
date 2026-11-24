#!/usr/bin/env python3
"""Serve the blind survey page from this computer and collect the answers, so that a rater needs only a link.

    ./experiments/t2m_compare/serve_study.py [--port 8765] [--study study]

Serves <study>/survey (index.html and the videos, with byte ranges so that phones play them) and nothing else: the
answer key in stimuli.json stays outside that folder. The page is sent with a few added lines of script that post the
answers when the rater reaches the end and again on "결과 파일 저장"; the file download of the page still works. Each
submission is written to <study>/answers/study_answers_<id>_<token>.csv, where the token is a random word the page
keeps in the rater's browser: two people who type the same id stay two raters, and one person who submits twice
replaces their own file. The rater column is rewritten to <id>_<token> to match. Nothing is uploaded anywhere; the
link works for whoever can reach this computer (same network, or a tunnel the user chooses to open).
"""
import argparse
import os
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
HEADER = "rater,key,question,choice,position,seconds"
HOOK = """
<script>
(function () {
  let token = "";
  try { token = localStorage.getItem("study_token") || ""; } catch (e) {}
  if (!token) { token = Math.random().toString(36).slice(2, 8); try { localStorage.setItem("study_token", token); } catch (e) {} }
  function submit() {
    if (!rater) return;
    fetch("submit?id=" + encodeURIComponent(rater) + "&token=" + token, {method: "POST", body: csv()})
      .then(r => { if (r.ok) note("응답이 제출되었습니다. 창을 닫아도 됩니다."); else note("제출에 실패했습니다. 결과 파일을 저장해 전달해 주세요."); })
      .catch(() => note("제출에 실패했습니다. 결과 파일을 저장해 전달해 주세요."));
  }
  function note(text) {
    let p = document.getElementById("submitted");
    if (!p) { p = document.createElement("p"); p.id = "submitted"; p.style.fontWeight = "bold"; document.getElementById("save").parentNode.before(p); }
    p.textContent = text;
  }
  document.getElementById("save").addEventListener("click", submit);
  document.getElementById("next").addEventListener("click", () => { if (pos >= ITEMS.length - 1) setTimeout(submit, 50); });
})();
</script>
"""


class Handler(SimpleHTTPRequestHandler):
    answers: Path

    def log_message(self, fmt, *args):
        if args and "submit" in str(args[0]):
            super().log_message(fmt, *args)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            page = Path(self.directory, "index.html").read_text(encoding="utf-8").replace("</body>", HOOK + "</body>")
            body = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        span = re.fullmatch(r"bytes=(\d*)-(\d*)", self.headers.get("Range", ""))
        file = Path(self.translate_path(path))
        if span and file.is_file():
            size = file.stat().st_size
            start = int(span.group(1)) if span.group(1) else max(size - int(span.group(2) or 0), 0)
            end = min(int(span.group(2)), size - 1) if span.group(1) and span.group(2) else size - 1
            if start > end:
                self.send_error(416)
                return
            self.send_response(206)
            self.send_header("Content-Type", self.guess_type(str(file)))
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Content-Length", str(end - start + 1))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            with file.open("rb") as f:
                f.seek(start)
                self.wfile.write(f.read(end - start + 1))
            return
        super().do_GET()

    def do_POST(self):
        match = re.fullmatch(r"/submit\?id=([^&]*)&token=([0-9a-z]{1,12})", self.path)
        length = int(self.headers.get("Content-Length") or 0)
        if not match or not 0 < length <= 20000:
            self.send_error(400)
            return
        from urllib.parse import unquote
        rater = re.sub(r"[^0-9A-Za-z_-]", "_", unquote(match.group(1)))[:20] or "rater"
        name = f"{rater}_{match.group(2)}"
        lines = self.rfile.read(length).decode("utf-8-sig", "replace").replace("\r\n", "\n").strip().split("\n")
        rows = [line.split(",") for line in lines[1:]]
        if lines[0].strip() != HEADER or not rows or any(len(r) != 6 for r in rows):
            self.send_error(400)
            return
        text = "\r\n".join([HEADER] + [",".join([f'"{name}"'] + r[1:]) for r in rows]) + "\r\n"
        self.answers.mkdir(exist_ok=True)
        (self.answers / f"study_answers_{name}.csv").write_text(text, encoding="utf-8")
        self.send_response(204)
        self.end_headers()


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--study", default="study")
    args = parser.parse_args()
    study = HERE / args.study
    Handler.answers = study / "answers"
    os.chdir(study / "survey")
    server = ThreadingHTTPServer(("0.0.0.0", args.port), lambda *a: Handler(*a, directory=str(study / "survey")))
    print(f"survey on port {args.port}; answers go to {Handler.answers}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
