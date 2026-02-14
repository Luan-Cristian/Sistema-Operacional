import random
import sys
from collections import deque

STATE_READY = "Pronto"
STATE_RUNNING = "Executando"
STATE_BLOCKED = "Bloqueado"
STATE_FINISHED = "Finalizado"

class Process:
    def __init__(self, pid, name, cpu, mem, prio, arrival):
        self.pid = pid
        self.name = name
        self.cpu = cpu
        self.mem = mem
        self.prio = prio
        self.state = STATE_READY
        self.arrival = arrival

    def __repr__(self):
        return f"{self.pid} | {self.name} | {self.cpu} | {self.mem} | {self.prio} | {self.state}"

class Scheduler:
    def __init__(self):
        self.next_pid = 1
        self.processes = {}
        self.arrival_counter = 0

    def create(self, name):
        cpu = random.randint(1, 10)
        mem = random.randint(10, 200)
        prio = random.randint(1, 5)
        pid = self.next_pid
        self.next_pid += 1
        self.arrival_counter += 1
        p = Process(pid, name, cpu, mem, prio, self.arrival_counter)
        self.processes[pid] = p
        print(f"Processo criado: PID={pid}, nome='{name}', CPU={cpu}, MEM={mem}, PRIO={prio}, Estado={p.state}")
        return p

    def list_processes(self):
        if not self.processes:
            print("Nenhum processo criado.")
            return
        print("PID | Nome     | CPU | MEM | PRIO | Estado")
        for pid in sorted(self.processes.keys()):
            p = self.processes[pid]
            print(f"{p.pid:3d} | {p.name:8} | {p.cpu:3d} | {p.mem:3d} | {p.prio:4d} | {p.state}")

    def _ready_processes(self):
        return [p for p in self.processes.values() if p.state == STATE_READY]

    def block(self, pid):
        p = self.processes.get(pid)
        if not p:
            print("PID não encontrado.")
            return
        if p.state == STATE_BLOCKED:
            print("Processo já está bloqueado.")
            return
        if p.state == STATE_FINISHED:
            print("Processo já finalizado.")
            return
        p.state = STATE_BLOCKED
        print(f"Processo {pid} bloqueado.")

    def unblock(self, pid):
        p = self.processes.get(pid)
        if not p:
            print("PID não encontrado.")
            return
        if p.state != STATE_BLOCKED:
            print("Processo não está bloqueado.")
            return
        p.state = STATE_READY
        print(f"Processo {pid} desbloqueado (Pronto).")

    def kill(self, pid):
        p = self.processes.get(pid)
        if not p:
            print("PID não encontrado.")
            return
        if p.state == STATE_FINISHED:
            print("Processo já finalizado.")
            return
        p.state = STATE_FINISHED
        p.cpu = 0
        print(f"Processo {pid} finalizado (kill).")

    def run(self, algorithm):
        algo = algorithm.lower()
        valid = {"fifo", "sjf", "rr", "prio"}
        if algo not in valid:
            print("Algoritmo inválido. Use: fifo, sjf, rr, prio")
            return

        cycle = 0
        rr_quantum = 2

        def any_runnable():
            return any(p.state in (STATE_READY, STATE_RUNNING) for p in self.processes.values())

        if algo == "rr":
            rr_queue = deque(sorted([p for p in self.processes.values() if p.state == STATE_READY],
                                    key=lambda x: x.arrival))
        print(f"Executando por {algo.upper()}...")
        while True:
            ready = [p for p in self.processes.values() if p.state == STATE_READY]
            if not ready and (algo != "rr" or not rr_queue):
                if not any_runnable():
                    break

            cycle += 1
            selected = None
            if algo == "fifo":
                ready_list = sorted([p for p in self.processes.values() if p.state == STATE_READY],
                                     key=lambda x: x.arrival)
                selected = ready_list[0] if ready_list else None
                cycles_to_run = 1
            elif algo == "sjf":
                ready_list = sorted([p for p in self.processes.values() if p.state == STATE_READY],
                                     key=lambda x: (x.cpu, x.arrival))
                selected = ready_list[0] if ready_list else None
                cycles_to_run = 1
            elif algo == "prio":
                ready_list = sorted([p for p in self.processes.values() if p.state == STATE_READY],
                                     key=lambda x: (x.prio, x.arrival))
                selected = ready_list[0] if ready_list else None
                cycles_to_run = 1
            elif algo == "rr":
                while rr_queue and rr_queue[0].state != STATE_READY:
                    rr_queue.popleft()
                if rr_queue:
                    selected = rr_queue[0]
                    cycles_to_run = min(rr_quantum, selected.cpu)
                else:
                    selected = None
                    cycles_to_run = 0
            else:
                selected = None
                cycles_to_run = 0

            if not selected:
                print(f"[Ciclo {cycle}] Nenhum processo pronto para executar neste ciclo.")
                if not any(p.state == STATE_READY for p in self.processes.values()):
                    break
                else:
                    continue

            quantum_used = 0
            while quantum_used < cycles_to_run:
                selected.state = STATE_RUNNING
                selected.cpu -= 1
                quantum_used += 1
                print(f"[Ciclo {cycle}] -> Executando {selected.name} (PID {selected.pid}) - CPU restante: {selected.cpu}")
                self._print_status_line()
                cycle += 1

                if selected.cpu <= 0:
                    selected.cpu = 0
                    selected.state = STATE_FINISHED
                    print(f"✓ Processo {selected.pid} finalizado!")
                    break

                if algo == "rr" and quantum_used >= cycles_to_run:
                    selected.state = STATE_READY

            if algo == "rr" and selected and selected.state == STATE_READY and selected.cpu > 0:
                if rr_queue and rr_queue[0] is selected:
                    rr_queue.popleft()
                    rr_queue.append(selected)
            else:
                if selected and selected.state == STATE_RUNNING:
                    if selected.cpu <= 0:
                        selected.state = STATE_FINISHED
                        selected.cpu = 0
                    else:
                        selected.state = STATE_READY

        print("Simulação finalizada.")

    def _print_status_line(self):
        lines = []
        for pid in sorted(self.processes.keys()):
            p = self.processes[pid]
            lines.append(f"{p.pid}:{p.state[0]}(CPU={p.cpu})")
        print("Estados: " + " | ".join(lines))

