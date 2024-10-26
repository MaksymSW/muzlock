from models import Users
# pylint: disable=no-member


def change_status(tg_id: int, status: bool) -> None:
    user = Users.objects(tg_id=tg_id).first()
    user.is_active = status
    user.save()


def check_user(tg_id: int) -> bool:
    user = Users.objects(tg_id=tg_id).first()
    print(user)
    if user:
        return True
    else:
        return False


def create_user(first_name, last_name, tg_id, lang):
    if check_user(tg_id):
        print('User exists')
        change_status(tg_id, True)
        return
    new_user = Users(
        first_name=first_name,
        last_name=last_name,
        tg_id=tg_id,
        language=lang
    )
    new_user.save()
    print('New user added.')


def get_all_users() -> list[Users]:
    users = Users.objects(is_active=True).all()
    return users
