#converte gli interi di un dizionario (non nostro)
def to_dict(csv: [dict]):
    for k, e in enumerate(csv):
        for f, i in e.items():
            if i.isdigit():
                e[f] = int(i)
    return csv