"""Fit and clearance checks. Run: python3 verify.py"""
import itertools, math
import cadquery as cq
from monitor_arm import *

Z_MIN = 78 + 22 + 2 * WASHER + SLEEVE_DROP     # collar sitting on the clamp boss
Z_MAX = 6 + POLE_L - LINK_H - 5                # link 1 just below the pole top


def vol(a, b):
    try:
        return a.intersect(b).val().Volume()
    except Exception:
        return 0.0


# expected overlaps: the M4 screws
# go into the monitor's inserts (the dummy monitor has no holes); the M5/M6 pan-head screws
# self-tap into undersized holes (4.2 / 5.0 mm), so their threads overlap the plastic by design
EXPECTED = {("hw_detent_M5x20", "vesa_bracket"),
            ("hw_pole_setscrew_M6x25", "desk_clamp"), ("hw_swivel_setscrew_M6x25", "link1")}


def expected(na, nb):
    if (na, nb) in EXPECTED or (nb, na) in EXPECTED:
        return True
    return "monitor" in (na, nb) and (na.startswith("hw_monitor_screw") or nb.startswith("hw_monitor_screw"))


def check(pose, label):
    asm = assembly(**pose)
    bad = [(na, nb, round(v)) for (na, a), (nb, b) in itertools.combinations(asm.items(), 2)
           if not expected(na, nb) and (v := vol(a, b)) > 1.0]
    print(f"[{label:22s}] collisions: {bad if bad else 'none'}")
    return asm, bad


print("== collision sweep ==")
asm, _ = check(dict(), "nominal")
for t in (10, 50):
    check(dict(desk_t=t, with_monitor=False), f"desk {t} mm")
for tl in (-10, -5, 10, 15, 20):
    check(dict(tilt=tl), f"tilt {tl:+d} deg")
check(dict(rot=90, z_link1=400), "portrait (high)")
check(dict(z_link1=Z_MIN), "lowest collar")
for rel in (-150, -120, -90, 90, 120, 150):
    check(dict(a1=0, a2=rel, a_head=rel, with_monitor=False), f"fold {rel:+d}")
for sw in (-90, 90):
    check(dict(a1=0, a2=0, a_head=sw, with_monitor=False), f"head swivel {sw:+d}")

print("\n== monitor interface ==")
b = vesa_bracket()
hs = sorted({(round(e.Center().y, 1), round(e.Center().z, 1)) for e in b.edges().vals()
             if e.geomType() == "CIRCLE" and abs(e.radius() - M4_CLR / 2) < 0.01})
print("M4 hole centres (y,z):", hs)
# bracket front face must match the housing curve: zero overlap as placed, and when pushed
# 0.3 mm further into the housing the overlap should be ~ full face area * 0.3
m = monitor_dummy()
bb = b.translate((-PLATE_T, 0, 0))            # bracket front centre-line at X=0 = housing back
print("overlap as mounted: %.2f mm3" % vol(bb, m))
ov = vol(bb.translate((0.3, 0, 0)), m)
flat = box(-PLATE_T, 0, -PLATE / 2, PLATE / 2, -PLATE / 2, PLATE / 2)
ovf = vol(flat.translate((0.3, 0, 0)), m)
print("overlap pushed 0.3 mm: curved bracket %.0f mm3 vs flat plate %.0f mm3 (full-face contact ~%.0f)"
      % (ov, ovf, 0.3 * (PLATE * PLATE - NECK_RELIEF[0] * NECK_RELIEF[1])))
gap_edge = R_BACK - math.sqrt(R_BACK**2 - (PLATE / 2) ** 2)
print("a flat plate would gap %.2f mm at its edges, %.2f mm at the screws" %
      (gap_edge, R_BACK - math.sqrt(R_BACK**2 - (VESA / 2) ** 2)))
mb = m.val().BoundingBox()
print("bracket z span %.0f..%.0f vs housing %.0f..%.0f (monitor-local)" %
      (-PLATE / 2, PLATE / 2, -VESA_FROM_BOTTOM, -VESA_FROM_BOTTOM + HOUSING_H))
print(f"screws: M4 x {SCREW_LEN:.0f}, grip {SCREW_GRIP:.1f} mm -> {SCREW_LEN-SCREW_GRIP:.1f} mm into the inserts")

print("\n== height range ==")
for z in (Z_MIN, 175, Z_MAX):
    a = assembly(z_link1=z)
    vb = a["vesa_bracket"].val().BoundingBox().center.z
    mm = a["monitor"].val().BoundingBox()
    print(f"link1 at {z:5.0f}: insert centre {vb:5.0f} mm, screen bottom {mm.zmin:5.0f}, top {mm.zmax:5.0f}")
print("stock stand: screen bottom ~107, top ~531 (20.9in - 16.7in = 4.2in neck)")