def main_loop():
    sched = Scheduler()
    print("Mini Simulador de Escalonador - comandos: create <nome>, list, run <fifo|sjf|rr|prio>, block <pid>, unblock <pid>, kill <pid>, exit")
    while True:
        try:
            cmd = input("SO> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando.")
            break
        if not cmd:
            continue
        parts = cmd.split()
        c = parts[0].lower()

        if c == "create":
            if len(parts) < 2:
                print("Uso: create <nome>")
                continue
            name = " ".join(parts[1:])
            sched.create(name)
        elif c == "list":
            sched.list_processes()
        elif c == "run":
            if len(parts) != 2:
                print("Uso: run <fifo|sjf|rr|prio>")
                continue
            sched.run(parts[1])
        elif c == "block":
            if len(parts) != 2 or not parts[1].isdigit():
                print("Uso: block <PID>")
                continue
            sched.block(int(parts[1]))
        elif c == "unblock":
            if len(parts) != 2 or not parts[1].isdigit():
                print("Uso: unblock <PID>")
                continue
            sched.unblock(int(parts[1]))
        elif c == "kill":
            if len(parts) != 2 or not parts[1].isdigit():
                print("Uso: kill <PID>")
                continue
            sched.kill(int(parts[1]))
        elif c == "exit":
            print("Encerrando o sistema.")
            break
        else:
            print("Comando desconhecido.")

if __name__ == "__main__":
    main_loop()