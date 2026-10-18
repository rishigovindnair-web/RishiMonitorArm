"""
Pole-mount monitor arm for the Sceptre C32 240 Hz, C325B-185RD1 (confirmed from the unit label)
  - No flat VESA pad: four M4 inserts (100 x 100) sit directly in the CURVED back of
    the lower electronics housing, ~84 mm above the bottom edge (not at screen centre)
  - 1800R panel -> housing back is convex toward the arm, R ~ 1840 mm
  - 5.3 kg (11.6 lb) without stand, centre of mass ~105 mm ABOVE the VESA centre
  - Desk C-clamp (10-50 mm desks), 3/4" EMT steel conduit pole
  - Height: stop collar on the pole (pinch bolt + optional 1/4" cross pin)
  - Swivel + reach: two horizontal links on vertical M10 pivots
  - Head hangs BELOW link 2 so the low-mounted screen can sit at stock-stand height
  - Head: swivel (M10), tilt (M8 friction w/ disc springs), rotate (M8 + detent pin)
  - Monitor interface: curved saddle bracket screwed straight into the 4 inserts

Units: mm. World frame: Z up, pole axis at X=Y=0, desk top at Z=0,
desk extends toward +X (toward the user), back edge of desk at X=-44.

Run:  python3 monitor_arm.py   -> writes out/step, out/stl
"""
import math, os
import cadquery as cq

# ------------------------------------------------------------------ parameters
POLE_KIND   = os.environ.get("MONITOR_POLE", "emt")
if POLE_KIND == "pipe":   # 3/4" schedule-40 steel pipe nipple, 18" long, bought pre-cut (no saw needed)
    POLE_D, POLE_WALL, POLE_L = 26.67, 2.87, 457.2
else:                     # 3/4" EMT conduit, OD 0.922" (23.42 mm), cut to 500 mm. Measure yours!
    POLE_D, POLE_WALL, POLE_L = 23.4, 1.24, 500.0
SOCKET_FIT  = 0.5     # diametral clearance, clamp socket / collar
SLEEVE_FIT  = 0.3     # diametral clearance, link-1 sleeve (keep tight = less droop)
M10_CLR     = 10.5
M8_CLR      = 8.4
M6_TAP      = 5.0     # M6 screw self-taps into PETG
M5_CLR      = 5.5
M5_TAP      = 4.2
M4_CLR      = 4.5
NUT_FIT     = 0.4

L1          = 230.0   # link 1 pivot spacing (278 mm part -> fits a 235x235 bed diagonally)
L2          = 200.0   # link 2 pivot spacing
LINK_H      = 45.0    # link height (vertical)
L1_W, L2_W  = 30.0, 28.0
HUB_R       = 22.0
SLEEVE_R    = 24.0
SLEEVE_DROP = 35.0    # sleeve extends this far below link 1 beam
WASHER      = 1.0     # PTFE/nylon washer between stacked parts

VESA        = 100.0
PLATE       = 120.0   # bracket is 120 x 120; stays on the lower housing (~157 mm tall)
PLATE_T     = 15.0    # bracket thickness on the centre line (edges are ~1 mm thicker)
R_BACK      = 1840.0  # radius of the housing back (1800R panel + ~40 mm housing depth)
NECK_RELIEF = (46.0, 40.0, 1.5, 0.0)   # w, h, depth, z-centre: clears the rim of the neck slot
                                       # (slot opening ~38 x 31 mm, centred in the insert square - from photos)
VESA_FROM_BOTTOM = 90.0           # insert centre above the monitor's bottom edge (tape photo IMG_4966:
                                  # inserts 17 / 116 mm below the housing's top step -> centre 67 mm below it)
HOUSING_H   = 157.0   # lower housing height, bottom edge -> top step (photo: flat back ends ~144 mm, then vents)
COG_UP, COG_FWD  = 95.0, 31.0     # monitor centre of mass vs insert centre (estimate)
SCREW_LEN   = 12.0    # the stand's own neck screws: M4 x 12 pan head (use 4)
SCREW_GRIP  = 5.0     # bracket material under the screw head -> 7 mm thread engagement
TILT_X      = 60.0    # swivel axis -> tilt axis
TILT_Z      = 20.0    # tilt axis height above head-yoke bottom (ear circle sits on the bed)
EAR_R       = 20.0
TONGUE_R    = 18.0
TONGUE_W    = 24.0
EAR_T       = 12.0
HEAD_HUB_H  = 40.0

