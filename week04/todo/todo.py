import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("todo.json")


def load_todos():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            todos = json.load(file)
        return todos if isinstance(todos, list) else []
    except (json.JSONDecodeError, OSError):
        print("todo.json을 읽을 수 없어 빈 목록으로 시작합니다.")
        return []


def save_todos(todos):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(todos, file, ensure_ascii=False, indent=2)


def show_todos(todos):
    if not todos:
        print("등록된 할 일이 없습니다.")
        return

    print("\n할 일 목록")
    print("-" * 30)
    for todo in todos:
        status = "완료" if todo["completed"] else "미완료"
        print(f"{todo['id']}. [{status}] {todo['title']}")
    print("-" * 30)


def find_todo(todos, todo_id):
    return next((todo for todo in todos if todo["id"] == todo_id), None)


def read_todo_id():
    try:
        return int(input("할 일 번호를 입력하세요: ").strip())
    except ValueError:
        print("번호는 숫자로 입력하세요.")
        return None


def add_todo(todos):
    title = input("추가할 할 일을 입력하세요: ").strip()
    if not title:
        print("할 일 내용을 입력해야 합니다.")
        return

    next_id = max((todo["id"] for todo in todos), default=0) + 1
    todos.append({"id": next_id, "title": title, "completed": False})
    save_todos(todos)
    print("할 일이 추가되었습니다.")


def complete_todo(todos):
    todo_id = read_todo_id()
    if todo_id is None:
        return

    todo = find_todo(todos, todo_id)
    if todo is None:
        print("해당 번호의 할 일을 찾을 수 없습니다.")
        return

    todo["completed"] = True
    save_todos(todos)
    print("할 일이 완료 처리되었습니다.")


def delete_todo(todos):
    todo_id = read_todo_id()
    if todo_id is None:
        return

    todo = find_todo(todos, todo_id)
    if todo is None:
        print("해당 번호의 할 일을 찾을 수 없습니다.")
        return

    todos.remove(todo)
    save_todos(todos)
    print("할 일이 삭제되었습니다.")


def main():
    todos = load_todos()

    while True:
        print("\n===== 할 일 목록 =====")
        print("1. 할 일 추가")
        print("2. 할 일 목록 보기")
        print("3. 할 일 완료 표시")
        print("4. 할 일 삭제")
        print("5. 종료")

        choice = input("메뉴를 선택하세요: ").strip()
        if choice == "1":
            add_todo(todos)
        elif choice == "2":
            show_todos(todos)
        elif choice == "3":
            complete_todo(todos)
        elif choice == "4":
            delete_todo(todos)
        elif choice == "5":
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 메뉴 번호를 선택하세요.")


if __name__ == "__main__":
    main()