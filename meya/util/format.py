import asyncio
import black

from meya.util.pathspec import make_pathspec
from meya.util.pathspec import read_gitignore_lines
from meya.util.pathspec import subtract_pathspec
from meya.util.pathspec import walk_pathspec
from meya.util.yaml import from_multi_yaml
from meya.util.yaml import from_yaml
from meya.util.yaml import to_multi_yaml
from meya.util.yaml import to_yaml
from pathlib import Path
from ruamel.yaml.composer import ComposerError


def sort_python_imports(check=False):
    # Import setuptools first to avoid distutils warning (triggered by isort)
    import setuptools

    # TODO Put isort back as a top-level import once it leaves appdirs as is
    #      https://github.com/timothycrosley/isort/pull/1166
    from isort import SortImports
    from isort.main import iter_source_code as iter_isort_source_code
    from isort.settings import from_path as get_isort_config_from_path

    skipped = []
    config = get_isort_config_from_path(".")
    file_names = iter_isort_source_code(["."], config, skipped)
    results = [SortImports(file_name, check=check) for file_name in file_names]
    if any(result.incorrectly_sorted for result in results):
        raise SystemExit(1)


def format_python_code(check=False):
    try:
        asyncio.set_event_loop(asyncio.new_event_loop())
        black.main(args=(*(("--check",) if check else ()), "."))
    except SystemExit as e:
        if e.code == 0:
            pass
        else:
            raise


def format_yaml_code(check=False):
    check_pass = True
    pathspec = subtract_pathspec(
        pathspec=make_pathspec(["*.yaml", "*.yml"]),
        ignore_pathspec=make_pathspec(read_gitignore_lines()),
    )
    for yaml_path in walk_pathspec(Path("."), pathspec):
        with yaml_path.open("r", encoding="utf-8") as yaml_file:
            old_yaml_text = yaml_file.read()
        try:
            new_yaml_text = to_yaml(from_yaml(old_yaml_text))
        except ComposerError:
            new_yaml_text = to_multi_yaml(from_multi_yaml(old_yaml_text))
        if not new_yaml_text == old_yaml_text:
            if check:
                check_pass = False
                print(f"Incorrect format {yaml_path}")
            else:
                with yaml_path.open("w", encoding="utf-8") as yaml_file:
                    yaml_file.write(new_yaml_text)
                print(f"Formatted {yaml_path}")
    if not check_pass:
        raise SystemExit(1)
