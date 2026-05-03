"""Phone number lookup using the phonenumbers library (Google libphonenumber)."""

import phonenumbers
from phonenumbers import carrier, geocoder, timezone


def lookup_number(raw_number: str, default_region: str = "IN") -> dict:
    """Return publicly available info for *raw_number*.

    Returns a dict with keys: valid, international, national, country,
    region, carrier, timezone, number_type.
    """
    try:
        parsed = phonenumbers.parse(raw_number, default_region)
    except phonenumbers.NumberParseException as exc:
        return {"error": str(exc)}

    if not phonenumbers.is_valid_number(parsed):
        return {"error": "Invalid phone number."}

    num_type_map = {
        phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
        phonenumbers.PhoneNumberType.MOBILE: "Mobile",
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
        phonenumbers.PhoneNumberType.TOLL_FREE: "Toll Free",
        phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
        phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
        phonenumbers.PhoneNumberType.VOIP: "VoIP",
        phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
        phonenumbers.PhoneNumberType.PAGER: "Pager",
        phonenumbers.PhoneNumberType.UAN: "UAN",
        phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
    }

    tz_list = timezone.time_zones_for_number(parsed)

    return {
        "valid": True,
        "international": phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        ),
        "national": phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.NATIONAL
        ),
        "country": geocoder.country_name_for_number(parsed, "en"),
        "region": geocoder.description_for_number(parsed, "en"),
        "carrier": carrier.name_for_number(parsed, "en") or "Unknown",
        "timezone": ", ".join(tz_list) if tz_list else "Unknown",
        "number_type": num_type_map.get(
            phonenumbers.number_type(parsed), "Unknown"
        ),
    }