CLAMP_W     = 76.0    # clamp width along the desk edge

OUT = os.environ.get("MONITOR_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"))


def hex_prism(af, depth, plane="XY", rot=30):
    d = af / math.cos(math.radians(30))
    return cq.Workplane(plane).polygon(6, d).extrude(depth).rotate((0, 0, 0), (0, 0, 1), rot) \
        if plane == "XY" else cq.Workplane(plane).polygon(6, d).extrude(depth)


def teardrop_z(d, h, z0=0.0):
    """Hole along +Z with a 45deg tip toward +Y (prints clean when part lies on its -Y face)."""
    r = d / 2
    tri = (cq.Workplane("XY").workplane(offset=z0)
           .polyline([(-r * math.cos(math.radians(45)), r * math.sin(math.radians(45))),
                      (0, r * math.sqrt(2)),
                      (r * math.cos(math.radians(45)), r * math.sin(math.radians(45))),
                      (0, 0)]).close().extrude(h))
    return cq.Workplane("XY").workplane(offset=z0).circle(r).extrude(h).union(tri)


def cyl_x(r, x0, x1, y=0, z=0):
    return cq.Workplane("YZ").workplane(offset=x0).center(y, z).circle(r).extrude(x1 - x0)


def cyl_y(r, y0, y1, x=0, z=0):
    return (cq.Workplane("XZ").workplane(offset=-y1).center(x, z).circle(r).extrude(y1 - y0))


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


# ------------------------------------------------------------------ desk clamp
def desk_clamp():
    # C-profile in XZ, extruded 90 mm along Y. Print lying on its side (-Y face down):
    # every bending stress then runs along the layers, not across them.
    pts = [(-69, -89), (25, -89), (25, -67), (-36, -67), (-44, -59), (-44, 0),
           (60, 0), (60, 22), (30, 40), (30, 78), (-30, 78), (-30, 44), (-69, 26)]
    body = (cq.Workplane("XZ").polyline(pts).close().extrude(CLAMP_W / 2, both=True))
    # pole socket (6 mm floor)
    body = body.cut(teardrop_z(POLE_D + SOCKET_FIT, 80, z0=6))
    # M6 set screw into pole (self-tapping)
    body = body.cut(cyl_x(M6_TAP / 2, 0, 31, z=60))
    # M10 clamp screw + captive nut (top of lower jaw)
    body = body.cut(teardrop_z(M10_CLR, 30, z0=-92))
    nut = (cq.Workplane("XY").workplane(offset=-76)
           .polygon(6, (17 + NUT_FIT) / math.cos(math.radians(30))).extrude(10)
           .rotate((0, 0, 0), (0, 0, 1), 30))
    body = body.cut(nut)
    # soften outside vertical edges a bit
    try:
        body = body.edges("|Y").edges(cq.selectors.BoxSelector((-70, -50, -90), (-60, 50, -80))).fillet(6)
    except Exception:
        pass
    return body


def clamp_knob():
    k = cq.Workplane("XY").circle(25).extrude(22)
    for i in range(8):
        a = math.radians(i * 45)
        k = k.cut(cq.Workplane("XY").center(28 * math.cos(a), 28 * math.sin(a)).circle(6).extrude(22))
    k = k.edges(">Z or <Z").chamfer(1.2)
    k = k.cut(cq.Workplane("XY").circle(M10_CLR / 2).extrude(22))
    # hex head pocket (M10 head = 17 mm AF DIN 933; ISO 4017 is 16 -> set to 16.3)
    k = k.cut(cq.Workplane("XY").workplane(offset=22 - 7)
              .polygon(6, (17 + 0.3) / math.cos(math.radians(30))).extrude(7))
    return k


def clamp_pad():
    p = cq.Workplane("XY").circle(20).extrude(12).edges(">Z").chamfer(1.5)
    return p.cut(cq.Workplane("XY").circle(10.6 / 2).extrude(6))


