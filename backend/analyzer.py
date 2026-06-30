import re
import random
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

def _load_lines(filename: str) -> list[str]:
    path = DATA_DIR / filename
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
    
COMMON_PATTERNS = _load_lines("common_patterns.txt")
KEYBOARD_SEQUENCES = _load_lines("keyboard_sequences.txt")
TRIVIAL_PASSWORDS = set(_load_lines("trivial_passwords.txt"))
SARCASTIC_MESSAGE = _load_lines("sarcastic_message.txt")

@dataclass
class CriterionResult:
    name: str
    passed: bool
    points: int
    max_points: int
    message: str

@dataclass
class PasswordAnalysis:
    score: int
    category: str
    criteria: list[CriterionResult] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    web_comment: str = ""

def _check_trivial(password: str) -> bool:
    return password.lower() in TRIVIAL_PASSWORDS

def _check_length(password: str) -> CriterionResult:
    length = len(password)
    if length >=16:
        points = 30
    elif length >= 12:
        points = 24
    elif length >=8:
        points = 16
    elif length >=6:
        points = 8
    else:
        points = 0

    passed = length >= 8
    message = f"Length of password: {length} symbols"
    if not passed:
        message += " (recommended minimum is 8)"

    return CriterionResult("length", passed, points, 30, message)

def _check_character_variety(password: str) -> CriterionResult:
    has_lower = bool(re.search(r"[a-zа-яё]", password, re.IGNORECASE))
    has_upper = bool(re.search(r"[A-ZА-ЯЁ]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^a-zA-Zа-яА-ЯёЁ0-9]", password))

    types_present = sum([has_lower, has_upper, has_digit, has_special])
    points = types_present * 7 + (2 if types_present == 4 else 0)
    missing = []
    if not has_lower:
        missing.append("lower case letters")
    if not has_upper:
        missing.append("upper case letters")
    if not has_digit:
        missing.append("numbers")
    if not has_special:
        missing.append("special symbols (!@#$%...)")

    passed = types_present == 4
    if missing:
        message = f"Missing: {', '.join(missing)}"
    else:
        message = "All character types are used"

    return CriterionResult("character_variety", passed, points, 30, message)

def _check_repetition(password: str) -> CriterionResult:
    max_repeat = 1
    current_repeat = 1

    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            current_repeat +=1
            max_repeat = max(max_repeat, current_repeat)
        else:
            current_repeat = 1
    
    if max_repeat >= 4:
        points = 0
        passed = False
        message = f"Found {max_repeat} same symbols in a row"

    elif max_repeat == 3:
        points = 5
        passed = False
        message = "Found 3 same symbols in a row"

    else:
        points = 15
        passed = True
        message = "No suspicious character repetitions"

    return CriterionResult("repetition", passed, points, 15, message)

def _check_sequences(password: str) -> CriterionResult:
    lower = password.lower()
    has_numeric_sequence = bool(
        re.search(r"(012|123|234|345|456|567|678|789|987|876|765|654|543|432|321|210)", lower)

    )
    has_alpha_sequence = bool(
        re.search(r"(abc|bcd|cde|def|efg|xyz|wxy)", lower)
    )
    has_keyboard_sequence = any( seq in lower for seq in KEYBOARD_SEQUENCES)

    found_issues = []
    if has_numeric_sequence:
        found_issues.append("numeric sequence")
    if has_alpha_sequence:
        found_issues.append("alphabet sequence")
    if has_keyboard_sequence:
        found_issues.append("keyboard sequence")
    
    if found_issues:
        points = 0
        passed = False
        message = f"Found: {', '.join(found_issues)}"
    else:
        points = 15
        passed = True
        message = "No obvious sequences found"

    return CriterionResult("sequences", passed, points, 15, message)

def _check_common_patterns(password: str) -> CriterionResult:
    lower = password.lower()
    found = [pattern for pattern in COMMON_PATTERNS if pattern in lower]

    if found:
        points = 0
        passed = False
        message = f"Has a common pattern: {', '.join(found)}"
    else:
        points = 10
        passed = True
        message = "Doesn't have common keyword-passwords"
    return CriterionResult("common_patterns", passed, points, 10, message)

def _categorize(score: int) -> str:
    if score >= 80:
        return "strong"
    if score >=60:
        return "good"
    if score >= 35:
        return "fair"
    return "weak"

def _apply_critical_caps(password: str, criteria: list[CriterionResult], score: int) -> int:
    length = len(password)
    if length <=6:
        score = min(score, 40)
    common_check = next((c for c in criteria if c.name == "common_patterns"), None)
    if common_check and not common_check.passed:
        score = min(score, 15)
    sequences_check = next((c for c in criteria if c.name == "sequences"), None)
    if sequences_check and not sequences_check.passed:
        score = min(score, 25)
 
    return score

def _build_suggestions(criteria: list[CriterionResult], password: str) -> list:
    suggestions = []
    for criterion in criteria:
        if criterion.passed:
            continue
        if criterion.name == "length":
            suggestions.append("Increase the password length to at least 12 symbols")
        elif criterion.name == "character_variety":
            suggestions.append(criterion.message.replace("Doesn't have: ", "Please add: "))
        elif criterion.name == "repetition":
            suggestions.append("Avoid repeating same symbol several times in a row")
        elif criterion.name == "sequences":
            suggestions.append("Avoid obvious patterns (123, abc, qwerty)")
        elif criterion.name == "common_patterns":
            suggestions.append("Please don't use common keyword passwords")
    if not suggestions:
        suggestions.append("Password looks strong!")

    return suggestions

def analyze_password(password: str) -> PasswordAnalysis:
    if not password:
        return PasswordAnalysis(
            score=0,
            category="weak",
            criteria=[],
            suggestions=["Enter password for analyze"],
        )
    if _check_trivial(password):
        return PasswordAnalysis(
            score=0,
            category="weak",
            criteria=[
                CriterionResult("trivial", False, 0, 100, "This is one of the most common passwords in existence",)
            ],
            suggestions=["Try to add more characters, numbers or specific symbols."],
            web_comment=random.choice(SARCASTIC_MESSAGE),
        )
    if len(password) <= 4:
        return PasswordAnalysis(
            score=0,
            category="weak",
            criteria=[
                CriterionResult(
                    "length",
                    False,
                    0,
                    30,
                    f"Length of password: {len(password)} symbols (recommended minimum is 8)"
                )
            ], 
            suggestions=["Increase the password length to at least 8 symbols"],
            web_comment=random.choice(SARCASTIC_MESSAGE),
        )
    criteria = [
        _check_length(password),
        _check_character_variety(password),
        _check_repetition(password),
        _check_sequences(password),
        _check_common_patterns(password),
    ]
    score = min(100, sum(c.points for c in criteria))
    score = _apply_critical_caps(password, criteria, score)

    category = _categorize(score)
    suggestions = _build_suggestions(criteria, password)

    return PasswordAnalysis(
        score=score,
        category=category,
        criteria=criteria,
        suggestions=suggestions,
    )