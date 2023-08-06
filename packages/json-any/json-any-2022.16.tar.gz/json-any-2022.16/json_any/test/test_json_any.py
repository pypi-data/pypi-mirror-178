# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2022)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from __future__ import annotations

import dataclasses as dtcl
import random as rndm
from array import array as py_array_t
from datetime import date as date_t
from datetime import datetime as date_time_t
from datetime import time as time_t
from datetime import timedelta as time_delta_t
from datetime import timezone as time_zone_t
from enum import Enum as enum_t
from io import BytesIO as io_bytes_t
from pathlib import Path as path_t
from pathlib import PureWindowsPath as windows_path_t
from sys import stderr
from typing import NamedTuple as named_tuple_base_t
from uuid import UUID as uuid_t

import json_any.json_any as jsny

try:
    import matplotlib.pyplot as pypl
except ModuleNotFoundError:
    pypl = None
try:
    import networkx as grph
except ModuleNotFoundError:
    grph = None
try:
    import numpy as nmpy
except ModuleNotFoundError:
    nmpy = None
try:
    import pandas as pnds
except ModuleNotFoundError:
    pnds = None
try:
    import scipy.sparse as sprs
except ModuleNotFoundError:
    sprs = None


if pypl is None:
    figure_t = bytes
else:
    figure_t = pypl.Figure
if grph is None:
    graph_t = bytes
else:
    graph_t = grph.Graph
if nmpy is None:
    array_t = bytes
else:
    array_t = nmpy.ndarray
if pnds is None:
    series_t = data_frame_t = bytes
else:
    series_t = pnds.Series
    data_frame_t = pnds.DataFrame
if sprs is None:
    _SPARSE_ARRAY_CLASSES = None
else:
    _SPARSE_ARRAY_CLASSES = (
        sprs.bsr_array,
        sprs.coo_array,
        sprs.csc_array,
        sprs.csr_array,
        sprs.dia_array,
        sprs.dok_array,
        sprs.lil_array,
    )


class enum_e(enum_t):
    ONE = 1
    TWO = 2
    THREE = 3


class named_tuple_t(named_tuple_base_t):
    string: str
    integer: int


@dtcl.dataclass
class dataclass_t:
    one: int = 1
    two: int = 2
    three: int = dtcl.field(init=False, default=3)


class class_t:
    one: int
    two: int
    three: int

    def __init__(self, one: int, two: int, three: int, /) -> None:
        self.one = one
        self.two = two
        self.three = three

    def __eq__(self, other, /) -> bool:
        if type(other) is type(self):
            return ClassAsTuple(other) == ClassAsTuple(self)

        return False


def NewClassFromTuple(all_three: tuple[int, int, int], /) -> class_t:
    return class_t(*all_three)


def ClassAsTuple(instance: class_t, /) -> tuple[int, int, int]:
    return instance.one, instance.two, instance.three


class class_w_special_methods_t:
    one: int
    two: int
    three: int

    def __init__(self, one: int, two: int, three: int, /) -> None:
        self.one = one
        self.two = two
        self.three = three

    @classmethod
    def __NewFromJsonDescription__(
        cls, all_three: tuple[int, int, int], /
    ) -> class_w_special_methods_t:
        return cls(*all_three)

    def __DescriptionForJSON__(self) -> tuple[int, int, int]:
        return self.one, self.two, self.three

    def __eq__(self, other, /) -> bool:
        if type(other) is type(self):
            return other.__DescriptionForJSON__() == self.__DescriptionForJSON__()

        return False


def CheckJsonization(instance: object, /, *, descriptors=None, builders=None) -> bool:
    """"""
    if hasattr(instance, "AsJsonString"):
        jsoned = instance.AsJsonString()
    else:
        jsoned = jsny.JsonStringOf(instance, descriptors=descriptors)

    return DecodeAndCompare(jsoned, instance, builders=builders)


