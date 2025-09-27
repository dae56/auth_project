class DuplicateEmail(Exception):
    def __init__(self, email: str):
        super().__init__(f"The user with the email <{email}> already exists.")
