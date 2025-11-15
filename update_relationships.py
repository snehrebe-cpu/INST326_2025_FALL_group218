def update_relationships(roommates, action, history):
    base = {
        'help_chores': 0.15,
        'listen': 0.10,
        'share_food': 0.12,
        'ignore': -0.12,
        'argue': -0.20,
        'break_promise': -0.25,
    }
    a_type = action.get('type', 'ignore')
    target = action.get('target', 'all')
    mag = float(action.get('magnitude', 0.5))
    delta = base.get(a_type, 0.0) * mag
    recent = history[-5:]
    trend = 0.02 * sum(1 for a in recent if a.get('type') == a_type)
    for rid, state in roommates.items():
        if target not in ('all', rid): 
            continue
        d = delta
        mood = state.get('mood', 'neutral')
        if mood in ('annoyed', 'angry'): d *= 1.2
        if mood in ('happy', 'grateful'): d *= 0.8
        traits = set(state.get('traits', []))
        if 'sensitive' in traits and d < 0: d *= 1.5
        if 'chill' in traits and d < 0: d *= 0.7
        if 'messy' in traits and a_type == 'help_chores': d *= 1.3
        d += trend if d > 0 else -trend
        score = max(-1.0, min(1.0, state.get('relationship', 0.0) + d))
        state['relationship'] = score
    return roommates