def DecodeAndCompare(jsoned: str, instance: object, /, *, builders=None) -> bool:
    """"""
    type_ = type(instance)
    if hasattr(type_, "NewFromJsonString"):
        rebuilt = type_.NewFromJsonString(jsoned)
    else:
        rebuilt = jsny.ObjectFromJsonString(jsoned, builders=builders)

    if type(instance) is type(rebuilt):
        if isinstance(instance, io_bytes_t):
            equality = instance.getvalue() == rebuilt.getvalue()
        elif (nmpy is not None) and isinstance(instance, array_t):
            equality = nmpy.array_equal(instance, rebuilt) and (
                instance.dtype == rebuilt.dtype
            )
        elif (nmpy is not None) and nmpy.issubclass_(
            type(instance), (nmpy.bool_, nmpy.number, nmpy.character)
        ):
            equality = (instance == rebuilt) and (instance.dtype == rebuilt.dtype)
        elif (pnds is not None) and isinstance(instance, (data_frame_t, series_t)):
            equality = instance.equals(rebuilt)
        elif (_SPARSE_ARRAY_CLASSES is not None) and isinstance(
            instance, _SPARSE_ARRAY_CLASSES
        ):
            instance_as_array = instance.toarray()
            rebuilt_as_array = rebuilt.toarray()
            equality = nmpy.array_equal(instance_as_array, rebuilt_as_array) and (
                instance_as_array.dtype == rebuilt_as_array.dtype
            )
        elif (grph is not None) and isinstance(instance, graph_t):
            equality = grph.utils.misc.graphs_equal(instance, rebuilt)
        else:
            equality = instance == rebuilt
            if not isinstance(equality, bool):
                print(
                    f"{type(instance).__name__}: Cannot check equality of objects of this type",
                    file=stderr,
                )
                return True
        if equality:
            reason = None
        else:
            reason = "Different values"
    else:
        equality = False
        reason = f"Different types ({type(instance)} != {type(rebuilt)})"

    if equality:
        print(type(instance).__name__, "PASSED")
        return True
    else:
        print(instance, "!=", rebuilt, ":", reason, file=stderr)
        return False


