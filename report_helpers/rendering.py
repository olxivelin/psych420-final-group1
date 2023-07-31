

def render_recalled_words(recalled_from_stm):
    o = []
    for original, recalled, strength in recalled_from_stm:
        o.append(f"{'/'.join(recalled)}")

    return ", ".join(o)
