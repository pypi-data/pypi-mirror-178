import pathlib

import mantik.tracking._server as _server
import mantik.tracking.environment as _environment
import mantik.utils as utils

_MANTIK_FOLDER = pathlib.Path.home() / ".mantik"
_MANTIK_TOKEN_FILE = _MANTIK_FOLDER / "tokens.json"


def init_tracking() -> _environment.Environment:
    """Authenticate at the MLflow Tracking Server.

    Returns
    -------
    Environment
        Holds the environment variables required for tracking.

    Notes
    -----
    MLflow prioritizes the username and password environment variables over
    the token variable, causing an `Unauthorized` error. As a consequence,
    these have to be unset before setting the token variable.

    The tokens will be stored in a file `~/.mantik/tokens.json` to reuse
    tokens and refresh them only if they have expired.

    """
    environment = _get_required_env_vars()
    _unset_conflicting_env_vars()
    utils.env.set_env_vars(environment.to_dict())
    return environment


def _get_required_env_vars() -> _environment.Environment:
    tokens = _get_and_store_tokens()
    return _environment.Environment(token=tokens.access_token)


def _get_and_store_tokens() -> _server.tokens.Tokens:
    if not _MANTIK_TOKEN_FILE.exists():
        return _create_and_store_new_tokens()
    return _read_stored_tokens()


def _create_and_store_new_tokens() -> _server.tokens.Tokens:
    tokens = _server.api.create_tokens()
    tokens.write_to_file(_MANTIK_TOKEN_FILE)
    return tokens


def _read_stored_tokens() -> _server.tokens.Tokens:
    tokens = _server.tokens.Tokens.from_file(_MANTIK_TOKEN_FILE)
    if tokens.has_expired:
        refreshed = _server.api.refresh_tokens(
            tokens=tokens,
        )
        refreshed.write_to_file(_MANTIK_TOKEN_FILE)
        return refreshed
    return tokens


def _unset_conflicting_env_vars() -> None:
    env_vars_to_unset = {
        utils.mlflow.TRACKING_USERNAME_ENV_VAR,
        utils.mlflow.TRACKING_PASSWORD_ENV_VAR,
    }
    utils.env.unset_env_vars(env_vars_to_unset)
