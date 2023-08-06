from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Dict, Type, Iterable, List, Tuple, Literal

# import chromedriver_autoinstaller
# from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
import codecs
import json
from selenium.common.exceptions import (
    WebDriverException,
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import urllib.parse
from dataclasses import dataclass
import time
from seletrans.util import get_path
from .seletrans import register
import os
import tempfile
from functools import reduce


@dataclass
class Handlers:
    process: List[Callable[[str], bool]] | None = None
    debug: Callable[[str, str]] | None = None


class ChromeWithPrefs(uc.Chrome):
    def __init__(self, *args, options=None, **kwargs):
        if options:
            self._handle_prefs(options)

        super().__init__(*args, options=options, **kwargs)

        # remove the user_data_dir when quitting
        self.keep_user_data_dir = False

    @staticmethod
    def _handle_prefs(options):
        if prefs := options.experimental_options.get("prefs"):
            # turn a (dotted key, value) into a proper nested dict
            def undot_key(key, value):
                if "." in key:
                    key, rest = key.split(".", 1)
                    value = undot_key(rest, value)
                return {key: value}

            # undot prefs dict keys
            undot_prefs = reduce(
                lambda d1, d2: {**d1, **d2},  # merge dicts
                (undot_key(key, value) for key, value in prefs.items()),
            )

            # create an user_data_dir and add its path to the options
            user_data_dir = os.path.normpath(tempfile.mkdtemp())
            options.add_argument(f"--user-data-dir={user_data_dir}")

            # create the preferences json file in its default directory
            default_dir = os.path.join(user_data_dir, "Default")
            os.mkdir(default_dir)

            prefs_file = os.path.join(default_dir, "Preferences")
            with open(prefs_file, encoding="latin1", mode="w") as f:
                json.dump(undot_prefs, f)

            # pylint: disable=protected-access
            # remove the experimental_options to avoid an error
            del options._experimental_options["prefs"]


class Base:
    NAME = "base"
    URL = ""
    TIMEOUT_MAX = 60
    DEFAULT_SOURCE = "auto"
    DEFAULT_TARGET = "zh"
    SUPPORT_TTS = False
    url_map: Dict[Iterable[str], Type(Handlers)]

    def __init__(self, debug=False) -> None:
        self.debug = debug
        # chromedriver_autoinstaller.install()
        options = Options()
        options.add_experimental_option(
            "prefs", {"profile.managed_default_content_settings.images": 2}
        )
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument(
            "--no-first-run --no-service-autorun --password-store=basic"
        )
        if not debug:
            options.headless = True
        # self.driver = webdriver.Chrome(options=options)
        self.driver = ChromeWithPrefs(options=options)
        self.url_map = {}
        self.net_logs = []

    def check_url(self, parts: Tuple[str], url: str):
        for part in parts:
            if part in url:
                return True
        return False

    def close(self):
        self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def preprocess(self):
        pass

    def validate_lang(self):
        pass

    def set_source_lang(self):
        pass

    def set_target_lang(self):
        pass

    def wait_and_find_elem(self, by, value: str, timeout: float = None):
        timeout = self.TIMEOUT_MAX if timeout is None else timeout
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        elem = self.driver.find_element(by, value)
        return elem

    def get_textarea(self):
        return self.wait_and_find_elem(By.XPATH, "//textarea")

    def wait_for_response(self, text, urls=None):
        self._wait_for_url_change(text)
        self._wait_for_network_idle()
        if urls is None:
            return
        st_time = time.time()
        while True:
            self._get_net_logs()
            flags = [False] * len(urls)
            for log in self.net_logs:
                log_json = json.loads(log["message"])["message"]
                if log_json["method"] != "Network.responseReceived":
                    continue
                url = log_json["params"]["response"]["url"]
                for idx, _url in enumerate(urls):
                    if self.check_url((_url,), url) and (
                        urls[_url] is None or urls[_url](log_json)
                    ):
                        flags[idx] = True
                if all(flags):
                    break
            if all(flags):
                break
            time.sleep(0.1)
            if time.time() - st_time > self.TIMEOUT_MAX:
                raise Exception("Timeout for waiting response")

    def try_click(self, elem):
        try:
            elem.click()
            # WebDriverWait(self.driver, 0.01).until(EC.element_to_be_clickable(elem))
            return True
        except ElementClickInterceptedException:
            return False
        except TimeoutException:
            return False

    def _wait_for_url_change(self, text):
        WebDriverWait(self.driver, self.TIMEOUT_MAX).until(
            EC.url_contains(urllib.parse.quote(text))
        )

    def _wait_for_network_idle(self, check_interval=0.1):
        st = time.time()
        logs = self._get_net_logs()
        while len(logs) != 0:
            time.sleep(check_interval)
            if time.time() - st > self.TIMEOUT_MAX:
                return False
            logs = self._get_net_logs()
        return True

    def _handle_pattern(self, log_json, handler):
        requestId = log_json["params"]["requestId"]
        try:
            response_body = self.driver.execute_cdp_cmd(
                "Network.getResponseBody", {"requestId": requestId}
            )
            body = response_body["body"]
            if handler.process:
                if callable(handler.process):
                    flag = handler.process(body)
                else:
                    flag = any([p(body) for p in handler.process])
            else:
                flag = True
            if flag and self.debug:
                fn = f"{self.__class__.__name__}_{requestId}"
                if handler.debug:
                    handler.debug(fn, body)
                else:
                    self._debug_save_raw(fn, body)
        except WebDriverException:
            pass
        except:
            import traceback

            traceback.print_exc()

    def _handle_patterns(self, log_json):
        url = log_json["params"]["response"]["url"]
        for pattern, handler in self.url_map.items():
            if self.check_url(pattern, url):
                self._handle_pattern(log_json, handler)

    def _debug_save_json(self, fn, body):
        resp = json.loads(body)
        with codecs.open(f"{get_path('tmp', parent=True)}/{fn}.json", "w", "utf8") as f:
            json.dump(resp, f, ensure_ascii=False, indent=2)

    def _debug_save_raw(self, fn, body, suffix="body"):
        with codecs.open(
            f"{get_path('tmp', parent=True)}/{fn}.{suffix}", "w", "utf8"
        ) as f:
            f.write(body)

    def _clear_net_logs(self):
        self.net_logs = []

    def _get_net_logs(self):
        logs = self.driver.get_log("performance")
        self.net_logs.extend(logs)
        return logs

    def _check_response(self, log_json):
        requestId = log_json["params"]["requestId"]
        try:
            # https://chromedevtools.github.io/devtools-protocol/
            response_body = self.driver.execute_cdp_cmd(
                "Network.getResponseBody", {"requestId": requestId}
            )
            body = response_body["body"]
            if self._get_simple_result(body):
                return True
            else:
                return False
        except WebDriverException:
            return False
        except:
            return False

    def query(self, text, source=None, target=None):
        self.url = self.URL
        self.source = source if source is not None else self.DEFAULT_SOURCE
        self.target = target if target is not None else self.DEFAULT_TARGET
        self.result = []
        self.dict_result = []
        self.validate_lang()
        self.driver.get(self.url)
        self.preprocess()
        self.set_source_lang()
        self.set_target_lang()
        self._get_net_logs()
        self._clear_net_logs()
        time.sleep(0.1)
        self.text = text.strip()
        elem = self.get_textarea()
        elem.send_keys(self.text)
        self.wait_for_response(self.text)
        try:
            elem.send_keys(Keys.TAB)
        except:
            pass
        self._get_net_logs()
        for log in self.net_logs:
            log_json = json.loads(log["message"])["message"]
            if log_json["method"] != "Network.responseReceived":
                continue
            self._handle_patterns(log_json)
        assert isinstance(self.result, list)
        assert isinstance(self.dict_result, list)
        return self

    def prepare(self):
        self.url = self.URL
        self.driver.get(self.url)
        self.preprocess()

    def instant_query(self, text, source=None, target=None):
        self.source = source if source is not None else self.DEFAULT_SOURCE
        self.target = target if target is not None else self.DEFAULT_TARGET
        self.result = []
        self.dict_result = []
        self.validate_lang()
        self.set_source_lang()
        self.set_target_lang()
        self._get_net_logs()
        self._clear_net_logs()
        time.sleep(0.1)
        self.text = text.strip()
        elem = self.get_textarea()
        elem.send_keys(self.text)
        self.wait_for_response(self.text)
        try:
            elem.send_keys(Keys.TAB)
        except:
            pass
        self._get_net_logs()
        for log in self.net_logs:
            log_json = json.loads(log["message"])["message"]
            if log_json["method"] != "Network.responseReceived":
                continue
            self._handle_patterns(log_json)
        assert isinstance(self.result, list)
        assert isinstance(self.dict_result, list)
        return self

    def play_sound(self, check_interval=0.1, ignore_exception=True):
        if not self.SUPPORT_TTS:
            return
        try:
            self._play_sound(check_interval)
        except Exception as e:
            if not ignore_exception:
                raise e

    def _play_sound(self, check_interval=0.1):
        pass
