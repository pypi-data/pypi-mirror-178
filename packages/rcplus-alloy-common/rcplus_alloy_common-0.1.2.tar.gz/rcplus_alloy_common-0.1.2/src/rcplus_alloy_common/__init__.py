"""
Various metrics, logging, retry etc. utils and helpers.

Details:
https://github.com/ringier-data/rcplus-alloy-onelog-rawdata/issues/11
https://github.com/ringier-data/rcplus-alloy-onelog-rawdata/issues/7
https://github.com/ringier-data/rcplus-alloy-lib-py-common/issues/5

Notes:
    Both structured logging configuration functions (`configure_existing_loggers` and `configure_new_logger`) support
    `capture_warnings` parameter. This parameter configure Python's logging library to capture Python's warnings
    globally and output them as formatted logging messages with the WARNING level. Python's warnings are used quite
    often by various libraries, such as Pandas, to notify their users about things like deprecation warnings.
    Usually such warnings are initialized lazily so to capture them correctly the logger with the name `py.warnings`
    should be created in advance and configured. See `app/src/scripts/one_log_data_import.py` for the usage example.
"""
import os
import logging
import asyncio
import functools
from time import sleep
from typing import Union, Tuple, Callable, Type
from functools import partial
from datetime import datetime, timezone

import requests
from requests.adapters import HTTPAdapter, Retry
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pythonjsonlogger import jsonlogger
from logzio.handler import LogzioHandler

from .constants import (
    DEFAULT_RETRY_COUNT, DEFAULT_RETRY_BACKOFF, DEFAULT_REQUEST_TIMEOUT, DEFAULT_ALLOWED_METHODS,
    DEFAULT_RETRY_HTTP_STATUS_CODES, METRIC_SCHEMA, GRAPHITE_API_KEY, GRAPHITE_API_USER, GRAPHITE_API_ENDPOINT,
    ENV_TAG, PROJECT_TAG, REPOSITORY_TAG, LOG_NAME, LOG_LEVEL, LOG_MODE, LOGGING_FORMAT, LOGGING_DATETIME_FORMAT,
    LOGZIO_TOKEN, LOGZIO_ENDPOINT, DEFAULT_TRIES_COUNT, DEFAULT_DELAY_AMOUNT, DEFAULT_BACKOFF_VALUE,
    DEFAULT_EXCEPTIONS_TUPLE,
)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def formatTime(self, record, datefmt=None):
        return f'{datetime.fromtimestamp(record.created, tz=timezone.utc).strftime(LOGGING_DATETIME_FORMAT)[:-3]}Z'


class CustomLoggingFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return f'{datetime.fromtimestamp(record.created, tz=timezone.utc).strftime(LOGGING_DATETIME_FORMAT)[:-3]}Z'


def configure_existing_loggers(
        log_mode: str = LOG_MODE,
        log_level: Union[str, int] = LOG_LEVEL,
        log_name_filter: str = None,
        capture_warnings: bool = True,
) -> None:
    """
    Configure all existing loggers to be the same (output as text/json, level) or
    configure only some specific 3rd party loggers (like urllib3 etc.) using log_name_filter.
    """
    logging.captureWarnings(capture_warnings)

    if log_mode == 'JSON':
        handler = logging.StreamHandler()
        handler.setFormatter(
            CustomJsonFormatter(LOGGING_FORMAT, rename_fields={'levelname': 'level', 'asctime': 'time'})
        )
    elif log_mode == 'LOGZIO':
        handler = LogzioHandler(LOGZIO_TOKEN, url=LOGZIO_ENDPOINT, backup_logs=False)
        handler.setFormatter(
            CustomJsonFormatter(LOGGING_FORMAT, rename_fields={'levelname': 'level', 'asctime': 'time'})
        )
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(CustomLoggingFormatter(LOGGING_FORMAT))

    for log_name in logging.root.manager.loggerDict:
        if log_name_filter is not None and log_name_filter not in log_name:
            continue
        existing_logger = logging.getLogger(log_name)
        existing_logger.handlers.clear()
        existing_logger.setLevel(log_level)
        existing_logger.addHandler(handler)


