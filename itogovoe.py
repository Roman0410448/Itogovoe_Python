import json
from datetime import datetime

class Note:
    def __init__(self, id, title, body, timestamp):
        self.id = id
        self.title = title
        self.body = body
        self.timestamp = timestamp

class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.file_path, 'r') as file:
                notes_data = json.load(file)
                notes = []
                for note_data in notes_data:
                    note = Note(note_data['id'], note_data['title'], note_data['body'], note_data['timestamp'])
                    notes.append(note)
                return notes
        except FileNotFoundError:
            return []

    def save_notes(self):
        notes_data = []
        for note in self.notes:
            note_data = {'id': note.id, 'title': note.title, 'body': note.body, 'timestamp': note.timestamp}
            notes_data.append(note_data)
        with open(self.file_path, 'w') as file:
            json.dump(notes_data, file, indent=4)

    def create_note(self, title, body):
        id = len(self.notes) + 1
        timestamp = datetime.now().isoformat()
        note = Note(id, title, body, timestamp)
        self.notes.append(note)
        self.notes.sort(key=lambda x: x.timestamp)
        self.save_notes()
        print("Заметка создана")

    def read_notes(self):
        for note in self.notes:
            print(f"ID: {note.id}")
            print(f"Title: {note.title}")
            print(f"Body: {note.body}")
            print(f"Timestamp: {note.timestamp}")
            print()

    def update_note(self, id, title, body):
        for note in self.notes:
            if note.id == id:
                note.title = title
                note.body = body
                note.timestamp = datetime.now().isoformat()
                self.notes.sort(key=lambda x: x.timestamp)
                self.save_notes()
                print("Заметка обновлена")
                return
        print("Заметка с указанным ID не найдена")

    def delete_note(self, id):
        note_found = False
        for note in self.notes:
            if note.id == id:
                self.notes.remove(note)
                note_found = True
                break
        if note_found:
            # Перезаписываем ID после удаления заметки
            for i, note in enumerate(self.notes):
                note.id = i + 1
            self.save_notes()
            print("Заметка удалена")
        else:
            print("Заметка с указанным ID не найдена")


file_path = "notes.json"
note_manager = NoteManager(file_path)

while True:
    print("1. Просмотреть список заметок")
    print("2. Создать заметку")
    print("3. Редактировать заметку")
    print("4. Удалить заметку")
    print("5. Выход")

    choice = input("Выберите действие: ")

    if choice == "1":
        note_manager.read_notes()
    elif choice == "2":
        title = input("Введите заголовок заметки: ")
        body = input("Введите текст заметки: ")
        note_manager.create_note(title, body)
    elif choice == "3":
        id = int(input("Введите ID заметки для редактирования: "))
        title = input("Введите новый заголовок заметки: ")
        body = input("Введите новый текст заметки: ")
        note_manager.update_note(id, title, body)
    elif choice == "4":
        id = int(input("Введите ID заметки для удаления: "))
        note_manager.delete_note(id)
    elif choice == "5":
        break
    else:
        print("Некорректный выбор. Повторите попытку")
        
    print()