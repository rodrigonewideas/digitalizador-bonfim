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
- 🔐 Autenticação via JWT (login obrigatório para acessar qualquer rota)

---

## 🔐 Autenticação JWT

Desde junho de 2025, o sistema exige login para acessar qualquer rota da API. A autenticação é feita via JWT e usa a tabela `USUARIO` do banco `DIGITALIZADOR.GDB`.

### 1. Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "login": "admin",
  "senha": "123"
}
```

Resposta:

```json
{
  "access_token": "<token JWT>",
  "token_type": "bearer"
}
```

### 2. Acesso a rotas protegidas

Adicione o header:

```
Authorization: Bearer <seu_token_jwt>
```

### 3. Obter dados do usuário logado

```http
GET /api/auth/me
Authorization: Bearer <token>
```

Resposta:

```json
{
  "usuario": "admin",
  "nome": "Rodrigo de Paula",
  "admin": true
}
```

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
│   ├── main.py                     # Entrada principal da aplicação FastAPI
│   ├── routers/
│   │   ├── digitalizador_router.py # Consulta por lote (protegida por JWT)
│   │   ├── imagens_router.py       # Consulta de imagens vinculadas (protegida)
│   │   └── auth_router.py          # Login e dados do usuário autenticado
│   ├── dependencies/
│   │   └── auth.py                 # Validação de token JWT e verificação de admin
├── .env                            # Configurações locais (não versionado)
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
```

---

### 🔐 Arquivo .env (exemplo)

Crie um `.env` na raiz do projeto com o seguinte conteúdo:

```env
SECRET_KEY=acarrocafazmaisbarulho

FIREBIRD_HOST=192.168.5.232
FIREBIRD_USER=SYSDBA
FIREBIRD_PASSWORD=bonfim2005
FIREBIRD_DB=C:/solution/data/PDV_BONFIM.GDB
```

---

### 📸 Montagem da pasta de imagens

Adicione ao `/etc/fstab`:

```fstab
//192.168.5.232/Imagens /mnt/imagens cifs credentials=/etc/samba/credenciais_imagens,iocharset=utf8,uid=rps,gid=rps,file_mode=0775,dir_mode=0775,noserverino,nofail 0 0
```

---

## 🌐 Exemplo de uso via API (agora com JWT)

- Buscar contrato por lote:  
  `GET /api/digitalizador/lote?lote=1588`

- Buscar por nome:  
  `GET /api/digitalizador/cessionario?nome=MURILO`

- Buscar imagens vinculadas:  
  `GET /api/imagens?contrato=25362`

- Abrir imagem full:  
  `GET /api/imagens/05102022/FULL/433461%2025362-111419.jpg`

> Todas essas rotas exigem autenticação com header `Authorization: Bearer <token>`

---

## ✅ Status

✅ Projeto em produção  
✅ Integração Lovable funcional  
✅ Código versionado no GitHub  
✅ Autenticação e proteção de rotas ativa  
✅ CORS e thumbnails funcionando

---

## 👨‍💻 Autor

Rodrigo de Paula Soares  
GitHub [@rodrigonewideas](https://github.com/rodrigonewideas)
