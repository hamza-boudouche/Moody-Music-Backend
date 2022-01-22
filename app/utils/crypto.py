from bcrypt import hashpw, gensalt, checkpw


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    # 		the parameter 10 given to the gensalt function defines the slowness of the check
    # 		slowness is desirable because it protects against brute force attacks
    return hashpw(plain_text_password.encode("utf-8"), gensalt(10)).decode("utf-8")


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return checkpw(plain_text_password.encode("utf-8"), hashed_password.encode("utf-8"))


if __name__ == "__main__":
    print(get_hashed_password("test123"))
