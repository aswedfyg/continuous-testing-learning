import pytest

pytestmark = pytest.mark.api  # 标记整个模块为 API 测试

@pytest.mark.smoke # 标记为冒烟测试
def test_health_returns_ok(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
