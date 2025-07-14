from .driver import Driver
from .team import Team

# utils.py
def format_time(seconds):
    if seconds is None:
        return "N/A"
    m = int(seconds // 60)
    s = seconds % 60
    return f"{m}:{s:06.3f}"

# helper func to sort avg times
def best_avg_lap(obj):
    if isinstance(obj, Driver):
        med = obj.avg_lap_time("MEDIUM")
        hard = obj.avg_lap_time("HARD")
    elif isinstance(obj, Team):
        med = obj.team_avg("MEDIUM")
        hard = obj.team_avg("HARD")
    else:
        return None, None # unexpected type fallback
    
    compound_times = {
        'MEDIUM': med,
        'HARD': hard
    }

    valid = {comp: t for comp, t in compound_times.items() if t is not None}

    if not valid:
        return None, None # fallback

    best_compound = min(valid, key=valid.get)
    return valid[best_compound], best_compound