# Buzón Efímero: Transferencia de Archivos "Drop & Destroy"

El **Buzón Efímero** es la solución definitiva al clásico problema moderno: *"¿Cómo me paso este PDF o esta foto del móvil al ordenador sin enviármelo por correo o por WhatsApp?"*.

En lugar de utilizar nubes de terceros que comprimen tus imágenes o servidores externos que se quedan con copias de tus documentos, esta utilidad te permite transferir archivos instantáneamente dentro de tu propia red Tailscale.

## ¿Cómo funciona?

El concepto se basa en un flujo de un solo uso (efímero) diseñado para mantener tu servidor de bajo consumo siempre limpio:

1. **Subida (Desde el dispositivo origen):** Entras a la web desde tu móvil y seleccionas un archivo. Este se envía directamente a tu servidor mediante PocketBase (colección `Transfer`).
2. **Espera en el Servidor:** El archivo se aloja en el disco duro de tu servidor de forma temporal. Puedes ver la lista de archivos pendientes desde cualquier otro ordenador o dispositivo conectado a tu VPN.
3. **Descarga y Autodestrucción (Desde el dispositivo destino):** Te sientas en tu ordenador y le das al botón de descargar. En el momento exacto en que el archivo se transfiere a tu memoria local, la aplicación web lanza una orden de borrado (`DELETE`) a la API del servidor.

El archivo **desaparece para siempre** del servidor.

## Beneficios Clave

*   **Privacidad Total:** Los archivos nunca viajan por internet abierto. Solo circulan por el túnel cifrado de tu red local (Tailscale). Ideal para pasar documentos personales, contratos o fotos sensibles.
*   **Cero Mantenimiento de Disco:** Al destruirse automáticamente tras su primer uso, no tienes que preocuparte de estar borrando "basura" del servidor doméstico ni de quedarte sin espacio en tu disco de 500GB.
*   **Velocidad Local:** Si estás en la misma red Wi-Fi que el servidor, las transferencias alcanzan la velocidad máxima de tu router, transfiriendo gigabytes en segundos.
*   **Sin Límites Propietarios:** Olvídate de los límites de tamaño por archivo que imponen aplicaciones de mensajería como Telegram o WhatsApp. (Configurando el límite a `0` en el campo File de PocketBase, el tamaño es infinito).