# Desafio Python - Instruct

* [Magpy](https://desafiomagpy-instruct.herokuapp.com/api/projects/)

Esse projeto consiste na resolução do desafio proposto pela Instruct, onde foi solicitado o desenvolvimento da MagPy, uma API REST que gerencia uma coleção de projetos. No qual o projeto tem um nome e uma lista de pacotes e cada pacote tem um nome e uma versão.
## Aplicação
O projeto foi desenvolvido com as ferramentas: Python e Django.
Para o desenvolvimento, foi solicitado o clone do [repositório](https://github.com/instruct-br/teste-python-jr-remoto-2021-06), e para que a Magpy funcione corretamente foi criado funções para sobrescrever os metódos padrões de requisição HTPP.

## Utilidade
O Magpy tem utilidade para o gerenciamento de pacotes de projetos, onde é possível ter a gestão de quais pacotes se encontram no projeto e o quão atual ele está. Além de validar sua existência e caso não seja fornecida a versão daquele pacote, é retornado a sua versão mais atual.
## Testes

Há duas maneiras de realizar os testes básicos deste projeto:

* 1ª maneira:
1. Clone o repositório através do comando "git clone https://github.com/Jennysoares/DesafioPython-Instruct.git"
2. Abra o CMD na pasta onde foi clonado o repositório.
3. Execute o comando "k6 run -e API_BASE="[endereço base]" tests-open.js"

* 2ª maneira:
1. Baixe o [k6](https://k6.io/) no seu sistema operacional
2. Baixe o arquivo [teste-open.js](https://github.com/instruct-br/teste-python-jr-remoto-2021-06/blob/main/tests-open.js)
3. Com os dois abra o CMD e execute o comando "k6 run -e API_BASE="https://desafiomagpy-instruct.herokuapp.com/" tests-open.js"

* * Para realizar testes na aplicação, basta utilizar alguma ferramenta API Client como por exemplo o "Postman" passando a URL request "https://desafiomagpy-instruct.herokuapp.com/api/projects/" Ou utilizar o [Swagger](https://desafiomagpy-instruct.herokuapp.com/) 