def test_calculate_budget_amount(transaction, transaction_expense):
    sum = transaction.amount - transaction_expense.amount
    assert transaction.budget.amount == sum
