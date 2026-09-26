# kikad_stuff — Librería KiCad Sector7GP

Símbolos, footprints y modelos 3D propios/adaptados para KiCad (probado con KiCad 10).
Cada componente usa **el mismo nombre base** en los tres tipos (símbolo ↔ footprint ↔ modelo 3D).

## Estructura

```
symbols/Sector7GP.kicad_sym              # librería de símbolos
footprints/Sector7GP.pretty/             # librería de footprints
3dmodels/Sector7GP.3dshapes/             # modelos 3D (.step / .wrl)
docs/                                    # imágenes de referencia y catálogo SMD
cad_sources/                             # fuentes CAD (SolidWorks, FreeCAD, Fusion, STL, IGES, scripts)
```

## Instalación

1. Clonar el repo.
2. En KiCad → *Preferencias → Configurar rutas*, crear la variable
   `S7GP_KICAD_LIB` apuntando a la carpeta raíz del repo.
3. *Preferencias → Administrar librerías de símbolos* → agregar
   `Sector7GP` = `${S7GP_KICAD_LIB}/symbols/Sector7GP.kicad_sym`
4. *Preferencias → Administrar librerías de footprints* → agregar
   `Sector7GP` = `${S7GP_KICAD_LIB}/footprints/Sector7GP.pretty`

Los footprints referencian los modelos como
`${S7GP_KICAD_LIB}/3dmodels/Sector7GP.3dshapes/<nombre>.step`, y los símbolos
apuntan a `Sector7GP:<footprint>`.

## Componentes

| Nombre | Símbolo | Footprint | Modelo 3D |
|---|:-:|:-:|---|
| DFPlayer_Mini_DFR0299 | ✔ | ✔ | DFPlayer_Mini_DFR0299.step |
| DFPlayer_Pro_DFR0768 | ✔ | ✔ | DFPlayer_Pro_DFR0768.step |
| ESP32-S3-DevKitC-1_Narrow_Breadboard | ✔ | ✔ | YD-ESP32-S3.step (+ ESP32-S3-DevKitC-1_N8R8.step alternativo) |
| YD-ESP32-S3 | ✔ | ✔ | YD-ESP32-S3.step |
| LM2596S_StepDown_Module | ✔ | ✔ | LM2596S_StepDown_Module.step |
| SW_MINI-SPDT-SW | ✔ | ✔ | SW_MINI-SPDT-SW.step (no asignado en el footprint) |
| HC-SR501 (PIR, 3 pines) | – | ✔ | HC-SR501_Lens.step + HC-SR501_Sensor.step (+ SensorBoard.step, .wrl) |
| HC-SR501_6Pin | – | ✔ | – |
| PIR_Motion_Sensor_3Pin | – | ✔ | ref. legacy a Pin_Headers.3dshapes |
| SW_E-Switch_EG2211A | – | ✔ | SW_E-Switch_EG2211A.step (+ _alt) |
| Battery_Nokia_BL-5C | – | ✔ | Battery_Nokia_BL-5C.step (no asignado) |
| TP4056-18650 | – | ✔ | TP4056-18650.step (no asignado) |
| LED_Strip_WS2811_3Pin_P2.54mm | – | ✔ | – |
| LED_Strip_WS2812B_3Pin_P2.0mm | – | ✔ | – |
| ESP8266_ESP-01 | – | – | ESP8266_ESP-01.step, ESP8266_ESP-01_cp.step/.wrl |
| Reed_Switch | – | – | Reed_Switch.step |
| RJ45_8P8C_Shielded_NoLED_THT | – | – | RJ45_8P8C_Shielded_NoLED_THT.step (generado con `cad_sources/RJ45_8P8C/rj45_step_generator.py`) |
| SW_APEM_MSHS1105_SPDT | – | – | SW_APEM_MSHS1105_SPDT.step |

## Notas

- El símbolo `SW_MINI-SPDT-SW` fue convertido desde la librería legacy SnapEDA
  (`cad_sources/SW_MINI-SPDT-SW/MINI-SPDT-SW_legacy.lib`, CC BY-SA 4.0).
- Algunos modelos 3D provienen de terceros (GrabCAD, SnapEDA, fabricantes); respetar sus licencias.