# ------------------------------------------------------------------ height collar
def stop_collar():
    h = 22
    c = cq.Workplane("XY").circle(SLEEVE_R).extrude(h)
    c = c.union(box(18, 36, -11, 11, 0, h))
    c = c.cut(cq.Workplane("XY").circle((POLE_D + SOCKET_FIT) / 2).extrude(h))
    c = c.cut(box(8, 37, -1.0, 1.0, 0, h))                    # pinch slit
    c = c.cut(cyl_y(M5_CLR / 2, -12, 12, x=29, z=h / 2))         # M5 pinch bolt
    nut = (cq.Workplane("XZ").workplane(offset=-12).center(29, h / 2)
           .polygon(6, (8 + NUT_FIT) / math.cos(math.radians(30))).extrude(4))
    c = c.cut(nut)
    c = c.cut(cyl_y(6.6 / 2, -30, 30, x=0, z=h / 2))             # optional 1/4" cross pin
    return c


# ------------------------------------------------------------------ links
def link_plan(L, w, r0, r1, h):
    s = (cq.Workplane("XY").circle(r0).extrude(h)
         .union(box(0, L, -w / 2, w / 2, 0, h))
         .union(cq.Workplane("XY").center(L, 0).circle(r1).extrude(h)))
    return s


def link1():
    s = link_plan(L1, L1_W, SLEEVE_R, HUB_R, LINK_H)
    s = s.union(cq.Workplane("XY").workplane(offset=-SLEEVE_DROP).circle(SLEEVE_R)
                .extrude(SLEEVE_DROP + LINK_H))
    # web fillets between beam and hubs
    try:
        s = s.edges("|Z").edges(cq.selectors.BoxSelector((15, -20, -1), (L1 - 15, 20, LINK_H + 1))).fillet(10)
    except Exception:
        pass
    s = s.cut(cq.Workplane("XY").workplane(offset=-SLEEVE_DROP).circle((POLE_D + SLEEVE_FIT) / 2)
              .extrude(SLEEVE_DROP + LINK_H))
    s = s.cut(cq.Workplane("XY").center(L1, 0).circle(M10_CLR / 2).extrude(LINK_H))
    # M6 thumb screw (nylon-tipped) for swivel drag / lock on the pole
    s = s.cut(cyl_x(M6_TAP / 2, -SLEEVE_R - 1, 0, z=-SLEEVE_DROP / 2))
    return s


def link2():
    s = link_plan(L2, L2_W, HUB_R, HUB_R, LINK_H)
    try:
        s = s.edges("|Z").edges(cq.selectors.BoxSelector((15, -20, -1), (L2 - 15, 20, LINK_H + 1))).fillet(10)
    except Exception:
        pass
    for x in (0, L2):
        s = s.cut(cq.Workplane("XY").center(x, 0).circle(M10_CLR / 2).extrude(LINK_H))
    return s


# ------------------------------------------------------------------ head
def head_yoke():
    H = HEAD_HUB_H
    hub = cq.Workplane("XY").circle(HUB_R).extrude(H)
    bridge = box(0, 44, -(TONGUE_W / 2 + WASHER + EAR_T), TONGUE_W / 2 + WASHER + EAR_T, 0, H)
    gap = TONGUE_W / 2 + WASHER
    ears = None
    for sgn in (1, -1):
        y0, y1 = (gap, gap + EAR_T) if sgn > 0 else (-gap - EAR_T, -gap)
        e = (cq.Workplane("XZ").workplane(offset=-y1).center(TILT_X, TILT_Z).circle(EAR_R).extrude(EAR_T)
             .union(cq.Workplane("XZ").workplane(offset=-y1)
                    .polyline([(30, 0), (TILT_X, 0), (TILT_X, 2 * EAR_R), (30, 2 * EAR_R)]).close().extrude(EAR_T)))
        ears = e if ears is None else ears.union(e)
    y = hub.union(bridge).union(ears)
    # clearance for the tilting tongue
    y = y.cut(cyl_y(TONGUE_R + 1.5, -gap, gap, x=TILT_X, z=TILT_Z))
    y = y.cut(cq.Workplane("XY").circle(M10_CLR / 2).extrude(H))
    y = y.cut(cyl_y(M8_CLR / 2, -40, 40, x=TILT_X, z=TILT_Z))
    return y


