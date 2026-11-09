def is_employee(user):
    return user.groups.filter(name='Employee').exists()


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


def is_it_admin(user):
    return user.groups.filter(name='IT Admin').exists()