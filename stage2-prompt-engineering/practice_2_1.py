# practice_2_1.py
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

vague_prompt = "帮我整理：我被扣款两次，请帮我查。"

structured_prompt = """目标：将客服留言分到 billing、bug 或 other。
资料：<input_data>我被扣款两次，请帮我查。</input_data>
规则：只根据资料分类；不知道时选 other。
输出：只返回一个小写标签。"""

for name, p in [("模糊版", vague_prompt), ("四部分版", structured_prompt)]:
    r = client.chat.completions.create(
        model="gemma4:e4b",
        messages=[{"role": "user", "content": p}],
        temperature=0,          # 教材指定 0:分类任务要稳定
    )
    print(f"===== {name} =====")
    print(r.choices[0].message.content.strip())
    print()