def tilt_block():
    """Local frame: origin on tilt axis, +X toward monitor."""
    t = cyl_y(TONGUE_R, -TONGUE_W / 2, TONGUE_W / 2)
    t = t.union(box(0, 40, -TONGUE_W / 2, TONGUE_W / 2, -TONGUE_R, TONGUE_R))
    t = t.union(cyl_x(30, 30, 40))                                # rotation disc, front face X=40
    t = t.cut(cyl_y(M8_CLR / 2, -20, 20))                         # tilt bolt
    t = t.cut(cyl_x(M8_CLR / 2, 15, 40))                          # rotation bolt
    # captive M8 nylock, slot open to the top
    af = 13 + NUT_FIT
    nut = (cq.Workplane("YZ").workplane(offset=19).polygon(6, af / math.cos(math.radians(30))).extrude(9))
    t = t.cut(nut).cut(box(19, 28, -af / 2, af / 2, 0, 20))
    # detent pin hole (M5 thumbscrew) at r=24, top
    t = t.cut(cyl_x(M5_CLR / 2, 30, 40, z=24))
    return t


def vesa_bracket():
    """Curved saddle that screws straight into the monitor's 4 M4 inserts.
    Local frame: flat back face X=0 (arm side). Front face is a concave cylinder
    (vertical axis, radius R_BACK) that matches the convex housing back; X=PLATE_T on the
    centre line. A flat plate would only touch along the middle and the 4 screws would
    bend the housing ~0.7 mm to pull it flat."""
    T = PLATE_T
    p = box(0, T + 2, -PLATE / 2, PLATE / 2, -PLATE / 2, PLATE / 2).edges("|X").fillet(8)
    cx = T + R_BACK
    p = p.cut(cq.Workplane("XY").workplane(offset=-PLATE).center(cx, 0).circle(R_BACK).extrude(2 * PLATE))
    w, h, d, zc = NECK_RELIEF
    p = p.cut(box(T - d, T + 3, -w / 2, w / 2, zc - h / 2, zc + h / 2).edges("|X").fillet(4))
    for sy in (-1, 1):
        for sz in (-1, 1):
            y, z = sy * VESA / 2, sz * VESA / 2
            front = T + (R_BACK - math.sqrt(R_BACK**2 - y**2))
            p = p.cut(cyl_x(M4_CLR / 2, 0, T + 3, y, z))
            p = p.cut(cyl_x(9.5 / 2, 0, front - SCREW_GRIP, y, z))   # counterbore
    p = p.cut(cyl_x(M8_CLR / 2, 0, T + 3))
    # round recess for the M8 head (bracket turns around it; nut is captive in the tilt block)
    p = p.cut(cyl_x(15.5 / 2, T - NECK_RELIEF[2] - 6, T + 3))
    for a in (0, 90, 180, 270):
        r = math.radians(a)
        p = p.cut(cyl_x(M5_TAP / 2, 0, 10, 24 * math.sin(r), 24 * math.cos(r)))
    return p


def friction_washer():
    """Print 2 in TPU (or cut from 1 mm rubber/cork). Sits on each side of the tilt tongue."""
    return cq.Workplane("XY").circle(TONGUE_R).circle(M8_CLR / 2 + 0.2).extrude(WASHER)


# ------------------------------------------------------------------ reference geometry
PIN_HOLE_D = 6.5      # drill through the pole for the 1/4" (6.35 mm) cross pin


def pole(pin_z=None):
    """3/4" EMT. pin_z: height of the cross-pin hole you drill (at the collar's centre)."""
    p = cq.Workplane("XY").workplane(offset=6).circle(POLE_D / 2).circle(POLE_D / 2 - POLE_WALL).extrude(POLE_L)
    if pin_z is not None:
        p = p.cut(cyl_y(PIN_HOLE_D / 2, -POLE_D, POLE_D, x=0, z=pin_z))
    return p


def monitor_dummy():
    """C32 240 Hz from Sceptre's product renders/specs: 719 x 424 mm, 1800R, thin upper
    panel (~12 mm at centre) and a full-width lower housing ~157 mm tall, ~40 mm deep at
    centre, carrying the inserts. Local frame: housing back (VESA face) at X=0 on the centre
    line, insert-pattern centre at origin, screen toward +X."""
    W, H, R = 719.0, 424.0, 1800.0
    depth_c = R_BACK - R          # housing depth at centre (40)
    panel_t = 12.0
    zb = -VESA_FROM_BOTTOM
    cx = R_BACK                   # screen axis: screen centre at X=depth_c
    def ring(r_out, r_in, z0, h):
        return (cq.Workplane("XY").workplane(offset=z0).center(cx, 0).circle(r_out).extrude(h)
                .cut(cq.Workplane("XY").workplane(offset=z0).center(cx, 0).circle(r_in).extrude(h)))
    clip = box(-5, 200, -W / 2, W / 2, zb, zb + H)
    panel = ring(R + panel_t, R, zb, H).intersect(clip)
    housing = ring(R_BACK, R, zb, HOUSING_H).intersect(clip)
    return panel.union(housing)



