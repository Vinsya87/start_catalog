import logging
from decimal import Decimal

logger = logging.getLogger(__name__)
from django.core.exceptions import ObjectDoesNotExist
from moneybox.models import BalanceChange, UserBalance
from tgbot.views import system_telegram_message
from yookassa import Payment


def is_payment_exists(payment_id, user_id):
    try:
        payment = Payment.find_one(payment_id)
        change = BalanceChange.objects.get(id=payment.metadata['table_id'])
        if (payment.id == payment_id and
                payment.metadata['user_id'] == str(user_id) and
                not change.is_accepted):
            return True
    except Exception as e:
        error_message = f'Ошибка проверки существования платежа {e} - {user_id}'
        logger.exception("Ошибка: %s", error_message)
        system_telegram_message(error_message)
    return False


def payment_acceptance(response):
    try:
        table = BalanceChange.objects.get(
            id=response['object']['metadata']['table_id']
        )
    except ObjectDoesNotExist as e:
        payment_id = response['object']['id']
        error_message = (
            f'Невозможно получить таблицу по идентификатору {response["object"]["metadata"]["table_id"]}. '
            f'Идентификатор платежа: {payment_id}. '
            f'Ошибка: {str(e)}'
        )
        logger.exception("Ошибка при получении таблицы: %s", error_message)
        system_telegram_message(error_message)
        return False

    if response['event'] == 'payment.succeeded':
        user_id = response['object']['metadata']['user_id']
        income_amount = Decimal(response['object']['amount']['value'])

        # Проверяем, существует ли платеж у YooKassa
        if is_payment_exists(response['object']['id'], user_id):
            table.is_accepted = True
            table.save()
            UserBalance.deposit(
                user=user_id,
                amount=income_amount,
            )
        else:
            obj_id = response['object']['id']
            error_message = (
                'Платеж не найден или не соответствует пользователю:',
                f'Ошибка: {obj_id}, {user_id}')
            logger.exception("Ошибка: %s", error_message)
            system_telegram_message(error_message)

    elif response['event'] == 'payment.canceled':
        table.delete()
        error_message = f'отмена и удаление {table}'
        logger.exception("Ошибка: %s", error_message)
        system_telegram_message(error_message)
    return True
