"""Various type aliases."""

__description__ = "Various type aliases."
__url__ = "https://github.com/nekitdev/typing-aliases"

__title__ = "typing_aliases"
__author__ = "nekitdev"
__license__ = "MIT"
__version__ = "1.0.0"

from typing_aliases.typing import (
    AnyAsyncCallable,
    AnyCallable,
    AnyException,
    AnyExceptionType,
    AnyType,
    AsyncBinary,
    AsyncNullary,
    AsyncPredicate,
    AsyncQuaternary,
    AsyncTernary,
    AsyncUnary,
    Binary,
    ClassDecorator,
    ClassDecoratorIdentity,
    Decorator,
    DecoratorIdentity,
    DynamicAsyncCallable,
    DynamicCallable,
    DynamicTuple,
    EmptyTuple,
    ExceptionType,
    IntoMapping,
    IntoPath,
    IntoStringMapping,
    Nullary,
    Pairs,
    Parse,
    Predicate,
    Quaternary,
    StringDict,
    StringMapping,
    StringPairs,
    Ternary,
    Tuple1,
    Tuple2,
    Tuple3,
    Tuple4,
    Tuple5,
    Tuple6,
    Tuple7,
    Tuple8,
    Unary,
    is_instance,
    is_subclass,
)

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
