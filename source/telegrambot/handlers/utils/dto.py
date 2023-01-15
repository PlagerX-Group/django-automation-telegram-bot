from telegram import Update


def update_to_dict(update: Update) -> dict:
    user = update.effective_user.to_dict()
    return dict(
        user_id=user.get("id"),
        first_name=user.get("first_name"),
        last_name=user.get("last_name"),
    )
