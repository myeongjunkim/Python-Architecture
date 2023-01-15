from datetime import date, timedelta

import pytest

from app.exceptions import OutOfStock
from app.models import Batch, OrderLine
from app.utils import allocate

TODAY = date.today()
TOMORROW = TODAY + timedelta(days=1)
THREE_DAYS = TODAY + timedelta(days=3)


def test_prefers_current_stock_batches_to_shipments() -> None:
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=TOMORROW)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches() -> None:
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=TODAY)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=TOMORROW)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=THREE_DAYS)

    line = OrderLine("order1", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref() -> None:
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=TOMORROW)
    line = OrderLine("oref", "HIGHBROW-POSTER", 10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate() -> None:
    batch = Batch("batch1", "SMALL-FORK", qty=10, eta=TODAY)
    allocate(OrderLine("order1", "SMALL-FORK", 10), [batch])
    with pytest.raises(OutOfStock, match="SMALL-FORK"):
        allocate(OrderLine("order2", "SMALL-FORK", 10), [batch])
