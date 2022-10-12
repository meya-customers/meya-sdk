from meya.util.context_var import ScopedContextVar
from typing import ClassVar
from typing import cast


class AppVault(dict):
    current: ClassVar = cast(ScopedContextVar["AppVault"], ScopedContextVar())

    @classmethod
    def from_combined_keys(cls, data):
        nested_data = {}

        # Sort dot-separated keys to ensure consistent results
        for combined_key in sorted(data.keys()):
            inner_data = nested_data
            [*inner_keys, key] = combined_key.split(".")

            # Construct/navigate inner data
            for inner_key in inner_keys:
                next_inner_data = inner_data.get(inner_key)

                # If inner data isn't a dict, allow overwriting it
                if isinstance(next_inner_data, dict):
                    inner_data = next_inner_data
                else:
                    inner_data[inner_key] = {}
                    inner_data = inner_data[inner_key]

            # Assign value
            inner_data[key] = data[combined_key]

        return AppVault(nested_data)
