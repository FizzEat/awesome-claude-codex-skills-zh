#!/usr/bin/env python3
"""从 data/projects.json 拉取最新星数，按分类、星数排序生成 README.md。

用法: python3 scripts/build.py      (需要已登录的 gh CLI)
"""
import datetime
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent

CATEGORIES = [
    ("start", "起手必装：方法论与行为规范"),
    ("token", "省 Token 与长期记忆"),
    ("graph", "读懂代码与画图"),
    ("design", "设计与审美"),
    ("content", "内容创作：调研、写作、PPT、视频"),
    ("zh", "中文圈爆款"),
    ("cross", "Claude Code × Codex 联动与多 Agent"),
    ("life", "工作与学习场景"),
    ("official", "官方仓库"),
    ("lists", "其他合集"),
]


def stars(repo):
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}", "--jq", ".stargazers_count"],
        capture_output=True, text=True,
    )
    return int(out.stdout.strip()) if out.returncode == 0 else 0


def anchor(title):
    # GitHub 标题锚点规则：保留字母数字、空格、连字符，空格转连字符
    kept = "".join(c for c in title.lower() if c.isalnum() or c in " -")
    return kept.replace(" ", "-")


def fmt(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def main():
    projects = json.loads((ROOT / "data/projects.json").read_text())
    for p in projects:
        p["stars"] = stars(p["repo"])

    today = datetime.date.today().isoformat()
    total = len(projects)
    lines = (ROOT / "scripts/header.md").read_text().format(total=total, today=today).splitlines()

    lines.append("## 目录\n")
    for key, title in CATEGORIES:
        n = sum(1 for p in projects if p["cat"] == key)
        lines.append(f"- [{title}](#{anchor(title)}) ({n})")
    lines.append("")

    for key, title in CATEGORIES:
        items = sorted((p for p in projects if p["cat"] == key), key=lambda p: -p["stars"])
        lines.append(f"## {title}\n")
        lines.append("| 项目 | 一句话 | 星数 | 适用 |")
        lines.append("| --- | --- | ---: | --- |")
        for p in items:
            lines.append(
                f"| [{p['repo']}](https://github.com/{p['repo']}) | {p['zh']} | {fmt(p['stars'])} | {p['tools']} |"
            )
        lines.append("")

    lines.extend((ROOT / "scripts/footer.md").read_text().splitlines())
    (ROOT / "README.md").write_text("\n".join(lines) + "\n")
    print(f"README.md 已生成，共 {total} 个项目")


if __name__ == "__main__":
    main()
