"""Tests for the Nexus world model."""

from nexus.core.world_model import WorldModel


def test_world_model_update_and_get_state():
    model = WorldModel()
    model.update({"foo": "bar"})
    assert model.get_state() == {"foo": "bar"}


def test_world_model_clear():
    model = WorldModel()
    model.update({"a": 1})
    model.clear()
    assert model.get_state() == {}
