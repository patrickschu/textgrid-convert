import pathlib

HERE = pathlib.PurePath(__file__).parent
# READ FILES
RESOURCES = HERE / "resources"
INFILES = RESOURCES  / "sample_files"

INFILES_SRT = INFILES / "srts"
INFILES_SBV = INFILES / "sbvs"
INFILES_JSON = INFILES / "jsons"
INFILES_GRID = INFILES / "textgrids"

GOLDFILES = RESOURCES / "gold_files"

# WRITE FILES
OUTFILES = RESOURCES / "output_files"
