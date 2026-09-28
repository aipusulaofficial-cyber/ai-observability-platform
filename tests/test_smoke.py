from observability import get_logger


def test_platform_contract_smoke():
    logger = get_logger("contract-smoke")
    assert logger.name == "contract-smoke"
    assert logger.level > 0
