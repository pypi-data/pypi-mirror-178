"""logging_filters."""
import logging
import math
import time


class TokenBucket:
    """TokenBucket."""

    def __init__(
        self, tokens_per_sec, starting_tokens=0, max_tokens_balance=math.inf
    ):
        """Init.

        args:
            tokens_per_sec: <float> mandatory
        kwargs:
            starting_tokens: <int> optional
            max_tokens_balance: <int> optional
        """
        self.tokens_per_sec = tokens_per_sec
        self.max_tokens_balance = max_tokens_balance
        self.bucket = starting_tokens
        self.last_check = time.time()

    def is_action_allowed(self):
        """is_action_allowed."""
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current

        self.bucket = self.bucket + (time_passed * self.tokens_per_sec)

        if (self.bucket > self.max_tokens_balance):
            self.bucket = self.max_tokens_balance

        if (self.bucket < 1):
            return False
        else:
            self.bucket = self.bucket - 1
            return True


class RateLimitingFilter(logging.Filter):
    """RateLimitingFilter.

    kwargs:
        default: {
            "tokens_per_sec": <tokens_per_sec>, # mandatory key
            "starting_tokens": <starting_tokens>, # optiional key
            "max_tokens_balance": <max_tokens_balance> # optiional key
        },
        <log_level>: {
            "tokens_per_sec": <tokens_per_sec>, # mandatory key
            "starting_tokens": <starting_tokens>, # optiional key
            "max_tokens_balance": <max_tokens_balance> # optiional key
        },
        result_callback: <function>

    there can be multiple keywords  for log_level each representing
     rate_config for each log level,

    """

    def __init__(
        self, result_callback=None, **kwargs
    ):
        """Init."""
        super().__init__()
        self.rate_limiter_map = {}
        for log_level, rate_config in kwargs.items():
            self.rate_limiter_map[log_level] = TokenBucket(
                **rate_config
            ).is_action_allowed
        self.result_callback = result_callback

    def filter(self, record):  # noqa: A003
        """filter."""
        if record.levelname not in self.rate_limiter_map:
            if "default" not in self.rate_limiter_map:
                result = True
            else:
                result = self.rate_limiter_map["default"]()
        else:
            result = self.rate_limiter_map.get(record.levelname)()
        if self.result_callback:
            self.result_callback(result, record=record)
        return result
