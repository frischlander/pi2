# CLAUDE.md - PI2 UNIVESP - Sistema de Gestão de Ordens de Serviço CAAO

## 🤖 Instruções para Assistentes de IA

Este documento fornece contexto essencial para assistentes de IA (Claude CLI, Cursor, GitHub Copilot) trabalhando no projeto PI2 UNIVESP.

## 📋 Visão Geral do Projeto

**Nome:** Sistema de Gestão de Ordens de Serviço - CAAO
**Cliente:** Centro de Acolhimento e Assessoria Operacional (CAAO)
**Objetivo:** Gerenciar ordens de serviço de forma eficiente e organizada
**Repositório:** https://github.com/frischlander/pi2
**Deploy:** https://pi2univesp.onrender.com (Render)

## 🏗️ Arquitetura do Projeto

### Stack Tecnológica

```
Backend:
- Python 3.11+
- Django 5.2.6
- PostgreSQL (Render)
- Gunicorn (WSGI Server)

Frontend:
- Bootstrap 4
- JavaScript (Vanilla)
- Chart.js 2.7.3
- Feather Icons

Infraestrutura:
- Render (Hosting + PostgreSQL)
- WhiteNoise (Static Files)
- GitHub (Version Control)
```

### Estrutura de Diretórios

```
pi2/
├── authentication/          # App de autenticação
│   ├── templates/
│   │   └── authentication/
│   │       └── login.html
│   ├── views.py
│   └── urls.py
├── caaordserv/             # App principal (Ordens de Serviço)
│   ├── migrations/
│   ├── templates/
│   │   └── pdf/
│   ├── management/
│   │   └── commands/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── relatorios/             # App de relatórios
│   ├── templates/
│   ├── views.py
│   └── urls.py
├── templates/              # Templates globais
│   ├── base_auth.html
│   └── partials/
│       └── _messages.html
├── static/                 # Arquivos estáticos globais
│   ├── css/
│   ├── js/
│   └── img/
├── staticfiles/            # Arquivos coletados (gitignored)
├── media/                  # Uploads de usuários (gitignored)
├── venv/                   # Virtual environment (gitignored)
├── settings.py             # Configurações Django
├── urls.py                 # URLs principais
├── wsgi.py                 # WSGI application
├── asgi.py                 # ASGI application
├── manage.py               # Django CLI
├── requirements.txt        # Dependências Python
├── build.sh                # Script de build Render
├── render.yaml             # Configuração Render
├── .env                    # Variáveis de ambiente (gitignored)
├── .env.example            # Template de variáveis
├── .gitignore              # Git ignore rules
├── README.md               # Documentação geral
├── DEPLOY_RENDER.md        # Guia de deploy
└── CLAUDE.md               # Este arquivo
```

## 🔧 Configuração e Setup

### Ambiente Local

```bash
# 1. Clonar repositório
git clone https://github.com/frischlander/pi2.git
cd pi2

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Criar arquivo .env (copiar de .env.example)
cp .env.example .env

# 6. Configurar variáveis de ambiente no .env
# Editar .env com suas credenciais

# 7. Executar migrações
python manage.py migrate

# 8. Criar superusuário
python manage.py createsuperuser

# 9. Coletar arquivos estáticos
python manage.py collectstatic --noinput

# 10. Rodar servidor local
python manage.py runserver
```

### Variáveis de Ambiente

**Arquivo:** `.env` (não commitado)

```env
# Django
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False

# Database (Render PostgreSQL)
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DATABASE

# OU usar variáveis separadas:
DB_NAME=pi2_database_fie6
DB_USER=pi2_database_fie6_user
DB_USER_PASSWORD=BN7UQg9KHoOgG3CCCngrlM3ua0Rgdbc4
DB_HOST=dpg-d3dl14ogjchc73aks1mg-a.oregon-postgres.render.com
```

## 📝 Convenções de Código

### Python/Django

```python
# 1. Sempre usar type hints
def process_ordem(ordem_id: int) -> dict:
    """
    Processa ordem de serviço.

    Args:
        ordem_id: ID da ordem de serviço

    Returns:
        Dict com resultado do processamento
    """
    pass

# 2. Docstrings obrigatórias em funções públicas
# 3. Seguir PEP 8
# 4. Imports organizados: stdlib → third-party → local
# 5. Nome de classes: PascalCase
# 6. Nome de funções/variáveis: snake_case
# 7. Constantes: UPPER_SNAKE_CASE
```

