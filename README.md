# Monitor arm for the Sceptre C32 (C325B-185RD1)

A desk-clamped, 3D-printed monitor arm for the Sceptre C32 240 Hz curved monitor, model C325B-185RD1. It screws into the four M4 inserts on the back of the monitor and holds its 5.26 kg (11.6 lb).

The joints and links are printed in PETG. The parts under the most load are store-bought steel: a ¾" pipe for the pole, M10 bolts for the swing pivots and an M8 bolt for the tilt. All the parts come to about $66 including tax, and every one is listed with a link in the parts table below.

## What it does

| Motion | How it works | Range |
|---|---|---|
| Height | A stop collar pinned to the pole with a ¼" bolt through a drilled hole | Bottom of the screen 72 to 348 mm above the desk (the stock stand puts it at about 107 mm) |
| Swivel and reach | Two links, 230 mm and 200 mm long, on vertical M10 pivots | 0 to 546 mm from the pole to the back of the monitor, and the links fold up to 150° either way |
| Pan | The head turns on a vertical M10 pivot | 90° either way |
| Tilt | An M8 friction joint, kept tight by 3 disc springs | 10° forward to 20° back. Keep forward tilt to 5° or less |
| Rotate | An M8 centre bolt, locked by an M5 screw | 0, 90, 180 and 270°. Portrait needs the collar set high |

### How it attaches to the monitor

The C32 has no flat VESA plate. It has four M4 threaded inserts in a 100 × 100 mm square, set into the curved back of the lower housing around the slot where the stand's neck plugs in. The front face of `vesa_bracket` is curved to match the monitor's 1800R back, so it sits flat on the housing. It also has a shallow pocket over the rim of the neck slot so the rim can't hold it off. The bracket uses the same M4 × 12 pan-head screws as the stand's neck. With 5 mm of plastic under each screw head, they go 7 mm into the inserts and don't bottom out.

## Files

```
step/monitor_arm_assembly.step   the whole arm: every printed part, the pipe, every bolt, nut and
                                 washer (the grey hw_* parts) and a stand-in monitor. Opens in
                                 Fusion, Onshape, FreeCAD and SolidWorks
step/*.step                      each printed part on its own
stl/*.stl                        print-ready meshes
```

## Parts and cost

I checked these prices on October 17 and 18, 2026. Amazon prices are Prime prices. AliExpress prices change from day to day, so look at each cart total before you pay.

