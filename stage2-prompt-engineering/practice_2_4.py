# practice_2_4.py — 多轮统计版:3 次运行对比
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

CASES = [
    ("退款迟迟没有到账", "billing"),
    ("下单后没收到确认邮件", "bug"),
    ("扣款金额和确认书不一致", "billing"),
    ("登录后立刻被登出", "bug"),
    ("怎么更改收货地址", "other"),
    ("App 一直转圈加载不出来", "bug"),
]

BASE_PROMPT = """目标：将客服留言分到 billing、bug 或 other。
资料：<input_data>{msg}</input_data>
规则：只根据资料分类；不知道时选 other。
输出：只返回一个小写标签。"""

MODIFICATION = "\n规则补充：与支付、金额、退款、扣款有关的留言一律归为 billing；如果用户描述的是“应当发生但未发生”的现象（比如没收到应有的确认邮件、通知），归为 bug；用户只是询问方法或感谢时归为 other。"

RUNS = 3

def run_once():
    score = 0
    for msg, expected in CASES:
        prompt = BASE_PROMPT.format(msg=msg) + MODIFICATION
        r = client.chat.completions.create(
            model="gemma4:e4b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=512,
        )
        answer = r.choices[0].message.content.strip().lower()
        found = [t for t in ("billing", "bug", "other") if t in answer]
        ok = len(found) == 1 and found[0] == expected
        if ok:
            score += 1
    return score

scores = []
for i in range(RUNS):
    s = run_once()
    scores.append(s)
    print(f"第 {i+1} 轮: {s}/6")
print(f"平均: {sum(scores)/len(scores):.2f}/6  (各轮: {scores})")
