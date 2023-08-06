import unittest
from http.client import HTTPMessage
from unittest.mock import patch
from urllib.error import HTTPError

from parametrize import parametrize

from get_chromedriver import (
    get_chromium_version,
    get_closest_version,
    get_releases_tree,
    run,
    run_cli,
)

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2022 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("GetChromedriverTestCase",)

RELEASES = [
    "100.0.4896.20",
    "100.0.4896.60",
    "101.0.4951.15",
    "101.0.4951.41",
    "102.0.5005.27",
    "102.0.5005.61",
    "103.0.5060.24",
    "103.0.5060.53",
    "104.0.5112.20",
    "104.0.5112.29",
    "104.0.5112.79",
    "105.0.5195.19",
    "105.0.5195.52",
    "106.0.5249.21",
    "106.0.5249.61",
    "107.0.5304.18",
    "107.0.5304.19",
    "107.0.5304.62",
    "108.0.5359.22",
    "2.38",
    "2.45.2",
    "2.45.3",
    "2.46",
    "78.0.3904.11",
    "78.0.3904.70",
    "79.0.3945.16",
    "79.0.3945.36",
    "80.0.3987.16",
    "81.0.4044.20",
    "81.0.4044.69",
    "83.0.4103.14",
    "83.0.4103.39",
    "84.0.4147.30",
    "85.0.4183.38",
    "85.0.4183.83",
    "85.0.4183.87",
    "86.0.4240.22",
    "87.0.4280.20",
    "87.0.4280.88",
    "88.0.4324.27",
    "88.0.4324.96",
    "89.0.4389.23",
    "90.0.4430.24",
    "91.0.4472.19",
    "92.0.4515.107",
    "92.0.4515.43",
    "93.0.4577.15",
    "93.0.4577.63",
    "94.0.4606.41",
    "95.0.4638.10",
    "95.0.4638.17",
    "96.0.4664.18",
    "96.0.4664.35",
    "96.0.4664.45",
    "97.0.4692.20",
    "97.0.4692.36",
    "97.0.4692.37",
    "97.0.4692.71",
    "98.0.4758.102",
    "98.0.4758.48",
    "98.0.4758.80",
    "99.0.4844.17",
    "99.0.4844.35",
    "99.0.4844.51",
]

