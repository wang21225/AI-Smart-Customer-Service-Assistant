import json
import tempfile
import urllib.request
import uuid
from pathlib import Path

from openpyxl import Workbook

BASE = "http://localhost:8000"


def build_sample_xlsx() -> Path:
    output = Path(tempfile.gettempdir()) / "after_sales_faq.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "FAQ"
    sheet.append(["问题", "答案"])
    rows = [
        ("商品签收后几天内可以退货？", "普通商品自签收之日起7天内，在商品完好、配件齐全、不影响二次销售的情况下，可以申请无理由退货。"),
        ("退款审核通过后多久能到账？", "退款申请审核通过后，通常会在3个工作日内原路退回，具体到账时间以支付渠道或银行处理时间为准。"),
        ("软件激活后还能退款吗？", "软件类、会员类、激活码类等虚拟商品，如已经激活、兑换、下载或使用，一般不支持无理由退款。"),
        ("质量问题退货运费谁承担？", "如确认是商品质量问题、错发漏发或平台原因导致退货，商家承担合理退货运费。"),
        ("我要投诉应该怎么处理？", "用户明确投诉或要求人工客服时，AI客服应创建工单并转接人工客服继续处理。"),
    ]
    for row in rows:
        sheet.append(row)
    workbook.save(output)
    return output


def upload(path: Path, knowledge_base_id: int) -> dict:
    boundary = "----codexxlsx" + uuid.uuid4().hex
    payload = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="file"; filename="after_sales_faq.xlsx"\r\n'
        "Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\r\n\r\n"
    ).encode("utf-8") + path.read_bytes() + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/api/knowledge-bases/{knowledge_base_id}/documents",
        data=payload,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    return json.loads(urllib.request.urlopen(req, timeout=60).read().decode("utf-8"))


def post_json(path: str, data: dict) -> dict:
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))


def main() -> None:
    file_path = build_sample_xlsx()
    uploaded = upload(file_path, 1)
    print("UPLOAD", json.dumps(uploaded, ensure_ascii=False))
    document_id = uploaded["data"]["id"]
    chunks = json.loads(urllib.request.urlopen(f"{BASE}/api/documents/{document_id}/chunks", timeout=20).read().decode("utf-8"))
    print("CHUNK_COUNT", len(chunks["data"]))
    result = post_json("/api/retrieval/test", {"knowledge_base_id": 1, "query": "软件激活了还能退吗？", "top_k": 3})
    print("RETRIEVAL", json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
