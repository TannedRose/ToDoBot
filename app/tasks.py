from celery import shared_task

import logging

import httpx

from bot.config import settings

logger = logging.getLogger(__name__)

@shared_task
def send_task_reminder(user_id: int, title: str, due_date: str):
    try:
        message = f"🔔 Напоминание: «{title}»"
        # message = (f"🔔 Напоминание: задача «{title}» должна быть выполнена до"
        #            f" {str(due_date)[:-6].replace('T', ' ')}")

        url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": user_id,
            "text": message
        }
        response = httpx.post(url, json=payload)
        response.raise_for_status()

        logger.info(f"✅ Напоминание отправлено пользователю {user_id}: {title}")
        return {"status": "sent", "user_id": user_id, "title": title}

    except Exception as e:
        logger.error(f"❌ Ошибка при отправке напоминания: {e}")
        return {"status": "error", "error": str(e)}
