# Déploiement sur Raspberry Pi — PaperWise

Ce guide explique comment héberger PaperWise sur un Raspberry Pi pour le rendre
accessible à tous les appareils du réseau local (Wi-Fi ou Ethernet).

## Matériel requis

- Raspberry Pi 4 (ou 5) avec **4 Go de RAM minimum** (8 Go recommandé)
- Carte microSD de 32 Go minimum (classe 10)
- Raspberry Pi OS 64 bits (obligatoire pour Ollama)
- Accès au réseau local

## Étape 1 — Préparer le Pi

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3-pip python3-venv
```

## Étape 2 — Cloner le projet et installer les dépendances

```bash
git clone https://github.com/EFMFL/PaperWise.git
cd PaperWise

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> ⏳ L'installation de PyTorch sur ARM peut être longue (30 min ou plus).

## Étape 3 — Installer Ollama et un modèle léger

```bash
curl -fsSL https://ollama.com/install.sh | sh

# Sur Raspberry Pi, utilisez impérativement un petit modèle :
ollama pull llama3.2:1b
```

Indiquez au projet quel modèle utiliser (variable lue par `src/generation.py`) :

```bash
export OLLAMA_MODEL="llama3.2:1b"
```

## Étape 4 — Lancer l'interface sur le réseau local

```bash
streamlit run interface/app.py --server.address 0.0.0.0 --server.port 8501
```

- `--server.address 0.0.0.0` : rend l'interface accessible depuis les autres
  appareils du réseau (pas seulement le Pi lui-même).
- Trouvez l'adresse IP du Pi avec `hostname -I`.
- Depuis n'importe quel appareil du même réseau, ouvrez : `http://<IP-du-Pi>:8501`

## Étape 5 (optionnel) — Démarrage automatique au boot

Créez un service systemd pour que PaperWise se lance tout seul au démarrage du Pi :

```bash
sudo tee /etc/systemd/system/paperwise.service > /dev/null <<'EOF'
[Unit]
Description=PaperWise - Chat documentaire local
After=network.target ollama.service

[Service]
User=pi
WorkingDirectory=/home/pi/PaperWise
Environment="OLLAMA_MODEL=llama3.2:1b"
ExecStart=/home/pi/PaperWise/venv/bin/streamlit run interface/app.py --server.address 0.0.0.0 --server.port 8501
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now paperwise
```

Vérifiez l'état du service :

```bash
sudo systemctl status paperwise
```

## Conseils de performance

| Problème | Solution |
| --- | --- |
| Génération trop lente | Restez sur `llama3.2:1b` ou `tinyllama`. Les modèles 7B (mistral) sont trop lourds pour un Pi. |
| Manque de mémoire | Fermez les autres applications, ou ajoutez du swap (`sudo dphys-swapfile`). |
| Pi qui chauffe | Ajoutez un dissipateur/ventilateur ; la génération sollicite le CPU à 100 %. |
| Indexation lente | Indexez les PDF depuis un PC puis copiez le dossier `data/chroma_db/` sur le Pi. |
