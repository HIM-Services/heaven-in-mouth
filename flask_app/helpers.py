import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


def validate_email(email: str) -> bool:
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}"
    # Check if email matches the pattern
    if (re.fullmatch(pattern, email)):
        # Email is valid
        return True
    else:
        # Email is invalid
        return False


def validate_phone(phone: str) -> bool:
    pattern = r"^[0-9]{5,10}$"
    if (re.fullmatch(pattern, phone)):
        # Phone is valid
        return True
    else:
        # Phone is invalid
        return False


# Change address to latitude and longitude
def geocode_address(address: str) -> dict:
    # user agent is used to identify the application which is making the request
    geolocator = Nominatim(user_agent="heaven-in-mouth")
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return {
                'latitude': location.latitude,
                'longitude': location.longitude
            }
        else:
            raise ValueError('Unable to geocode the address')
    except GeocoderTimedOut:
        raise RuntimeError('Geocoding service timed out')
    except GeocoderServiceError as e:
        raise RuntimeError(f'Geocoding service error: {e}')
    except Exception as e:
        raise RuntimeError(f'Unexpected error: {e}')
