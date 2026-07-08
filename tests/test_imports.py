import pytest
from glob import glob
import pkgutil
import sys
import nbformat

# Global variables
TIMEOUT = 120

# Load notebooks
notebooks1 = glob("notebooks/book1/*/*.ipynb")
notebooks2 = glob("notebooks/book2/*/*.ipynb")
notebooks = notebooks1 + notebooks2

# get IGNORE_LIST of notebooks
IGNORE_LIST = []
with open("internal/ignored_notebooks.txt") as fp:
    ignored_notebooks = fp.readlines()
    for nb in ignored_notebooks:
        IGNORE_LIST.append(nb.strip().split("/")[-1])


def in_ignore_list(nb_path):
    nb_name = nb_path.split("/")[-1]
    return nb_name in IGNORE_LIST


notebooks = list(filter(lambda nb: not in_ignore_list(nb), notebooks))

# load installed modules
all_modules = set(map(lambda x: x[1], list(pkgutil.iter_modules())))
all_modules.update(getattr(sys, "stdlib_module_names", set()))

# Special cases
special_modules = set(
    [
        "mpl_toolkits",
        "itertools",
        "time",
        "sys",
        "d2l",
        "augmax",
        "google",
        "flax",
        "numba",
        "optax",
        "patsy",
        "pkg_resources",
        "statsmodels",
        "tests_as_linear",
        "tqdm",
        "absl",
        "bambi",
        "bijax",
        "blackjax",
        "bokeh",
        "clu",
        "dynamax",
        "gan",
        "haven",
        "kaleido",
        "modAL",
        "models",
        "networkx",
        "nltk",
        "numpyro",
        "particles",
        "pgmpy",
        "pl_bolts",
        "plotly",
        "probml_utils",
        "pyro",
        "pytorch_lightning",
        "sgmcmcjax",
        "skimage",
        "tensorflow",
        "tensorflow_probability",
        "theano",
        "tinygp",
        "torch",
        "torchvision",
        "utils",
    ]
)
all_modules = all_modules.union(special_modules)


def get_imported_modules(line):
    line = line.lstrip().split("#", 1)[0].split(";", 1)[0].rstrip()

    if line.startswith("import "):
        modules = [
            module.strip().split(" ", 1)[0].split(".", 1)[0]
            for module in line[len("import ") :].split(",")
        ]
        return set(filter(None, modules))
    elif line.startswith("from ") and " import " in line:
        module = line[len("from ") :].split(" import ", 1)[0].strip()
        if module.startswith("."):
            return set()
        return {module.split(".", 1)[0]} if module else set()
    else:
        return set()


def collect_required_imports(lines):
    """Return imports outside try/except blocks.

    Optional dependency probes in notebooks are commonly guarded by try/except.
    Indentation alone is not enough to detect those guards because imports can
    also live in functions and classes where they are still required.
    """
    required_modules = set()
    try_block_indents = []

    for line in lines:
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(stripped)
        while try_block_indents and indent <= try_block_indents[-1]:
            if indent == try_block_indents[-1] and stripped.startswith(("except ", "except:", "else:", "finally:")):
                break
            try_block_indents.pop()

        if stripped.startswith("try:"):
            try_block_indents.append(indent)
            continue

        modules = get_imported_modules(line)
        if modules and not (try_block_indents and indent > try_block_indents[-1]):
            required_modules.update(modules)

    return required_modules


# Parameterize notebooks
@pytest.mark.parametrize("notebook", notebooks)
def test_run_notebooks(notebook):
    """
    Test notebooks
    """
    nb = nbformat.read(notebook, as_version=4)
    lines = "\n".join(map(lambda x: x["source"], nb.cells)).split("\n")
    modules = collect_required_imports(lines)
    missing_modules = modules - all_modules
    assert len(missing_modules) == 0, f"Missing {missing_modules} in {notebook}"


if __name__ == "__main__":
    for notebook in notebooks:
        test_run_notebooks(notebook)
