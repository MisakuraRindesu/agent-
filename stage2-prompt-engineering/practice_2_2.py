# practice_2_2.py — 六题 eval:Zero-Shot vs Few-Shot
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

CASES = [
    ("我被扣款两次", "billing"),
    ("发票上的金额不对", "billing"),
    ("按下登录后画面全白", "bug"),
    ("更新后一直闪退", "bug"),
    ("你们周末上班吗", "other"),
    ("谢谢你帮我处理", "other"),
]

def build_prompt(with_examples):
    p = """目标：将客服留言分到 billing、bug 或 other。
资料：<input_data>{msg}</input_data>
规则：只根据资料分类；不知道时选 other。
输出：只返回一个小写标签。"""
    if with_examples:
        p += """
范例：
输入：信用卡又扣了一次
输出：billing

输入：提交表单后没有反应
输出：bug

输入：可以更改联系邮箱吗
输出：other"""
    return p

def run_eval(with_examples):
    score = 0
    for msg, expected in CASES:
        prompt = build_prompt(with_examples).format(msg=msg)
        r = client.chat.completions.create(
            model="gemma4:e4b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=512,          # 防御:上轮 502 的教训,限制输出预算
        )
        answer = r.choices[0].message.content.strip().lower()
        found = [t for t in ("billing", "bug", "other") if t in answer]
        ok = len(found) == 1
        if ok:
            score += 1
        print(f"  {'✅' if ok else '❌'} 期望={expected:<7} 输出={answer[:60]!r}")
    return score

print("=== Zero-Shot（0 个范例）===")
s0 = run_eval(False)
print(f"分数: {s0}/6")

print("\n=== Few-Shot（3 个范例）===")
s3 = run_eval(True)
print(f"分数: {s3}/6")
