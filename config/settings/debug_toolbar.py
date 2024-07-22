from .env import DEBUG, TOOLBAR

if DEBUG and TOOLBAR:
    def show_toolbar(*args, **kwargs):
        return True


    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }

