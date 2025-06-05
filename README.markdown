# Consulta de Capa de Processo - Escavador API

Este projeto é uma aplicação web que permite consultar e detalhar informações de processos judiciais utilizando a API do Escavador. Os dados são armazenados em um banco de dados SQLite no servidor e apresentados em uma interface amigável com tabelas e abas dinâmicas.

## Descrição do Projeto

A aplicação permite aos usuários:
- Consultar processos judiciais pelo número CNJ (individualmente ou em lote via arquivo `.txt`).
- Armazenar os dados em um banco SQLite no servidor para consultas futuras.
- Visualizar detalhes dos processos em um modal com abas organizadas:
  - **Processo**: Informações principais (ex.: número CNJ, polos ativo e passivo).
  - **Fontes**: Detalhes das fontes do processo (ex.: tribunal, data de início).
  - **Envolvidos**: Informações sobre as partes envolvidas e seus advogados.
  - **Capa**: Dados da capa do processo (ex.: classe, assunto).
  - **Assuntos Normalizados**: Assuntos normalizados da capa.
  - **Informações Complementares**: Informações adicionais da capa.
- Filtrar dados em cada aba com um campo de pesquisa.
- Expandir/contrair seções para melhor visualização.

O projeto utiliza o Flask como framework backend para gerenciar requisições à API do Escavador e o banco de dados SQLite. A interface frontend é construída com HTML, CSS e JavaScript puro.

## Estrutura do Projeto

```
consulta-capa-processo-escavador/
│
├── app.py              # Script Flask principal
├── .env                # Arquivo para armazenar o token da API
├── templates/
│   └── index.html      # Arquivo HTML da interface
└── static/
    └── db/             # Pasta para armazenar o banco de dados SQLite
```

## Pré-requisitos

- Python 3.6 ou superior
- Um navegador web moderno (ex.: Chrome, Firefox)
- Um token de API válido da Escavador (obtido na sua conta Escavador)

## Como Usar

### Configuração

1. **Clone ou Baixe o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/consulta-capa-processo-escavador.git
   ```
   Ou baixe o arquivo ZIP e extraia.

2. **Crie um Ambiente Virtual (Opcional, mas Recomendado)**:
   ```bash
   cd consulta-capa-processo-escavador
   python -m venv venv
   source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   ```

3. **Instale as Dependências**:
   ```bash
   pip install flask python-dotenv requests
   ```

4. **Configure o Token da API**:
   - Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
     ```
     API_TOKEN=seu-token-aqui
     ```
   - Substitua `seu-token-aqui` pelo seu token da API Escavador.

### Executando a Aplicação

1. **Inicie o Servidor Flask**:
   ```bash
   python app.py
   ```
   O servidor estará disponível em `http://localhost:5000`.

2. **Acesse a Aplicação**:
   - Abra `http://localhost:5000` no seu navegador.

3. **Consulte Processos**:
   - **Consulta Única**: Digite um número CNJ (ex.: `0007356-56.2007.4.03.6119`) no campo "Número CNJ Único" e clique em "Consultar Dados".
   - **Consulta em Lote**: Carregue um arquivo `.txt` com até 2000 CNJs (um por linha) e clique em "Consultar Dados".

4. **Visualize os Detalhes**:
   - Clique em uma linha da tabela para abrir um modal com detalhes.
   - Navegue pelas abas ("Processo", "Fontes", etc.) para explorar os dados.
   - Use o campo de pesquisa em cada aba para filtrar os dados.
   - Clique em "Expandir/Contrair" para ocultar ou mostrar tabelas.

## Como Contribuir

1. **Fork o Repositório**:
   - Clique em "Fork" no GitHub para criar uma cópia no seu perfil.

2. **Clone o Fork**:
   ```bash
   git clone https://github.com/seu-usuario/consulta-capa-processo-escavador.git
   ```

3. **Crie uma Branch para sua Contribuição**:
   ```bash
   git checkout -b minha-contribuicao
   ```

4. **Faça suas Alterações**:
   - Adicione novas funcionalidades, corrija bugs ou melhore a documentação.
   - Teste localmente executando o servidor Flask.

5. **Commit e Push**:
   ```bash
   git add .
   git commit -m "Descrição da minha contribuição"
   git push origin minha-contribuicao
   ```

6. **Crie um Pull Request**:
   - No GitHub, abra um Pull Request descrevendo suas alterações.

## Limitações Conhecidas

- A API do Escavador tem um limite de 500 requisições por minuto. O script processa CNJs em lotes de 5 com um intervalo de 1 segundo para evitar exceder esse limite.
- Algumas informações podem não estar disponíveis em todos os processos, dependendo da resposta da API.
- O banco de dados SQLite é gerenciado no servidor, e os dados são persistidos em `static/db/processos.db`.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contato

Para dúvidas ou sugestões, entre em contato via GitHub Issues ou diretamente com os mantenedores do projeto.

---

**Desenvolvido com ❤️ pela equipe de desenvolvimento.**