# ------------------------------------------------------------------ bought hardware (reference only)
def _hexz(af, z0, h, rot=0.0):
    return (cq.Workplane("XY").workplane(offset=z0)
            .polygon(6, af / math.cos(math.radians(30))).extrude(h)
            .rotate((0, 0, 0), (0, 0, 1), rot))


def _disc(od, idia, z0, t):
    return cq.Workplane("XY").workplane(offset=z0).circle(od / 2).circle(idia / 2).extrude(t)


def hw_bolt(d, L, head="hex", head_af=None, head_h=None, nut_at=None, nut_af=None, nut_h=None, nut_rot=0.0):
    """Bolt along +Z, head underside at z=0, tip at z=L. Optional nut whose
    near face sits at z=nut_at. Simplified (no threads)."""
    b = cq.Workplane("XY").circle(d / 2).extrude(L)
    if head == "hex":
        b = b.union(_hexz(head_af, -head_h, head_h))
    else:                                   # pan / thumb head
        b = b.union(cq.Workplane("XY").workplane(offset=-head_h).circle(head_af / 2).extrude(head_h))
    if nut_at is not None:
        b = b.union(_hexz(nut_af, nut_at, nut_h, nut_rot))
    return b


M10 = dict(head_af=17, head_h=6.4)
M8 = dict(head_af=13, head_h=5.3)


PARTS = {
    "desk_clamp": desk_clamp, "clamp_knob": clamp_knob, "clamp_pad": clamp_pad,
    "stop_collar": stop_collar, "link1": link1, "link2": link2,
    "head_yoke": head_yoke, "tilt_block": tilt_block, "vesa_bracket": vesa_bracket,
    "friction_washer": friction_washer,
}


def assembly(z_link1=175.0, a1=45.0, a2=-45.0, a_head=0.0, tilt=0.0, rot=0.0, desk_t=25.0,
             with_monitor=True, with_hardware=True):
    """Return dict name -> (shape, colour). Angles in degrees, absolute headings."""
    P = {k: f() for k, f in PARTS.items()}
    out = {}
    out["desk_clamp"] = P["desk_clamp"]
    bolt_tip = -desk_t - 12 + 6
    out["clamp_pad"] = P["clamp_pad"].translate((0, 0, -desk_t - 12))
    out["clamp_knob"] = P["clamp_knob"].mirror("XY").translate((0, 0, bolt_tip - 100 + 15))
    out["pole"] = pole(pin_z=z_link1 - SLEEVE_DROP - WASHER - 22 + 11)
    out["stop_collar"] = P["stop_collar"].translate((0, 0, z_link1 - SLEEVE_DROP - WASHER - 22))
    out["link1"] = P["link1"].rotate((0, 0, 0), (0, 0, 1), a1).translate((0, 0, z_link1))
    j1 = (L1 * math.cos(math.radians(a1)), L1 * math.sin(math.radians(a1)))
    z2 = z_link1 + LINK_H + WASHER
    out["link2"] = P["link2"].rotate((0, 0, 0), (0, 0, 1), a2).translate((j1[0], j1[1], z2))
    j2 = (j1[0] + L2 * math.cos(math.radians(a2)), j1[1] + L2 * math.sin(math.radians(a2)))
    z3 = z2 - WASHER - HEAD_HUB_H      # head yoke hangs under link 2's distal hub

    def head_place(s):
        return s.rotate((0, 0, 0), (0, 0, 1), a_head).translate((j2[0], j2[1], z3))

    out["head_yoke"] = head_place(P["head_yoke"])
    # tilt: rotate about Y axis (positive = screen tips up)
    tb = P["tilt_block"].rotate((0, 0, 0), (0, 1, 0), -tilt).translate((TILT_X, 0, TILT_Z))
    out["tilt_block"] = head_place(tb)
    for k, y in (("friction_washer_L", TONGUE_W / 2), ("friction_washer_R", -TONGUE_W / 2 - WASHER)):
        fw = P["friction_washer"].rotate((0, 0, 0), (1, 0, 0), -90).translate((0, y, 0))
        out[k] = head_place(fw.rotate((0, 0, 0), (0, 1, 0), -tilt).translate((TILT_X, 0, TILT_Z)))
    vp = (P["vesa_bracket"].rotate((0, 0, 0), (1, 0, 0), rot).translate((40 + WASHER, 0, 0))
          .rotate((0, 0, 0), (0, 1, 0), -tilt).translate((TILT_X, 0, TILT_Z)))
    out["vesa_bracket"] = head_place(vp)
    if with_monitor:
        m = (monitor_dummy().rotate((0, 0, 0), (1, 0, 0), rot).translate((40 + WASHER + PLATE_T, 0, 0))
             .rotate((0, 0, 0), (0, 1, 0), -tilt).translate((TILT_X, 0, TILT_Z)))
        out["monitor"] = head_place(m)
    if with_hardware:
        out.update(hardware(z_link1, j1, z2, j2, z3, a_head, tilt, rot, bolt_tip, head_place))
    return out


