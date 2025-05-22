# Professor Girafales Diretor - Teste de Consultas SQL e Horários

Este projeto contém um script Python que simula o gerenciamento de horários escolares usando SQLite em memória.

## O que o script faz

1. Cria um banco de dados em memória com tabelas para departamentos, professores, prédios, salas, disciplinas, turmas e horários das aulas.
2. Insere dados de exemplo, incluindo professores, salas e aulas.
3. Realiza consultas SQL para:
   - Calcular a quantidade de horas comprometidas em aulas para cada professor.
   - Listar os horários ocupados por sala.
4. Usa lógica em Python para calcular os horários livres em cada sala, considerando o expediente das 08:00 às 18:00 de segunda a sexta-feira.

## Como executar

- Requisitos: Python 3.x
- Rodar o script:

```bash
python main.py

Saída esperada
O script imprime no console:

Horas comprometidas por professor.

Horários ocupados por sala.

Horários livres por sala.

Feito por André Azevedo de Oliveira
