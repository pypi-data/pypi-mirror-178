"""Class implementations for the month-related mix-in.
"""

from typing import Union

from typing_extensions import final

from apysc._html.debug_mode import add_debug_info_setting
from apysc._type.int import Int
from apysc._type.revert_mixin import RevertMixIn
from apysc._type.variable_name_mixin import VariableNameMixIn
from apysc._type.variable_name_suffix_attr_mixin import VariableNameSuffixAttrMixIn
from apysc._validation import arg_validation_decos


class MonthMixIn(VariableNameMixIn, VariableNameSuffixAttrMixIn, RevertMixIn):

    _initial_month: Union[int, Int]
    _month: Int

    @final
    @add_debug_info_setting(module_name=__name__)
    @arg_validation_decos.is_month_int(arg_position_index=1)
    def _set_init_month_value(self, *, month: Union[int, Int]) -> None:
        """
        Set an initial month value.

        Parameters
        ----------
        month : Union[int, Int]
            A month value to set.
        """
        from apysc._converter.to_apysc_val_from_builtin import (
            get_copied_int_from_builtin_val,
        )

        self._initial_month = month
        suffix: str = self._get_attr_variable_name_suffix(attr_identifier="month")
        self._month = get_copied_int_from_builtin_val(
            integer=month, variable_name_suffix=suffix
        )

    @final
    @add_debug_info_setting(module_name=__name__)
    def _get_init_month_argument_expression(self) -> str:
        """
        Get an initial month's argument expression string.

        Returns
        -------
        expression : str
            A created expression string.
        """
        if isinstance(self._initial_month, Int):
            return f", {self._initial_month.variable_name} - 1"

        return f", {self._month._value - 1}"

    def _make_snapshot(self, *, snapshot_name: str) -> None:
        """
        Make a value snapshot.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        self._month._run_all_make_snapshot_methods(snapshot_name=snapshot_name)

    def _revert(self, *, snapshot_name: str) -> None:
        """
        Revert a value if a snapshot exists.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        self._month._run_all_revert_methods(snapshot_name=snapshot_name)
