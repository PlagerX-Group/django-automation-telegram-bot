from typing import Dict, List, Optional, Union

import telegram
from application import celery_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery_app.task(ignore_result=True)
def broadcast_message(
    user_ids: List[Union[str, int]],
    text: str,
    entities: Optional[List[Dict]] = None,
    reply_markup: Optional[List[List[Dict]]] = None,
    sleep_between: float = 0.4,
    parse_mode=telegram.ParseMode.HTML,
) -> None:
    """It's used to broadcast message to big amount of telegramusers"""
    # logger.info(f"Going to send message: '{text}' to {len(user_ids)} telegramusers")
    #
    # entities_ = from_celery_entities_to_entities(entities)
    # reply_markup_ = from_celery_markup_to_markup(reply_markup)
    # for user_id in user_ids:
    #     try:
    #         send_one_message(
    #             user_id=user_id,
    #             text=text,
    #             entities=entities_,
    #             parse_mode=parse_mode,
    #             reply_markup=reply_markup_,
    #         )
    #         logger.info(f"Broadcast message was sent to {user_id}")
    #     except Exception as e:
    #         logger.error(f"Failed to send message to {user_id}, reason: {e}")
    #     time.sleep(max(sleep_between, 0.1))
    #
    # logger.info("Broadcast finished!")
