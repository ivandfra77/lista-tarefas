import argparse
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


def load_tasks():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def add_task(description):
    tasks = load_tasks()
    task = {"id": next_id(tasks), "description": description, "done": False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Tarefa {task['id']} adicionada: {description}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Nenhuma tarefa cadastrada.")
        return
    pendentes = [t for t in tasks if not t["done"]]
    concluidas = [t for t in tasks if t["done"]]

    ids_pendentes = ", ".join(str(t["id"]) for t in pendentes)
    ids_concluidas = ", ".join(str(t["id"]) for t in concluidas)
    print(f"Pendentes ({ids_pendentes}) Concluídas ({ids_concluidas})")
    print()

    tasks_ordenadas = pendentes + concluidas
    linhas = [f"[{'x' if t['done'] else ' '}] {t['id']}: {t['description']}" for t in tasks_ordenadas]
    print("\n\n".join(linhas))


def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"Tarefa {task_id} concluída.")
            return
    print(f"Tarefa {task_id} não encontrada.")


def remove_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Tarefa {task_id} não encontrada.")
        return
    save_tasks(new_tasks)
    print(f"Tarefa {task_id} removida.")


def build_parser():
    parser = argparse.ArgumentParser(description="Lista de tarefas simples")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Adicionar tarefa")
    add_parser.add_argument("description", nargs="+", help="Descrição da tarefa")

    subparsers.add_parser("list", help="Listar tarefas")

    done_parser = subparsers.add_parser("done", help="Concluir tarefa")
    done_parser.add_argument("id", type=int, help="ID da tarefa")

    remove_parser = subparsers.add_parser("remove", help="Remover tarefa")
    remove_parser.add_argument("id", type=int, help="ID da tarefa")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_task(" ".join(args.description))
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "remove":
        remove_task(args.id)


if __name__ == "__main__":
    main()
