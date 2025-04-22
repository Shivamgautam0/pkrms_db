# utils/helpers.py

def generate_admin_code(record: dict) -> dict:
    if 'province_code' in record and 'kabupaten_code' in record:
        prov = int(record.pop('province_code'))
        kab = int(record.pop('kabupaten_code'))
        record['admin_code'] = int(f"{prov:02d}{kab:02d}")
    return record
