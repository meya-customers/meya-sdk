def snake_case_to_human(value: str) -> str:
    return " ".join(map(lambda w: w.lower().capitalize(), value.split("_")))