RELEASES_TREE = {
    "100": {
        "version": "100.0.4896.20",
        "0": {
            "version": "100.0.4896.20",
            "4896": {
                "version": "100.0.4896.20",
                "20": {"version": "100.0.4896.20"},
                "60": {"version": "100.0.4896.60"},
            },
        },
    },
    "101": {
        "version": "101.0.4951.15",
        "0": {
            "version": "101.0.4951.15",
            "4951": {
                "version": "101.0.4951.15",
                "15": {"version": "101.0.4951.15"},
                "41": {"version": "101.0.4951.41"},
            },
        },
    },
    "102": {
        "version": "102.0.5005.27",
        "0": {
            "version": "102.0.5005.27",
            "5005": {
                "version": "102.0.5005.27",
                "27": {"version": "102.0.5005.27"},
                "61": {"version": "102.0.5005.61"},
            },
        },
    },
    "103": {
        "version": "103.0.5060.24",
        "0": {
            "version": "103.0.5060.24",
            "5060": {
                "version": "103.0.5060.24",
                "24": {"version": "103.0.5060.24"},
                "53": {"version": "103.0.5060.53"},
            },
        },
    },
    "104": {
        "version": "104.0.5112.20",
        "0": {
            "version": "104.0.5112.20",
            "5112": {
                "version": "104.0.5112.20",
                "20": {"version": "104.0.5112.20"},
                "29": {"version": "104.0.5112.29"},
                "79": {"version": "104.0.5112.79"},
            },
        },
    },
    "105": {
        "version": "105.0.5195.19",
        "0": {
            "version": "105.0.5195.19",
            "5195": {
                "version": "105.0.5195.19",
                "19": {"version": "105.0.5195.19"},
                "52": {"version": "105.0.5195.52"},
            },
        },
    },
    "106": {
        "version": "106.0.5249.21",
        "0": {
            "version": "106.0.5249.21",
            "5249": {
                "version": "106.0.5249.21",
                "21": {"version": "106.0.5249.21"},
                "61": {"version": "106.0.5249.61"},
            },
        },
    },
    "107": {
        "version": "107.0.5304.18",
        "0": {
            "version": "107.0.5304.18",
            "5304": {
                "version": "107.0.5304.18",
                "18": {"version": "107.0.5304.18"},
                "19": {"version": "107.0.5304.19"},
                "62": {"version": "107.0.5304.62"},
            },
        },
    },
    "108": {
        "version": "108.0.5359.22",
        "0": {
            "version": "108.0.5359.22",
            "5359": {
                "version": "108.0.5359.22",
                "22": {"version": "108.0.5359.22"},
            },
        },
    },
    "2": {
        "version": "2.38",
        "38": {"version": "2.38"},
        "45": {
            "version": "2.45.2",
            "2": {"version": "2.45.2"},
            "3": {"version": "2.45.3"},
        },
        "46": {"version": "2.46"},
    },
    "78": {
        "version": "78.0.3904.11",
        "0": {
            "version": "78.0.3904.11",
            "3904": {
                "version": "78.0.3904.11",
                "11": {"version": "78.0.3904.11"},
                "70": {"version": "78.0.3904.70"},
            },
        },
    },
    "79": {
        "version": "79.0.3945.16",
        "0": {
            "version": "79.0.3945.16",
            "3945": {
                "version": "79.0.3945.16",
                "16": {"version": "79.0.3945.16"},
                "36": {"version": "79.0.3945.36"},
            },
        },
    },
    "80": {
        "version": "80.0.3987.16",
        "0": {
            "version": "80.0.3987.16",
            "3987": {
                "version": "80.0.3987.16",
                "16": {"version": "80.0.3987.16"},
            },
        },
    },
    "81": {
        "version": "81.0.4044.20",
        "0": {
            "version": "81.0.4044.20",
            "4044": {
                "version": "81.0.4044.20",
                "20": {"version": "81.0.4044.20"},
                "69": {"version": "81.0.4044.69"},
            },
        },
    },
    "83": {
        "version": "83.0.4103.14",
        "0": {
            "version": "83.0.4103.14",
            "4103": {
                "version": "83.0.4103.14",
                "14": {"version": "83.0.4103.14"},
                "39": {"version": "83.0.4103.39"},
            },
        },
    },
    "84": {
        "version": "84.0.4147.30",
        "0": {
            "version": "84.0.4147.30",
            "4147": {
                "version": "84.0.4147.30",
                "30": {"version": "84.0.4147.30"},
            },
        },
    },
    "85": {
        "version": "85.0.4183.38",
        "0": {
            "version": "85.0.4183.38",
            "4183": {
                "version": "85.0.4183.38",
                "38": {"version": "85.0.4183.38"},
                "83": {"version": "85.0.4183.83"},
                "87": {"version": "85.0.4183.87"},
            },
        },
    },
    "86": {
        "version": "86.0.4240.22",
        "0": {
            "version": "86.0.4240.22",
            "4240": {
                "version": "86.0.4240.22",
                "22": {"version": "86.0.4240.22"},
            },
        },
    },
    "87": {
        "version": "87.0.4280.20",
        "0": {
            "version": "87.0.4280.20",
            "4280": {
                "version": "87.0.4280.20",
                "20": {"version": "87.0.4280.20"},
                "88": {"version": "87.0.4280.88"},
            },
        },
    },
    "88": {
        "version": "88.0.4324.27",
        "0": {
            "version": "88.0.4324.27",
            "4324": {
                "version": "88.0.4324.27",
                "27": {"version": "88.0.4324.27"},
                "96": {"version": "88.0.4324.96"},
            },
        },
    },
    "89": {
        "version": "89.0.4389.23",
        "0": {
            "version": "89.0.4389.23",
            "4389": {
                "version": "89.0.4389.23",
                "23": {"version": "89.0.4389.23"},
            },
        },
    },
    "90": {
        "version": "90.0.4430.24",
        "0": {
            "version": "90.0.4430.24",
            "4430": {
                "version": "90.0.4430.24",
                "24": {"version": "90.0.4430.24"},
            },
        },
    },
    "91": {
        "version": "91.0.4472.19",
        "0": {
            "version": "91.0.4472.19",
            "4472": {
                "version": "91.0.4472.19",
                "19": {"version": "91.0.4472.19"},
            },
        },
    },
    "92": {
        "version": "92.0.4515.107",
        "0": {
            "version": "92.0.4515.107",
            "4515": {
                "version": "92.0.4515.107",
                "107": {"version": "92.0.4515.107"},
                "43": {"version": "92.0.4515.43"},
            },
        },
    },
    "93": {
        "version": "93.0.4577.15",
        "0": {
            "version": "93.0.4577.15",
            "4577": {
                "version": "93.0.4577.15",
                "15": {"version": "93.0.4577.15"},
                "63": {"version": "93.0.4577.63"},
            },
        },
    },
    "94": {
        "version": "94.0.4606.41",
        "0": {
            "version": "94.0.4606.41",
            "4606": {
                "version": "94.0.4606.41",
                "41": {"version": "94.0.4606.41"},
            },
        },
    },
    "95": {
        "version": "95.0.4638.10",
        "0": {
            "version": "95.0.4638.10",
            "4638": {
                "version": "95.0.4638.10",
                "10": {"version": "95.0.4638.10"},
                "17": {"version": "95.0.4638.17"},
            },
        },
    },
    "96": {
        "version": "96.0.4664.18",
        "0": {
            "version": "96.0.4664.18",
            "4664": {
                "version": "96.0.4664.18",
                "18": {"version": "96.0.4664.18"},
                "35": {"version": "96.0.4664.35"},
                "45": {"version": "96.0.4664.45"},
            },
        },
    },
    "97": {
        "version": "97.0.4692.20",
        "0": {
            "version": "97.0.4692.20",
            "4692": {
                "version": "97.0.4692.20",
                "20": {"version": "97.0.4692.20"},
                "36": {"version": "97.0.4692.36"},
                "37": {"version": "97.0.4692.37"},
                "71": {"version": "97.0.4692.71"},
            },
        },
    },
    "98": {
        "version": "98.0.4758.102",
        "0": {
            "version": "98.0.4758.102",
            "4758": {
                "version": "98.0.4758.102",
                "102": {"version": "98.0.4758.102"},
                "48": {"version": "98.0.4758.48"},
                "80": {"version": "98.0.4758.80"},
            },
        },
    },
    "99": {
        "version": "99.0.4844.17",
        "0": {
            "version": "99.0.4844.17",
            "4844": {
                "version": "99.0.4844.17",
                "17": {"version": "99.0.4844.17"},
                "35": {"version": "99.0.4844.35"},
                "51": {"version": "99.0.4844.51"},
            },
        },
    },
}