def hardware(z_link1, j1, z2, j2, z3, a_head, tilt, rot, bolt_tip, head_place):
    """Store-bought bolts, nuts, washers and the cross pin, placed in the assembly.
    Names start with hw_ so they're easy to hide; none of these get printed."""
    h = {}
    # desk clamp screw: M10 x 100 fully threaded, captive nut in the lower jaw
    h["hw_clamp_bolt_M10x100"] = hw_bolt(10, 100, nut_at=-75 - (bolt_tip - 100), nut_af=17, nut_h=8, nut_rot=30,
                                         **M10).translate((0, 0, bolt_tip - 100))
    # link pivots: M10 x 120, fender washers both ends, nylock on top, PTFE washer between hubs
    def pivot(xy, z_bot, z_top, name):
        b = hw_bolt(10, 120, nut_at=(z_top + 2.5) - (z_bot - 2.5), nut_af=17, nut_h=10, **M10)
        b = b.union(_disc(38.1, 10.5, 0, 2.5))                                            # under head
        b = b.union(_disc(38.1, 10.5, z_top - (z_bot - 2.5), 2.5))                        # under nut
        return b.translate((xy[0], xy[1], z_bot - 2.5))
    h["hw_pivot1_M10x120"] = pivot(j1, z_link1, z2 + LINK_H, "p1")
    h["hw_ptfe_washer_1"] = _disc(30, 10.5, z_link1 + LINK_H, WASHER).translate((j1[0], j1[1], 0))
    h["hw_pivot2_M10x120"] = pivot(j2, z3, z2 + LINK_H, "p2")
    h["hw_ptfe_washer_2"] = _disc(30, 10.5, z3 + HEAD_HUB_H, WASHER).translate((j2[0], j2[1], 0))
    # tilt: M8 x 70 along +Y, fender washers, 3 disc springs, nylock
    ear_out = TONGUE_W / 2 + WASHER + EAR_T
    t = hw_bolt(8, 70, nut_at=(2 + 2 * ear_out + 3.75 + 2), nut_af=13, nut_h=8, **M8)
    t = t.union(_disc(38.1, 8.4, 0, 2)).union(_disc(16, 8.2, 2 + 2 * ear_out, 3.75)) \
         .union(_disc(38.1, 8.4, 2 + 2 * ear_out + 3.75, 2))
    t = t.rotate((0, 0, 0), (1, 0, 0), -90).translate((TILT_X, -ear_out - 2, TILT_Z))
    h["hw_tilt_bolt_M8x70"] = head_place(t)

    def in_tilt(shape):        # tilt-block frame -> world
        return head_place(shape.rotate((0, 0, 0), (0, 1, 0), -tilt).translate((TILT_X, 0, TILT_Z)))

    def in_bracket(shape):     # bracket frame -> world
        return in_tilt(shape.rotate((0, 0, 0), (1, 0, 0), rot).translate((40 + WASHER, 0, 0)))

    # rotation: M8 x 30, head in the bracket's round recess, captive nylock in the tilt block
    head_seat = PLATE_T - NECK_RELIEF[2] - 6                  # bracket-local x of the recess floor
    r = hw_bolt(8, 30, nut_at=(40 + WASHER + head_seat) - 28, nut_af=13, nut_h=8, nut_rot=30, **M8)
    r = r.rotate((0, 0, 0), (0, 1, 0), -90).translate((40 + WASHER + head_seat, 0, 0))
    h["hw_rotation_bolt_M8x30"] = in_tilt(r)
    h["hw_nylon_washer_M8"] = in_tilt(cq.Workplane("YZ").workplane(offset=40).circle(10).circle(4.2).extrude(WASHER))
    # rotation detent: M5 x 20 pan-head machine screw through the disc into the bracket
    dsc = hw_bolt(5, 20, head="round", head_af=9.5, head_h=3.5).rotate((0, 0, 0), (0, 1, 0), 90).translate((30, 0, 24))
    h["hw_detent_M5x20"] = in_tilt(dsc)
    # monitor screws: the stand's M4 x 12 pan heads, 5 mm grip -> 7 mm into the inserts
    for sy in (-1, 1):
        for sz in (-1, 1):
            y, z = sy * VESA / 2, sz * VESA / 2
            seat = PLATE_T + (R_BACK - math.sqrt(R_BACK**2 - y**2)) - SCREW_GRIP
            sc = hw_bolt(4, SCREW_LEN, head="round", head_af=8, head_h=3.1)
            sc = sc.rotate((0, 0, 0), (0, 1, 0), 90).translate((seat, y, z))
            h[f"hw_monitor_screw_M4x12_{'T' if sz > 0 else 'B'}{'L' if sy > 0 else 'R'}"] = in_bracket(sc)
    # set screws: M6 x 25 pan-head machine screws (self-tap), tips touching the pole
    h["hw_pole_setscrew_M6x25"] = (hw_bolt(6, 25, head="round", head_af=10, head_h=4.2)
                                   .rotate((0, 0, 0), (0, 1, 0), -90).translate((POLE_D / 2 + 0.2 + 25, 0, 60)))
    tip = (POLE_D + SLEEVE_FIT) / 2 + 0.2
    h["hw_swivel_setscrew_M6x25"] = (hw_bolt(6, 25, head="round", head_af=10, head_h=4.2)
                                     .rotate((0, 0, 0), (0, 1, 0), 90).translate((-tip - 25, 0, z_link1 - SLEEVE_DROP / 2))
                                     .rotate((0, 0, 0), (0, 0, 1), math.degrees(math.atan2(j1[1], j1[0]))))
    # stop collar: 1/4"-20 x 2-1/2" hex bolt + nut as the cross pin (pinch bolt left out)
    zc = z_link1 - SLEEVE_DROP - WASHER - 22
    pin = hw_bolt(6.35, 63.5, head_af=11.1, head_h=4.4, nut_at=2 * SLEEVE_R + 0.5, nut_af=11.1, nut_h=5.6)
    h["hw_cross_pin_bolt_1-4x2-1-2"] = pin.rotate((0, 0, 0), (1, 0, 0), -90).translate((0, -SLEEVE_R - 0.25, zc + 11))
    return h


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "stl"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "step"), exist_ok=True)
    for name, f in PARTS.items():
        s = f()
        cq.exporters.export(s, os.path.join(OUT, "stl", f"{name}.stl"), tolerance=0.05, angularTolerance=0.1)
        cq.exporters.export(s, os.path.join(OUT, "step", f"{name}.step"))
        bb = s.val().BoundingBox()
        print(f"{name:12s} vol={s.val().Volume()/1000:7.1f} cm3  bbox={bb.xlen:.0f}x{bb.ylen:.0f}x{bb.zlen:.0f}")
    asm = assembly()
    colors = {"pole": (0.75, 0.75, 0.78), "monitor": (0.12, 0.12, 0.14)}
    a = cq.Assembly(name="monitor_arm")
    for k, s in asm.items():
        c = (0.55, 0.57, 0.6) if k.startswith("hw_") else colors.get(k, (0.95, 0.45, 0.1))
        a.add(s, name=k, color=cq.Color(*c))
    a.save(os.path.join(OUT, "step", "monitor_arm_assembly.step"))
    print("assembly written")
