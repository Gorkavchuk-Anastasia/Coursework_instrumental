class User:
    def __init__(self, role):
        self.role = role

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'
