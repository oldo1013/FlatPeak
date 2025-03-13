from functions import *


def test_task():
    r = APIRequests()
    r.session_start()
    ecotricity_id = r.provide_uk_address()
    r.provider_select(ecotricity_id)
    r.tariff_structure_select()
    r.market_surcharge_capture()
    r.tariff_name_capture()
    r.contract_term_capture()
    r.save_contract()
    location_id = r.exchange_the_connect_token()
    response_tariff_rates = r.fetch_tariff_rates(location_id)
    assert response_tariff_rates.get('request').get('end_time') == end_time, "End time mismatch"
    assert response_tariff_rates.get('request').get('start_time') == current_time, "Start time mismatch"
    assert response_tariff_rates.get('currency_code') == 'GBP', "Currency mismatch"
    assert all(rate.get("tariff").get("confidence") == 1 for rate in
               response_tariff_rates.get("data")), "Confidence check failed"


if __name__ == '__main__':
    test_task()
