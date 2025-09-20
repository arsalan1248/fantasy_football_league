import secrets

from datetime import datetime
import string

from transactions.models import PlayerTransaction


def generate_transaction_no():
    prefix = "TXN"
    date_part = datetime.now().strftime("%y%m%d")  # YYMMDD format
    chars = string.ascii_uppercase + string.digits

    for _ in range(5):
        random_part = "".join(secrets.choice(chars) for _ in range(10))  # 5 chars
        txn_no = f"{prefix}-{date_part}-{random_part}"

        if not PlayerTransaction.objects.filter(transaction_no=txn_no).exists():
            return txn_no

    raise Exception("Failed to generate unique transaction number after 5 attempts")
