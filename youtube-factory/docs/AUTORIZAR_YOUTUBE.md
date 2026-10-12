# Conectar los canales con la API oficial de YouTube (opcional)

No hace falta para producir videos. Sirve para **subir y programar desde la fábrica** y para **leer métricas**.
Nunca compartas contraseñas, códigos ni el contenido de los archivos de `secrets/` en un chat.

## Una sola vez: crear el proyecto en Google Cloud (gratis)
1. Entra a https://console.cloud.google.com/ con la cuenta de Google dueña de los canales.
2. Crea un proyecto, por ejemplo "fabrica-youtube".
3. En **APIs y servicios → Biblioteca**, habilita **YouTube Data API v3** y **YouTube Analytics API**.
4. En **Pantalla de consentimiento de OAuth**, elige tipo **Externo**, completa el nombre de la app y tu correo, y agrega tu cuenta en **Usuarios de prueba**.
5. En **Credenciales → Crear credenciales → ID de cliente de OAuth**, elige el tipo **App de escritorio**. Descarga el JSON.
6. Guarda ese archivo como `secrets/client_secret.json` dentro de la carpeta de la fábrica. Esa carpeta no se sube a Git.
7. Copia `.env.example` como `.env` (sin cambiar nada más por ahora).
8. Instala los paquetes opcionales: `.venv\Scripts\pip install -r requirements-youtube.txt`.

## Por cada canal
```
fabrica.bat autorizar canal_a     (Atajo IA)
fabrica.bat autorizar canal_b     (Celda Clara)
```
Se abre tu navegador. **Elige el canal correcto** cuando Google pregunte qué cuenta o canal usar, y acepta.
La fábrica guarda el ID del canal en `config/canal_x.yaml`. A partir de ahí **se niega a subir** si el permiso
corresponde a otro canal.

## Limitaciones oficiales que debes conocer
- **Proyecto sin verificar:** Google deja en **privado** los videos subidos por API desde proyectos no auditados
  (creados después del 28-jul-2020). Mientras tanto, la fábrica sube en privado y tú programas la fecha en YouTube Studio.
  La alternativa es pedir la auditoría de Google o seguir publicando a mano con el paquete de `paquetes/`.
- **Modo "Prueba":** con la app en modo de prueba, el permiso caduca a los **7 días**. Ejecuta `autorizar` de nuevo cuando la fábrica lo pida.
- **Cuota:** es limitada y gratuita. La fábrica cuenta las unidades que usa y no supera 5 subidas por día por defecto (`config/global.yaml`).

## Subir
```
fabrica.bat publicar canal_a --desde 2026-10-19 --hasta 2026-10-25            (solo SIMULA y muestra qué haría)
fabrica.bat publicar canal_a --desde 2026-10-19 --hasta 2026-10-25 --confirmar
```
`--confirmar` además exige `AUTO_PUBLICAR=1` en `.env` o `publicacion.auto_publicar: true` en `config/global.yaml`.
Un video figura como "programado" solo si la API lo confirma.
