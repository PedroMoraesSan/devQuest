from devquest.dashboard import run_dashboard
from devquest.profile import require_profile


def dashboard():
    require_profile()
    run_dashboard()
