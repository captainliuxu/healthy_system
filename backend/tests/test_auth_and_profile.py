from __future__ import annotations

from tests.conftest import assert_beijing_datetime


def test_auth_and_profile_crud_uses_beijing_time(client, create_user):
    current = create_user("profile")

    me_response = client.get("/api/v1/users/me", headers=current["headers"])
    assert me_response.status_code == 200, me_response.text
    me_data = me_response.json()["data"]
    assert me_data["username"] == current["username"]
    user_created_at = assert_beijing_datetime(me_data["created_at"])
    user_updated_at = assert_beijing_datetime(me_data["updated_at"])
    assert user_updated_at >= user_created_at

    create_response = client.post(
        "/api/v1/profiles/me",
        headers=current["headers"],
        json={
            "name": "张三",
            "age": 66,
            "gender": "male",
            "height": 172.5,
            "weight": 63.0,
            "chronic_history": "高血压",
            "allergy_history": "无",
            "emergency_contact": "李四 13900000000",
            "remark": "阶段九验收样例",
        },
    )
    assert create_response.status_code == 201, create_response.text
    create_data = create_response.json()["data"]
    profile_created_at = assert_beijing_datetime(create_data["created_at"])
    profile_updated_at = assert_beijing_datetime(create_data["updated_at"])
    assert profile_updated_at >= profile_created_at
    assert create_data["name"] == "张三"

    get_response = client.get("/api/v1/profiles/me", headers=current["headers"])
    assert get_response.status_code == 200, get_response.text
    assert get_response.json()["data"]["id"] == create_data["id"]

    update_response = client.put(
        "/api/v1/profiles/me",
        headers=current["headers"],
        json={
            "weight": 61.5,
            "remark": "已完成北京时间修复验证",
        },
    )
    assert update_response.status_code == 200, update_response.text
    update_data = update_response.json()["data"]
    updated_at = assert_beijing_datetime(update_data["updated_at"])
    assert updated_at >= profile_updated_at
    assert update_data["weight"] == 61.5
    assert update_data["remark"] == "已完成北京时间修复验证"
