from __future__ import annotations

from tests.conftest import assert_beijing_datetime


def test_record_crud_and_permission_checks(client, create_user):
    owner = create_user("record_owner")
    other = create_user("record_other")

    create_response = client.post(
        "/api/v1/records",
        headers=owner["headers"],
        json={
            "record_type": "blood_pressure",
            "value": "120/80",
            "unit": "mmHg",
            "note": "晨间测量",
        },
    )
    assert create_response.status_code == 201, create_response.text
    record = create_response.json()["data"]
    record_id = record["id"]
    assert_beijing_datetime(record["record_time"])
    created_at = assert_beijing_datetime(record["created_at"])
    updated_at = assert_beijing_datetime(record["updated_at"])
    assert updated_at >= created_at

    list_response = client.get("/api/v1/records", headers=owner["headers"])
    assert list_response.status_code == 200, list_response.text
    list_data = list_response.json()["data"]
    assert list_data["total"] == 1
    assert list_data["items"][0]["id"] == record_id

    detail_response = client.get(
        f"/api/v1/records/{record_id}",
        headers=owner["headers"],
    )
    assert detail_response.status_code == 200, detail_response.text
    assert detail_response.json()["data"]["value"] == "120/80"

    update_response = client.put(
        f"/api/v1/records/{record_id}",
        headers=owner["headers"],
        json={
            "value": "118/78",
            "record_time": "2026-04-17T09:30:00+08:00",
            "note": "复测",
        },
    )
    assert update_response.status_code == 200, update_response.text
    update_data = update_response.json()["data"]
    assert update_data["value"] == "118/78"
    assert assert_beijing_datetime(update_data["record_time"]).hour == 9

    forbidden_response = client.get(
        f"/api/v1/records/{record_id}",
        headers=other["headers"],
    )
    assert forbidden_response.status_code == 404, forbidden_response.text
    assert forbidden_response.json()["code"] == 40421

    delete_response = client.delete(
        f"/api/v1/records/{record_id}",
        headers=owner["headers"],
    )
    assert delete_response.status_code == 200, delete_response.text

    list_after_delete_response = client.get("/api/v1/records", headers=owner["headers"])
    assert list_after_delete_response.status_code == 200, list_after_delete_response.text
    assert list_after_delete_response.json()["data"]["total"] == 0
