# Sistema de Gestão de Ordens de Serviço - CAAO

## 📋 Sobre o Projeto

Este sistema foi desenvolvido para gerenciar ordens de serviço do Centro de Acolhimento e Assessoria Operacional (CAAO). O projeto permite o controle, acompanhamento e gestão de ordens de serviço de forma eficiente e organizada.

## 🚀 Funcionalidades

- **Autenticação de Usuários**
  - Login seguro
  - Recuperação de senha
  - Gestão de permissões

- **Gestão de Ordens de Serviço**
  - Criação e edição de ordens
  - Acompanhamento de status
  - Anexo de documentos
  - Registro de pareceres
  - Controle de processos

- **Relatórios**
  - Visualização de dados consolidados
  - Exportação de informações
  - Análise de indicadores

## 💻 Tecnologias Utilizadas

- Python 3.13
- Django Framework
- Bootstrap
- JavaScript
- SQLite (Banco de Dados)

## 🔧 Instalação e Configuração

1. Clone o repositório:
```bash
git clone https://github.com/frischlander/pi2.git
cd pi2
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
- Crie um arquivo `.env` na raiz do projeto
- Configure as variáveis necessárias (veja `.env.example` para referência)

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

## 📁 Estrutura do Projeto

- `authentication/` - Módulo de autenticação e gestão de usuários
- `caaordserv/` - Módulo principal de gestão de ordens de serviço
- `relatorios/` - Módulo de geração e visualização de relatórios
- `static/` - Arquivos estáticos (CSS, JavaScript, imagens)
- `templates/` - Templates HTML do projeto
- `media/` - Arquivos enviados pelos usuários

## 🔐 Segurança

- Autenticação robusta de usuários
- Proteção contra CSRF
- Validação de formulários
- Controle de acesso baseado em permissões
- Armazenamento seguro de senhas

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 👥 Autores

- **Seu Nome** - *Trabalho Inicial* - [@frischlander](https://github.com/frischlander)

## 📞 Suporte

Para suporte e dúvidas, por favor abra uma [issue](https://github.com/frischlander/pi2/issues) no GitHub.

---
Desenvolvido como parte do Projeto Integrador 2 - UNIVESP