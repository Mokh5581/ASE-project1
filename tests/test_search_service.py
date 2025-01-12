# tests/test_search_service.py
from charging.application.services.search_service import SearchService

def test_search_by_postal_code():
    service = SearchService()
    result = service.search_by_postal_code("10115")
    assert len(result) > 0
    assert all(station.postal_code == "10115" for station in result)
