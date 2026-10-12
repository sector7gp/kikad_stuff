# Genera símbolo, footprint y modelo 3D (STEP) del NodeMCU-32S (Ai-Thinker, ESP32-WROOM-32, 38 pines)
# Medidas tomadas de foto + spec NodeMCU-32S: placa 25.4 x 48.26 mm, filas a 22.86 mm (0.9"), paso 2.54 mm.
# Origen = pad 1 (3V3), vista superior, antena hacia arriba. Uso: python3 nodemcu32s_gen.py <dir_salida>
import sys, os, uuid
import cadquery as cq

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
NAME = 'NodeMCU-32S'
P = 2.54; N = 19; ROW = 22.86          # paso, pines por lado, separación entre filas
BW, BL = 25.4, 48.26                   # placa
X0 = ROW/2 - BW/2; Y0 = -(BL - (N-1)*P)/2  # esquina sup-izq (coord footprint, Y hacia abajo)
STANDOFF = 2.5                         # plástico del header macho (soldado directo)
LEFT = ['3V3','EN','SVP','SVN','IO34','IO35','IO32','IO33','IO25','IO26','IO27','IO14','IO12','GND','IO13','SD2','SD3','CMD','5V']
RIGHT = ['GND','IO23','IO22','TX','RX','IO21','GND','IO19','IO18','IO5','IO17','IO16','IO4','IO0','IO2','IO15','SD1','SD0','CLK']  # de arriba a abajo
# numeración tipo DIP: 1-19 izquierda hacia abajo, 20-38 derecha hacia arriba
pins = [(i+1, LEFT[i], 0.0, i*P) for i in range(N)] + [(20+k, RIGHT[N-1-k], ROW, (N-1-k)*P) for k in range(N)]
U = lambda: str(uuid.uuid4())

def etype(n):
    if n in ('3V3','5V','GND'): return 'power_in'
    if n in ('EN','SVP','SVN','IO34','IO35','RX'): return 'input'
    if n == 'TX': return 'output'
    return 'bidirectional'

# ---------------- footprint ----------------
def line(layer, x1, y1, x2, y2, w):
    return f'\t(fp_line (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (stroke (width {w}) (type solid)) (layer "{layer}") (uuid "{U()}"))\n'
def rect(layer, x1, y1, x2, y2, w):
    return f'\t(fp_rect (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (stroke (width {w}) (type solid)) (fill no) (layer "{layer}") (uuid "{U()}"))\n'
def text(layer, s, x, y, size=1.0, kind='user', rot=0, just=''):
    th = round(size*0.15, 3)
    j = f' (justify {just})' if just else ''
    return f'\t(fp_text {kind} "{s}" (at {x:.3f} {y:.3f} {rot}) (layer "{layer}") (uuid "{U()}") (effects (font (size {size} {size}) (thickness {th})){j}))\n'

x1, y1, x2, y2 = X0, Y0, X0+BW, Y0+BL
fp = f'''(footprint "{NAME}"
\t(version 20240108)
\t(generator "s7gp_gen")
\t(layer "F.Cu")
\t(descr "NodeMCU-32S (Ai-Thinker) ESP32-WROOM-32, 38 pines THT, 2x19, paso 2.54mm, filas a 22.86mm, placa 25.4x48.26mm. Pad 1 = 3V3 (lado antena). Antena arriba: no poner cobre debajo.")
\t(tags "ESP32 NodeMCU-32S ESP-32S WROOM-32 DevKit 38pin")
\t(property "Reference" "U**" (at {ROW/2:.3f} {y1-1.5:.3f} 0) (layer "F.SilkS") (uuid "{U()}") (effects (font (size 1 1) (thickness 0.15))))
\t(property "Value" "{NAME}" (at {ROW/2:.3f} {y2+1.5:.3f} 0) (layer "F.Fab") (uuid "{U()}") (effects (font (size 1 1) (thickness 0.15))))
\t(property "Datasheet" "https://docs.ai-thinker.com/_media/esp32/docs/nodemcu-32s_product_specification.pdf" (at 0 0 0) (layer "F.Fab") (hide yes) (uuid "{U()}") (effects (font (size 1.27 1.27))))
\t(property "Description" "Modulo NodeMCU-32S / ESP-32S (ESP32-WROOM-32) 38 pines" (at 0 0 0) (layer "F.Fab") (hide yes) (uuid "{U()}") (effects (font (size 1.27 1.27))))
\t(attr through_hole)
'''
fp += rect('F.SilkS', x1-0.11, y1-0.11, x2+0.11, y2+0.11, 0.12)
fp += line('F.SilkS', x1-0.6, -1.0, x1-0.6, 1.0, 0.12)   # marca pin 1
fp += rect('F.Fab', x1, y1, x2, y2, 0.1)
fp += rect('F.CrtYd', x1-0.5, y1-0.5, x2+0.5, y2+0.5, 0.05)
# zona de antena (WROOM-32: ~6.5mm desde el borde)
ax1, ax2, ay2 = ROW/2-9, ROW/2+9, y1+6.5
fp += rect('Dwgs.User', ax1, y1, ax2, ay2, 0.1)
fp += text('Dwgs.User', 'ANTENA - sin cobre debajo', ROW/2, (y1+ay2)/2, 0.8)
fp += rect('F.Fab', ROW/2-3.75, y2-5, ROW/2+3.75, y2+0.6, 0.1)
fp += text('F.Fab', 'USB', ROW/2, y2-2.5, 0.8)
fp += text('F.Fab', '${REFERENCE}', ROW/2, BL/2, 1.0)
for num, nm, x, y in pins:
    shape = 'rect' if num == 1 else 'circle'
    fp += f'\t(pad "{num}" thru_hole {shape} (at {x:.3f} {y:.3f}) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (pinfunction "{nm}") (pintype "{etype(nm)}") (uuid "{U()}"))\n'
    fp += text('F.Fab', nm, x + (1.2 if x == 0 else -1.2), y, 0.6, just=('left' if x == 0 else 'right'))
