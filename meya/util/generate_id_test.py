import meya.util.generate_id

from inspect import signature


def test_unique_generated_prefixes():
    generators = [
        value
        for (key, value) in meya.util.generate_id.__dict__.items()
        if key.startswith("generate")
    ]
    generated_ids = [
        generator(*(["?"] * len(signature(generator).parameters)))
        for generator in generators
    ]
    prefixes = [
        generated_id[0 : generated_id.find("-")]
        for generated_id in generated_ids
    ]
    assert len(set(prefixes)) == len(prefixes)
