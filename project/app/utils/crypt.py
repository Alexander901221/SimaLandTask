import bcrypt


def crypt_pass(password: str):
    """
    Crypt password
    :param password: str
    :return: hash crypt password
    """
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt).decode('utf-8')
    return hashed


def check_pass(password: str, hash_pass: str):
    """
    Check valid password
    :param password: str
    :param hash_pass: bytes
    :return: bool
    """
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hash_pass.encode('utf-8'))
