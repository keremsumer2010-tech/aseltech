"""Build the four Aquifer Run levels (web/run/levels/*.json) from a compact recipe (PC1).

Why a generator: every level stays consistent with the engine (48 px tiles, jump ≈ 2 tiles up,
≈ 3 tiles across), and the real NISAR numbers are read from data/global/atlas.json instead of being
typed by hand. Usage: python tools/make_run_levels.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "web" / "run" / "levels"
H = 14            # rows (extra underground rows so the water layer is visible)
BASE = 9          # default ground surface row
atlas = {r["id"]: r for r in json.loads((ROOT / "data/global/atlas.json").read_text(encoding="utf-8"))["regions"]}


def rate(rid):
    return atlas[rid]["rate_cm_per_100d_common"]


BIOME = {
    "tulare": {"top": "grass", "under": "dirt", "deep": "clay", "pit": None, "decor": ["orchard", "bush", "fence", "tree"]},
    "eloy": {"top": "sand", "under": "sand", "deep": "clay", "pit": "fissure", "decor": ["cotton", "bush", "fence"]},
    "konya": {"top": "grass", "under": "dirt", "deep": "clay", "pit": None, "decor": ["wheat", "wheat", "bush", "fence"]},
    "mexico": {"top": "road", "under": "brick", "deep": "brick", "pit": None, "decor": ["lamp", "tree", "fence"]},
}
CH = {"grass": "G", "dirt": "D", "clay": "C", "sand": "N", "road": "R", "brick": "B", "sink1": "S", "sink2": "T",
      "fissure": "F", "crate": "X", "bridge": "=", "orchard": "o", "bush": "b", "fence": "f", "tree": "t",
      "cotton": "c", "wheat": "w", "lamp": "l", "sign": "s", "rock": "#"}


INTRO = {
    "tulare": "First valley: the tips will show you everything, step by step.",
    "eloy": "New here: jump over earth fissures; splash dust devils with E.",
    "konya": "New here: in Konya, sinking ground can open sinkholes (obruk).",
    "mexico": "New here: a whole city built on an old lake bed.",
}


class Level:
    def __init__(self, lid, name, biome):
        self.id, self.name, self.biome, self.b = lid, name, biome, BIOME[biome]
        self.cols = []        # per column: surface row or None (pit), top tile name
        self.ents, self.plats, self.tips, self.decor = [], [], [], {}

    # --- terrain recipe ---
    def flat(self, n, h=0, top=None):
        for _ in range(n): self.cols.append((BASE - h, top or self.b["top"]))
        return self

    def gap(self, n):
        for _ in range(n): self.cols.append((None, None))
        return self

    def sink(self, n, h=0):
        for i in range(n): self.cols.append((BASE - h, "sink1" if i % 2 else "sink2"))
        return self

    @property
    def x(self):
        return len(self.cols)

    def surf(self, x):
        return self.cols[x][0]

    # --- objects (y = the cell above the ground at column x, unless dy is given) ---
    def ent(self, typ, back=0, dy=0, **kw):
        """Place an object `back` columns before the current end of the level, `dy` cells above the ground."""
        x = self.x - 1 - back
        s = self.surf(x)
        assert s is not None, f"{self.id}: {typ} at x={x} has no ground"
        e = {"type": typ, "x": x, "y": s - 1 - dy}
        e.update(kw); self.ents.append(e)
        return self

    def plat(self, back, up, n, tile="crate"):
        """Floating platform starting `back` columns before the end, `up` rows above the ground there."""
        up = min(up, 2)                      # the hero jumps ~2.2 tiles: keep platforms reachable
        x = self.x - 1 - back; y = self.surf(x) - up
        self.plats.append((x, y, n, tile)); return self

    def tip(self, text, until, keys=None, hud=False, back=0):
        t = {"x": max(1, self.x - 1 - back), "text": text, "until": until}
        if keys: t["keys"] = keys
        if hud: t["hud"] = True
        self.tips.append(t); return self

    def deco(self, tile, back=0):
        self.decor[self.x - 1 - back] = tile; return self

    def build(self, aquifer, nisar):
        W = len(self.cols)
        grid = [["." for _ in range(W)] for _ in range(H)]
        for x, (s, top) in enumerate(self.cols):
            if s is None:
                if self.b["pit"]:
                    for y in range(BASE, H): grid[y][x] = CH[self.b["pit"]]
                continue
            grid[s][x] = CH[top]
            for y in range(s + 1, H): grid[y][x] = CH[self.b["deep"] if y >= H - 1 else self.b["under"]]
        for x, y, n, tile in self.plats:
            for i in range(n): grid[y][x + i] = CH[tile]
        auto = self.b["decor"]
        for x in range(3, W - 3):
            s = self.surf(x)
            if s is None or grid[s - 1][x] != ".": continue
            if x in self.decor: grid[s - 1][x] = CH[self.decor[x]]
            elif x % 7 == 3 and not any(e["x"] == x for e in self.ents): grid[s - 1][x] = CH[auto[(x // 7) % len(auto)]]
        legend = {v: k for k, v in CH.items()}
        used = {c for row in grid for c in row} - {"."}
        return {
            "id": self.id, "name": self.name, "biome": self.biome, "width": W, "height": H, "groundRow": BASE,
            "spawn": {"x": 2, "y": self.surf(2) - 2}, "intro": INTRO[self.id],
            "tiles": ["".join(r) for r in grid],
            "legend": {c: legend[c] for c in sorted(used)},
            "entities": self.ents, "tips": self.tips, "aquifer": aquifer, "nisar": nisar,
            "radar": {"tulare": "../data/central_valley/disp/2026-10-14.png", "eloy": "../data/global/eloy/disp/2026-10-17.png",
                      "konya": "../data/karapinar/disp/2026-10-12.png", "mexico": "../data/global/mexico_city/disp/2026-10-20.png"}[self.biome],
        }


def tulare():
    L = Level("tulare", "Tulare Basin, California", "tulare")
    L.flat(4).tip("Move with", "moved", ["←", "→"], back=2).flat(5).deco("sign", 3).ent("drop", 2)
    L.tip("Jump with", "jumped", ["SPACE"]).flat(3).plat(1, 1, 1)            # crate to jump on
    L.flat(6).ent("drop", 4, dy=1).ent("drop", 2, dy=2).ent("drop", 0)
    L.tip("Catch raindrops: they fill your water tank", "tank3", back=5)
    L.flat(5).ent("pump", 1).tip("This pump drains the water underground. Stand at it and press", "pump", ["E"], back=3)
    L.flat(6).ent("crop", 4).ent("farmer", 2, line="Thanks! With rain in my tank I don't have to pump.")
    L.tip("Thirsty crop! Press E to give it 1 water from your tank", "crop", ["E"], back=5)
    L.flat(3).tip("This bar is the water underground. Below the yellow line, the ground sinks for good", "time5", hud=True, back=1)
    L.sink(6).tip("Cracked ground drops if the water underground gets too low", "pass", back=6)
    L.flat(4).ent("checkpoint", 1)
    L.flat(3).ent("drop", 1).gap(2).flat(4).ent("drop", 1)
    L.flat(2, 1).flat(2, 2).ent("chip", 0, dy=2, fact="tulare-1").flat(3, 1).flat(4).ent("pump", 1)
    L.flat(5).ent("drop", 3, dy=1).ent("crop", 1)
    L.sink(8).ent("drop", 4).flat(3).gap(3).flat(5).ent("pump", 2)
    L.flat(6).plat(4, 3, 3, "bridge").ent("chip", 3, dy=4, fact="tulare-2").ent("crop", 1).ent("drop", 5)
    L.flat(3).ent("checkpoint", 1)
    L.flat(4).sink(6).ent("drop", 3).flat(3, 1).gap(2).flat(4).ent("chip", 1, fact="qc")
    L.flat(6).ent("pump", 4).ent("chip", 2, dy=3, fact="tulare-3").flat(4).ent("crop", 1)
    L.flat(8).ent("flag", 3)
    return L.build({"start": 64, "redLine": 40, "drainPerPump": 0.16, "recharge": 0.15, "cropRefill": 3, "pumpBoost": 4},
                   {"scanEverySec": 22, "realFactCm": rate("central_valley"),
                    "realFactText": "NISAR measured California's Central Valley sinking up to 7.8 cm (3 in) in just 108 days of summer 2026."})


def eloy():
    L = Level("eloy", "Eloy, Arizona", "eloy")
    L.flat(10).ent("drop", 5).ent("drop", 2).tip("Earth fissures are long cracks that open when too much water is pumped. Jump over them!", "pass", back=6)
    L.flat(4).ent("pump", 2).gap(2).flat(6).ent("dust", 2, range=3).ent("drop", 4, dy=1)
    L.tip("Dust devils steal water. Run past them, or splash them with", "pass", ["E"], back=6)
    L.flat(4).ent("crop", 1).gap(3).flat(5).ent("drop", 3).ent("checkpoint", 1)
    L.flat(2, 1).flat(3, 2).ent("chip", 1, dy=2, fact="eloy-1").flat(2, 1).flat(4).ent("pump", 1)
    L.sink(6).flat(4).ent("crop", 3).ent("farmer", 1, line="Cotton needs a lot of water. Your rain helps!")
    L.gap(2).flat(6).ent("dust", 2, range=3).ent("drop", 5)
    L.gap(3).flat(4).ent("pump", 1).flat(5).plat(3, 3, 4, "bridge").ent("chip", 2, dy=4, fact="eloy-2")
    L.flat(5).ent("crop", 3).ent("checkpoint", 1).sink(8).ent("drop", 4)
    L.flat(4).ent("pump", 1).gap(2).flat(5).ent("dust", 1, range=2).ent("drop", 4)
    L.flat(2, 1).flat(2, 2).flat(2, 1).ent("chip", 2, dy=1, fact="qc").flat(5).ent("crop", 1)
    L.gap(3).flat(6).ent("chip", 3, dy=3, fact="eloy-3").ent("pump", 1).flat(8).ent("flag", 3)
    return L.build({"start": 54, "redLine": 40, "drainPerPump": 0.2, "recharge": 0.15, "cropRefill": 3, "pumpBoost": 4},
                   {"scanEverySec": 22, "realFactCm": rate("eloy"),
                    "realFactText": f"Eloy is the fastest-sinking reliable basin in our atlas: {rate('eloy')} cm per 100 days (NISAR, 2026)."})


def konya():
    L = Level("konya", "Karapınar, Konya", "konya")
    L.flat(8).ent("drop", 3).tip("In Konya, sinking ground can open sinkholes (obruk). Keep the water up!", "pass", back=4)
    L.sink(3).flat(4).ent("pump", 1).flat(4).ent("crop", 1).gap(2).flat(5).ent("drop", 2)
    L.sink(5).ent("drop", 2).flat(4).ent("checkpoint", 2).ent("pump", 0)
    L.flat(2, 1).flat(3, 2).ent("chip", 1, dy=2, fact="konya-1").flat(2, 1)
    L.flat(5).ent("crop", 3).ent("farmer", 1, line="My grandfather's well is dry now. The water table keeps falling.")
    L.sink(8).ent("drop", 4).gap(3).flat(5).ent("pump", 2)
    L.flat(5).plat(4, 3, 3, "bridge").ent("chip", 3, dy=4, fact="konya-2").ent("crop", 1)
    L.sink(6).ent("drop", 3).flat(3).ent("checkpoint", 1).gap(2).flat(5).ent("pump", 1)
    L.flat(2, 1).flat(2, 2).ent("chip", 0, dy=1, fact="qc").flat(2, 1).sink(8).ent("drop", 4)
    L.flat(5).ent("crop", 2).gap(3).flat(5).ent("pump", 3).ent("chip", 1, dy=3, fact="konya-3")
    L.sink(6).flat(8).ent("flag", 3)
    return L.build({"start": 55, "redLine": 40, "drainPerPump": 0.2, "recharge": 0.15, "cropRefill": 3, "pumpBoost": 4},
                   {"scanEverySec": 20, "realFactCm": rate("konya_plain"),
                    "realFactText": f"NISAR saw the strongest signal of our atlas in the Konya Plain ({rate('konya_plain')} cm per 100 days); our own check keeps it 'indicative' until more data arrive."})


def mexico():
    L = Level("mexico", "Mexico City", "mexico")
    L.flat(9).ent("drop", 4).tip("Mexico City is built on an old lake bed. Pumping makes whole streets sink.", "pass", back=5)
    L.flat(4).ent("pump", 2).flat(2, 1).flat(2, 2).ent("drop", 1, dy=1).flat(2, 1).flat(4).ent("crop", 1)
    L.gap(2).flat(5).ent("dust", 3, range=2).ent("checkpoint", 1).sink(6).ent("drop", 3)
    L.flat(4).ent("pump", 2).flat(4).plat(3, 3, 3, "bridge").ent("chip", 2, dy=4, fact="mexico-1")
    L.flat(6).ent("crop", 4).ent("farmer", 2, line="Our old church tilts a little more every year.")
    L.gap(3).flat(4).ent("pump", 1).flat(2, 1).flat(2, 2).ent("chip", 0, dy=1, fact="qc").flat(2, 1)
    L.sink(8).ent("drop", 4).flat(4).ent("checkpoint", 1).gap(2).flat(5).ent("dust", 2, range=2)
    L.flat(3).ent("pump", 1).flat(2, 1).flat(3, 2).ent("chip", 1, dy=2, fact="mexico-2").flat(2, 1)
    L.flat(4).ent("crop", 1).sink(6).gap(3).flat(5).ent("pump", 3).ent("crop", 1)
    L.flat(3).ent("chip", 1, dy=3, fact="mexico-3").sink(5).flat(8).ent("flag", 3)
    return L.build({"start": 55, "redLine": 40, "drainPerPump": 0.2, "recharge": 0.15, "cropRefill": 3, "pumpBoost": 4},
                   {"scanEverySec": 20, "realFactCm": rate("mexico_city"),
                    "realFactText": f"NISAR measured parts of Mexico City sinking {rate('mexico_city')} cm per 100 days in 2026."})


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (tulare, eloy, konya, mexico):
        lvl = fn()
        (OUT / f"{lvl['id']}.json").write_text(json.dumps(lvl, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        pumps = sum(e["type"] == "pump" for e in lvl["entities"]); crops = sum(e["type"] == "crop" for e in lvl["entities"])
        print(f"{lvl['id']:7} {lvl['width']}x{lvl['height']} pumps={pumps} crops={crops} tips={len(lvl['tips'])} rate={lvl['nisar']['realFactCm']}")
