# openscad-batch-exporter

Export multiple STL files from OpenSCAD based on a CSV file.

## How to use

### 1. Prepare a CSV file

First row will be used as variables name in OpenSCAD command, rest as parameters to be used for generation. For example:

```csv
material,materialBrand,materialType,materialColor
PETG,Sunlu,HS Matte,BLACK
PLA,Sunlu,HS,WHITE
PLA,Sunlu,HS,RED
```

### 2. Prepare your .scad file

Put it somewhere accessible for this script.

### 3. Run this script

Pass path to .csv file and path to .scad file as arguments:

```bash
python app.py list.csv model.scad
```

For CSV example provided in point 1, following commands will be executed:

```bash
openscad --export-format binstl -o "output/PETG_Sunlu_HS Matte_BLACK.stl" -D material="PETG" -D materialBrand="Sunlu" -D "materialType="HS Matte"" -D materialColor="BLACK" model.scad
openscad --export-format binstl -o output/PLA_Sunlu_HS_WHITE.stl -D material="PLA" -D materialBrand="Sunlu" -D materialType="HS" -D materialColor="WHITE" model.scad
openscad --export-format binstl -o output/PLA_Sunlu_HS_RED.stl -D material="PLA" -D materialBrand="Sunlu" -D materialType="HS" -D materialColor="RED" model.scad
```

Generated models will appear in `output` directory.

## Concurrency

This script will run `openscad` commands in parallel to reduce execution time. You can control how many processes can be run at once by changing value of `NUMBER_OF_PARALLEL_RENDERS` variable in `app.py`. 4 is a reasonable default.
