import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

# База данных (вместо настоящей базы данных будем использовать словари)
doctors = {}
appointments = []

# Функции для пользователей
def view_schedule():
    schedule_window = tk.Toplevel(root)
    schedule_window.title("Расписание врачей")
    
    for doc_id, doc_info in doctors.items():
        doc_label = tk.Label(schedule_window, text=f"ID: {doc_id}, {doc_info['name']}, {doc_info['position']}, Время работы: {doc_info['schedule']}")
        doc_label.pack()

def book_appointment():
    book_window = tk.Toplevel(root)
    book_window.title("Запись на прием")
    
    tk.Label(book_window, text="ФИО:").pack()
    patient_name = tk.Entry(book_window)
    patient_name.pack()
    
    tk.Label(book_window, text="Номер телефона:").pack()
    patient_phone = tk.Entry(book_window)
    patient_phone.pack()
    
    tk.Label(book_window, text="Адрес:").pack()
    patient_address = tk.Entry(book_window)
    patient_address.pack()
    
    tk.Label(book_window, text="Проблема:").pack()
    patient_problem = tk.Entry(book_window)
    patient_problem.pack()
    
    tk.Label(book_window, text="ID Врача:").pack()
    doctor_id = tk.Entry(book_window)
    doctor_id.pack()
    
    tk.Label(book_window, text="Дата и время приема:").pack()
    appointment_time = tk.Entry(book_window)
    appointment_time.pack()
    
    def submit_appointment():
        appointment = {
            "name": patient_name.get(),
            "phone": patient_phone.get(),
            "address": patient_address.get(),
            "problem": patient_problem.get(),
            "doctor_id": doctor_id.get(),
            "time": appointment_time.get()
        }
        appointments.append(appointment)
        messagebox.showinfo("Успех", f"Запись прошла успешно: {appointment}")
        book_window.destroy()
    
    tk.Button(book_window, text="Записаться", command=submit_appointment).pack()

# Функции для администраторов
def add_doctor():
    add_window = tk.Toplevel(root)
    add_window.title("Добавить врача")
    
    tk.Label(add_window, text="ФИО:").pack()
    doctor_name = tk.Entry(add_window)
    doctor_name.pack()
    
    tk.Label(add_window, text="Должность:").pack()
    doctor_position = tk.Entry(add_window)
    doctor_position.pack()
    
    tk.Label(add_window, text="Время приема:").pack()
    doctor_schedule = tk.Entry(add_window)
    doctor_schedule.pack()
    
    def submit_doctor():
        doc_id = len(doctors) + 1
        doctors[doc_id] = {
            "name": doctor_name.get(),
            "position": doctor_position.get(),
            "schedule": doctor_schedule.get()
        }
        messagebox.showinfo("Успех", f"Добавлен врач: ID: {doc_id}, {doctor_name.get()}, {doctor_position.get()}, {doctor_schedule.get()}")
        add_window.destroy()
    
    tk.Button(add_window, text="Добавить", command=submit_doctor).pack()

def edit_schedule():
    edit_window = tk.Toplevel(root)
    edit_window.title("Редактировать расписание")
    
    doc_id = simpledialog.askinteger("ID Врача", "Введите ID врача:")
    
    if doc_id in doctors:
        doctor = doctors[doc_id]
        
        tk.Label(edit_window, text=f"ФИО ({doctor['name']}):").pack()
        doctor_name = tk.Entry(edit_window)
        doctor_name.insert(0, doctor['name'])
        doctor_name.pack()
        
        tk.Label(edit_window, text=f"Должность ({doctor['position']}):").pack()
        doctor_position = tk.Entry(edit_window)
        doctor_position.insert(0, doctor['position'])
        doctor_position.pack()
        
        tk.Label(edit_window, text=f"Время приема ({doctor['schedule']}):").pack()
        doctor_schedule = tk.Entry(edit_window)
        doctor_schedule.insert(0, doctor['schedule'])
        doctor_schedule.pack()
        
        def submit_changes():
            changes = []
            if doctor_name.get() != doctor['name']:
                changes.append(f"ФИО: {doctor['name']} -> {doctor_name.get()}")
                doctor['name'] = doctor_name.get()
            if doctor_position.get() != doctor['position']:
                changes.append(f"Должность: {doctor['position']} -> {doctor_position.get()}")
                doctor['position'] = doctor_position.get()
            if doctor_schedule.get() != doctor['schedule']:
                changes.append(f"Время приема: {doctor['schedule']} -> {doctor_schedule.get()}")
                doctor['schedule'] = doctor_schedule.get()
            
            if changes:
                messagebox.showinfo("Успех", f"Изменены данные: {', '.join(changes)}")
            else:
                messagebox.showinfo("Нет изменений", "Данные не были изменены.")
            edit_window.destroy()
        
        tk.Button(edit_window, text="Сохранить изменения", command=submit_changes).pack()
    else:
        messagebox.showerror("Ошибка", "Врач с таким ID не найден.")
        edit_window.destroy()

# Главная страница
def main():
    global root
    root = tk.Tk()
    root.title("Регистратура поликлиники")

    tk.Label(root, text="Выберите тип пользователя:").pack()
    
    tk.Button(root, text="Пользователь", command=user_mode).pack()
    tk.Button(root, text="Администратор", command=admin_mode).pack()
    
    root.mainloop()

def user_mode():
    user_window = tk.Toplevel(root)
    user_window.title("Пользователь")
    
    tk.Button(user_window, text="Просмотреть расписание врачей", command=view_schedule).pack()
    tk.Button(user_window, text="Записаться на прием", command=book_appointment).pack()

def admin_mode():
    admin_window = tk.Toplevel(root)
    admin_window.title("Администратор")
    
    tk.Button(admin_window, text="Добавить врача", command=add_doctor).pack()
    tk.Button(admin_window, text="Редактировать расписание", command=edit_schedule).pack()

if __name__ == "__main__":
    main()

