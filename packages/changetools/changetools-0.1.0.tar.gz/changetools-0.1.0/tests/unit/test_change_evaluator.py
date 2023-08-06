from changetools import ChangeEvaluator


def test_change_evaluator_simple():
    evaluator = ChangeEvaluator(lambda: 1)
    assert evaluator.changed is True
    assert evaluator.changed is False
    assert evaluator.changed is False


def test_change_evaluator_key():
    evaluator = ChangeEvaluator(lambda: 1, key=lambda x: x % 2)
    assert evaluator.changed is True
    assert evaluator.changed is False
    assert evaluator.changed is False


def test_change_evaluator_cycle():
    evaluator = ChangeEvaluator(lambda: 1)
    assert list(evaluator.cycle(3)) == [0]
    assert list(evaluator.cycle(3)) == []
    assert list(evaluator.cycle(3)) == []


def test_change_evaluator_cycle_key():
    evaluator = ChangeEvaluator(lambda: 1, key=lambda x: x % 2)
    assert list(evaluator.cycle(3)) == [0]
    assert list(evaluator.cycle(3)) == []
    assert list(evaluator.cycle(3)) == []
