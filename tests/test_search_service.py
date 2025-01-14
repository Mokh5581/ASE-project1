# tests/test_search_service.py
# tests/test_search_service.py

from unittest.mock import Mock
from src.charging.application.services.search_service import SearchService
# from charging.domain.entities.charging_station import ChargingStation

def test_search_by_postal_code():
    # Mock repository
    mock_repo = Mock()
    mock_repo.get_stations_by_postal_code.return_value = [
        ChargingStation("1", "10117", (52.52, 13.40), "Available"),
        ChargingStation("2", "10117", (52.53, 13.41), "Available")
    ]
    service = SearchService(mock_repo)
    stations = service.search_by_postal_code("10117")
    assert len(stations) == 2
    assert all(isinstance(station, ChargingStation) for station in stations)










# from charging.application.services.search_service import SearchService
#
# def test_search_by_postal_code():
#     service = SearchService()
#     result = service.search_by_postal_code("10115")
#     assert len(result) > 0
#     assert all(station.postal_code == "10115" for station in result)
