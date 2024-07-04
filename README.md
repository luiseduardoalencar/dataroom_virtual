# DataRoom Virtual

Este projeto é uma aplicação Django para um DataRoom virtual, que permite upload e download de arquivos, registro de considerações e log de atividades dos usuários.

## Pré-requisitos

- Docker
- Docker Compose

## Instalação e Configuração

### Passos para Executar a Aplicação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/luiseduardoalencar/dataroom_virtual
   cd dataroom_virtual
   ```

2. **Configure o arquivo `.env`:**

   Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis de ambiente:

   ```env
   POSTGRES_DB=dataroom_db
   POSTGRES_USER=dataroom_user
   POSTGRES_PASSWORD=YOUR_PASSSWORD
   ```

3. **Construir e iniciar os contêineres:**

   ```bash
   docker-compose up --build -d
   ```

4. **Aplicar as migrações:**

   ```bash
   docker exec -it mydataroom-web-1 python manage.py makemigrations
   docker exec -it mydataroom-web-1 python manage.py migrate
   ```

5. **Acessar a aplicação:**

   A aplicação estará disponível em `http://localhost:8000`.

## Uso

### Registrar um novo usuário

1. Acesse a página de registro: `http://localhost:8000/register`
2. Preencha o formulário de registro e envie.

### Fazer login

1. Acesse a página de login: `http://localhost:8000/login`
2. Preencha suas credenciais e envie.

### Upload de Arquivos

1. Após o login, vá para a página de upload de arquivos: `http://localhost:8000/upload`
2. Preencha o formulário de upload e envie.

### Download de Arquivos

1. Após o login, vá para a página principal: `http://localhost:8000/`
2. Clique no arquivo que deseja baixar.

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/fooBar`)
3. Commit suas mudanças (`git commit -am 'Add some fooBar'`)
4. Faça o push para a branch (`git push origin feature/fooBar`)
5. Crie um novo Pull Request

## Licença

Distribuído sob a licença MIT.
