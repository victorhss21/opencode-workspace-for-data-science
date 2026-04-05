from meu_projeto_ds.models.predict import predict


def test_predict_contract_contains_status() -> None:
    result = predict()
    assert "status" in result
