from backend.analyzer import analyze_password

def test_empty_password_has_zero_score():
    result = analyze_password("")
    assert result.score == 0
    assert result.category == "weak"

def test_very_short_password_is_weak():
    result = analyze_password("abc")
    assert result.category == "weak"
    assert result.score < 35

def test_strong_password_scores_high():
    result = analyze_password("Tr@v3l$2024!Nz")
    assert result.score >= 80
    assert result.category == "strong"

def test_password_with_all_character_types_passes_variety_check():
    result = analyze_password("Abcdef1!")
    variety = next(c for c in result.criteria if c.name == "character_variety")
    assert variety.passed is True

def test_password_missing_special_chars_fails_variety_partially():
    result = analyze_password("Abcdefgh1")
    variety = next(c for c in result.criteria if c.name == "character_variety")
    assert "special symbols" in variety.message.lower() or not variety.passed or variety.points < 30

def test_repeated_charactes_are_penalized():
    result = analyze_password("Paaaassword1!")
    repetition = next(c for c in result.criteria if c.name == "repetition")
    assert repetition.passed is False
    assert repetition.points == 0

def test_no_repetition_passes():
    result = analyze_password("Tr@v3l$2024!Nz")
    repetition = next(c for c in result.criteria if c.name == "repetition")
    assert repetition.passed is True

def test_numeric_sequence_is_detected():
    result = analyze_password("MyPass123!")
    sequences = next(c for c in result.criteria if c.name == "sequences")
    assert sequences.passed is False

def test_keyboard_sequence_is_detected():
    result = analyze_password("MyQwerty1!")
    sequences = next(c for c in result.criteria if c.name == "sequences")
    assert sequences.passed is False

def test_no_sequence_passed():
    result = analyze_password("Tr@v3l$2024!Nz")
    sequences = next(c for c in result.criteria if c.name == "sequences")
    assert sequences.passed is True


def test_common_pattern_is_detedcted():
    result = analyze_password("password123!")
    common = next(c for c in result.criteria if c.name == "common_patterns")
    assert common.passed is False

def test_no_common_pattern_passes():
    result = analyze_password("Tr@v3l$2024!Nz")
    common = next(c for c in result.criteria if c.name == "common_patterns")
    assert common.passed is True

def test_suggestions_are_provided_for_weak_password():
    result = analyze_password("abc")
    assert len(result.suggestions) > 0

def test_suggestions_show_success_message_for_strong_password():
    result = analyze_password("Tr@v3l$2024!Nz")
    assert any("strong" in s for s in result.suggestions)

def test_score_never_exceeds_100():
    result = analyze_password("&()faW1E679#48k(OmX)9()wXck56h")
    assert result.score <=100

def test_categories_are_consistent_with_score():
    weak = analyze_password("abc")
    strong = analyze_password("Tr@v3l$2024!Nz")
    assert weak.score < strong.score

def test_trivial_password_gets_zero_score():
    result = analyze_password("123")
    assert result.score == 0
    assert result.category == "weak"
 
 
def test_trivial_password_has_sarcastic_suggestion():
    result = analyze_password("qwerty")
    assert len(result.suggestions) == 1
    assert result.suggestions[0] 
 
 
def test_password_containing_trivial_substring_is_not_zeroed():
    result = analyze_password("MyPass123!")
    assert result.score > 0
 
def test_password_under_four_chars_always_gets_zero():
    for pwd in ["a", "ab", "abc", "Z@9", "!!!"]:
        result = analyze_password(pwd)
        assert result.score == 0