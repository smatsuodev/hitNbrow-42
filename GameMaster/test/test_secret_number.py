import pytest

from game.SecretNumber import SecretNumber


@pytest.mark.parametrize(
    ["secret", "challenge", "exp_hit", "exp_blow"],
    [
        ("0123", "0123", 4, 0),
        ("0123", "0124", 3, 0),
        ("0123", "0143", 3, 0),
        ("0123", "0423", 3, 0),
        ("0123", "4123", 3, 0),
        ("1234", "1256", 2, 0),
        ("1234", "1536", 2, 0),
        ("1234", "1564", 2, 0),
        ("1234", "5236", 2, 0),
        ("1234", "5264", 2, 0),
        ("1234", "5634", 2, 0),
        ("5678", "1238", 1, 0),
        ("5678", "1274", 1, 0),
        ("5678", "1634", 1, 0),
        ("5678", "5234", 1, 0),
        ("0123", "1230", 0, 4),
        ("0123", "1234", 0, 3),
        ("0123", "1240", 0, 3),
        ("0123", "1430", 0, 3),
        ("0123", "4230", 0, 3),
        ("0987", "7812", 0, 2),
        ("0987", "7192", 0, 2),
        ("0987", "7120", 0, 2),
        ("0987", "1892", 0, 2),
        ("0987", "1820", 0, 2),
        ("0987", "1290", 0, 2),
        ("0147", "2306", 0, 1),
        ("0147", "2351", 0, 1),
        ("0147", "4356", 0, 1),
        ("0147", "2756", 0, 1),
        ("9876", "1234", 0, 0),
        ("0124", "0421", 2, 2),
        ("8965", "5869", 1, 3),
        ("0861", "8431", 1, 1),
    ]
)
def test_challenge(secret, challenge, exp_hit, exp_blow):
    sec = SecretNumber(number=secret)
    act = sec.get_hit_blow_count(challenge)

    assert act.hit == exp_hit
    assert act.blow == exp_blow


@pytest.mark.parametrize(
    ["secret", "exp_high", "exp_low"],
    [
        ("4444", 0, 4),
        ("0000", 0, 4),
        ("5555", 4, 0),
        ("9999", 4, 0),
        ("0156", 2, 2),
        ("9367", 3, 1),
        ("8043", 1, 3)
    ]
)
def test_high_low(secret, exp_high, exp_low):
    sec = SecretNumber(number=secret)
    act = sec.get_high_low_count()

    assert act.high == exp_high
    assert act.low == exp_low


@pytest.mark.parametrize(
    ["secret", "target", "exp_idx"],
    [
        ("0123", "4", -1),
        ("0123", "0", 0),
        ("0123", "1", 1),
        ("0123", "2", 2),
        ("0123", "3", 3),
    ]
)
def test_target(secret, target, exp_idx):
    sec = SecretNumber(number=secret)
    act = sec.get_number_index(target)

    assert act == exp_idx


@pytest.mark.parametrize(
    ["secret", "changed", "exp_res", "exp_digit", "exp_is_high"],
    [
        ("0123", "0123", False, -1, False),
        ("0123", "0124", True, 3, False),
        ("0123", "0143", True, 2, False),
        ("0123", "0423", True, 1, False),
        ("0123", "4123", True, 0, False),
        ("0123", "5123", False, -1, False),
        ("5678", "9678", True, 0, True),
        ("5678", "5674", False, -1, False),
        ("0123", "1230", False, -1, False),
        ("0123", "0123", False, -1, False),
        ("0123", "0145", False, -1, False),
        ("0123", "0456", False, -1, False),
        ("0123", "4567", False, -1, False),
    ]
)
def test_valid_change(secret, changed, exp_res, exp_digit, exp_is_high):
    sec = SecretNumber(number=secret)
    [act_res, act_digit, act_is_high] = sec.check_valid_change_number(changed)

    assert act_res == exp_res
    assert act_digit == exp_digit
    assert act_is_high == exp_is_high


@pytest.mark.parametrize(
    ["secret", "shuffled", "exp"],
    [
        ("0123", "0123", True),
        ("0123", "0132", True),
        ("0123", "0213", True),
        ("0123", "0231", True),
        ("0123", "0312", True),
        ("0123", "0321", True),
        ("0123", "1023", True),
        ("0123", "1032", True),
        ("0123", "1203", True),
        ("0123", "1230", True),
        ("0123", "1302", True),
        ("0123", "1320", True),
        ("0123", "2013", True),
        ("0123", "2031", True),
        ("0123", "2103", True),
        ("0123", "2130", True),
        ("0123", "2301", True),
        ("0123", "2310", True),
        ("0123", "3012", True),
        ("0123", "3021", True),
        ("0123", "3102", True),
        ("0123", "3120", True),
        ("0123", "3201", True),
        ("0123", "3210", True),
        ("0123", "0124", False),
    ]
)
def test_valid_shuffle(secret, shuffled, exp):
    sec = SecretNumber(number=secret)
    act = sec.check_valid_shuffle_number(shuffled)

    assert act == exp
