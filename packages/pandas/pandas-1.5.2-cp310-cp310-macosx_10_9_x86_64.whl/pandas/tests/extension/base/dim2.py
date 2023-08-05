"""
Tests for 2D compatibility.
"""
import numpy as np
import pytest

from pandas._libs.missing import is_matching_na

import pandas as pd
from pandas.core.arrays.integer import INT_STR_TO_DTYPE
from pandas.tests.extension.base.base import BaseExtensionTests


class Dim2CompatTests(BaseExtensionTests):
    # Note: these are ONLY for ExtensionArray subclasses that support 2D arrays.
    #  i.e. not for pyarrow-backed EAs.

    def test_transpose(self, data):
        arr2d = data.repeat(2).reshape(-1, 2)
        shape = arr2d.shape
        assert shape[0] != shape[-1]  # otherwise the rest of the test is useless

        assert arr2d.T.shape == shape[::-1]

    def test_frame_from_2d_array(self, data):
        arr2d = data.repeat(2).reshape(-1, 2)

        df = pd.DataFrame(arr2d)
        expected = pd.DataFrame({0: arr2d[:, 0], 1: arr2d[:, 1]})
        self.assert_frame_equal(df, expected)

    def test_swapaxes(self, data):
        arr2d = data.repeat(2).reshape(-1, 2)

        result = arr2d.swapaxes(0, 1)
        expected = arr2d.T
        self.assert_extension_array_equal(result, expected)

    def test_delete_2d(self, data):
        arr2d = data.repeat(3).reshape(-1, 3)

        # axis = 0
        result = arr2d.delete(1, axis=0)
        expected = data.delete(1).repeat(3).reshape(-1, 3)
        self.assert_extension_array_equal(result, expected)

        # axis = 1
        result = arr2d.delete(1, axis=1)
        expected = data.repeat(2).reshape(-1, 2)
        self.assert_extension_array_equal(result, expected)

    def test_take_2d(self, data):
        arr2d = data.reshape(-1, 1)

        result = arr2d.take([0, 0, -1], axis=0)

        expected = data.take([0, 0, -1]).reshape(-1, 1)
        self.assert_extension_array_equal(result, expected)

    def test_repr_2d(self, data):
        # this could fail in a corner case where an element contained the name
        res = repr(data.reshape(1, -1))
        assert res.count(f"<{type(data).__name__}") == 1

        res = repr(data.reshape(-1, 1))
        assert res.count(f"<{type(data).__name__}") == 1

    def test_reshape(self, data):
        arr2d = data.reshape(-1, 1)
        assert arr2d.shape == (data.size, 1)
        assert len(arr2d) == len(data)

        arr2d = data.reshape((-1, 1))
        assert arr2d.shape == (data.size, 1)
        assert len(arr2d) == len(data)

        with pytest.raises(ValueError):
            data.reshape((data.size, 2))
        with pytest.raises(ValueError):
            data.reshape(data.size, 2)

    def test_getitem_2d(self, data):
        arr2d = data.reshape(1, -1)

        result = arr2d[0]
        self.assert_extension_array_equal(result, data)

        with pytest.raises(IndexError):
            arr2d[1]

        with pytest.raises(IndexError):
            arr2d[-2]

        result = arr2d[:]
        self.assert_extension_array_equal(result, arr2d)

        result = arr2d[:, :]
        self.assert_extension_array_equal(result, arr2d)

        result = arr2d[:, 0]
        expected = data[[0]]
        self.assert_extension_array_equal(result, expected)

        # dimension-expanding getitem on 1D
        result = data[:, np.newaxis]
        self.assert_extension_array_equal(result, arr2d.T)

    def test_iter_2d(self, data):
        arr2d = data.reshape(1, -1)

        objs = list(iter(arr2d))
        assert len(objs) == arr2d.shape[0]

        for obj in objs:
            assert isinstance(obj, type(data))
            assert obj.dtype == data.dtype
            assert obj.ndim == 1
            assert len(obj) == arr2d.shape[1]

    def test_tolist_2d(self, data):
        arr2d = data.reshape(1, -1)

        result = arr2d.tolist()
        expected = [data.tolist()]

        assert isinstance(result, list)
        assert all(isinstance(x, list) for x in result)

        assert result == expected

    def test_concat_2d(self, data):
        left = type(data)._concat_same_type([data, data]).reshape(-1, 2)
        right = left.copy()

        # axis=0
        result = left._concat_same_type([left, right], axis=0)
        expected = data._concat_same_type([data] * 4).reshape(-1, 2)
        self.assert_extension_array_equal(result, expected)

        # axis=1
        result = left._concat_same_type([left, right], axis=1)
        assert result.shape == (len(data), 4)
        self.assert_extension_array_equal(result[:, :2], left)
        self.assert_extension_array_equal(result[:, 2:], right)

        # axis > 1 -> invalid
        msg = "axis 2 is out of bounds for array of dimension 2"
        with pytest.raises(ValueError, match=msg):
            left._concat_same_type([left, right], axis=2)

    @pytest.mark.parametrize("method", ["backfill", "pad"])
    def test_fillna_2d_method(self, data_missing, method):
        arr = data_missing.repeat(2).reshape(2, 2)
        assert arr[0].isna().all()
        assert not arr[1].isna().any()

        result = arr.fillna(method=method)

        expected = data_missing.fillna(method=method).repeat(2).reshape(2, 2)
        self.assert_extension_array_equal(result, expected)

    @pytest.mark.parametrize("method", ["mean", "median", "var", "std", "sum", "prod"])
    def test_reductions_2d_axis_none(self, data, method):
        arr2d = data.reshape(1, -1)

        err_expected = None
        err_result = None
        try:
            expected = getattr(data, method)()
        except Exception as err:
            # if the 1D reduction is invalid, the 2D reduction should be as well
            err_expected = err
            try:
                result = getattr(arr2d, method)(axis=None)
            except Exception as err2:
                err_result = err2

        else:
            result = getattr(arr2d, method)(axis=None)

        if err_result is not None or err_expected is not None:
            assert type(err_result) == type(err_expected)
            return

        assert is_matching_na(result, expected) or result == expected

    @pytest.mark.parametrize("method", ["mean", "median", "var", "std", "sum", "prod"])
    def test_reductions_2d_axis0(self, data, method):
        arr2d = data.reshape(1, -1)

        kwargs = {}
        if method == "std":
            # pass ddof=0 so we get all-zero std instead of all-NA std
            kwargs["ddof"] = 0

        try:
            result = getattr(arr2d, method)(axis=0, **kwargs)
        except Exception as err:
            try:
                getattr(data, method)()
            except Exception as err2:
                assert type(err) == type(err2)
                return
            else:
                raise AssertionError("Both reductions should raise or neither")

        def get_reduction_result_dtype(dtype):
            # windows and 32bit builds will in some cases have int32/uint32
            #  where other builds will have int64/uint64.
            if dtype.itemsize == 8:
                return dtype
            elif dtype.kind in "ib":
                return INT_STR_TO_DTYPE[np.dtype(int).name]
            else:
                # i.e. dtype.kind == "u"
                return INT_STR_TO_DTYPE[np.dtype(np.uint).name]

        if method in ["mean", "median", "sum", "prod"]:
            # std and var are not dtype-preserving
            expected = data
            if method in ["sum", "prod"] and data.dtype.kind in "iub":
                dtype = get_reduction_result_dtype(data.dtype)

                expected = data.astype(dtype)
                if data.dtype.kind == "b" and method in ["sum", "prod"]:
                    # We get IntegerArray instead of BooleanArray
                    pass
                else:
                    assert type(expected) == type(data), type(expected)
                assert dtype == expected.dtype

            self.assert_extension_array_equal(result, expected)
        elif method == "std":
            self.assert_extension_array_equal(result, data - data)
        # punt on method == "var"

    @pytest.mark.parametrize("method", ["mean", "median", "var", "std", "sum", "prod"])
    def test_reductions_2d_axis1(self, data, method):
        arr2d = data.reshape(1, -1)

        try:
            result = getattr(arr2d, method)(axis=1)
        except Exception as err:
            try:
                getattr(data, method)()
            except Exception as err2:
                assert type(err) == type(err2)
                return
            else:
                raise AssertionError("Both reductions should raise or neither")

        # not necessarily type/dtype-preserving, so weaker assertions
        assert result.shape == (1,)
        expected_scalar = getattr(data, method)()
        res = result[0]
        assert is_matching_na(res, expected_scalar) or res == expected_scalar