def configure_new_logger(
        log_name: str = LOG_NAME,
        log_mode: str = LOG_MODE,
        log_level: Union[str, int] = LOG_LEVEL,
        capture_warnings: bool = True,
) -> logging.Logger:
    """
    Configure a new logger.
    """
    logging.captureWarnings(capture_warnings)

    if log_mode == 'JSON':
        handler = logging.StreamHandler()
        handler.setFormatter(
            CustomJsonFormatter(LOGGING_FORMAT, rename_fields={'levelname': 'level', 'asctime': 'time'})
        )
    elif log_mode == 'LOGZIO':
        handler = LogzioHandler(LOGZIO_TOKEN, url=LOGZIO_ENDPOINT)
        handler.setFormatter(
            CustomJsonFormatter(LOGGING_FORMAT, rename_fields={'levelname': 'level', 'asctime': 'time'})
        )
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(CustomLoggingFormatter(LOGGING_FORMAT))

    new_logger = logging.getLogger(log_name)
    new_logger.handlers.clear()
    new_logger.setLevel(log_level)
    new_logger.addHandler(handler)

    return new_logger


# The default utility logger.
logger = configure_new_logger(log_name=str(os.path.basename(__file__).split('.')[0]))


class RetryWithLog(Retry):
    def sleep(self, response=None):
        attempt = len(self.history)
        history = self.history[-1]
        error = history.error or f'Status {history.status}'
        logger.warning(f'Failed to publish metrics in attempt {attempt} because of "{error}".')
        super(RetryWithLog, self).sleep()


def get_request_retry_session(
        retry_count: int = DEFAULT_RETRY_COUNT,
        retry_backoff: float = DEFAULT_RETRY_BACKOFF,
        allowed_methods: Tuple[str] = DEFAULT_ALLOWED_METHODS,
        retry_status_codes: Tuple[int] = DEFAULT_RETRY_HTTP_STATUS_CODES,
) -> requests.Session:
    retries = RetryWithLog(
        total=retry_count,
        backoff_factor=retry_backoff,
        allowed_methods=allowed_methods,
        status_forcelist=retry_status_codes,
    )

    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


def make_single_metric(
        name: str,
        value: Union[int, float],
        interval: int = 3600,
        timestamp: int = 0,
        env_tag: str = None,
        project_tag: str = None,
        repository_tag: str = None,
        extra_tags: Tuple[str] = None,
) -> dict:
    """
    Helper function to construct a new single metric dict.
    The env_tag, project_tag, repository_tag are the explicit env, project, repository tag values.
    The extra_tags is a list of 'key=value' extra tag strings which also can include the explicit tags.
    """
    tags_list = []
    extra_tags = extra_tags or []

    # Find env, project and repository explicit tags in extra_tags
    extra_env = list(filter(lambda tag: tag.startswith('env='), extra_tags))
    extra_project = list(filter(lambda tag: tag.startswith('project='), extra_tags))
    extra_repository = list(filter(lambda tag: tag.startswith('repository='), extra_tags))

    if env_tag:
        # if the env tag was set explicitly then clean anything related to env in extra_tags
        for value in extra_env:
            extra_tags.remove(value)
        # add the explict env value
        tags_list.append(f'env={env_tag}')
    elif not extra_env and ENV_TAG:
        # if no explicit env value provided and no env tag in extra_tags then use ENV_TAG ENV var
        tags_list.append(f'env={ENV_TAG}')

    if project_tag:
        # if the project tag was set explicitly then clean anything related to project in extra_tags
        for value in extra_project:
            extra_tags.remove(value)
        # add the explict project value
        tags_list.append(f'project={project_tag}')
    elif not extra_project and PROJECT_TAG:
        # if no explicit project value provided and no project tag in extra_tags then use PROJECT_TAG ENV var
        tags_list.append(f'project={PROJECT_TAG}')

    if repository_tag:
        # if the repository tag was set explicitly then clean anything related to repository in extra_tags
        for value in extra_repository:
            extra_tags.remove(value)
        # add the explict repository value
        tags_list.append(f'repository={repository_tag}')
    elif not extra_repository and REPOSITORY_TAG:
        # if no explicit repository value provided and no repository tag in extra_tags then use REPOSITORY_TAG ENV var
        tags_list.append(f'repository={REPOSITORY_TAG}')

    # merge collected explicit tags and extra_tags
    tags_list += extra_tags
    return {
        'name': name,
        'value': value,
        'interval': interval,
        'time': timestamp or int(datetime.utcnow().timestamp()),
        'tags': tags_list,
    }


def is_valid_metric(metric: dict) -> bool:
    """
    Validate a metric dict against metric schema.
    """
    try:
        validate(metric, schema=METRIC_SCHEMA)
        return True
    except ValidationError as ex:
        error = str(ex).split('\n')[0]
        logger.error(f'Failed to validate metric "{metric}" because of "{error}".')
        return False


