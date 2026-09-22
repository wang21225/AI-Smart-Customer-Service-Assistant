from app.agents.intent import detect_intent


def test_detect_logistics_intent():
    result = detect_intent("帮我查询订单 202607160001 到哪里了")
    assert result["intent"] == "logistics_query"
    assert result["slots"]["order_no"] == "202607160001"
