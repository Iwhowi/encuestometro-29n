"""Genera data.json para la web pública a partir de la salida de aggregate.py.

Uso: python3 tools/build_data.py OUT_DIR data.json
Lee partidos.csv, promedio_diario.csv, encuestas.csv, verificacion.csv y actualizacion.json.
"""
import csv, json, sys

out, dst = sys.argv[1], sys.argv[2]

def read_csv(name):
    with open(f"{out}/{name}", newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        cols = next(r)
        return {"columns": cols, "rows": [dict(zip(cols, row)) for row in r]}

act = json.load(open(f"{out}/actualizacion.json", encoding="utf-8"))
data = {
    "actualizacion": {"columns": list(act[0].keys()), "rows": act},
    "partidos": read_csv("partidos.csv"),
    "serie": read_csv("promedio_diario.csv"),
    "encuestas": read_csv("encuestas.csv"),
    "verificacion": read_csv("verificacion.csv"),
}
assert len(data["partidos"]["rows"]) >= 5, "partidos.csv incompleto"
json.dump(data, open(dst, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("data.json:", {k: len(v["rows"]) for k, v in data.items()})
