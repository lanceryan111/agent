#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日股票行情 Agent
流程：查询股价 (yfinance) → 本地 Qwen3-32B (Ollama) 生成中文点评 → Gmail 发邮件给自己
配置在同目录 config.json 中（参考 config.example.json）
"""

import json
import re
import smtplib
import ssl
import sys
import traceback
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import requests
import yfinance as yf

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
LOG_PATH = BASE_DIR / "stock_agent.log"


def log(msg: str):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def fetch_quotes(tickers: list[str]) -> list[dict]:
    """抓取每只股票的最新价、涨跌幅、52周区间等。"""
    quotes = []
    for symbol in tickers:
        try:
            t = yf.Ticker(symbol)
            info = t.fast_info
            price = info.last_price
            prev = info.previous_close
            change_pct = (price - prev) / prev * 100 if prev else 0.0
            hist = t.history(period="5d")["Close"]
            five_day = ""
            if len(hist) >= 2:
                five_day_pct = (hist.iloc[-1] - hist.iloc[0]) / hist.iloc[0] * 100
                five_day = f"{five_day_pct:+.2f}%"
            quotes.append({
                "symbol": symbol,
                "price": round(price, 2),
                "prev_close": round(prev, 2) if prev else None,
                "change_pct": round(change_pct, 2),
                "five_day": five_day,
                "year_high": round(info.year_high, 2) if info.year_high else None,
                "year_low": round(info.year_low, 2) if info.year_low else None,
            })
            log(f"{symbol}: {price:.2f} ({change_pct:+.2f}%)")
        except Exception as e:
            log(f"获取 {symbol} 失败: {e}")
            quotes.append({"symbol": symbol, "error": str(e)})
    return quotes


def ask_local_model(cfg: dict, quotes: list[dict]) -> str:
    """调用本地 Ollama 的 Qwen3-32B 生成中文总结。失败则返回空字符串。"""
    data_text = json.dumps(quotes, ensure_ascii=False, indent=2)
    prompt = (
        "你是一位专业的股票市场分析助手。下面是今天美股几只科技股的行情数据（JSON）：\n\n"
        f"{data_text}\n\n"
        "请用中文写一段简洁的每日行情点评（200字以内）：先一句话概括整体涨跌，"
        "然后指出表现最好和最差的股票及可能值得注意的点（如接近52周高点/低点）。"
        "不要编造数据中没有的信息，不要给出买卖建议。"
    )
    try:
        resp = requests.post(
            f"{cfg.get('ollama_url', 'http://localhost:11434')}/api/generate",
            json={
                "model": cfg.get("model", "qwen3:32b"),
                "prompt": prompt,
                "stream": False,
                "think": False,
                "options": {"temperature": 0.5, "num_predict": 600},
            },
            timeout=600,
        )
        resp.raise_for_status()
        text = resp.json().get("response", "").strip()
        # 兜底：去掉 Qwen3 可能输出的思考标签
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
        return text
    except Exception as e:
        log(f"调用本地模型失败（将发送纯数据邮件）: {e}")
        return ""


def build_html(quotes: list[dict], summary: str) -> str:
    rows = []
    for q in quotes:
        if "error" in q:
            rows.append(
                f"<tr><td>{q['symbol']}</td>"
                f"<td colspan='5' style='color:#999'>获取失败: {q['error']}</td></tr>"
            )
            continue
        color = "#c0392b" if q["change_pct"] < 0 else "#27ae60"
        rows.append(
            f"<tr>"
            f"<td><b>{q['symbol']}</b></td>"
            f"<td>${q['price']}</td>"
            f"<td style='color:{color}'><b>{q['change_pct']:+.2f}%</b></td>"
            f"<td>{q['five_day'] or '—'}</td>"
            f"<td>${q['year_low']} – ${q['year_high']}</td>"
            f"</tr>"
        )
    summary_html = (
        f"<div style='background:#f6f8fa;border-radius:8px;padding:14px 18px;"
        f"margin:16px 0;line-height:1.7'>{summary}</div>"
        if summary
        else "<p style='color:#999'>（本地模型今日未生成点评，仅附行情数据）</p>"
    )
    return f"""
    <div style="font-family:-apple-system,'PingFang SC',sans-serif;max-width:640px">
      <h2>📈 每日股票行情 · {datetime.now().strftime('%Y-%m-%d')}</h2>
      {summary_html}
      <table cellpadding="8" cellspacing="0" border="0"
             style="border-collapse:collapse;width:100%;font-size:14px">
        <tr style="background:#2c3e50;color:#fff;text-align:left">
          <th>代码</th><th>现价</th><th>日涨跌</th><th>近5日</th><th>52周区间</th>
        </tr>
        {''.join(rows)}
      </table>
      <p style="color:#999;font-size:12px;margin-top:16px">
        由本地 Qwen3-32B (Ollama) 于 Mac mini 自动生成 · 数据来自 Yahoo Finance，仅供参考，不构成投资建议
      </p>
    </div>
    """


def send_email(cfg: dict, html: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📈 每日股票行情 {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = cfg["gmail_address"]
    msg["To"] = cfg["email_to"]
    msg.attach(MIMEText(html, "html", "utf-8"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as server:
        server.login(cfg["gmail_address"], cfg["gmail_app_password"])
        server.send_message(msg)
    log(f"邮件已发送至 {cfg['email_to']}")


def main():
    log("===== 开始运行 =====")
    cfg = load_config()
    quotes = fetch_quotes(cfg["tickers"])
    ok = [q for q in quotes if "error" not in q]
    if not ok:
        log("所有股票均获取失败，退出（不发邮件）")
        sys.exit(1)
    summary = ask_local_model(cfg, quotes)
    html = build_html(quotes, summary)
    send_email(cfg, html)
    log("===== 运行结束 =====")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log("运行出错:\n" + traceback.format_exc())
        sys.exit(1)
