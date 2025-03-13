from time import sleep

from functions import *
from datetime import datetime, timedelta

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
    print("We are going to sleep to wait apply tariff")
    sleep(20)
    print("Go on")
    location_id = r.exchange_the_connect_token()
    response_tariff_rates = r.fetch_tariff_rates(location_id)
    assert response_tariff_rates.get('request').get('end_time') == end_time, "End time mismatch"
    assert response_tariff_rates.get('request').get('start_time') == current_time, "Start time mismatch"
    assert response_tariff_rates.get('currency_code') == 'GBP', "Currency mismatch"

    expected_valid_from_time = datetime.strptime(current_time, Date_time_format)
    expected_valid_to_time = (expected_valid_from_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    for i, rate in enumerate(response_tariff_rates.get('data')):
        tariff = rate.get('tariff')
        assert rate.get('valid_from') == expected_valid_from_time.strftime(Date_time_format), f"Check valid_from time failed in {i=}"
        assert rate.get('valid_to') == expected_valid_to_time.strftime(Date_time_format), f"Check valid_to time failed in {i=}"
        assert tariff.get('confidence') == 1, f"Confidence check failed in {i=}"
        if i != (len(response_tariff_rates.get('data')) - 1):
            expected_valid_from_time = expected_valid_to_time
            expected_valid_to_time = (expected_valid_from_time + timedelta(hours=1))
        else:
            assert rate.get('valid_to') == end_time, "Check final valid_to time failed, should be end_time"


if __name__ == '__main__':
    test_task()
