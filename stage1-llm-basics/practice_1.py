# 需要：pip install openai
# 运行前：ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # 让中文输出正常显示

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",   # 指向本机 Ollama 的地址
    api_key="ollama",                        # 占位值,Ollama 不检查它
)

r = client.chat.completions.create(          # 发一次"聊天"请求
    model="gemma4:e4b",                      # 用本地拉好的模型
    max_tokens=2048,                          # 输出上限 100 token
    messages=[{"role": "user", "content": "用一句话自我介绍。"}],  # 我们的提问
)

# === 自我验证 ===
text = r.choices[0].message.content         # 取出模型的回答
print("响应：", text)
print("usage:", r.usage)                     # ★ 这里能看到用了多少 token

assert r.choices[0].finish_reason in ("stop", "length"), f"非预期 finish_reason: {r.choices[0].finish_reason}"
assert len(text) > 0, "响应不应为空"
assert r.usage.completion_tokens > 0, "output token 应大于 0"
print("✅ 练习 1 通过 — Ollama gemma4:e4b 已能在本地响应，每次 $0")
