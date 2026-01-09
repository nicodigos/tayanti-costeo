from decimal import Decimal, InvalidOperation

def to_decimal(value, field_name: str) -> Decimal:
    try:
        d = Decimal(str(value))
    except (InvalidOperation, TypeError):
        raise ValueError(f"{field_name} must be a number.")
    return d

def require_nonempty(text: str, field_name: str) -> str:
    t = (text or "").strip()
    if not t:
        raise ValueError(f"{field_name} is required.")
    return t

def require_int(value, field_name: str) -> int:
    try:
        i = int(value)
    except Exception:
        raise ValueError(f"{field_name} must be an integer.")
    if i <= 0:
        raise ValueError(f"{field_name} must be > 0.")
    return i

def require_decimal_gt(value, field_name: str, min_value: Decimal) -> Decimal:
    d = to_decimal(value, field_name)
    if d <= min_value:
        raise ValueError(f"{field_name} must be > {min_value}.")
    return d

def require_decimal_gte(value, field_name: str, min_value: Decimal) -> Decimal:
    d = to_decimal(value, field_name)
    if d < min_value:
        raise ValueError(f"{field_name} must be >= {min_value}.")
    return d

def require_percentage_0_100(value, field_name: str) -> Decimal:
    d = to_decimal(value, field_name)
    if d < 0 or d > 100:
        raise ValueError(f"{field_name} must be between 0 and 100.")
    return d
