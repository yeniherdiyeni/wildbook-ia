# -*- coding: utf-8 -*-
"""\
Bootstrapping functionality for commandline invocation
"""
from .threadlocal import manager
from .config import discover_settings


__all__ = ('prepare',)


def prepare(settings=None, controller=None):
    """
    Initializes the Controller (heart of the application) for use
    in a scripted setting. This returns a dictionary of locals
    including a controller object, settings data and closer function.

    The closer function should be used at the end of your script
    for data safety. Tip, use this function as a context-manager
    to automatically call the closer.

    This function places the settings and controller on the thread-local stack.
    You can access the data from anywhere in your program,
    because the variables are essentially global.

    Args:
        controller (Controller): an instantiated controller object

    Returns:
        dict: locals to be used within a scripting setting
    """
    # Discover settings and configuration
    if not settings:
        settings = discover_settings()

    # Build the controller
    # TODO (18-Aug-12020) Initialize the controller
    controller = None

    def closer():  # pragma: no cover
        controller.close()

    # Push the controller onto the threadlocal stack
    locals_ = {'controller': controller, 'settings': settings}
    manager.push(locals_)

    # Prepare the locals for return
    return AppContext(closer=closer, **locals_)


class AppContext(dict):
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        getattr(self, 'closer', lambda: None)()
