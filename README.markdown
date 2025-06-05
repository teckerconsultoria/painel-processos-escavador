# Consulta de Capa de Processo - Escavador API

Este projeto é uma aplicação web que permite consultar e detalhar informações de processos judiciais utilizando a API do Escavador. Os dados são armazenados em um banco de dados SQLite no navegador e apresentados em uma interface amigável com tabelas e abas dinâmicas.

## Descrição do Projeto

A aplicação permite aos usuários:
- Consultar processos judiciais pelo número CNJ (individualmente ou em lote via arquivo `.txt`).
- Armazenar os dados em um banco SQLite para consultas futuras.
- Visualizar detalhes dos processos em um modal com abas organizadas:
  - **Processo**: Informações principais (ex.: número CNJ, polos ativo e passivo).
  - **Fontes**: Detalhes das fontes do processo (ex.: tribunal, data de início).
  - **Envolvidos**: Informações sobre as partes envolvidas e seus advogados.
  - **Capa**: Dados da capa do processo (ex.: classe, assunto).
  - **Assuntos Normalizados**: Assuntos normalizados da capa.
  - **Informações Complementares**: Informações adicionais da capa.
- Filtrar dados em cada aba com um campo de pesquisa.
- Expandir/contrair seções para melhor visualização.
- Baixar o banco de dados SQLite com os dados armazenados.

O projeto utiliza a biblioteca `sql.js` para gerenciar o banco SQLite no navegador e é construído com HTML, CSS e JavaScript puro.

## Como Usar

### Pré-requisitos
- Um navegador web moderno (ex.: Chrome, Firefox).
- Um token de API válido da Escavador (obtido na sua conta Escavador).

### Instruções
1. **Clone ou Baixe o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/consulta-capa-processo-escavador.git
   ```
   Ou baixe o arquivo ZIP e extraia.

2. **Abra o Arquivo `index.html`**:
   - Abra o arquivo `index.html` no seu navegador.

3. **Insira o Token da API**:
   - No campo "Token da API", insira seu token da Escavador.

4. **Consulte Processos**:
   - **Consulta Única**: Digite um número CNJ (ex.: `0007356-56.2007.4.03.6119`) no campo "Número CNJ Único" e clique em "Consultar Dados".
   - **Consulta em Lote**: Carregue um arquivo `.txt` com até 2000 CNJs (um por linha) e clique em "Consultar Dados".

5. **Visualize os Detalhes**:
   - Clique em uma linha da tabela para abrir um modal com detalhes.
   - Navegue pelas abas ("Processo", "Fontes", etc.) para explorar os dados.
   - Use o campo de pesquisa em cada aba para filtrar os dados.
   - Clique em "Expandir/Contrair" para ocultar ou mostrar tabelas.

6. **Baixe o Banco de Dados**:
   - Clique em "Baixar Banco de Dados" para salvar o arquivo `processos.db` com os dados armazenados.

## Estrutura do Projeto

- `index.html`: Arquivo principal contendo o código HTML, CSS e JavaScript.
  - Inclui a biblioteca `sql.js` via CDN para gerenciar o banco SQLite no navegador.
  - Estrutura o layout com uma tabela principal e um modal com abas dinâmicas.
- Banco de Dados SQLite (em memória):
  - Tabelas: `processos`, `fontes_processo`, `fontes_capa`, `fontes_capa_assuntos_normalizados`, `fontes_capa_informacoes_complementares`, `fontes_envolvidos`, `fontes_envolvidos_advogados`, `fontes_envolvidos_advogados_oabs`.

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
   - Teste localmente abrindo o `index.html` no navegador.

5. **Commit e Push**:
   ```bash
   git add .
   git commit -m "Descrição da minha contribuição"
   git push origin minha-contribuicao
   ```

6. **Crie um Pull Request**:
   - No GitHub, abra um Pull Request descrevendo suas alterações.

## Limitações Conhecidas

- O banco de dados SQLite é armazenado em memória e será perdido ao recarregar a página. Use o botão "Baixar Banco de Dados" para salvar os dados.
- A API do Escavador tem um limite de 500 requisições por minuto. O script processa CNJs em lotes de 5 com um intervalo de 1 segundo para evitar exceder esse limite.
- Algumas informações podem não estar disponíveis em todos os processos, dependendo da resposta da API.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contato

Para dúvidas ou sugestões, entre em contato via GitHub Issues ou diretamente com os mantenedores do projeto.

---

**Desenvolvido com ❤️ pela equipe de desenvolvimento.**