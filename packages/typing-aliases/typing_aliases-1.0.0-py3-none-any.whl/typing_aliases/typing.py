from builtins import isinstance as is_instance
from builtins import issubclass as is_subclass
from os import PathLike
from typing import Any, Awaitable, Callable, Dict, Iterable, Mapping, Tuple, Type, TypeVar, Union

from typing_extensions import ParamSpec, TypeAlias

__all__ = (
    # types
    "AnyType",
    # exceptions
    "AnyException",
    "AnyExceptionType",
    "ExceptionType",
    # functions
    "DynamicCallable",
    "AnyCallable",
    "Nullary",
    "Unary",
    "Binary",
    "Ternary",
    "Quaternary",
    "Decorator",
    "DecoratorIdentity",
    "ClassDecorator",
    "ClassDecoratorIdentity",
    "Predicate",
    "Parse",
    # async functions
    "DynamicAsyncCallable",
    "AnyAsyncCallable",
    "AsyncNullary",
    "AsyncUnary",
    "AsyncBinary",
    "AsyncTernary",
    "AsyncQuaternary",
    "AsyncPredicate",
    # into
    "Pairs",
    "IntoMapping",
    "IntoPath",
    # string-related
    "StringPairs",
    "StringDict",
    "StringMapping",
    "IntoStringMapping",
    # tuples
    "EmptyTuple",
    "Tuple1",
    "Tuple2",
    "Tuple3",
    "Tuple4",
    "Tuple5",
    "Tuple6",
    "Tuple7",
    "Tuple8",
    "DynamicTuple",
    # type guards
    "is_instance",
    "is_subclass",
)

# types

AnyType: TypeAlias = Type[Any]

C = TypeVar("C", bound=AnyType)
D = TypeVar("D", bound=AnyType)

# exceptions

AnyException: TypeAlias = BaseException
AnyExceptionType: TypeAlias = Type[AnyException]

ExceptionType: TypeAlias = Type[Exception]

# functions

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
W = TypeVar("W")
R = TypeVar("R")

P = ParamSpec("P")

DynamicCallable: TypeAlias = Callable[..., T]
AnyCallable: TypeAlias = DynamicCallable[Any]

F = TypeVar("F", bound=AnyCallable)
G = TypeVar("G", bound=AnyCallable)

Nullary: TypeAlias = Callable[[], R]
Unary: TypeAlias = Callable[[T], R]
Binary: TypeAlias = Callable[[T, U], R]
Ternary: TypeAlias = Callable[[T, U, V], R]
Quaternary: TypeAlias = Callable[[T, U, V, W], R]

Decorator: TypeAlias = Unary[F, G]
DecoratorIdentity: TypeAlias = Decorator[F, F]

ClassDecorator: TypeAlias = Unary[C, D]
ClassDecoratorIdentity: TypeAlias = ClassDecorator[C, C]

Predicate: TypeAlias = Unary[T, bool]

Parse: TypeAlias = Unary[str, T]

# async functions

DynamicAsyncCallable: TypeAlias = Callable[..., Awaitable[T]]
AnyAsyncCallable: TypeAlias = DynamicAsyncCallable[Any]

AsyncNullary: TypeAlias = Nullary[Awaitable[R]]
AsyncUnary: TypeAlias = Unary[T, Awaitable[R]]
AsyncBinary: TypeAlias = Binary[T, U, Awaitable[R]]
AsyncTernary: TypeAlias = Ternary[T, U, V, Awaitable[R]]
AsyncQuaternary: TypeAlias = Quaternary[T, U, V, W, Awaitable[R]]

AsyncPredicate: TypeAlias = AsyncUnary[T, bool]

# into

Pairs: TypeAlias = Iterable[Tuple[T, U]]

IntoMapping: TypeAlias = Union[Pairs[T, U], Mapping[T, U]]

try:  # pragma: no cover
    IntoPath: TypeAlias = Union[str, PathLike[str]]  # type: ignore

except TypeError:  # pragma: no cover
    IntoPath: TypeAlias = Union[str, PathLike]  # type: ignore


# string-related

StringPairs: TypeAlias = Pairs[str, T]
StringDict: TypeAlias = Dict[str, T]
StringMapping: TypeAlias = Mapping[str, T]

IntoStringMapping: TypeAlias = IntoMapping[str, T]

# tuples

EmptyTuple: TypeAlias = Tuple[()]

Tuple1: TypeAlias = Tuple[T]
Tuple2: TypeAlias = Tuple[T, T]
Tuple3: TypeAlias = Tuple[T, T, T]
Tuple4: TypeAlias = Tuple[T, T, T, T]
Tuple5: TypeAlias = Tuple[T, T, T, T, T]
Tuple6: TypeAlias = Tuple[T, T, T, T, T, T]
Tuple7: TypeAlias = Tuple[T, T, T, T, T, T, T]
Tuple8: TypeAlias = Tuple[T, T, T, T, T, T, T, T]

DynamicTuple: TypeAlias = Tuple[T, ...]
