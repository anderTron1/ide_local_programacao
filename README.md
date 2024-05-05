#IDE LOCAL DE PROGRAMAÇÃO

## Tabela de Conteúdos

- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Créditos](#créditos)

## Instalação

Para configura a IDE, primeiramente instale o requirements.txt (sugiro colocar dentro de um venv).
Na primeira vez que vou usar, execute o comando python create_database.py -t 1B (1B é o nome da primeira turma que será criada, por isso é necessário executar o comando -t com o nome da turma) dessa forma, será criado uma database chamada users com duas tabelas, uma chamada users e outra chamada turma e para fazer o primeiro login, um usuario chamdado [admin] e uma  senha [123] será criado por padrão.

## Uso

Para executar o sistema colocar o código no terminal: python index.py.
Em outro terminal vai até a pasta onde estão as pastas dos alunos e execute o comando: twistd -n web --path ./
esse comando vai gerar um server para acessar a todos os arquivos das pastas dos alunos. Para cada aluno o professor tem que criar as pastas e arquivos que serão executados.
O sistema executa códigos: HTML, CSS E JAVASCRIPT
## Contribuição


## Licença

Este projeto é licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT), o que significa que é open-source e você é livre para usar, modificar e distribuir o código-fonte do projeto de acordo com os termos da licença.


## Créditos
Criado por: André Luiz 
Objetivo: para uso educacional no ensino de programação web
