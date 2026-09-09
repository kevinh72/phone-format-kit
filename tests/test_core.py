from phonefmt.core import classify, extract_candidates, format_national, normalize


def test_extract_candidates_finds_multiple_in_one_line():
    text = "call 415-555-0100 or +44 20 7946 0958 for support"
    assert extract_candidates(text) == ["415-555-0100", "+44 20 7946 0958"]


def test_extract_candidates_skips_runs_too_short_to_plausibly_be_a_number():
    assert extract_candidates("code 12345 end") == []


def test_extract_candidates_skips_digits_glued_to_a_leading_word_char():
    # a leading letter (as in an ID like "x4155550100") means this isn't a
    # standalone number, so the candidate boundary must not match here.
    assert extract_candidates("x4155550100") == []


def test_extract_candidates_skips_digits_glued_to_a_trailing_word_char():
    assert extract_candidates("4155550100x") == []


def test_extract_candidates_returns_text_as_written_not_normalized():
    assert extract_candidates("call 415.555.0100 today") == ["415.555.0100"]


def test_classify_matches_known_calling_code_and_length():
    fmt = classify("14155550100")
    assert fmt is not None
    assert fmt.key == "US"


def test_classify_rejects_unknown_calling_code():
    assert classify("9991234567") is None


def test_classify_rejects_right_calling_code_wrong_length():
    # "44" is a real calling code, but the national part here is too short
    # to be a UK number.
    assert classify("4412345") is None


def test_normalize_passes_through_a_leading_plus_when_recognized():
    assert normalize("+1 (415) 555-0100") == "+14155550100"


def test_normalize_rejects_a_leading_plus_when_unrecognized():
    assert normalize("+9991234567") is None


def test_normalize_returns_none_for_text_with_no_digits():
    assert normalize("not a phone number") is None


def test_normalize_returns_none_for_empty_string():
    assert normalize("") is None


def test_normalize_uses_default_country_for_a_locally_dialed_number():
    assert normalize("020 7946 0958", "GB") == "+442079460958"


def test_normalize_applies_default_country_with_no_trunk_prefix_to_strip():
    assert normalize("415-555-0100", "US") == "+14155550100"


def test_normalize_rejects_wrong_length_for_default_country():
    assert normalize("12345", "US") is None


def test_normalize_rejects_unknown_default_country_key():
    assert normalize("4155550100", "ZZ") is None


def test_normalize_default_country_key_is_case_insensitive():
    assert normalize("4155550100", "us") == "+14155550100"


def test_normalize_falls_back_to_calling_code_detection_without_default_country():
    assert normalize("442079460958") == "+442079460958"


def test_normalize_strips_surrounding_whitespace():
    assert normalize("  +1 415 555 0100  ") == "+14155550100"


def test_format_national_uses_the_declared_grouping_when_it_fits():
    assert format_national("+442079460958") == "020 7946 0958"
    assert format_national("415-555-0100", "US") == "415 555 0100"


def test_format_national_falls_back_to_generic_grouping():
    # Italy has no national_groups declared, so this exercises _generic_groups.
    assert format_national("0212345678", "IT") == "021 234 5678"


def test_format_national_returns_none_when_normalize_would():
    assert format_national("not a phone number") is None
