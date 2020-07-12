def get_base_context(request):
    context = {}

    return context

def is_existing_user(users_list, username):
    for user in users_list:
        if user.username == username:
            return True

    return False
