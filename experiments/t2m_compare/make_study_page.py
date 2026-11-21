#!/home/jong/isaaclab/.venv/bin/python
"""The blind human-study survey as one local web page: per command the sentence, four videos A-D and two questions.

Usage on this computer (after make_study_films.py and film_compare.py):
    ./experiments/t2m_compare/make_study_page.py [--study study]

Reads experiments/t2m_compare/<study>/stimuli.json and the videos in <study>/videos. Writes <study>/survey/ with
index.html and videos/<n>_<letter>.mp4: copies whose names say nothing about the method (the answer key stays in
stimuli.json, outside the survey folder). The folder works offline in any browser and can be zipped and sent. A rater
types an id, answers every command (the order of the commands is shuffled per rater id) and at the end saves
study_answers_<id>.csv, in the form analyze_study.py reads (rater,key,question,choice, plus position and the seconds
the rater spent on the command's page).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PAGE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>동작 영상 평가</title>
<style>
  :root { --bg: #f6f6f4; --card: #ffffff; --text: #1d1d1b; --muted: #6b6b66; --line: #d9d9d4; --accent: #1f3864; --pick: #dfe7f5; }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--text); font-family: "Noto Sans KR", "Malgun Gothic", "Apple SD Gothic Neo", sans-serif; }
  main { max-width: 1500px; margin: 0 auto; padding: 16px; }
  .card { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 20px 24px; }
  h1 { font-size: 22px; margin: 0 0 12px; }
  p, li { line-height: 1.6; }
  .muted { color: var(--muted); }
  .top { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap; }
  .command { font-size: 26px; font-weight: 700; margin: 6px 0 14px; }
  .grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
  .cell { text-align: center; }
  .cell .letter { font-size: 22px; font-weight: 700; margin-bottom: 4px; }
  video { width: 100%; max-height: 58vh; object-fit: contain; background: #e4e4e0; border-radius: 6px; display: block; }
  .question { margin-top: 16px; display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
  .question .label { font-size: 17px; font-weight: 600; min-width: 330px; }
  .choices { display: flex; gap: 10px; }
  .choices label { border: 2px solid var(--line); border-radius: 8px; padding: 8px 22px; font-size: 18px; font-weight: 700; cursor: pointer; user-select: none; }
  .choices input { display: none; }
  .choices input:checked + span { color: var(--accent); }
  .choices label:has(input:checked) { border-color: var(--accent); background: var(--pick); }
  .buttons { margin-top: 20px; display: flex; gap: 10px; justify-content: space-between; }
  button { font: inherit; font-size: 16px; padding: 10px 22px; border-radius: 8px; border: 1px solid var(--accent); background: var(--accent); color: #fff; cursor: pointer; }
  button.secondary { background: #fff; color: var(--accent); }
  button:disabled { opacity: 0.4; cursor: default; }
  input[type=text] { font: inherit; font-size: 18px; padding: 8px 12px; border: 1px solid var(--line); border-radius: 8px; width: 220px; }
  .hidden { display: none; }
  @media (max-width: 900px) { .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } .question .label { min-width: 0; } }
</style>
</head>
<body>
<main>
  <section id="start" class="card">
    <h1>동작 영상 평가</h1>
    <p>문항마다 한국어 문장(동작 명령) 하나와, 그 명령으로 만든 동작 영상 네 개(A~D)가 나옵니다. 네 영상은 서로 다른 방법으로 만들었으며, 어느 방법인지는 알려 드리지 않습니다. 각 영상에서 위는 옆에서, 아래는 정면에서 본 같은 동작입니다.</p>
    <p>문항마다 두 가지를 하나씩 골라 주세요.</p>
    <ol>
      <li>명령과 가장 잘 맞는 영상</li>
      <li>가장 자연스럽고 물리적으로 그럴듯한 영상</li>
    </ol>
    <p class="muted">정답은 없습니다. 영상은 반복 재생되며, "다시 재생"을 누르면 네 영상이 처음부터 함께 재생됩니다. 영상을 한두 번 본 뒤 첫 느낌대로 골라 주세요. 문항은 모두 __N__개이고 8분 안팎이 걸립니다. 끝나면 결과 파일을 저장해 전달해 주세요.</p>
    <p><label>참가자 번호 <input type="text" id="rater" placeholder="예: P01" autocomplete="off"></label></p>
    <button id="begin" disabled>시작</button>
  </section>

  <section id="item" class="card hidden">
    <div class="top"><span class="muted" id="progress"></span><button class="secondary" id="replay">다시 재생</button></div>
    <div class="command" id="command"></div>
    <div class="grid" id="videos"></div>
    <div class="question"><span class="label">1. 명령과 가장 잘 맞는 영상</span><span class="choices" id="q_match"></span></div>
    <div class="question"><span class="label">2. 가장 자연스럽고 물리적으로 그럴듯한 영상</span><span class="choices" id="q_natural"></span></div>
    <div class="buttons"><button class="secondary" id="prev">이전</button><button id="next" disabled>다음</button></div>
  </section>

  <section id="end" class="card hidden">
    <h1>끝났습니다. 감사합니다.</h1>
    <p>아래 버튼으로 결과 파일을 저장해 전달해 주세요. 파일 이름은 <b id="filename"></b>입니다.</p>
    <div class="buttons" style="justify-content:flex-start"><button id="save">결과 파일 저장</button><button class="secondary" id="back">마지막 문항으로</button></div>
  </section>
</main>
<script>
const ITEMS = __ITEMS__;
const LETTERS = ["A", "B", "C", "D"];
const QUESTIONS = ["match", "natural"];
let rater = "", order = [], pos = 0, answers = {};
let spent = {}, shownKey = null, shownAt = 0;  // seconds on each command's page, summed over visits

function hash(text) {  // FNV-1a, so that the same rater id always gets the same order
  let h = 2166136261;
  for (const ch of text) { h ^= ch.codePointAt(0); h = Math.imul(h, 16777619) >>> 0; }
  return h >>> 0;
}
function shuffled(n, seed) {  // mulberry32 + Fisher-Yates
  let s = seed;
  const rand = () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const idx = Array.from({length: n}, (_, i) => i);
  for (let i = n - 1; i > 0; i--) { const j = Math.floor(rand() * (i + 1)); [idx[i], idx[j]] = [idx[j], idx[i]]; }
  return idx;
}
function store() {
  try { localStorage.setItem("study_" + rater, JSON.stringify({answers: answers, pos: pos, spent: spent})); } catch (e) {}
}
function restore() {
  try { const saved = JSON.parse(localStorage.getItem("study_" + rater) || "null"); if (saved) { answers = saved.answers || {}; spent = saved.spent || {}; pos = Math.min(saved.pos || 0, ITEMS.length - 1); } } catch (e) {}
}
function show(id) {
  for (const s of ["start", "item", "end"]) document.getElementById(s).classList.toggle("hidden", s !== id);
  window.scrollTo(0, 0);
}
function replay() {
  const vids = document.querySelectorAll("#videos video");
  vids.forEach(v => { v.pause(); v.currentTime = 0; });
  vids.forEach(v => { const p = v.play(); if (p) p.catch(() => {}); });
}
function choices(question, item) {
  const box = document.getElementById("q_" + question);
  box.textContent = "";
  for (const letter of LETTERS) {
    const label = document.createElement("label");
    const input = document.createElement("input");
    input.type = "radio"; input.name = question; input.value = letter;
    input.checked = (answers[item.key] || {})[question] === letter;
    input.addEventListener("change", () => {
      answers[item.key] = Object.assign({}, answers[item.key], {[question]: letter});
      store(); ready();
    });
    const span = document.createElement("span");
    span.textContent = letter;
    label.append(input, span);
    box.append(label);
  }
}
function ready() {
  const item = ITEMS[order[pos]];
  const a = answers[item.key] || {};
  document.getElementById("next").disabled = !(a.match && a.natural);
}
function tally() {  // adds the time since the shown command appeared to that command
  if (shownKey !== null) spent[shownKey] = (spent[shownKey] || 0) + (Date.now() - shownAt) / 1000;
  shownKey = null;
}
function render() {
  tally();
  const item = ITEMS[order[pos]];
  shownKey = item.key; shownAt = Date.now();
  document.getElementById("progress").textContent = (pos + 1) + " / " + ITEMS.length;
  document.getElementById("command").textContent = "“" + item.text + "”";
  const grid = document.getElementById("videos");
  grid.textContent = "";
  for (const letter of LETTERS) {
    const cell = document.createElement("div");
    cell.className = "cell";
    const head = document.createElement("div");
    head.className = "letter"; head.textContent = letter;
    const video = document.createElement("video");
    video.src = item.videos[letter]; video.muted = true; video.loop = true; video.playsInline = true; video.preload = "auto";
    video.setAttribute("muted", ""); video.setAttribute("playsinline", "");
    cell.append(head, video);
    grid.append(cell);
  }
  QUESTIONS.forEach(q => choices(q, item));
  document.getElementById("prev").disabled = pos === 0;
  document.getElementById("next").textContent = pos === ITEMS.length - 1 ? "마치기" : "다음";
  ready();
  show("item");
  setTimeout(replay, 300);
}
function csv() {
  const rows = ["rater,key,question,choice,position,seconds"];
  order.forEach((index, p) => {
    const item = ITEMS[index];
    for (const q of QUESTIONS) {
      const choice = (answers[item.key] || {})[q];
      if (choice) rows.push([rater, item.key, q, choice, p + 1, Math.round(spent[item.key] || 0)].map(v => '"' + String(v).replace(/"/g, '""') + '"').join(","));
    }
  });
  return "﻿" + rows.join("\r\n") + "\r\n";
}
function filename() {
  return "study_answers_" + rater.replace(/[^0-9A-Za-z_-]/g, "_") + ".csv";
}

document.getElementById("rater").addEventListener("input", e => {
  document.getElementById("begin").disabled = e.target.value.trim() === "";
});
document.getElementById("begin").addEventListener("click", () => {
  rater = document.getElementById("rater").value.trim();
  order = shuffled(ITEMS.length, hash(rater));
  pos = 0; answers = {};
  restore();
  render();
});
document.getElementById("replay").addEventListener("click", replay);
document.getElementById("prev").addEventListener("click", () => { if (pos > 0) { pos--; store(); render(); } });
document.getElementById("next").addEventListener("click", () => {
  if (pos < ITEMS.length - 1) { pos++; store(); render(); }
  else { tally(); store(); document.querySelectorAll("#videos video").forEach(v => v.pause()); document.getElementById("filename").textContent = filename(); show("end"); }
});
document.getElementById("back").addEventListener("click", render);
document.getElementById("save").addEventListener("click", () => {
  const blob = new Blob([csv()], {type: "text/csv;charset=utf-8"});
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = filename();
  document.body.append(link);
  link.click();
  link.remove();
});
</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--study", default="study", help="folder under experiments/t2m_compare (default study)")
    args = parser.parse_args()
    study = HERE / args.study
    stimuli = json.loads((study / "stimuli.json").read_text())
    survey = study / "survey"
    if survey.exists():
        shutil.rmtree(survey)
    (survey / "videos").mkdir(parents=True)
    items, missing = [], []
    for n, s in enumerate(stimuli, start=1):
        videos = {}
        for letter, name in s["videos"].items():
            source = study / "videos" / name
            if not source.exists():
                missing.append(str(source))
                continue
            target = f"videos/{n:02d}_{letter}.mp4"
            shutil.copyfile(source, survey / target)
            videos[letter] = target
        items.append({"key": s["key"], "text": s["text"], "videos": videos})
    if missing:
        print("영상이 없습니다:\n  " + "\n  ".join(missing), file=sys.stderr)
        return 1
    page = PAGE.replace("__ITEMS__", json.dumps(items, ensure_ascii=False)).replace("__N__", str(len(items)))
    (survey / "index.html").write_text(page, encoding="utf-8")
    size = sum(f.stat().st_size for f in (survey / "videos").iterdir()) / 1e6
    print(f"{len(items)}문항, 영상 {4 * len(items)}개 ({size:.0f} MB) -> {survey / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
