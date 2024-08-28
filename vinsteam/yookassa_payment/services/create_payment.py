import logging

from django.conf import settings

logger = logging.getLogger(__name__)

from django.shortcuts import get_object_or_404
from moneybox.models import BalanceChange
from tgbot.views import system_telegram_message
from users.models import User
from yookassa import Configuration, Payment

Configuration.account_id = settings.YOOKASSA_ID
Configuration.secret_key = settings.YOOKASSA_KEY



def create_payment(serialized_data):
    try:
        value = serialized_data.get('value')
        return_url = serialized_data.get('return_url')
        user_id = serialized_data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        try:
            change = BalanceChange.objects.create(
                account_id=user,
                amount=value,
                is_accepted=False,
                operation_type=BalanceChange.TransactionType.DEPOSIT,
            )
        except Exception as e:
            message = f'Произошла ошибка при создании объекта BalanceChange: {str(e)}'
            logger.exception(message)
            system_telegram_message(message)

        try:
            payment = Payment.create({
                # "payment_method_data": {
                #     "type": "sbp"
                # },
                'amount': {
                    'value': value,
                    'currency': 'RUB',
                },
                'confirmation': {
                    'type': 'redirect',
                    'return_url': return_url,
                    # 'type': 'qr',
                },
                'metadata': {
                    'table_id': change.id,
                    'user_id': user.id,
                    'username': user.username,
                },
                'capture': True,
                'refundable': False,
                'description': 'Пополнение на ' + str(value) + ' от ' + str(user.username),
            })
        except Exception as e:
            message = f'Произошла ошибка при создании объекта Payment: {str(e)}'
            logger.exception(message)
            system_telegram_message(message)

        return payment.confirmation.confirmation_url
    except Exception as e:
        message = f'Произошла общая ошибка в функции create_payment: {str(e)}'
        logger.exception(message)
        system_telegram_message(message)