fp += f'''\t(model "${{S7GP_KICAD_LIB}}/3dmodels/Sector7GP.3dshapes/{NAME}.step"
\t\t(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0))
\t)
)
'''
open(os.path.join(OUT, f'{NAME}.kicad_mod'), 'w').write(fp)

# ---------------- símbolo ----------------
H = (N-1)*P/2
sx = 15.24
s = f'''\t(symbol "{NAME}"
\t\t(pin_names (offset 1.016))
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes)
\t\t(property "Reference" "U" (at 0 {H+5.08:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{NAME}" (at 0 {-H-5.08:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Sector7GP:{NAME}" (at 0 {-H-7.62:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t(property "Datasheet" "https://docs.ai-thinker.com/_media/esp32/docs/nodemcu-32s_product_specification.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t(property "Description" "NodeMCU-32S / ESP-32S (Ai-Thinker), ESP32-WROOM-32, 38 pines, filas a 22.86mm" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t(property "ki_keywords" "ESP32 NodeMCU WROOM DevKit WiFi Bluetooth" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t(symbol "{NAME}_0_1"
\t\t\t(rectangle (start {-sx+2.54:.2f} {H+2.54:.2f}) (end {sx-2.54:.2f} {-H-2.54:.2f}) (stroke (width 0.254) (type default)) (fill (type background)))
\t\t)
\t\t(symbol "{NAME}_1_1"
'''
for num, nm, x, y in pins:
    ys = H - y
    if x == 0: px, ang = -sx, 0
    else: px, ang = sx, 180
    s += f'\t\t\t(pin {etype(nm)} line (at {px:.2f} {ys:.2f} {ang}) (length 2.54) (name "{nm}" (effects (font (size 1.27 1.27)))) (number "{num}" (effects (font (size 1.27 1.27)))))\n'
s += '\t\t)\n\t)\n'
open(os.path.join(OUT, f'{NAME}.kicad_sym_fragment'), 'w').write(s)

# ---------------- modelo 3D ----------------
# coordenadas del modelo: X derecha, Y hacia arriba (Y_modelo = -Y_footprint), Z hacia arriba, Z=0 = superficie del PCB anfitrión
def box(w, d, h, cx, cy_fp, z0):
    return cq.Workplane('XY').box(w, d, h, centered=(True, True, False)).translate((cx, -cy_fp, z0))
zb = STANDOFF; tb = 1.6; zt = zb + tb
asm = cq.Assembly(name=NAME)
asm.add(box(BW, BL, tb, ROW/2, Y0+BL/2, zb), name='pcb', color=cq.Color(0.08, 0.08, 0.08))
hdr = None; pinsolid = None
for col in (0.0, ROW):
    h = box(2.54, N*P, STANDOFF, col, (N-1)*P/2, 0)
    hdr = h if hdr is None else hdr.union(h)
    for k in range(N):
        p = box(0.64, 0.64, 3.0 + STANDOFF + tb + 1.0, col, k*P, -3.0)
        pinsolid = p if pinsolid is None else pinsolid.union(p)
asm.add(hdr, name='header', color=cq.Color(0.1, 0.1, 0.1))
asm.add(pinsolid, name='pins', color=cq.Color(0.85, 0.75, 0.35))
# ESP32-WROOM-32 (18 x 25.5 x 0.8 + blindaje 16.6 x 17.6 x 2.3), a ras del borde de antena
my1 = Y0; mcy = my1 + 25.5/2
asm.add(box(18, 25.5, 0.8, ROW/2, mcy, zt), name='wroom_pcb', color=cq.Color(0.1, 0.1, 0.12))
asm.add(box(16.6, 17.6, 2.3, ROW/2, my1 + 25.5 - 0.7 - 17.6/2, zt + 0.8), name='wroom_shield', color=cq.Color(0.78, 0.78, 0.8))
# micro USB, botones, CP2102, AMS1117
ye = Y0 + BL
asm.add(box(7.5, 5.0, 2.6, ROW/2, ye - 2.5 + 0.6, zt), name='usb', color=cq.Color(0.8, 0.8, 0.82))
for bx in (ROW/2 - 6.6, ROW/2 + 6.6):
    asm.add(box(3.4, 4.2, 1.4, bx, ye - 3.0, zt), name=f'btn_body_{bx:.0f}', color=cq.Color(0.85, 0.85, 0.85))
    asm.add(cq.Workplane('XY').circle(0.7).extrude(0.6).translate((bx, -(ye - 3.0), zt + 1.4)), name=f'btn_cap_{bx:.0f}', color=cq.Color(0.1, 0.1, 0.1))
asm.add(box(5, 5, 0.9, ROW/2 + 0.3, ye - 10.5, zt), name='cp2102', color=cq.Color(0.15, 0.15, 0.15))
asm.add(box(3.5, 6.5, 1.6, ROW/2 - 3.5, ye - 16.5, zt), name='ams1117', color=cq.Color(0.15, 0.15, 0.15))
asm.export(os.path.join(OUT, f'{NAME}.step'))
print('ok')