if __name__ == "__main__":
    #
    jsny.AddNumpyNDArrayRepresentation("blosc")
    jsny.AddNumpyNDArrayRepresentation("pca_b_stream")

    instance_ = py_array_t("b")
    instance_.fromlist([0, 1, 2])
    CheckJsonization(instance_)

    for container_t in (bytes, bytearray, frozenset, set, list, tuple):
        instance_ = container_t([0, 1, 2])
        CheckJsonization(instance_)

    instance_ = named_tuple_t(string="string", integer=123)
    CheckJsonization(instance_)

    instance_ = complex(1, 2)
    CheckJsonization(instance_)

    instance_ = date_t(2000, 12, 31)
    CheckJsonization(instance_)
    #
    instance_ = date_time_t(2000, 12, 31, 23, 59, 1)
    CheckJsonization(instance_)
    #
    instance_ = time_t(23, 59, 1)
    CheckJsonization(instance_)
    #
    instance_ = time_delta_t(1, 2, 3)
    CheckJsonization(instance_)
    #
    instance_ = time_zone_t(time_delta_t(seconds=1, microseconds=2), name="fake")
    CheckJsonization(instance_)

    instance_ = enum_e.ONE
    CheckJsonization(instance_)

    instance_ = slice(0, 10, 2)
    CheckJsonization(instance_)

    instance_ = {"one": 1, "two": 2, "three": 3}
    CheckJsonization(instance_)

    instance_ = path_t("/folder/subfolder/file.txt")
    CheckJsonization(instance_)
    #
    instance_ = windows_path_t(r"C:\folder\subfolder\file.txt")
    CheckJsonization(instance_)

    instance_ = io_bytes_t(bytes((0, 1, 2)))
    CheckJsonization(instance_)

    instance_ = uuid_t("12345678123456781234567812345678")
    CheckJsonization(instance_)

    instance_ = dataclass_t(10, 20)
    CheckJsonization(instance_)

    instance_ = class_t(1, 2, 3)
    CheckJsonization(
        instance_,
        descriptors={"": ClassAsTuple},
        builders={"": NewClassFromTuple},
    )

    instance_ = class_w_special_methods_t(1, 2, 3)
    CheckJsonization(instance_)

    # Recursion test (appears as type "dict")
    instance_ = {
        enum_e.ONE: dataclass_t(10, 20),
        time_t(23, 59, 1): [slice(0, 10, 2), path_t("/folder/subfolder/file.txt")],
    }
    CheckJsonization(instance_)

    if nmpy is not None:
        instance_ = nmpy.array([[1, 2, 3], [4, 5, 6]], dtype=bool)
        CheckJsonization(instance_)
        instance_ = nmpy.array([[1, 2, 3], [4, 5, 6]], dtype=nmpy.bool_)
        CheckJsonization(instance_)

        instance_ = nmpy.array([[1, 2, 3], [4, 5, 6]], dtype=int)
        CheckJsonization(instance_)
        instance_ = nmpy.array([[1, 2, 3], [4, 5, 6]], dtype=nmpy.uint16)
        CheckJsonization(instance_)

        instance_ = nmpy.array([[1, 2, 3], [4, 5, 6]], dtype=float)
        CheckJsonization(instance_)
        instance_ = nmpy.array([[1, 2, 3], [4, 5, 6]], dtype=nmpy.float64)
        CheckJsonization(instance_)

        instance_ = nmpy.array([[1, 2, 3], [4, 5, 6]], dtype=complex)
        CheckJsonization(instance_)
        instance_ = nmpy.array([[1, 2, 3], [4, 5, 6]], dtype=nmpy.complex_)
        CheckJsonization(instance_)
        instance_ = nmpy.array([[1, 2, 3], [4, 5, 6]], dtype=nmpy.complex128)
        CheckJsonization(instance_)

        instance_ = nmpy.array([["a", "b", "c"], ["d", "e", "f"]], dtype=str)
        CheckJsonization(instance_)
        instance_ = nmpy.array([["a", "b", "c"], ["d", "e", "f"]], dtype=nmpy.str_)
        CheckJsonization(instance_)

        instance_ = nmpy.bool_(True)
        CheckJsonization(instance_)

        instance_ = nmpy.uint16(1)
        CheckJsonization(instance_)

        instance_ = nmpy.float64(1)
        CheckJsonization(instance_)

        instance_ = nmpy.complex_(1.0 + 2.0j)
        CheckJsonization(instance_)

        instance_ = nmpy.complex128(1.0 + 2.0j)
        CheckJsonization(instance_)

        instance_ = nmpy.str_("a")
        CheckJsonization(instance_)

    if pnds is not None:
        instance_ = pnds.Series([1, 2, 3])
        CheckJsonization(instance_)
        #
        instance_ = pnds.DataFrame([[1, 2, 3], [4, 5, 6]])
        CheckJsonization(instance_)

    if sprs is not None:
        instance_ = sprs.csr_array(nmpy.array([[1, 2, 3], [4, 5, 6]], dtype=nmpy.uint8))
        CheckJsonization(instance_)

    if grph is not None:
        instance_ = grph.fast_gnp_random_graph(10, 0.7, seed=0, directed=True)
        grph.set_node_attributes(
            instance_,
            {_nde: rndm.randrange(100) for _nde in instance_.nodes},
            name="attribute",
        )
        grph.set_edge_attributes(
            instance_,
            {_edg: rndm.randrange(100) for _edg in instance_.edges},
            name="attribute",
        )
        CheckJsonization(instance_)

    if pypl is not None:
        instance_, axes = pypl.subplots()
        axes.plot((0, 1, 2), (5, 4, 6), c="g")
        jsoned_ = jsny.JsonStringOf(instance_)
        rebuilt_ = jsny.ObjectFromJsonString(jsoned_)
        pypl.show()
