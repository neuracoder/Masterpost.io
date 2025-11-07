# 🔧 HOTFIX: Corregir Import de Supabase

**Archivo a corregir:** `backend/app/routers/upload.py`

---

## PROBLEMA

El archivo importa `supabase_client` desde una ubicación incorrecta.

**Import incorrecto (línea ~11):**
```python
from ..database.supabase_client import supabase_client
```

**Import correcto:**
```python
from ..config.supabase_config import supabase_client
```

---

## SOLUCIÓN

### PASO 1: Buscar el import incorrecto

En `backend/app/routers/upload.py`, línea aproximadamente 11:

```python
from ..database.supabase_client import supabase_client
```

### PASO 2: Reemplazar por el import correcto

```python
from ..config.supabase_config import supabase_client
```

---

## VERIFICACIÓN

Después de corregir, el backend debería arrancar sin errores:

```bash
cd backend
python app/main.py
```

**Salida esperada:**
```
>> Starting Simple Masterpost.io Backend on port 8002...
>> API Docs: http://localhost:8002/docs
>> Health: http://localhost:8002/health
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8002 (Press CTRL+C to quit)
```

Sin errores de import.

---

## EJECUTAR TEST

Una vez corregido y el backend arrancando:

```bash
cd backend
python test_protected_upload.py
```

---

## REPORTE

Después de corregir y probar, reporta:

```
✅ HOTFIX APLICADO: Import de supabase_client corregido
✅ Backend arranca sin errores
✅ Test de MÓDULO 2 ejecutado

Resultados:
[copiar salida del test]

Estado: MÓDULO 2 COMPLETADO
Listo para MÓDULO 3
```

---

**HAZLO AHORA Y REPORTA**
