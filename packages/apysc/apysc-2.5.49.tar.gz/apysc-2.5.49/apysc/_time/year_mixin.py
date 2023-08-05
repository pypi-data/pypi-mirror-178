"""Class implementations for the year-related mix-in.
"""

from typing import Union

from typing_extensions import final

from apysc._html.debug_mode import add_debug_info_setting
from apysc._type.int import Int
from apysc._type.revert_mixin import RevertMixIn
from apysc._type.variable_name_mixin import VariableNameMixIn
from apysc._type.variable_name_suffix_attr_mixin import VariableNameSuffixAttrMixIn
from apysc._validation import arg_validation_decos


class YearMixIn(VariableNameMixIn, VariableNameSuffixAttrMixIn, RevertMixIn):

    _initial_year: Union[int, Int]
    _year: Int

    @final
    @add_debug_info_setting(module_name=__name__)
    @arg_validation_decos.is_four_digit_year(arg_position_index=1)
    def _set_init_year_value(self, *, year: Union[int, Int]) -> None:
        """
        Set an initial year value.

        Parameters
        ----------
        year : Union[int, Int]
            A year value to set.
        """
        from apysc._converter.to_apysc_val_from_builtin import (
            get_copied_int_from_builtin_val,
        )

        self._initial_year = year
        suffix: str = self._get_attr_variable_name_suffix(attr_identifier="year")
        self._year = get_copied_int_from_builtin_val(
            integer=year, variable_name_suffix=suffix
        )

    @final
    @add_debug_info_setting(module_name=__name__)
    def _get_init_year_argument_expression(self) -> str:
        """
        Get an initial year's argument expression string.

        Returns
        -------
        expression : str
            A created expression string.
        """
        if isinstance(self._initial_year, Int):
            return f"{self._initial_year.variable_name}"
        return f"{self._year._value}"

    @property
    @add_debug_info_setting(module_name=__name__)
    def year(self) -> Int:
        """
        Get a current year value.

        Returns
        -------
        year : Int
            A current year value.
        """
        copied_year_val: Int = self._year._copy()
        self._append_year_getter_expression(year_val=copied_year_val)
        return copied_year_val

    @final
    @add_debug_info_setting(module_name=__name__)
    def _append_year_getter_expression(self, *, year_val: Int) -> None:
        """
        Append a year's getter expression string.

        Parameters
        ----------
        year_val : Int
            A year value to use in an expression.
        """
        import apysc as ap

        expression: str = (
            f"{year_val.variable_name} = {self.variable_name}.getFullYear();"
        )
        ap.append_js_expression(expression=expression)

    def _make_snapshot(self, *, snapshot_name: str) -> None:
        """
        Make a value snapshot.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        self._year._run_all_make_snapshot_methods(snapshot_name=snapshot_name)

    def _revert(self, *, snapshot_name: str) -> None:
        """
        Revert a value if a snapshot exists.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        self._year._run_all_revert_methods(snapshot_name=snapshot_name)
