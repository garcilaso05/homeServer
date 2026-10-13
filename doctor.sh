#!/bin/bash

echo "============================================="
echo "   Iniciando Autodiagnóstico del Servidor     "
echo "============================================="

# 1. Comprobar si somos root o tenemos sudo
if [ "$EUID" -ne 0 ]; then
  echo "[-] Por favor, ejecuta este script con sudo: sudo ./doctor.sh"
  exit 1
fi

echo "[+] 1. Comprobando permisos de la carpeta de datos de PocketBase..."
chown -R rogergd:rogergd /home/rogergd/pb_data 2>/dev/null

echo "[+] 2. Limpiando procesos huérfanos de PocketBase..."
killall pocketbase 2>/dev/null
sleep 1

echo "[+] 3. Recargando los servicios del sistema (systemd)..."
systemctl daemon-reload

echo "[+] 4. Verificando y reiniciando Caddy (Servidor Web)..."
systemctl enable caddy --now
systemctl restart caddy
if systemctl is-active --quiet caddy; then
  echo "    [ÉXITO] Caddy está funcionando correctamente."
else
  echo "    [ERROR] Caddy ha fallado. Revisa con: sudo journalctl -u caddy"
fi

echo "[+] 5. Verificando y reiniciando PocketBase (Base de Datos)..."
systemctl enable pocketbase --now
systemctl restart pocketbase
if systemctl is-active --quiet pocketbase; then
  echo "    [ÉXITO] PocketBase está activo y corriendo."
else
  echo "    [ERROR] PocketBase ha fallado. Revisa con: sudo journalctl -u pocketbase"
fi

echo "============================================="
echo "   Diagnóstico y reparación finalizados.     "
echo "============================================="
