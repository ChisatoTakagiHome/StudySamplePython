from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ユーザー情報取得API 正常系テスト
def test_get_user_NR001():
    response = client.get(
        "/users/abcde12345", headers={"token": "correct_token"})
    # レスポンス検証
    # ステータスコード
    assert response.status_code == 200
    # レスポンスボディ
    assert response.json() == {
        "id": "abcde12345",
        "name": "Yamada",
        "email_address": "yamada@example.com",
    }

# ユーザー情報取得API 異常系テスト
# トークン違い
def test_get_user_ABR001():
    response = client.get("/users/abcde12345",
                          headers={"token": "dummy_token"})
    assert response.status_code == 400
    assert response.json() == {"detail": "token_verification_failed"}

# ユーザー情報取得API 異常系テスト
# 存在しないユーザー指定
def test_get_user_ABR002():
    response = client.get(
        "/users/hogefuga", headers={"token": "correct_token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "user_not_found"}

# ユーザー情報登録API 正常系テスト
def test_create_user_NR001():
    # 正常系リクエスト
    # ヘッダーとボディは辞書型で渡す。
    response = client.post(
        "/users/",
        headers={"Token": "correct_token"},
        json={"id": "klmno12345", "name": "Kobayashi",
              "email_address": "kobayashi@example.com"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "klmno12345",
        "name": "Kobayashi",
        "email_address": "kobayashi@example.com",
    }

# ユーザー情報登録API 異常系テスト
# トークン違い
def test_create_user_ABR001():
    response = client.post(
        "/users/",
        headers={"Token": "dummy_token"},
        json={"id": "klmno12345", "name": "Kobayashi",
              "email_address": "kobayashi@example.com"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "token_verification_failed"}


# ユーザー情報登録API 異常系テスト
# 登録済みユーザーID指定
def test_create_user_ABR002():
    response = client.post(
        "/users/",
        headers={"Token": "correct_token"},
        json={
            "id": "abcde12345",
            "name": "Kobayashi",
            "email_address": "kobayashi@example.com"
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "user_id_duplicated"}