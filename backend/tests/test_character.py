def test_character_profile_and_attributes(client, auth_headers):
    # Fetch initial character
    char_res = client.get("/api/v1/character", headers=auth_headers)
    assert char_res.status_code == 200
    char_data = char_res.json()
    assert char_data["level"] == 1
    assert char_data["current_xp"] == 0
    assert char_data["xp_for_next_level"] == 100
    assert "attributes" in char_data
    assert set(char_data["attributes"].keys()) == {"STR", "INT", "WIS", "DIS", "VIT", "CHA"}

    # Fetch attribute breakdown
    attr_res = client.get("/api/v1/character/attributes", headers=auth_headers)
    assert attr_res.status_code == 200
    attr_data = attr_res.json()
    assert "attribute_percentages" in attr_data
