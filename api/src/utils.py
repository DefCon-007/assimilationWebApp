from django.contrib.auth import authenticate, login


def authenticateCredentials(username,password) :
    """
    Authenticates set of credentials on a user model
    :param username:
    :param password:
    :return: User object if authentication successful else None
    """
    user = authenticate(username=username, password=password)
    return user


# def addNewEvent() :
#