| # | Item | Store | Qty to buy | Used for | Price |
|---|---|---|---|---|---|
| 1 | [JAYO PETG filament, black, 1.75 mm, 1.1 kg](https://www.amazon.com/dp/B0DCZ9ZLP9) | Amazon | 1 | Printed parts | $9.99 |
| 2 | [eono PETG filament, black, 1.75 mm, 1 kg](https://www.amazon.com/dp/B0G2BQQ5RT) (limit 1 per customer) | Amazon | 1 | Printed parts | $9.99 |
| 3 | [¾" × 1.5 ft black steel pipe, schedule 40](https://www.homedepot.com/p/VPC-3-4-in-x-1-5-ft-Black-Steel-Schedule-40-Cut-Pipe-21-707518/304751767) | Home Depot | 1 | Pole (comes cut to length) | $8.74 |
| 4 | [¼"-20 × 2½" hex bolt](https://www.homedepot.com/p/Everbilt-1-4-in-20-x-2-1-2-in-Zinc-Plated-Hex-Bolt-800626/204633263) | Home Depot | 1 | Pin through the collar and pole | $0.39 |
| 5 | [¼"-20 hex nut](https://www.homedepot.com/p/Everbilt-1-4-in-20-Zinc-Plated-Hex-Nut-801736/204647886) | Home Depot | 1 | Nut for the pin | $0.14 |
| 6 | [M5 × 20 mm pan-head screws, 4-pack](https://www.homedepot.com/p/Everbilt-M5-0-8-x-20mm-Zinc-Pan-Head-Phillips-Drive-Machine-Screw-4-Pieces-836541/321071579) | Home Depot | 1 pack | Rotation lock | $1.95 |
| 7 | [M6 × 25 mm pan-head screws, 4-pack](https://www.homedepot.com/p/Everbilt-M6-1-0-x-25mm-Zinc-Pan-Head-Phillips-Drive-Machine-Screw-4-Pieces-836721/321071584) | Home Depot | 1 pack | Pole lock and swing stiffness | $1.95 |
| 8 | [⅜" × 1½" fender washer](https://www.homedepot.com/p/Everbilt-3-8-in-x-1-1-2-in-Zinc-Plated-Fender-Washer-804816/204632769) | Home Depot | 4 | Both M10 pivots | $1.40 |
| 9 | [5/16" × 1½" fender washer](https://www.homedepot.com/p/Everbilt-5-16-in-x-1-1-2-in-Zinc-Plated-Fender-Washer-804806/204632770) | Home Depot | 2 | M8 tilt bolt | $0.58 |
| 10 | [Disc springs, 16 × 8.2 × 0.9 mm, 12 pcs](https://www.aliexpress.us/item/3256806536117647.html) (option "16x8.2x0.9 Silver") | AliExpress | 1 pack | Tilt tension (uses 3) | $1.09 |
| 11 | [M4 × 12 mm pan-head screws, 10 pcs](https://www.aliexpress.us/item/3256807033160325.html) (option "12mm/M4 x 10Pcs") | AliExpress | 1 pack | Monitor screws (2 here plus the stand's 2) | $1.42 |
| 12 | [M8 nylon lock nuts, 20 pcs](https://www.aliexpress.us/item/3256806985000344.html) (option "M8-20pcs") | AliExpress | 1 pack | Tilt and rotation bolts | $2.92 |
| 13 | [M10 nylon lock nuts, 20 pcs](https://www.aliexpress.us/item/3256806985000344.html) (option "M10-20pcs") | AliExpress | 1 pack | Both pivots and the clamp nut | $4.25 |
| 14 | [M8 × 30 mm hex bolts, 5 pcs](https://www.aliexpress.us/item/3256805904265069.html) (option "M8 5pcs/30mm") | AliExpress | 1 pack | Rotation bolt | $2.81 |
| 15 | [M8 × 70 mm hex bolts, 5 pcs](https://www.aliexpress.us/item/3256805904265069.html) (option "M8 5pcs/70mm") | AliExpress | 1 pack | Tilt bolt | $4.05 |
| 16 | [M10 × 100 mm hex bolts, fully threaded, 2 pcs](https://www.aliexpress.us/item/3256805904265069.html) (option "M10 2PCS/100mm") | AliExpress | 1 pack | Desk clamp screw | $3.92 |
| 17 | [M10 × 120 mm hex bolts, 2 pcs](https://www.aliexpress.us/item/3256812494224390.html) (option "M10 2pcs/120mm") | AliExpress | 1 pack | Both swing pivots | $4.82 |
| | Subtotal | | | | $60.41 |
| | Shipping (free on AliExpress, free with Prime, free store pickup at Home Depot) | | | | $0.00 |
| | Sales tax (estimated at Santa Clara's 9.75%) | | | | $5.89 |
| | Total | | | | $66.30 |

You don't need to buy:

- 2 of the M4 × 12 screws. They come off the monitor's own stand.
- Rubber. Cut it from an old bike inner tube for the clamp pad, the desk side of the clamp and the two tilt friction washers, or print `friction_washer` in TPU.
- The three thin washers between the pivots. Print them in PETG (`pivot_washer_M10` ×2, `rotation_washer_M8` ×1).
- A drill bit, if you can borrow a 6.5 mm (¼") one. It drills one hole.

Tools: a 3D printer, a drill with a 6.5 mm (¼") bit, a centre punch, 17 mm and 13 mm wrenches or sockets, a 7/16" wrench and a Phillips screwdriver.

## Printing

Print in PETG at 0.2 mm layers with no supports. PLA slowly bends under a constant load, so don't use it for anything that holds weight. The parts take about 1.35 kg of plastic, which is why you need both spools. Print each part from a single spool so none come out two-toned.

| Part | Qty | Walls | Infill | How it sits on the bed |
|---|---|---|---|---|
| desk_clamp | 1 | 8 | 40% | On its side, with the flat C-shaped face down |
| link1 | 1 | 6, with 8 top and bottom layers | 15% | Upside down, flat top on the bed. It's 276 mm long, so it goes corner to corner on a 235 mm bed |
| link2 | 1 | 6, with 8 top and bottom layers | 15% | Flat |
| head_yoke | 1 | 6 | 20% | Flat bottom down |
| tilt_block | 1 | 6 | 20% | Round disc face down |
| vesa_bracket | 1 | 6 | 15% | Flat back down, curved face up |
| clamp_knob | 1 | 6 | 15% | Flat, hex pocket up |
| clamp_pad | 1 | 6 | 15% | Flat |
| stop_collar | 1 | 4 | 15% | Flat |
| pivot_washer_M10 | 2 | | 100% | Flat |
| rotation_washer_M8 | 1 | | 100% | Flat |
| friction_washer | 2 | | 100% | Flat, in TPU, or cut them from inner tube |

## Assembly

1. Desk clamp:
   1. Press an M10 lock nut into the pocket in the lower jaw. It sticks out about 1 mm, which is fine.
   2. Thread the M10 × 100 bolt up through it from below. Glue `clamp_knob` onto the bolt head with a drop of epoxy and fit `clamp_pad` on the end.
   3. Glue a strip of inner tube under the top jaw and on the pad.
   4. Clamp it to the desk with the pole socket about 45 mm in from the back edge, and tighten it hard.
2. Pole: push the pipe all the way into the socket. Turn one M6 × 25 screw into the hole on the front of the clamp until it touches the pipe. It cuts its own thread in the plastic.
3. Height:
   1. Slide `stop_collar` onto the pipe at the height you want.
   2. Mark the pipe through the hole in the side of the collar, then take the collar off.
   3. Centre-punch the mark and drill a 6.5 mm (¼") hole straight through the pipe.
   4. Put the collar back, push the ¼" × 2½" bolt through the collar and pipe, and add the nut.
4. Link 1: slide it down the pipe until it rests on the collar. Turn the second M6 × 25 into the small hole in its sleeve. The tighter it is, the stiffer the arm swings.
5. Link 2 sits on top of the far end of link 1, with a printed `pivot_washer_M10` between them. Put an M10 × 120 through both with a 1½" fender washer under the bolt head and another under the M10 lock nut. Tighten until it swings with firm drag.
6. The head (`head_yoke`) hangs under the far end of link 2 the same way: a `pivot_washer_M10` between them, the second M10 × 120, fender washers at both ends and a lock nut.
7. Tilt: the tongue on `tilt_block` fits between the two ears of the yoke. Put the M8 × 70 through in this order:
   - bolt head
   - 5/16" fender washer
   - ear
   - rubber washer
   - tongue
   - rubber washer
   - ear
   - 3 disc springs, each one flipped the opposite way to the last
   - 5/16" fender washer
   - M8 lock nut

   Tighten it until the monitor stays put when tilted 5° forward.
8. Monitor:
   1. Lay the screen face down on something soft. Unscrew the stand's neck (2 screws) and keep the screws.
   2. Before the bracket goes on the monitor, put the M8 × 30 through the round recess in `vesa_bracket`, add `rotation_washer_M8`, and screw the bolt into the M8 lock nut held in `tilt_block`.
   3. Put the M5 × 20 through the locking hole. It holds the monitor at 0, 90, 180 or 270°.
   4. Screw the bracket to the monitor's four inserts with four M4 × 12 screws: the stand's 2 and 2 new ones. Don't add washers. If a screw stops before its head is down, it has hit the bottom of the insert, so stop turning.
9. Load test: leave the monitor on the arm at full reach for 24 hours with nothing underneath it, then tighten every nut once more. PETG settles a little at first.

## Checks

I checked the model in 18 positions, covering full folds, full pan, full tilt, portrait, and 10 mm and 50 mm desks. No parts hit each other, including every bolt, nut and washer.

The M4 holes are exactly 100 × 100 mm apart. Pressed 0.3 mm into the housing, the curved bracket overlaps about 99% of the area it covers. A flat plate would overlap less than half.

At full reach the monitor puts a 32 N·m tipping moment on the arm. Hand calculations put the steel pole at about a ninth of its yield strength and the root of link 1 at about 3 MPa. The arm should droop about 15 mm at full reach. These are hand calculations, not a simulation, so do the 24-hour load test before you leave the monitor on it unattended.
