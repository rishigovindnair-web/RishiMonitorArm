"""Hand calcs for the README. Conservative, back-of-envelope; not FEA."""
import math
from monitor_arm import *
g = 9.81
m_mon = 5.26                       # kg, C325B-FWD240 without stand (11.6 lb)
rho, fill = 1.27e-3, 0.5           # PETG g/mm3, effective solid fraction (6 walls, 30% gyroid)
vol = {k: f().val().Volume() for k, f in PARTS.items()}
mass = {k: v * rho * fill for k, v in vol.items()}
m_head = (mass["head_yoke"] + mass["tilt_block"] + mass["vesa_bracket"]) / 1000
m_l2, m_l1 = mass["link2"] / 1000, mass["link1"] / 1000
print("Printed mass estimate (g):", {k: round(v) for k, v in mass.items()}, "total", round(sum(mass.values()) + mass["friction_washer"]))

# full extension, everything in a straight line
x_plate = L1 + L2 + TILT_X + 40 + WASHER + PLATE_T       # VESA face from pole axis
x_cog = x_plate + COG_FWD                                  # monitor COG in front of VESA face (estimate)
M = g * (m_mon * x_cog + m_head * (L1 + L2 + 50) + m_l2 * (L1 + L2 / 2) + m_l1 * L1 / 2) / 1000
print(f"Reach: VESA face {x_plate:.0f} mm from pole; overturning moment {M:.1f} N*m")

# pole: 3/4in EMT, 23.42 OD x 1.245 wall, steel (C80.3 min yield ~ 207 MPa used conservatively)
Do, t = 23.42, 1.245; Di = Do - 2 * t
I = math.pi / 64 * (Do**4 - Di**4); S = I / (Do / 2)
sig = M * 1000 / S
print(f"Pole: S={S:.0f} mm3, bending {sig:.0f} MPa vs ~207 MPa yield -> SF {207/sig:.1f}")

# clamp: needed reaction when arm points sideways (tips about clamp side edge, lever = CLAMP_W/2)
F_side = M / (CLAMP_W / 2 / 1000)
F_cl = max(1000, F_side * 1.2)
Mspine = F_cl * 56.5
Sspine = CLAMP_W * 25**2 / 6
print(f"Clamp: pad reaction sideways {F_side:.0f} N -> design clamp force {F_cl:.0f} N; spine stress {Mspine/Sspine:.1f} MPa (in-layer)")

# link 1 root bending + torsion
M1 = g * (m_mon * (x_cog - SLEEVE_R) + m_head * (L1 + L2) + m_l2 * (L1 + L2 / 2)) / 1000
S1 = L1_W * LINK_H**2 / 6
T1 = g * m_mon * (L2 + 100) / 1000
tau = T1 * 1000 / (0.231 * L1_W**2 * LINK_H)
print(f"Link1: root bending {M1:.1f} N*m -> {M1*1000/S1:.1f} MPa; worst torsion {T1:.1f} N*m -> {tau:.1f} MPa")

# droop at full extension (cantilever, E_eff PETG print ~1500 MPa)
E = 1500.0
I1 = L1_W * LINK_H**3 / 12; I2 = L2_W * LINK_H**3 / 12
P = g * m_mon
l_after = x_cog - L1
th1 = P * L1**2 / (2 * E * I1) + P * l_after * L1 / (E * I1)
d1 = P * L1**3 / (3 * E * I1) + P * l_after * L1**2 / (2 * E * I1)
d2 = P * L2**3 / (3 * E * I2) + P * (x_cog - L1 - L2) * L2**2 / (2 * E * I2)
th2 = P * L2**2 / (2 * E * I2) + P * (x_cog - L1 - L2) * L2 / (E * I2)
pole_free = 200.0
th_p = M * 1000 * pole_free / (200000 * I)
th_s = SLEEVE_FIT / (SLEEVE_DROP + LINK_H)
droop = d1 + th1 * (x_cog - L1) + d2 + th2 * (x_cog - L1 - L2) + (th_p + th_s) * x_cog
print(f"Droop at full reach ~{droop:.0f} mm (links {d1+th1*(x_cog-L1)+d2+th2*(x_cog-L1-L2):.1f}, pole {th_p*x_cog:.1f}, sleeve slop {th_s*x_cog:.1f})")

# tilt friction: COG is COG_FWD in front of and COG_UP above the insert centre
a = 40 + WASHER + PLATE_T + COG_FWD            # tilt axis -> COG, horizontal, untilted
b = COG_UP
worst = 0
for deg in range(-10, 21):                     # -10 = screen tipped forward, +20 = back
    th = math.radians(deg)
    lever = a * math.cos(th) - b * math.sin(th)
    worst = max(worst, abs(lever))
T_tilt = P * worst / 1000
R, r = TONGUE_R, M8_CLR / 2
r_eff = 2 / 3 * (R**3 - r**3) / (R**2 - r**2)
mu = 0.5   # TPU on PETG
F_need = T_tilt / (2 * mu * r_eff / 1000)
print(f"Tilt: worst holding torque {T_tilt:.1f} N*m (lever {worst:.0f} mm), r_eff {r_eff:.1f} mm -> preload >= {F_need:.0f} N (aim {2*F_need:.0f} N)")
T_rot = P * COG_UP / 1000
print(f"Rotation: in portrait the COG sits {COG_UP:.0f} mm off the pivot -> {T_rot:.1f} N*m, "
      f"{T_rot*1000/24:.0f} N on the M5 detent at r=24")

# M10 stacked pivot bending
Mb = g * m_mon * (x_cog - L1) / 1000
Sb = math.pi * 8.16**3 / 32
print(f"M10 pivot (if face clamp fails, worst case): {Mb*1000/Sb:.0f} MPa vs 640 MPa (8.8)")