### Templates Django

```html
<!-- 1. Sempre usar {% load static %} quando necessário -->
{% load static %}

<!-- 2. Sempre usar {% csrf_token %} em forms -->
<form method="post">
  {% csrf_token %}
  <!-- form fields -->
</form>

<!-- 3. Usar {% url %} para URLs -->
<a href="{% url 'login' %}">Login</a>

<!-- 4. Incluir partials para reutilização -->
{% include 'partials/_messages.html' %}

<!-- 5. Extends sempre no topo -->
{% extends 'base_auth.html' %}
```

### JavaScript

```javascript
// 1. Usar const/let (nunca var)
const userId = 123;
let counter = 0;

// 2. Funções arrow quando apropriado
const fetchData = () => {
  // implementation
};

// 3. Event listeners com addEventListener
document.getElementById('btn').addEventListener('click', handleClick);

// 4. Comentários explicativos
// Toggle password visibility
function togglePassword() {
  // implementation
}
```

## 🗄️ Modelos de Dados

### OrdemServico (Principal)

```python
class OrdemServico(models.Model):
    processo = models.CharField(max_length=20)  # Formato: XXXX.XX.XXXXXX
    data_solicitacao = models.DateField()
    tipo_solicitacao = models.CharField(max_length=100)
    descricao = models.TextField()
    solicitante = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('em_andamento', 'Em Andamento'),
            ('concluido', 'Concluído'),
            ('cancelado', 'Cancelado'),
        ]
    )
    parecer = models.TextField(blank=True, null=True)
    ultimo_usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_ultima_alteracao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_solicitacao']
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
```

### AnexoOrdemServico

```python
class AnexoOrdemServico(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='anexos/')
    nome_arquivo = models.CharField(max_length=255)
    data_upload = models.DateTimeField(auto_now_add=True)
    usuario_upload = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

## 🛣️ Rotas e URLs

### URLs Principais

```python
# urls.py (root)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('caaordserv.urls')),
    path('authentication/', include('authentication.urls')),
    path('relatorios/', include('relatorios.urls')),
]

# authentication/urls.py
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

# caaordserv/urls.py
urlpatterns = [
    path('', views.index, name='caaordserv'),
    path('ordens/', views.lista_ordens, name='lista_ordens'),
    path('ordens/criar/', views.criar_ordem, name='criar_ordem'),
    path('ordens/<int:id>/', views.detalhe_ordem, name='detalhe_ordem'),
    path('ordens/<int:id>/editar/', views.editar_ordem, name='editar_ordem'),
    path('ordens/<int:id>/pdf/', views.gerar_pdf, name='gerar_pdf'),
]
```

## 🎨 Frontend e Estáticos

### Static Files

```
static/
├── css/
│   ├── bootstrap.min.css
│   ├── main.css
│   └── dashboard.css
├── js/
│   ├── login.js
│   └── main.js
└── img/
    ├── logo.png
    └── centro-acolhimento.jpeg
```

### Bootstrap Components Utilizados

- Cards
- Forms (form-control, form-group)
- Buttons (btn, btn-primary, btn-success)
- Modals
- Alerts (para mensagens)
- Tables (table, table-striped)
- Grid System (container, row, col)

## 🔐 Autenticação e Segurança

### Settings de Segurança

```python
# settings.py

# CSRF
CSRF_TRUSTED_ORIGINS = ['https://pi2univesp.onrender.com']
CSRF_COOKIE_SECURE = True

# SSL/HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True

# Allowed Hosts
ALLOWED_HOSTS = ['pi2univesp.onrender.com', '.onrender.com', 'localhost', '127.0.0.1']

# Debug (NUNCA True em produção)
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Secret Key (sempre via variável de ambiente)
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-for-dev-only')
```

### Proteção de Views

```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Function-based view
@login_required
def minha_view(request):
    pass

# Class-based view
@method_decorator(login_required, name='dispatch')
class MinhaView(View):
    pass
```

## 🚀 Deploy no Render

### Arquivos de Deploy

**build.sh** - Script executado no build
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

**render.yaml** - Configuração do serviço
```yaml
services:
  - type: web
    name: pi2univesp
    env: python
    region: oregon
    buildCommand: "./build.sh"
    startCommand: "gunicorn wsgi:application"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: pi2_database_fie6
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: PYTHON_VERSION
        value: 3.11.0

databases:
  - name: pi2_database_fie6
    region: oregon
    plan: free
