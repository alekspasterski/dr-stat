#!/usr/bin/env python3

def renderMetric(help: str, unit: str, type: str, name: str, metrics: dict[str,str]) -> str:
    result : str = ""
    if type:
        result += "# TYPE " + name + " " + type + "\n"
    if unit:
        result += "# UNIT " + name + " " + unit + "\n"
    if help:
        result += "# HELP " + name + " " + help + "\n"
    for k in metrics:
        result += k + " " + metrics[k] + "\n"
    return result
