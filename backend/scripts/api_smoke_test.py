import json
import urllib.error
import urllib.request
import uuid

BASE = "http://localhost:8000"


def request(method: str, path: str, data=None, headers=None):
    if isinstance(data, (dict, list)):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        headers = headers or {"Content-Type": "application/json"}
    else:
        body = data
        headers = headers or {}
    req = urllib.request.Request(BASE + path, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            text = resp.read().decode("utf-8")
            print("OK", method, path, resp.status, text[:700])
            return json.loads(text) if text else None
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        print("ERR", method, path, exc.code, text[:1200])
        return None
    except Exception as exc:
        print("EXC", method, path, repr(exc))
        return None


def upload_text(kb_id: int):
    boundary = "----codextest" + uuid.uuid4().hex
    content = "售后政策：商品签收后7天内可以申请退货。退款一般在审核通过后3个工作日到账。"
    payload = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="file"; filename="test_policy.txt"\r\n'
        "Content-Type: text/plain\r\n\r\n"
        f"{content}\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")
    return request(
        "POST",
        f"/api/knowledge-bases/{kb_id}/documents",
        payload,
        {"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )


def main():
    request("GET", "/health")
    kb = request(
        "POST",
        "/api/knowledge-bases",
        {"name": "接口测试知识库-" + uuid.uuid4().hex[:6], "description": "自动测试", "is_default": False},
    )
    kb_id = kb["data"]["id"] if kb and kb.get("data") else 1
    upload_text(kb_id)
    request("GET", f"/api/knowledge-bases/{kb_id}/documents")
    request("POST", "/api/retrieval/test", {"knowledge_base_id": kb_id, "query": "商品签收后几天可以退货？", "top_k": 3})

    conv = request("POST", "/api/conversations", {"title": "接口二轮测试", "customer_id": None})
    conv_id = conv["data"]["id"] if conv and conv.get("data") else None
    request("POST", "/api/chat", {"message": "帮我查询订单 202607160001 到哪里了", "session_id": conv_id})
    request("POST", "/api/chat", {"message": "我要投诉，给我转人工", "session_id": conv_id})

    ticket = request("POST", "/api/tickets", {"category": "test", "content": "接口创建工单", "conversation_id": conv_id, "priority": "normal"})
    if ticket and ticket.get("data"):
        request("PUT", f"/api/tickets/{ticket['data']['id']}", {"status": "closed", "priority": "low"})

    request("POST", "/api/feedback", {"conversation_id": conv_id, "rating": "like", "comment": "接口测试"})
    request("GET", "/api/dashboard/statistics")
    request("GET", "/api/config")
    request("PUT", "/api/config", {"values": {"test_key": "test_value"}})


if __name__ == "__main__":
    main()
