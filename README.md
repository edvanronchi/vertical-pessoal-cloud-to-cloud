# Migração Folha Cloud para Folha Cloud

### Descrição
O projeto foi desenvolvido com o intuito de mudar o database do sistema Folha em uma entidade especifica, o mesmo faz a migração de grande parte dos dados para outra entidade, utilizando o Service Layer que o sistema nos disponibiliza.

### Escalabilidade
Todas as funções desenvolvidas no projeto atendem outras novas migrações do sistema Folha Cloud. Como o tempo foi escasso, algumas rotas do Service Layer não foram criadas, pois para aquela entidade especifica não precisava. Desta forma ao utilizar este projeto, lembrar de revisar todas rotas com base na entidade a ser migrada.

### Arquitetura
Na raiz principal do projeto:

- **main** -> arquivo principal, onde deve-se executar para dar inicio a migração;
- **functions** -> composto por algumas funções que auxiliam no processo de migração. Em nenhum momento este arquivo será importado ou consultado pelo projeto;
- **.env** -> variáveis de ambiente;
- **requirements** -> arquivo de texto, contendo uma lista de itens/pacotes para serem instalados.

Na pasta **src**:

- **database**-> configurações e funções referentes ao banco de dados local, onde ira armazenar a tabela de controle de migração;
- **routes** -> ficam armazenados todas as rotas do Service Layer que serão migrados. Nele você deve colocar as rotas e as dependências das rotas;
- **service** -> configurações e funções referentes ao Service Layer;

Na pasta **src/service-layer**: contém todas as rotas, para cada uma delas é montado o body de requisição conforme Service Layer especifica.

Na pasta **src/files**: nela você encontra todas as rotas mapeadas e cadastros do sistema Folha.

Como precisamos ter um controle de migração onde o mesmo tem como 	função armazenar algumas informações cruciais para a migração, devemos instalar na maquina um gerenciador de banco de dados. Optei por utilizar o  PostgreSQL, mas pode ser utilizado outro banco, desde de que não altere o real funcionamento do projeto.