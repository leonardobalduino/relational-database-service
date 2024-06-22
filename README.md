# Relational Database Service

Esse repositório tempos 2 projetos:
- DBaas
    - API
    - Worker
    - Beat
- Compute Xaas Api

## Pré-requisitos
Esse repositório requer o python na versão `3.12`

## Instalação
```shell
# Criação do ambiente virtual
make build-venv

# Ativação do ambiente virtual
source venv/bin/activate

# Instalar dependências
make install-dependencies

# Instalar git hooks
make install-git-hooks

# Criar/iniciar imagens docker
make docker-compose
```

## Migrações
```shell
# Executar migrações
make migrations
```

## Iniciar aplicações

Carregar variáveis de ambiente.
```shell
# Criar o arquivo .env na raiz do projeto
make load-dev-env
```

Iniciar apis e worker, cada aplicação deve ser iniciar em terminais separados, antes de iniciar cada aplicação ative o ambiente virtual `source venv/bin/activate`.
```shell
# Iniciar DBaaS API
make run-dbaas-api

# Iniciar DBaaS Worker
make run-dbaas-worker

# Iniciar DBaaS Beat
make run-dbaas-beat

# Iniciar Compute XaaS API
make run-computexaas-api
```

## Testes
```shell
make test
make coverage
```

# Database as a Service API
- Swagger -> http://localhost:8000/api/swagger
- Documentação -> http://localhost:8000/api/docs

# Compute XaaS API
- Swagger -> http://localhost:8001/api/swagger
- Documentação -> http://localhost:8001/api/docs


![](estatico/api.png)