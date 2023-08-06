from typing import Any, Callable, Iterator, Optional


class ChangeEvaluator:
    def __init__(self, func: Callable, key: Optional[Callable] = None, state: bool = True, checks: int = 0) -> None:
        self.func = func
        self.key = key
        self.state = state
        self.checks = checks
        self._previous: Any = None

    @property
    def changed(self) -> bool:
        self.checks += 1
        current = self.func()
        if self.key:
            current = self.key(current)

        if current == self._previous:
            self.state = False
        else:
            self.state = True
            self._previous = current

        return self.state is True

    def cycle(self, max: int) -> Iterator[int]:
        for i in range(max):
            if self.changed:
                yield i
            else:
                return
