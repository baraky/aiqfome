# Desafio Aiqfome

# Configuração
Download do repo e instalação dos pacotes:
- `git clone https://github.com/baraky/aiqfome.git && cd aiqfome`
- `python3 -m venv .venv`
- `pip3 install -r requirements.txt`

# Banco de dados
Subir banco de dados local para testes:
- `docker-compose up` (talvez precisa de usar sudo)

# Execução
Para rodar a aplicação:
- `fastapi dev src/main.py`

# Testes
Acesse http://127.0.0.1:8000/doc para realizar os testes na API:
- Crie um *customer* em [/customers](http://127.0.0.1:8000/docs#/Customers/register_customer_customers__post)
- Faça o login para gerar o Bearer Token em [/auth/login](http://127.0.0.1:8000/docs#/Authentication/login_auth_login_post)
- Adicione o Token gerado (apenas a string, sem o Bearer) no *Authorize*, canto superior direito da UI do Swagger

Pronto, agora pode brincar com os endpoints!

# Esclarecimentos

No desenvolvimento, tomei decisões que considerei que fizessem mais sentido, como:

- Sem autenticação, só é possível criar novos *customers*.
- Após um *customer* ter feito o login, só consegue ter acesso aos dados dele próprio e adicionar produtos na sua própria lista de favoritos.

# TODO
Alguns pontos que seria interessante adicionar na API, que não desenvolvi por falta de tempo:

- Redis para cachear requisições, principalmente dos produtos da API externa.
- Roles admnistrativas para poder gerenciar os customers e listas de favoritos.
- *Rate limit* para segurança contra DDOS e gastos da API.
- Testes unitários.
- Maior controle de fluxos de erros e exceções.
- Logging.