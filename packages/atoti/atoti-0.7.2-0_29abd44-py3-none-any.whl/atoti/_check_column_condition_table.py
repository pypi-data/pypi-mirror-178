from itertools import chain

from atoti_core import (
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    ConditionTargetBound,
    decombine_condition,
)

from ._column_coordinates import ColumnCoordinates


def check_column_condition_table(
    condition: Condition[
        ColumnCoordinates,
        ConditionComparisonOperatorBound,
        ConditionTargetBound,
        ConditionCombinationOperatorBound,
    ],
    /,
    expected_table_name: str,
) -> None:
    for decombined_conditions in decombine_condition(  # type: ignore[var-annotated]
        condition, allowed_subject_types=(ColumnCoordinates,)
    ):
        for sub_condition in chain(*decombined_conditions):
            # Pyright is able to check that `sub_condition` has a `subject` but mypy cannot.
            table_name = sub_condition.subject.table_name  # type: ignore[attr-defined]
            if table_name != expected_table_name:
                raise ValueError(
                    f"Expected the subject of the condition to belong to the table `{expected_table_name}` but got `{table_name}`."
                )
