"""
Interpret sql-to-pandas errors.
"""
from dslibrary import DSLibraryDataFormatException


def interpret_s2p_errors(err: dict):
    """
    Detect common SQL errors and add their description into a traceback.
    """
    _detect_datatype_conflict(err)


def _detect_datatype_conflict(err: dict):
    if err["ename"] not in {"ValueError", "TypeError"}:
        return
    if err["evalue"].startswith("Metadata inference failed in"):
        # dask
        pass
    elif "not supported between instances of " in err["evalue"]:
        # pandas
        pass
    else:
        return
    err["interpretation"] = \
        "The data types in the requested operation are not compatible.\n" \
        "You may need to clean one or more columns in order that they consistently contain the intended data type.\n"\
        "Reported error was: %s" % err["traceback"]["detail"].strip()


def translate_pandas_dask_exceptions(exc):
    """
    Recognize some exceptions and provide more helpful information/codes.
    """
    if isinstance(exc, UnicodeDecodeError):
        return DSLibraryDataFormatException(f"Encoding problem in file, reason={exc.reason}, offset={exc.start}, encoding={exc.encoding}")
    s_exc = str(exc)
    if "Error tokenizing data." in s_exc or ("Expected " in s_exc and "fields in line " in s_exc):
        return DSLibraryDataFormatException(f"CSV problem: {s_exc}")
    if isinstance(exc, ValueError) and ("Trailing data" in s_exc or "Expected object" in s_exc or "No ':'" in s_exc):
        return DSLibraryDataFormatException(f"JSON problem: {s_exc}")
    if isinstance(exc, ValueError):
        return DSLibraryDataFormatException(f"Data format problem: {s_exc}")
    return exc
