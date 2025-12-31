def importance_to_color(value, max_val=None):
        if max_val is None:
            max_val = 1  # par défaut, si déjà normalisé
        ratio = min(value / max_val, 1)  # s'assurer <=1
        g = int(255 * (1 - ratio))
        r = int(255 * ratio)
        b = 0
        return f"#{r:02x}{g:02x}{b:02x}"