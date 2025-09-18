import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services import credit_services as service
from datetime import date
from unittest.mock import patch, MagicMock
from datetime import date
from services import credit_services as service

@patch("services.credit_services.db.session")
@patch("services.credit_services.Credito")
def test_create_credito(mock_model, mock_session):
    # Mock de un crédito
    credito_mock = MagicMock()
    credito_mock.id = 1
    credito_mock.cliente = "Juan Perez"
    credito_mock.monto = 1000
    credito_mock.tasa_interes = 5
    credito_mock.plazo = 12
    mock_model.return_value = credito_mock

    data = {
        "cliente": "Juan Perez",
        "monto": 1000,
        "tasa_interes": 5,
        "plazo": 12,
        "fecha_otorgamiento": date.today().isoformat()
    }
    created = service.create_credito(data)

    # Validaciones
    assert created.id == 1
    assert created.cliente == "Juan Perez"
    mock_session.add.assert_called_once_with(credito_mock)
    mock_session.commit.assert_called_once()

@patch("services.credit_services.Credito")
def test_get_all_creditos(mock_model):
    c1 = MagicMock(cliente="A")
    c2 = MagicMock(cliente="B")
    mock_model.query.all.return_value = [c1, c2]

    result = service.get_all_creditos()
    assert result == [c1, c2]

@patch("services.credit_services.db.session")
@patch("services.credit_services.Credito")
def test_get_credito_by_id(mock_model, mock_session):
    credito_mock = MagicMock()
    credito_mock.id = 5
    credito_mock.cliente = "Carlos"
    mock_session.get.return_value = credito_mock

    fetched = service.get_credito_by_id(5)
    assert fetched.cliente == "Carlos"
    mock_session.get.assert_called_once_with(mock_model, 5)

@patch("services.credit_services.db.session")
@patch("services.credit_services.Credito")
def test_update_credito(mock_model, mock_session):
    credito_mock = MagicMock()
    credito_mock.cliente = "Ana"
    credito_mock.monto = 300
    credito_mock.plazo = 5
    mock_session.get.return_value = credito_mock

    data_update = {"monto": 400, "plazo": 6}
    updated = service.update_credito(1, data_update)

    assert updated.monto == 400
    assert updated.plazo == 6
    assert updated.cliente == "Ana"
    mock_session.commit.assert_called_once()

@patch("services.credit_services.db.session")
@patch("services.credit_services.Credito")
def test_delete_credito(mock_model, mock_session):
    credito_mock = MagicMock()
    mock_session.get.return_value = credito_mock

    result = service.delete_credito(1)
    assert result is True
    mock_session.delete.assert_called_once_with(credito_mock)
    mock_session.commit.assert_called_once()

def test_get_statistics():
    # Parches: db.session y Credito
    with patch("services.credit_services.db.session") as mock_session, \
         patch("services.credit_services.Credito") as mock_credito:

        # Mock del query base
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query

        # total_monto
        mock_query.with_entities.return_value.scalar.side_effect = [600, 3]

        # Por cliente: [('A', 300, 2), ('B', 300, 1)]
        por_cliente_mock = MagicMock()
        por_cliente_mock.group_by.return_value.all.return_value = [
            ("A", 300, 2),
            ("B", 300, 1)
        ]
        # Cuando se llama con Credito.cliente, sum, count
        def with_entities_side_effect(*args, **kwargs):
            if len(args) == 3:  # Credito.cliente, sum, count
                return por_cliente_mock
            return mock_query.with_entities.return_value
        mock_query.with_entities.side_effect = with_entities_side_effect

        # Ejecutar función
        stats = service.get_statistics()

        # Asserts
        assert stats["total_monto"] == 600
        assert stats["total_count"] == 3
        assert any(c["cliente"] == "A" and c["total"] == 300 and c["count"] == 2 for c in stats["por_cliente"])
        assert any(c["cliente"] == "B" and c["total"] == 300 and c["count"] == 1 for c in stats["por_cliente"])
