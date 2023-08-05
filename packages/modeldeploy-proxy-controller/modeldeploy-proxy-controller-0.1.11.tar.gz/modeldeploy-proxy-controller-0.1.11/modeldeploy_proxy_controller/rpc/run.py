import sys
import logging
import importlib
from modeldeploy_proxy_controller.common.utils import random_string
from modeldeploy_proxy_controller.rpc import errors, utils
from modeldeploy_proxy_controller.rpc.log import create_adapter, setup_logging

logger = create_adapter(logging.getLogger(__name__))

def import_func(request, import_func_str):
    """Import and return a function from a string."""
    mod_str, _sep, func_str = import_func_str.rpartition('.')
    if mod_str:
        mod_str = "modeldeploy_proxy_controller.rpc." + mod_str
    else:
        mod_str = "modeldeploy_proxy_controller.rpc"
    try:
        mod = importlib.import_module(mod_str)
        return getattr(mod, func_str)
    except (ValueError, AttributeError) as e:
        request.log.exception("Exception while importing function '%s' of" " module '%s': %s", func_str, mod_str, e)
        raise ImportError("Function `%s' of module `%s' cannot be found: %s" % (func_str, mod_str, e))

def format_success(result, trans_id):
    """Serialise the result."""
    return utils.serialize({"code": errors.Code.OK.value, "result": result, "trans_id": trans_id})

class ModelDeploymentControllerRPCRequest(object):
    """RPC request."""

    def __init__(self, trans_id=None, nb_path=None):
        if not trans_id:
            trans_id = random_string(size=10)
        self.log = create_adapter(logging.getLogger(__name__), trans_id, nb_path)
        self.trans_id = trans_id
        self.nb_path = nb_path

def sanitize_ctx(request, ctx):
    """Keep just the known context fields."""
    nb_path = ctx.pop("nb_path", None)
    if ctx:
        request.log.debug("Ignoring context fields: %s", ", ".join(ctx.keys()))
    return {"nb_path": nb_path}

def run(func, kwargs, ctx):
    """Execute command requests coming from the UI.

    Args:
        func: the name of function to be run
        kwargs: A dict object with the arguments to be passed to the function
        ctx: context

    Returns: The result of the called function
    """
    # Setup initial request obj to have something to log to
    request = ModelDeploymentControllerRPCRequest()
    setup_logging(request)
    request.log.debug("Decoding ctx of RPC function '%s'", func)
    try:
        ctx = utils.deserialize(ctx)
    except Exception:
        exc_info = sys.exc_info()
        request.log.exception("Failed to decode ctx: %s", ctx)
        return errors.RPCEncodingError(message=str(exc_info[1]),
                                       trans_id=request.trans_id).serialize()
    # Sanitize ctx and renew the request obj
    ctx = sanitize_ctx(request, ctx)
    request = ModelDeploymentControllerRPCRequest(request.trans_id, **ctx)

    request.log.debug("Decoding kwargs of RPC function '%s'", func)
    try:
        kwargs = utils.deserialize(kwargs)
        request.log.debug(kwargs)
    except Exception:
        exc_info = sys.exc_info()
        request.log.exception("Failed to decode kwargs: %s", kwargs)
        return errors.RPCEncodingError(message=str(exc_info[1]),
                                       trans_id=request.trans_id).serialize()

    request.log.debug("Importing RPC function '%s'", func)
    try:
        func = import_func(request, func)
    except ImportError as e:
        exc_info = sys.exc_info()
        request.log.exception("Failed to import RPC function '%s'", func)
        return errors.RPCImportError(message=str(e), trans_id=request.trans_id).serialize()

    request.log.info("Executing RPC function '%s(%s)'", func.__name__, ", ".join("%s=%s" % i for i in kwargs.items()))
    try:
        result = func(request, **kwargs)
        return format_success(result, request.trans_id)
    except errors._RPCError as e:
        request.log.exception("RPC function '%s' raised an RPCError",
                              func.__name__)
        return e.serialize()
    except Exception:
        exc_info = sys.exc_info()
        request.log.exception(("RPC function '%s' raised an unhandled"
                               " exception"), func.__name__)
        return errors.RPCUnhandledError(message=str(exc_info[1]), trans_id=request.trans_id).serialize()
