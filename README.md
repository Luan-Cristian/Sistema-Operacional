# 🖥️ Mini Simulador de Escalonador de Processos

## 📌 Descrição

Este projeto foi desenvolvido como atividade acadêmica e consiste na implementação de um **mini simulador de escalonador de processos**, inspirado no funcionamento de sistemas operacionais.

O sistema permite:

- Criar processos com atributos aleatórios
- Listar processos ativos
- Simular execução com diferentes algoritmos de escalonamento
- Bloquear, desbloquear e finalizar processos
- Visualizar estados durante a simulação

---

## 🎯 Objetivo Acadêmico

Simular conceitos fundamentais de **Sistemas Operacionais**, como:

- Estados de processos (Pronto, Executando, Bloqueado, Finalizado)
- Escalonamento de CPU
- Gerenciamento de fila de execução
- Políticas de escalonamento

---

## ⚙️ Algoritmos Implementados

O simulador suporta os seguintes algoritmos:

### 🔹 FIFO (First In, First Out)
Executa processos na ordem de chegada.

### 🔹 SJF (Shortest Job First)
Executa primeiro o processo com menor tempo de CPU restante.

### 🔹 PRIO (Prioridade)
Executa o processo com maior prioridade (menor valor numérico).

### 🔹 RR (Round Robin)
Executa processos em ciclos com quantum fixo de 2 ciclos por vez.

---

## 🧠 Estados dos Processos

| Estado      | Descrição                      |
|-------------|--------------------------------|
| Pronto      | Aguardando execução            |
| Executando  | Está utilizando a CPU          |
| Bloqueado   | Suspenso temporariamente       |
| Finalizado  | Processo encerrado             |

---

## 🛠 Estrutura do Processo

Cada processo possui:

- PID (Identificador único incremental)
- Nome
- Tempo de CPU restante (gerado aleatoriamente de 1 a 10)
- Uso de memória (10 a 200)
- Prioridade (1 a 5)
- Estado atual
- Ordem de chegada

---

## 🚀 Como Executar

### 1️⃣ Execute o arquivo Python

```bash
python nome_do_arquivo.py
