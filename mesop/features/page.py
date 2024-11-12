from copy import deepcopy
from functools import wraps
from typing import Callable

from mesop.runtime import OnLoadHandler, PageConfig, runtime
from mesop.security.security_policy import SecurityPolicy
from mesop.security.cross_origin_resource_controls import CrossOriginResourceControls


def page(
  *,
  path: str = "/",
  title: str | None = None,
  stylesheets: list[str] | None = None,
  security_policy: SecurityPolicy | None = None,
  cross_origin_resource_controls: CrossOriginResourceControls | None = None,
  on_load: OnLoadHandler | None = None,
) -> Callable[[Callable[[], None]], Callable[[], None]]:
  """Defines a page in a Mesop application.

  This function is used as a decorator to register a function as a page in a Mesop app.

  Args:
    path: The URL path for the page. Defaults to "/".
    title: The title of the page. If None, a default title is generated.
    stylesheets: List of stylesheet URLs to load.
    security_policy: The security policy for the page. If None, a default strict security policy is used.
    on_load: An optional event handler to be called when the page is loaded.

  Returns:
    A decorator that registers the decorated function as a page.
  """

  def decorator(func: Callable[[], None]) -> Callable[[], None]:
    @wraps(func)
    def wrapper() -> None:
      return func()

    # Note: this will be replaced downstream, so do not inline/rename.
    default_stylesheets = []
    runtime().register_page(
      path=path,
      page_config=PageConfig(
        page_fn=wrapper,
        title=title or f"Mesop: {path}",
        stylesheets=deepcopy(stylesheets or default_stylesheets),
        security_policy=deepcopy(security_policy),
        cross_origin_resource_controls = deepcopy(cross_origin_resource_controls)
        if security_policy
        else SecurityPolicy(),
        on_load=on_load,
      ),
    )
    return wrapper

  return decorator
