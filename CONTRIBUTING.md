# 投稿指南

1. 在 `data/projects.json` 里加一行：
   ```json
   {"cat": "分类key", "repo": "作者/仓库", "zh": "一句话中文说明", "tools": "适用工具"}
   ```
   分类 key 见 `scripts/build.py` 顶部的 `CATEGORIES`。
2. 运行 `python3 scripts/build.py` 重新生成 README（会自动拉取最新星数并排序）。
3. 提交 PR，标题写 `新增: 作者/仓库`。

一句话说明请写清楚“它解决什么问题”，不要照抄英文简介。
