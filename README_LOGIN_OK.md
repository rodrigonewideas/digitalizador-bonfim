# 📄 Digitalizador Bonfim API

API FastAPI para consulta de contratos e imagens digitalizadas a partir de banco Firebird (.GDB), com autenticação JWT baseada na tabela `USUARIO`.

---

## 🚀 Instalação

```bash
git clone https://github.com/rodrigonewideas/digitalizador-bonfim.git
cd digitalizador-bonfim
python3 -m venv digitalizador-venv
source digitalizador-venv/bin/activate  # Linux/Mac
digitalizador-venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---

## ⚙️ Execução local (modo dev)

```bash
uvicorn app.main:app --reload --port 8086
```

No servidor (modo serviço):

```bash
sudo systemctl restart digitalizador-api.service
```

---

## 🔐 Autenticação

### 🔧 Tabela usada: `USUARIO` (do DIGITALIZADOR.GDB)

- **login:** campo `LOGIN`
- **senha:** campo `FONE2`
- **nome:** campo `NOME`
- **admin:** campo `ADMINISTRADOR = 'S'`

---

## 🔑 Geração de token

### ✔️ Via Swagger

1. Acesse `/docs`
2. Clique em `POST /api/auth/login`
3. Envie:

```json
{
  "login": "RODRIGO",
  "senha": "squash"
}
```

4. Copie o `access_token` gerado.

5. Clique em “Authorize” e cole o token como:

```
Bearer <TOKEN_AQUI>
```

---

### ✔️ Via cURL

```bash
curl -X POST https://bonfim.malotedigital.com.br/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"login":"RODRIGO", "senha":"squash"}'
```

---

## 🔍 Endpoints

### Públicas

- `GET /ping` – Verifica se a API está viva
- `GET /lote?lote=XXXX` – Consulta contrato sem autenticação

### Protegidas com JWT

- `GET /api/digitalizador/lote`
- `GET /api/digitalizador/cessionario`
- `GET /api/imagens`
- `GET /api/imagens/{data}/{tipo}/{arquivo}`
- `GET /api/auth/me` – Dados do usuário logado

---

## 🔧 Configuração do .env

```env
SECRET_KEY=acarrocafazmaisbarulho
```

---

## 👤 Exemplo de retorno da rota `/api/auth/me`

```json
{
  "usuario": "rodrigo",
  "nome": "Rodrigo Soares",
  "admin": true
}
```

---

## 🌐 URL pública

[https://bonfim.malotedigital.com.br/docs](https://bonfim.malotedigital.com.br/docs)

---

## 🧠 Desenvolvido por

**Rodrigo de Paula Soares**  
[github.com/rodrigonewideas](https://github.com/rodrigonewideas)