#IDE LOCAL DE PROGRAMAÇÃO

## Tabela de Conteúdos

- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Créditos](#créditos)

## Instalação

Para configura a IDE, primeiramente instale o requirements.txt (sugiro colocar dentro de um venv).
Na primeira vez que vou usar execute o comando python create_database.py -d 2B. Neste exemplo, ele cria uma database chamada data_2B e uma pasta dentro do diretorio conteudos chamada 2B, você pode mudar o nome para a turma que você quer, ele vai criar um sqlite na pasta database
Dessa forma apenas fazer login com admin e senha 123 que ele cria por padrão e adicionar os usuarios desejados.
Cada usuario que for criado, ele cria uma pasta com o nome do usuario dentro da pasta que esta sendo executada o banco de dados, exemplo se vc esta usando o data_2B,e vocÊ for criar um novo usario, ele vai criar uma pasta com o nome do usuario na pasta 2B
## Uso
Antes de executar o codigo, configure as seguintes variaveis 

turma = '2B' aqui é o nome da turma que vai ficar na tela de login
diretory = 'conteudos\\2B' aqui a pasta
path_db = 'databases\\data_2B.sqlite'

Para executar apenas colocar no terminal python index.py.
Em outro terminal vai até a pasta onde estão as pastas dos alunos e execute o comando: twistd -n web --path ./
esse comando vai gerar um server para acesso a todos os arquivos das pastas dos alunos 

## Contribuição


## Licença

Este projeto é licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT), o que significa que é open-source e você é livre para usar, modificar e distribuir o código-fonte do projeto de acordo com os termos da licença.


## Créditos
