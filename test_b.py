import pytest
from . import b
import json

#
# What are the desired behaviors? #
# Exit gracefully with error message #
# when api call fails or gmial fails
# Desired formatting gets sent#
#

def test_format_success(mocker):
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {'speciesCode': 'rthhum',
        'comName': 'Ruby-throated Hummingbird',
        'sciName': 'Archilochus colubris',
        'locId': 'L25409552',
        'locName': 'Francis apartment - main',
        'obsDt': '2026-04-09 07:27',
        'howMany': 1,
        'lat': 35.232011,
        'lng': -80.768777,
        'obsValid': True,
        'obsReviewed': False,
        'locationPrivate': True,
        'subId': 'S319096882'}
    ]
    result = b.getNearby()
    print(repr(result))
    assert result == '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>count</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Ruby-throated Hummingbird</th>\n      <td>1</td>\n    </tr>\n  </tbody>\n</table>'

def test_api_failure(mocker):
#    mock_get = mocker.patch('requests.get', side_effect=ValueError())
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 404
    with pytest.raises(ValueError):
        b.getNearby()
