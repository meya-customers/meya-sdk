import freezegun

ignore_modules = ["pandas", "transformers", "tokenizers", "numpy"]


def freeze_time(*args, **kwargs):
    ignore = kwargs.pop("ignore", []) + ignore_modules
    return freezegun.freeze_time(*args, **kwargs, ignore=ignore)
