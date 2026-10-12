# Reubica el STEP del NodeMCU-32S al sistema de KiCad: pad 1 (3V3) en el origen, antena hacia +Y, Z=0 = PCB anfitrión.
# X_k = Z_s + 11.23 ; Y_k = X_s - 26.33 ; Z_k = Y_s + 3.75  (rotación propia, no espeja)
import re, sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='latin-1', newline='').read()
rep = re.search(r"=ADVANCED_BREP_SHAPE_REPRESENTATION\('[^']*',\(([^)]*)\)", t).group(1)
keep = set()
for i in (x.strip() for x in rep.split(',')):
    m = re.search(r"(?m)^" + re.escape(i) + r"=AXIS2_PLACEMENT_3D\('[^']*',([^;]*)\);", t)
    if m: keep |= {x.strip() for x in m.group(1).split(',')}
num = r'\s*([-+0-9.eE]+)\s*'
def fmt(v):
    v = round(v, 9); s = repr(float(v)); return f"{v:.9E}" if ('e' in s or 'E' in s) else s
def sub(kind):
    def f(m):
        if m.group(1) in keep: return m.group(0)
        x, y, z = map(float, m.group(3, 4, 5))
        v = (z + 11.23, x - 26.33, y + 3.75) if kind == 'p' else (z, x, y)
        return f"{m.group(1)}{m.group(2)}({','.join(fmt(a) for a in v)}))"
    return f
for kind, name in (('p', 'CARTESIAN_POINT'), ('d', 'DIRECTION')):
    t = re.sub(r"(?m)^(#\d+)(=" + name + r"\s*\(\s*'[^']*'\s*,\s*)\(" + num + "," + num + "," + num + r"\)\s*\)", sub(kind), t)
t = t.replace("PRODUCT('ESP32Wroom','ESP32Wroom'", "PRODUCT('NodeMCU-32S','NodeMCU-32S'")
open(dst, 'w', encoding='latin-1', newline='').write(t)
print('keep', keep)
