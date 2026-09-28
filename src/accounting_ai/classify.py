"""Suggest account types by comparing account-name sentence embeddings."""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from accounting_ai.types.ledger import AccountType

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Representative names let each category cover several accounting concepts.
ACCOUNT_EXAMPLES = {
    AccountType.asset: (
        "Cash", "Bank balance", "Accounts receivable", "Inventory", "Supplies",
        "Prepaid insurance", "Equipment", "Land", "Buildings",
        "Accumulated depreciation",
    ),
    AccountType.liability: (
        "Accounts payable", "Notes payable", "Loans payable", "Salaries payable",
        "Interest payable", "Taxes payable", "Unearned service revenue",
    ),
    AccountType.capital: (
        "Owner's capital", "Owner's equity", "Owner's withdrawal",
        "Retained earnings", "Share capital", "Dividends",
    ),
    AccountType.revenue: (
        "Sales revenue", "Service revenue", "Interest income", "Rental income",
        "Commission income", "Fees earned",
    ),
    AccountType.expenses: (
        "Salaries expense", "Rent expense", "Supplies expense", "Insurance expense",
        "Depreciation expense", "Interest expense", "Utilities expense",
        "Cost of goods sold", "Advertising expense",
    ),
}


@lru_cache(maxsize=1)
def _load_classifier():
    """Load the model and encode reference names once per process.

    The first call downloads the model from Hugging Face if it is not cached.
    CPU inference keeps this small model usable without a GPU.
    """
    model = SentenceTransformer(MODEL_NAME, device="cpu")
    labels = []
    examples = []
    for account_type, names in ACCOUNT_EXAMPLES.items():
        for name in names:
            labels.append(account_type)
            examples.append(f"Accounting account: {name}")
    embeddings = model.encode(examples, normalize_embeddings=True)
    return model, labels, embeddings


def classify_account(account_name: str) -> AccountType:
    """Return the type of the most semantically similar reference account.

    MiniLM is a general embedding model, not a trained accounting classifier.
    This nearest-example prediction is a suggestion and may be inaccurate for
    ambiguous or unfamiliar names. Blank names raise ValueError.
    """
    account_name = account_name.strip()
    if not account_name:
        raise ValueError("Account name must not be empty.")

    model, labels, reference_embeddings = _load_classifier()
    embedding = model.encode(
        f"Accounting account: {account_name}", normalize_embeddings=True
    )
    # The dot product of normalized embeddings is cosine similarity.
    similarities = reference_embeddings @ embedding
    return labels[int(similarities.argmax())]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Suggest an account type with MiniLM.")
    parser.add_argument("account_name", nargs="?", default="Cash")
    args = parser.parse_args()
    print(classify_account(args.account_name).value)
