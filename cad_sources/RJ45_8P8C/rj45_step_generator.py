# RJ45 8P8C blindado, sin LED, THT, montaje horizontal — modelo parametrico
# Origen: pin 1, Z=0 en la superficie del PCB, eje -Y hacia el frente (boca del conector)
import cadquery as cq

W, D, H = 15.9, 18.8, 13.5      # ancho, profundidad, altura sobre PCB (mm)
PITCH, ROW = 1.27, 2.54         # paso entre pines consecutivos, separacion entre filas
REAR_A, REAR_B = 1.0, 3.54      # distancia del borde trasero a cada fila de pines
PEG_X, PEG_Y, PEG_D, PEG_L = 11.43, 10.4, 3.2, 3.2
TABS_Y = (4.7, 13.2)            # patas de blindaje, medidas desde el borde trasero
PIN_L, T = 3.2, 0.25            # largo de pin bajo PCB, espesor de chapa

# sistema centrado: x=0 centro del cuerpo, y=0 borde trasero, frente en y=-D
x_pin = [(-3.5 + i) * PITCH for i in range(8)]   # 8 pines, 1..8
y_pin = [-(REAR_A if i % 2 == 0 else REAR_B) for i in range(8)]

# carcasa metalica
shell = cq.Workplane("XY").box(W, D, H, centered=(True, False, False)).translate((0, -D, 0))
# cuerpo plastico interior visible por la boca
housing = cq.Workplane("XY").box(W - 2*T, D - T, H - 2*T, centered=(True, False, False)).translate((0, -D + T, T))
# boca RJ45 (11.7 x 7.0 aprox) + ranura del latch
mouth = (cq.Workplane("XZ").workplane(offset=D)
         .center(0, 1.6 + 7.0/2).rect(11.7, 7.0).extrude(-12.0))
latch = (cq.Workplane("XZ").workplane(offset=D)
         .center(0, 1.6 + 7.0 + 1.2).rect(6.2, 2.4).extrude(-12.0))
cavity = mouth.union(latch)
shell = shell.cut(cq.Workplane("XY").box(W - 2*T, D - T, H - 2*T, centered=(True, False, False)).translate((0, -D + T, T)))
housing = housing.cut(cavity)
shell = shell.cut(cavity.translate((0, 0, 0)))

# contactos dorados dentro de la boca
contacts = cq.Workplane("XY")
for i in range(8):
    c = cq.Workplane("XY").box(0.35, 6.0, 0.35).translate(((-3.5 + i)*1.02, -D + 5.0, 1.6 + 0.4))
    contacts = contacts.union(c)

# pines THT
pins = cq.Workplane("XY")
for x, y in zip(x_pin, y_pin):
    pins = pins.union(cq.Workplane("XY").box(0.5, 0.5, PIN_L + 1.0).translate((x, y, -PIN_L/2 + 0.5)))

# postes plasticos de fijacion (partidos)
pegs = cq.Workplane("XY")
for sx in (-1, 1):
    p = cq.Workplane("XY").circle(PEG_D/2).extrude(-PEG_L).translate((sx*PEG_X/2, -PEG_Y, 0))
    p = p.cut(cq.Workplane("XY").box(0.6, PEG_D + 1, PEG_L*0.8, centered=(True, True, False))
              .translate((sx*PEG_X/2, -PEG_Y, -PEG_L)))
    pegs = pegs.union(p)

# patas de blindaje
tabs = cq.Workplane("XY")
for ty in TABS_Y:
    for sx in (-1, 1):
        tabs = tabs.union(cq.Workplane("XY").box(T*2, 1.2, 3.0).translate((sx*(W/2 - T), -ty, -1.2)))

# re-origen al pin 1
off = (-x_pin[0], -y_pin[0], 0)
asm = cq.Assembly(name="RJ45_8P8C_Shielded_NoLED")
asm.add(shell.translate(off), name="shell", color=cq.Color(0.78, 0.78, 0.80))
asm.add(housing.translate(off), name="housing", color=cq.Color(0.08, 0.08, 0.08))
asm.add(pegs.translate(off), name="pegs", color=cq.Color(0.08, 0.08, 0.08))
asm.add(contacts.translate(off), name="contacts", color=cq.Color(0.85, 0.65, 0.13))
asm.add(pins.translate(off), name="pins", color=cq.Color(0.85, 0.65, 0.13))
asm.add(tabs.translate(off), name="tabs", color=cq.Color(0.78, 0.78, 0.80))
asm.save("/mnt/user-data/outputs/RJ45_8P8C_Shielded_NoLED_THT.step")
bb = asm.toCompound().BoundingBox()
print(round(bb.xlen,2), round(bb.ylen,2), round(bb.zlen,2))
cq.exporters.export(asm.toCompound(), "iso.svg", opt={"projectionDir": (1.2, -1.5, 1), "width": 600, "height": 500, "showHidden": False})
cq.exporters.export(asm.toCompound(), "bot.svg", opt={"projectionDir": (0, 0, -1), "width": 500, "height": 500, "showHidden": False})
