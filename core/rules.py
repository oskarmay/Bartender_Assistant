import rules


@rules.predicate
def is_bartender(user):
    return user.is_bartender()


@rules.predicate
def is_waiter(user):
    return user.is_waiter()


@rules.predicate
def is_customer(user):
    return user.is_customer()


is_in_staff = is_bartender | is_waiter


rules.add_perm("bartender", is_bartender)
rules.add_perm("waiter", is_waiter)
rules.add_perm("customer", is_customer)
rules.add_perm("is_in_staff", is_in_staff)
