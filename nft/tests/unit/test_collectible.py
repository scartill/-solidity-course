import scripts.helpers as h
from brownie import network
import pytest
from scripts.deploy import deploy


def test_create_collectible():
    if not h.is_localnet():
        pytest.skip()

    (sc, tid) = deploy()
    assert sc.ownerOf(tid) == h.get_account()