class NDArrayBacked2DTests(Dim2CompatTests):
    # More specific tests for NDArrayBackedExtensionArray subclasses

    def test_copy_order(self, data):
        # We should be matching numpy semantics for the "order" keyword in 'copy'
        arr2d = data.repeat(2).reshape(-1, 2)
        assert arr2d._ndarray.flags["C_CONTIGUOUS"]

        res = arr2d.copy()
        assert res._ndarray.flags["C_CONTIGUOUS"]

        res = arr2d[::2, ::2].copy()
        assert res._ndarray.flags["C_CONTIGUOUS"]

        res = arr2d.copy("F")
        assert not res._ndarray.flags["C_CONTIGUOUS"]
        assert res._ndarray.flags["F_CONTIGUOUS"]

        res = arr2d.copy("K")
        assert res._ndarray.flags["C_CONTIGUOUS"]

        res = arr2d.T.copy("K")
        assert not res._ndarray.flags["C_CONTIGUOUS"]
        assert res._ndarray.flags["F_CONTIGUOUS"]

        # order not accepted by numpy
        msg = r"order must be one of 'C', 'F', 'A', or 'K' \(got 'Q'\)"
        with pytest.raises(ValueError, match=msg):
            arr2d.copy("Q")

        # neither contiguity
        arr_nc = arr2d[::2]
        assert not arr_nc._ndarray.flags["C_CONTIGUOUS"]
        assert not arr_nc._ndarray.flags["F_CONTIGUOUS"]

        assert arr_nc.copy()._ndarray.flags["C_CONTIGUOUS"]
        assert not arr_nc.copy()._ndarray.flags["F_CONTIGUOUS"]

        assert arr_nc.copy("C")._ndarray.flags["C_CONTIGUOUS"]
        assert not arr_nc.copy("C")._ndarray.flags["F_CONTIGUOUS"]

        assert not arr_nc.copy("F")._ndarray.flags["C_CONTIGUOUS"]
        assert arr_nc.copy("F")._ndarray.flags["F_CONTIGUOUS"]

        assert arr_nc.copy("K")._ndarray.flags["C_CONTIGUOUS"]
        assert not arr_nc.copy("K")._ndarray.flags["F_CONTIGUOUS"]
