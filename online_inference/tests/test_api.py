import pytest


VALID_BODY = {
    "features": [
        {
            "age": 25,
            "sex": 0,
            "cp": 3,
            "trestbps": 150.0,
            "chol": 226.0,
            "fbs": 0,
            "restecg": 1,
            "thalach": 114.0,
            "exang": 1,
            "oldpeak": 2.6,
            "slope": 2,
            "ca": 2,
            "thal": 2
        }
    ]

}

INVALID_BODY = {
    "features": [
        {
            "age": -10,
            "sex": 0,
            "cp": 3,
            "trestbps": 150.0,
            "chol": 226.0,
            "fbs": 0,
            "restecg": 1,
            "thalach": 114.0,
            "exang": 1,
            "oldpeak": 2.6,
            "slope": 2,
            "ca": -20,
            "thal": 2
        }
    ]
}

API_URL = "/predict"


def test_one_prediction(test_client):
    responce = test_client.post(API_URL, json=VALID_BODY)
    assert responce.status_code == 200
    assert responce.json() == [{"heart_disease": 0}]


def test_many_prediction(test_client):
    new_body = VALID_BODY.copy()
    num_repeat = 5
    new_body["features"] = new_body["features"] * num_repeat
    responce = test_client.post(API_URL, json=new_body)
    assert responce.status_code == 200
    assert responce.json() == [{"heart_disease": 0}] * num_repeat


@pytest.mark.parametrize("body", [[], [{"a": 20}, INVALID_BODY]])
def test_invalid_data(test_client, body):
    responce = test_client.post(API_URL, json=body)
    assert responce.status_code == 400


def test_invalid_data(test_client):
    responce = test_client.get("/health")
    assert responce.status_code == 200
    assert responce.json() == {"status": "OK"}