def urlopen_raise():
    raise HTTPError(
        url="https://pypi.org/pypi/chromedriver-py/json",
        code=404,
        msg="Not Found",
        hdrs=HTTPMessage(),
        fp=None,
    )


class GetChromedriverTestCase(unittest.TestCase):
    """get_chromedriver test case."""

    def test_get_chromium_version(self):
        """Test get_chromium_version."""
        chromium_version = get_chromium_version()
        self.assertIsNotNone(chromium_version)

    @parametrize(
        "chromium_version, chromedriver_version, releases_tree",
        [
            ("107.0.5304.110", "107.0.5304.18", RELEASES_TREE),
            ("100.0.4896.12", "100.0.4896.20", RELEASES_TREE),
            ("", None, RELEASES_TREE),
            ("9999", None, RELEASES_TREE),
            ("107.0.5304.110", None, {}),
        ]
    )
    def test_get_closest_version(
        self,
        chromium_version,
        chromedriver_version,
        releases_tree,
    ):
        """Test get_closest_version."""

        closest_version = get_closest_version(chromium_version, releases_tree)
        self.assertEqual(closest_version, chromedriver_version)

    def test_get_releases_tree(self):
        """Test get_releases_tree."""
        releases_tree = get_releases_tree()
        self.assertIsNotNone(releases_tree)

    def test_run(self):
        """Test run."""
        result = run()
        self.assertTrue(result)

    @patch(
        "get_chromedriver.get_chromium_version",
        new_callable=lambda: lambda: False,
    )
    def test_run_failed_get_chromium_version(self, func):
        """Test run failed due to errors in obtaining the Chromium version."""
        result = run()
        self.assertFalse(result)

    @patch(
        "get_chromedriver.urlopen",
        side_effect=HTTPError(
            url="https://pypi.org/pypi/chromedriver-py/json",
            code=404,
            msg="Not Found",
            hdrs=HTTPMessage(),
            fp=None,
        ),
    )
    def test_get_releases_tree_failed_urlopen(self, func):
        """Test run failed due to HTTP errors querying PyPI."""
        result = get_releases_tree()
        self.assertEqual(result, {})

    def test_run_cli(self):
        """Test run CLI."""
        result = run_cli()
        self.assertFalse(result)
