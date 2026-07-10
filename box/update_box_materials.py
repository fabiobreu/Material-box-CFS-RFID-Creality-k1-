import copy
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
option_paths = [ROOT / 'material_option.json', ROOT / 'material_options.json']
db_path = ROOT / 'material_database.json'
backup_dir = ROOT / 'backup'
backup_dir.mkdir(exist_ok=True)

def load_json(path):
    with path.open(encoding='utf-8') as f:
        return json.load(f)

existing_options = load_json(ROOT / 'material_option.json')

if not isinstance(existing_options, dict) or any(not isinstance(v, dict) for v in existing_options.values()):
    print('Aviso: material_option.json não está no formato esperado de {marca: {tipo: nome}}.')

for brand in ['eSUN', '3DFila']:
    existing_options.setdefault(brand, {})
    for material_type in ['PLA', 'PETG', 'ABS', 'TPU']:
        existing_options[brand][material_type] = f'{brand} {material_type}'

for path in option_paths:
    backup_path = backup_dir / f'{path.name}.{int(time.time())}.bak'
    path.rename(backup_path)
    path.write_text(json.dumps(existing_options, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Backup salvo: {backup_path.name}')

with db_path.open(encoding='utf-8') as f:
    db = json.load(f)

entries = db['result']['list']
profiles = {
    'PLA': {'min_temp': 190, 'max_temp': 220, 'nozzle_temp': 220, 'initial_temp': 220, 'inherits': 'Hyper PLA @Creality K1 0.4 nozzle', 'flow_ratio': '0.95', 'density': '1.24', 'cost': '30'},
    'PETG': {'min_temp': 220, 'max_temp': 250, 'nozzle_temp': 240, 'initial_temp': 240, 'inherits': 'Hyper PETG @Creality K1 0.4 nozzle', 'flow_ratio': '0.96', 'density': '1.27', 'cost': '32'},
    'ABS': {'min_temp': 240, 'max_temp': 280, 'nozzle_temp': 250, 'initial_temp': 250, 'inherits': 'Hyper ABS @Creality K1 0.4 nozzle', 'flow_ratio': '0.97', 'density': '1.04', 'cost': '34'},
    'TPU': {'min_temp': 200, 'max_temp': 240, 'nozzle_temp': 220, 'initial_temp': 220, 'inherits': 'CR-TPU @Creality K1 0.4 nozzle', 'flow_ratio': '0.98', 'density': '1.22', 'cost': '36'},
}

used_ids = {entry['base']['id'] for entry in entries if 'base' in entry and 'id' in entry['base']}
existing_custom = [int(x[2:]) for x in used_ids if isinstance(x, str) and x.startswith('90') and len(x) == 5]
next_num = max(existing_custom, default=0) + 1
if next_num < 1:
    next_num = 1


def find_template(material_type):
    for candidate in entries:
        if candidate.get('base', {}).get('meterialType') == material_type:
            return candidate
        if candidate.get('kvParam', {}).get('filament_type') == material_type:
            return candidate
    return entries[0] if entries else None

for brand in ['eSUN', '3DFila']:
    for material_type in ['PLA', 'PETG', 'ABS', 'TPU']:
        label = f'{brand} {material_type}'
        if any(entry.get('base', {}).get('name') == label for entry in entries):
            continue

        entry_id = f'90{next_num:03d}'
        while entry_id in used_ids:
            next_num += 1
            entry_id = f'90{next_num:03d}'
        used_ids.add(entry_id)
        next_num += 1

        template = find_template(material_type)
        if template is None:
            raise SystemExit('Nenhum template válido encontrado para o material.')

        template_entry = copy.deepcopy(template)
        template_entry['kvParam'] = copy.deepcopy(template.get('kvParam', {}))
        template_entry['kvParam']['filament_type'] = material_type
        template_entry['kvParam']['filament_vendor'] = brand
        template_entry['kvParam']['inherits'] = profiles[material_type]['inherits']
        template_entry['kvParam']['nozzle_temperature'] = str(profiles[material_type]['nozzle_temp'])
        template_entry['kvParam']['nozzle_temperature_initial_layer'] = str(profiles[material_type]['initial_temp'])
        template_entry['kvParam']['nozzle_temperature_range_low'] = str(profiles[material_type]['min_temp'])
        template_entry['kvParam']['nozzle_temperature_range_high'] = str(profiles[material_type]['max_temp'])
        template_entry['kvParam']['filament_density'] = profiles[material_type]['density']
        template_entry['kvParam']['filament_flow_ratio'] = profiles[material_type]['flow_ratio']
        template_entry['kvParam']['filament_cost'] = profiles[material_type]['cost']
        template_entry['kvParam']['material_flow_temp_graph'] = f'[[0.8,{profiles[material_type]["min_temp"]}], [1.0,{profiles[material_type]["nozzle_temp"]}], [1.3,{profiles[material_type]["max_temp"]}]]'
        template_entry['base'] = copy.deepcopy(template.get('base', {}))
        template_entry['base']['id'] = entry_id
        template_entry['base']['brand'] = brand
        template_entry['base']['name'] = label
        template_entry['base']['meterialType'] = material_type
        template_entry['base']['minTemp'] = profiles[material_type]['min_temp']
        template_entry['base']['maxTemp'] = profiles[material_type]['max_temp']
        entries.append(template_entry)

for entry in entries:
    if 'kvParam' in entry:
        for key, value in list(entry['kvParam'].items()):
            if isinstance(value, (int, float, bool)):
                entry['kvParam'][key] = str(value)

for entry in entries:
    if 'engineVersion' in entry:
        entry['engineVersion'] = '3.0.0'
    if 'printerIntName' in entry:
        entry['printerIntName'] = 'CR-K1'

backup_path = backup_dir / f'{db_path.name}.{int(time.time())}.bak'
db_path.rename(backup_path)
print(f'Backup do banco salvo: {backup_path.name}')

db['result']['count'] = len(entries)
db['result']['version'] = str(int(time.time()))
db_path.write_text(json.dumps(db, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print('Updated material options and database successfully.')
print(f'Total entries: {len(entries)}')
