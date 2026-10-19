import hashlib
import hmac
import secrets


PASSWORD_ITERATIONS = 310_000


def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), PASSWORD_ITERATIONS
    )
    return f"pbkdf2_sha256${PASSWORD_ITERATIONS}${salt}${digest.hex()}"


def verify_password(password, stored_hash):
    try:
        algorithm, iterations_text, salt, expected_digest = stored_hash.split("$", 3)
        iterations = int(iterations_text)
        if algorithm != "pbkdf2_sha256" or not 100_000 <= iterations <= 1_000_000:
            return False
        actual_digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
        ).hex()
    except (AttributeError, TypeError, ValueError):
        return False
    return hmac.compare_digest(actual_digest, expected_digest)