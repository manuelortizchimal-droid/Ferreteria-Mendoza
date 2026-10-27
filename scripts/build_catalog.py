import csv, json, pathlib, datetime, decimal
root=pathlib.Path(__file__).resolve().parents[1]
src=root/'catalogo/productos.csv'
dest=root/'catalogo/productos.json'
with src.open(encoding='utf-8-sig', newline='') as f:
    reader=csv.DictReader(f)
    required={'codigo','descripcion','precio'}
    if not required.issubset(reader.fieldnames or []):
        raise SystemExit('CSV requiere columnas codigo,descripcion,precio')
    products=[]
    seen=set()
    for line,row in enumerate(reader,2):
        code=(row['codigo'] or '').strip()
        name=(row['descripcion'] or '').strip()
        if not code or not name:
            raise SystemExit(f'Fila {line}: falta codigo o descripcion')
        if code in seen:
            raise SystemExit(f'Fila {line}: codigo duplicado {code}')
        seen.add(code)
        try:
            price=decimal.Decimal((row['precio'] or '').strip())
            if not price.is_finite() or price<0:
                raise ValueError()
        except (decimal.InvalidOperation,ValueError):
            raise SystemExit(f'Fila {line}: precio invalido')
        photo=(row.get('foto') or '').strip()
        if photo and not photo.startswith('https://'):
            raise SystemExit(f'Fila {line}: foto debe ser HTTPS')
        products.append({'code':code,'description':name,'price':float(price),'photo':photo})
if not products:
    raise SystemExit('No hay productos; se conserva catálogo anterior')
dest.write_text(json.dumps({'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(products),'source':'CSV validado por operador','products':products},ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(f'Catálogo central preparado: {len(products)} productos')