def publish_metrics_sync(
        metrics: Union[dict, list],
        retry_count: int = DEFAULT_RETRY_COUNT,
        retry_backoff: float = DEFAULT_RETRY_BACKOFF,
        request_timeout: int = DEFAULT_REQUEST_TIMEOUT,
        api_key: str = GRAPHITE_API_KEY,
        api_user: str = GRAPHITE_API_USER,
        api_endpoint: str = GRAPHITE_API_ENDPOINT,
) -> None:
    """
    Publish metrics to Grafana synchronous (blocking) way.
    """
    if any(param is None for param in (api_key, api_user, api_endpoint)):
        logger.warning(
            f'Skip metrics "{metrics}" publishing because some of parameters api_key, api_user, api_endpoint are None.')
        return

    if isinstance(metrics, dict):
        metrics = [metrics]

    metrics = [metric for metric in metrics if is_valid_metric(metric)]
    if not metrics:
        logger.warning('No valid metrics to publish found after the validation.')
        return

    headers = {
        'Authorization': f'Bearer {api_user}:{api_key}'
    }

    try:
        session = get_request_retry_session(retry_count=retry_count, retry_backoff=retry_backoff)
        response = session.post(api_endpoint, headers=headers, json=metrics, timeout=request_timeout)
        response.raise_for_status()
        logger.info(f'Metrics "{metrics}" published successfully.')
        return

    # Many errors are possible here, I tested at least ConnectTimeout, HTTPError, RetryError, ConnectionError and
    # I'm not sure if this is a complete list so I decided to capture everything because metrics publishing failures
    # must not disrupt any code executions.
    except Exception as ex:
        logger.error(f'Failed to publish metrics "{metrics}" in {retry_count} attempts because of "{ex}".')


def publish_metrics_async(
        metrics: Union[dict, list],
        retry_count: int = DEFAULT_RETRY_COUNT,
        retry_backoff: float = DEFAULT_RETRY_BACKOFF,
        request_timeout: int = DEFAULT_REQUEST_TIMEOUT,
        api_key: str = GRAPHITE_API_KEY,
        api_user: str = GRAPHITE_API_USER,
        api_endpoint: str = GRAPHITE_API_ENDPOINT,
) -> None:
    """
    Publish metrics to Grafana asynchronous (non-blocking) way.
    This function will continue to work until the end even if the main thread which called it is finished.
    """
    loop = asyncio.get_event_loop()
    publish_metrics_sync_partial = partial(
        publish_metrics_sync, metrics, retry_count, retry_backoff, request_timeout,
        api_key, api_user, api_endpoint,
    )
    loop.run_in_executor(None, publish_metrics_sync_partial)


def retry(
        *,
        tries: int = DEFAULT_TRIES_COUNT,
        delay: float = DEFAULT_DELAY_AMOUNT,
        backoff: float = DEFAULT_BACKOFF_VALUE,
        exceptions: Tuple[Type[Exception], ...] = DEFAULT_EXCEPTIONS_TUPLE,
        exceptions_filter: str = None,
        decorator_logger: logging.Logger = None,
        decorator_logger_level: Union[int, str] = logging.WARNING,
) -> Callable:
    """
    Retry decorator. It retries any Python callable in case of any exception thrown.

    if the exceptions_filter is set then retry only exceptions with the specific text, for example,
    if two ValueError exceptions can be raised for different reasons then one of them can be retried
    but another is skipped and raised.
    """
    if tries < 1:
        raise ValueError(f'The tries value must be 1 or greater. Received {tries} value.')

    if delay <= 0:
        raise ValueError(f'The delay value must be greater than 0. Received {delay} value.')

    if backoff < 1:
        raise ValueError(f'The backoff value must be 1 or greater. Received {backoff} value.')

    if not exceptions:
        raise ValueError(f'The exceptions tuple must not be empty. Received {exceptions} value.')

    def _decorator(func: Callable):
        # functools.wraps is required to preserve the original callable metadata like __name__

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            _tries, _delay = tries, delay

            while _tries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as ex:
                    if decorator_logger is not None:
                        decorator_logger.log(
                            level=decorator_logger_level,
                            msg=f'Callable "{func.__name__}" failed because of "{ex}", retrying in {_delay} seconds.')

                    ex_str = str(ex)
                    if exceptions_filter and exceptions_filter not in ex_str:
                        raise

                    if _tries == 1:
                        raise

                sleep(_delay)
                _tries -= 1
                _delay *= backoff

        return _wrapper

    return _decorator