```

### Processo de Deploy

1. **Push para GitHub** → Automático via git push
2. **Render detecta mudanças** → Trigger build
3. **Build phase** → Executa build.sh
4. **Deploy phase** → Inicia gunicorn
5. **Health check** → Verifica se app respondeu
6. **Live** → https://pi2univesp.onrender.com

### Variáveis de Ambiente no Render

Configuradas no Dashboard:
- `DATABASE_URL` - Auto-injetada pelo Render
- `SECRET_KEY` - Auto-gerada pelo Render
- `DEBUG` - Definida como `False`
- `PYTHON_VERSION` - `3.11.0`

## 📊 Database

### PostgreSQL (Render)

```
Host: dpg-d3dl14ogjchc73aks1mg-a.oregon-postgres.render.com
Database: pi2_database_fie6
User: pi2_database_fie6_user
Password: BN7UQg9KHoOgG3CCCngrlM3ua0Rgdbc4
Port: 5432
Region: Oregon (US West)
Plan: Free (750 hours/month)
```

### Migrações

```bash
# Criar migração
python manage.py makemigrations

# Ver SQL da migração
python manage.py sqlmigrate caaordserv 0001

# Aplicar migrações
python manage.py migrate

# Listar migrações
python manage.py showmigrations

# Reverter migração
python manage.py migrate caaordserv 0001
```

### Backup e Restore

```bash
# Backup local (SQLite)
cp db.sqlite3 db.sqlite3.backup

# Backup PostgreSQL (Render)
# Via Dashboard: Database → Backups → Create Backup

# Dump PostgreSQL
pg_dump DATABASE_URL > backup.sql

# Restore PostgreSQL
psql DATABASE_URL < backup.sql
```

## 🐛 Debugging e Troubleshooting

### Logs no Render

```bash
# Via Dashboard
# Render Dashboard → Service → Logs

# Via CLI (se instalado)
render logs -s pi2univesp
```

### Problemas Comuns

#### 1. Erro 500 no Login

**Causa:** Template ou static files não encontrados
**Solução:**
```bash
python manage.py collectstatic --noinput
# Verificar STATICFILES_DIRS e STATIC_ROOT em settings.py
```

#### 2. DisallowedHost

**Causa:** Host não está em ALLOWED_HOSTS
**Solução:**
```python
# settings.py
ALLOWED_HOSTS = ['pi2univesp.onrender.com', '.onrender.com', 'localhost']
```

#### 3. CSRF Verification Failed

**Causa:** CSRF_TRUSTED_ORIGINS não configurado
**Solução:**
```python
# settings.py
CSRF_TRUSTED_ORIGINS = ['https://pi2univesp.onrender.com']
```

#### 4. Database Connection Error

**Causa:** DATABASE_URL incorreta ou SSL não configurado
**Solução:**
```python
# settings.py
DATABASES = {
    'default': dj_database_url.config(
        conn_health_checks=True,
        ssl_require=True if os.environ.get('DATABASE_URL') else False
    )
}
```

#### 5. Static Files 404

**Causa:** WhiteNoise não configurado corretamente
**Solução:**
```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Deve estar aqui
    # ... outros middlewares
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## 🧪 Testes

### Estrutura de Testes

```
caaordserv/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_forms.py
```

### Executar Testes

```bash
# Todos os testes
python manage.py test

# App específica
python manage.py test caaordserv

# Teste específico
python manage.py test caaordserv.tests.test_models.OrdemServicoTestCase

# Com verbosidade
python manage.py test --verbosity=2

# Com coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Exemplo de Teste

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from caaordserv.models import OrdemServico

class OrdemServicoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'password')
        self.client = Client()

    def test_criar_ordem(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/ordens/criar/', {
            'processo': '1234.56.789012',
            'data_solicitacao': '2025-01-15',
            'tipo_solicitacao': 'Manutenção',
            'descricao': 'Teste',
            'solicitante': 'João Silva',
            'status': 'pendente',
        })
        self.assertEqual(response.status_code, 302)  # Redirect após criar
        self.assertEqual(OrdemServico.objects.count(), 1)
```

## 📚 Dependências Principais

```
Django==5.2.6              # Framework web
gunicorn==23.0.0           # WSGI server
psycopg2-binary==2.9.10    # PostgreSQL adapter
dj-database-url==3.0.1     # Database URL parser
python-dotenv==1.1.1       # .env file loader
whitenoise==6.11.0         # Static files serving
reportlab==4.4.4           # PDF generation
pillow==11.3.0             # Image processing
```

