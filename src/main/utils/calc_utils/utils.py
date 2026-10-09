from collections.abc import Callable
from main.api.schemas.dto.response.account.account_transactions_response import Transactions
import random


def get_transaction_types(transactions: list[Transactions]) -> set[str]:
    return {transaction.type for transaction in transactions}


def round_balance(balance: float) -> int:
    return round(balance)


def get_candidate_id(
        find_by_id: Callable[[int], object | None],
        min_id: int,
        max_id: int,
        max_attempts: int = 100,
) -> int:
    for _ in range(max_attempts):
        candidate_id = random.randint(min_id, max_id)

        if find_by_id(candidate_id) is None:
            return candidate_id

    raise RuntimeError("Не удалось найти несуществующий ID")
