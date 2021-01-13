from datetime import datetime
from typing import List, Callable

import inject
import pytest


@inject.autoparams()
def f(a: int, b: str) -> List[str]:
    return [b for _ in range(0, a)]


class A:
    @inject.autoparams()
    def __init__(self, i: int) -> None:
        self.i = i


class B:
    @inject.autoparams()
    def __init__(self, a: A) -> None:
        self.a = a
        self.dt = datetime.now()


class C:
    @inject.autoparams()
    def __init__(self) -> None:
        self.dt = datetime.now()


@inject.autoparams()
def get_b(b: B) -> B:
    return b


@inject.autoparams()
def get_c(c: C) -> C:
    return c


def config(binder: inject.Binder) -> None:
    binder.bind(int, 3)
    binder.bind(str, 'a')
    binder.bind_to_constructor(A, A)
    binder.bind_to_constructor(B, B)
    binder.bind_to_provider(C, lambda: C())


Init = Callable[[], None]


@pytest.fixture()
def init() -> None:
    inject.configure_once(config)


def test_引数なし(init: Init) -> None:
    assert f() == ['a', 'a', 'a']


def test_aだけ(init: Init) -> None:
    assert f(a=1) == ['a']


def test_bだけ(init: Init) -> None:
    assert f(b=1) == [1, 1, 1]


def test_戻り値の型(init: Init) -> None:
    nums: List[str] = f(a=2)
    assert nums == ['a', 'a']


def test_依存先もinjectされていても大丈夫(init: Init) -> None:
    assert B(A(3)).a.i == B().a.i


def test_一度呼び出したらずっと同じインスタンスを返す(init: Init) -> None:
    assert get_b() == get_b()
    assert get_b().dt.timestamp() == get_b().dt.timestamp()


def test_providerを使う場合は毎回別のインスタンスを返す(init: Init) -> None:
    assert get_c() != get_c()
    assert get_c().dt.timestamp() != get_c().dt.timestamp()
