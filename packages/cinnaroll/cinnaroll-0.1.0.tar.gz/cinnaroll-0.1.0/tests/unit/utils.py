from dataclasses import dataclass
import random
import string
from typing import List, Optional, Dict, Any

from cinnaroll_internal.constants import BACKEND_BASE_URL


@dataclass
class MockResponse:
    status_code: int
    json_data: Dict[str, str]

    def json(self) -> Dict[str, str]:
        return self.json_data

    def __str__(self) -> str:
        return f"status: {self.status_code}, response: {self.json_data}"


def mock_request(*args: Any, **kwargs: Any) -> MockResponse:
    print("\n<mock_request>")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

    if args[0].startswith(f"{BACKEND_BASE_URL}/modelUpload?projectId"):
        res = MockResponse(200, {})
    elif args[0] == f"{BACKEND_BASE_URL}/modelUploads":
        res = MockResponse(
            201,
            {
                "id": "abc123",
                "status": "great",
                "uploadUrl": f"{BACKEND_BASE_URL}/unique_upload_url",
            },
        )
    elif args[0] == f"{BACKEND_BASE_URL}/unique_upload_url":
        res = MockResponse(200, {"status": "good"})
    elif args[0] == f"{BACKEND_BASE_URL}/modelUploads/abc123":
        res = MockResponse(200, {"status": "good"})
    else:
        res = MockResponse(404, {"page not found": "get lost"})

    print(f"\n{res}")
    print("</mock_request>\n")
    return res


def generate_random_string(num_lines: int, line_length: int = 80) -> str:
    ret = ""

    for _ in range(num_lines):
        ret += "".join(random.choices(string.ascii_lowercase, k=line_length)) + "\n"

    return ret


def assert_optional_exception_like(
    expected: Optional[Exception], actual: Optional[Exception]
) -> None:
    if expected is None:
        assert actual is None
    else:
        assert actual is not None
        assert isinstance(actual, type(expected))
        assert expected.args[0] in actual.args[0]


def assert_optional_exception_equals(
    expected: Optional[Exception], actual: Optional[Exception]
) -> None:
    if expected is None:
        assert actual is None
    else:
        assert actual is not None
        assert isinstance(actual, type(expected)) and expected.args == actual.args


def assert_contains_single_exception(
    expected: Exception, actual_exceptions: List[Exception]
) -> None:
    for actual in actual_exceptions:
        if isinstance(actual, type(expected)) and expected.args == actual.args:
            return
    raise AssertionError(f"{repr(expected)} not found in {actual_exceptions}")


def assert_contains_exceptions(
    expected: List[Exception], actual: List[Exception]
) -> None:
    for expected_exception in expected:
        assert_contains_single_exception(expected_exception, actual)


def assert_list_exceptions_type_equality(
    expected: List[Exception], actual: List[Exception]
) -> None:
    if len(expected) == 0 or len(actual) == 0:
        assert len(expected) == 0 and len(actual) == 0
    else:
        assert set(map(type, expected)) == set(map(type, actual))
