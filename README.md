# 📄 Digitalizador Bonfim

Sistema backend em FastAPI com banco Firebird para digitalização e consulta de contratos do Cemitério Parque Senhor do Bonfim, com integração à interface Lovable.

---

## 🚀 Funcionalidades

- Consulta de contratos por lote
- Listagem e exibição de imagens digitalizadas (com thumbnails)
- Servidor HTTPS com NGINX + CORS dinâmico
- Integração com frontend Lovable
- Acesso a imagens via montagem CIFS (rede Windows)
- Estrutura de API moderna com FastAPI + Routers

---

## 📦 Tecnologias utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** – backend Python moderno
- **Firebird 1.5** – banco de dados legado
- **fdb** – driver Python para Firebird
- **NGINX** – servidor HTTPS e proxy reverso
- **CIFS** – montagem de compartilhamento Windows
- **Ubuntu Server 24.04 LTS**
- **Lovable.dev** – frontend interativo e personalizável

---

## 📂 Estrutura do projeto

digitalizador/
├── app/
│ ├── main.py # Entrada principal da aplicação FastAPI
│ ├── routers/
│ │ ├── digitalizador_router.py # Consulta por lote
│ │ └── imagens_router.py # Consulta de imagens vinculadas
├── .env # Configurações locais (não versionado)
├── .gitignore
└── requirements.txt


---

## 🔧 Instalação local

```bash
git clone https://github.com/rodrigonewideas/digitalizador-bonfim.git
cd digitalizador-bonfim
python3 -m venv digitalizador-venv
source digitalizador-venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

🔐 Arquivo .env (exemplo)

    Crie um .env para armazenar credenciais locais:

FIREBIRD_HOST=192.168.5.232
FIREBIRD_USER=SYSDBA
FIREBIRD_PASSWORD=bonfim2005
FIREBIRD_DB=C:/solution/data/PDV_BONFIM.GDB

📸 Montagem da pasta de imagens

Adicione ao /etc/fstab:
//192.168.5.232/Imagens /mnt/imagens cifs credentials=/etc/samba/credenciais_imagens,iocharset=utf8,uid=rps,gid=rps,file_mode=0775,dir_mode=0775,noserverino,nofail 0 0

🌐 Exemplo de uso via API

Buscar contrato por lote:
GET /lote?lote=1588

Buscar imagens:
GET /api/imagens?contrato=25362

Abrir imagem full:
https://bonfim.malotedigital.com.br/api/imagens/05102022/FULL/433461%2025362-111419.jpg

✅ Status

✅ Projeto em produção
✅ Integração Lovable funcional
✅ Código versionado no GitHub
✅ CORS e thumbnails funcionando

👨‍💻 Autor

Rodrigo de Paula Soares
GitHub @rodrigonewideas