## 🔄 Git Workflow

### Branch Strategy

```bash
# Main branch (produção)
main

# Development branch
git checkout -b dev

# Feature branch
git checkout -b feature/nova-funcionalidade

# Bugfix branch
git checkout -b bugfix/corrigir-erro
```

### Commit Messages

Seguir Conventional Commits:

```bash
# Feature
git commit -m "feat: adicionar filtro de ordens por status"

# Fix
git commit -m "fix: corrigir cálculo de datas no relatório"

# Docs
git commit -m "docs: atualizar README com instruções de deploy"

# Style
git commit -m "style: formatar código com black"

# Refactor
git commit -m "refactor: simplificar lógica de autenticação"

# Test
git commit -m "test: adicionar testes para modelo OrdemServico"

# Chore
git commit -m "chore: atualizar dependências"
```

## 🚨 Regras Críticas

### ❌ NUNCA FAZER:

1. **Commitar secrets/credentials**
   - Nunca adicionar `.env` ao git
   - Nunca hardcodar senhas no código
   - Usar sempre variáveis de ambiente

2. **Rodar DEBUG=True em produção**
   - Expõe informações sensíveis
   - Compromete segurança

3. **Fazer mudanças direto em produção**
   - Sempre testar localmente primeiro
   - Usar staging environment quando possível

4. **Ignorar migrações**
   - Sempre rodar makemigrations antes de commit
   - Nunca editar migrações já aplicadas

5. **Usar psycopg2 (sem -binary)**
   - Sempre usar psycopg2-binary no requirements.txt
   - Evita erros de compilação no deploy

### ✅ SEMPRE FAZER:

1. **Testar localmente antes de push**
```bash
python manage.py check
python manage.py test
python manage.py runserver
```

2. **Coletar static files antes de deploy**
```bash
python manage.py collectstatic --noinput
```

3. **Documentar mudanças significativas**
   - Atualizar README.md
   - Adicionar comentários no código
   - Documentar APIs e endpoints

4. **Usar virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```

5. **Manter requirements.txt atualizado**
```bash
pip freeze > requirements.txt
```

## 📞 Contatos e Recursos

### Documentação Oficial

- **Django:** https://docs.djangoproject.com/
- **Render:** https://render.com/docs
- **Bootstrap:** https://getbootstrap.com/docs/4.6/
- **PostgreSQL:** https://www.postgresql.org/docs/

### Repositório

- **GitHub:** https://github.com/frischlander/pi2
- **Issues:** https://github.com/frischlander/pi2/issues
- **Pull Requests:** https://github.com/frischlander/pi2/pulls

### Deploy

- **URL Produção:** https://pi2univesp.onrender.com
- **Render Dashboard:** https://dashboard.render.com
- **Database:** Render PostgreSQL (Oregon)

## 🎓 Para Novos Desenvolvedores

### Checklist de Onboarding

- [ ] Clonar repositório
- [ ] Criar e ativar venv
- [ ] Instalar dependências
- [ ] Configurar .env
- [ ] Rodar migrações
- [ ] Criar superuser
- [ ] Rodar servidor local
- [ ] Acessar http://localhost:8000
- [ ] Ler este CLAUDE.md completo
- [ ] Ler README.md
- [ ] Ler DEPLOY_RENDER.md
- [ ] Explorar código (models → views → templates)
- [ ] Fazer primeiro commit de teste

### Recursos de Aprendizado

- Django Tutorial: https://docs.djangoproject.com/en/5.2/intro/tutorial01/
- Django Best Practices: https://django-best-practices.readthedocs.io/
- Python Virtual Environments: https://realpython.com/python-virtual-environments/
- Git Basics: https://git-scm.com/book/en/v2/Getting-Started-Git-Basics

## 📅 Histórico de Versões

### v1.0.0 (2025-09-30)
- ✅ Deploy inicial no Render
- ✅ Autenticação de usuários
- ✅ CRUD de ordens de serviço
- ✅ Geração de PDFs
- ✅ Sistema de anexos
- ✅ Relatórios básicos
- ✅ WhiteNoise para static files
- ✅ PostgreSQL no Render

---

**Última atualização:** 2025-09-30
**Versão do documento:** 1.0
**Mantenedor:** @frischlander
**Para Assistentes IA:** Este documento deve ser consultado sempre que trabalhar neste projeto