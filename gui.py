import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
from user import User
from schedule import Schedule

class ClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система Регистрации Поликлиники")
        self.schedule = Schedule()
        self.current_user = None
        self.main_screen()

    # Главный экран с выбором роли пользователя
    def main_screen(self):
        self.clear_screen()
        tk.Button(self.root, text="User", command=lambda: self.login("user")).pack()
        tk.Button(self.root, text="Admin", command=lambda: self.login("admin")).pack()

    # Экран ввода пароля
    def login(self, role):
        self.clear_screen()
        tk.Label(self.root, text="Введите пароль:").pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()
        tk.Button(self.root, text="Войти", command=lambda: self.check_login(role)).pack()

    # Проверка пароля и переход к меню в зависимости от роли
    def check_login(self, role):
        password = self.password_entry.get()
        if (role == 'user' and password == 'user') or (role == 'admin' and password == 'admin'):
            self.current_user = User(role)
            if self.current_user.is_user():
                self.user_menu()
            elif self.current_user.is_admin():
                self.admin_menu()
        else:
            messagebox.showerror("Ошибка", "Неверный пароль")

    # Меню для пользователя
    def user_menu(self):
        self.clear_screen()
        tk.Button(self.root, text="Просмотреть расписание врачей", command=self.view_schedule).pack()
        tk.Button(self.root, text="Записаться на прием", command=self.book_appointment).pack()
        tk.Button(self.root, text="Назад", command=self.main_screen).pack()

    # Меню для администратора
    def admin_menu(self):
        self.clear_screen()
        tk.Button(self.root, text="Добавить врача", command=self.add_doctor).pack()
        tk.Button(self.root, text="Редактировать расписание врачей", command=self.edit_doctor_schedule).pack()
        tk.Button(self.root, text="Назад", command=self.main_screen).pack()

    # Просмотр расписания врачей
    def view_schedule(self):
        self.clear_screen()
        doctors = self.schedule.get_doctors()
        for doctor in doctors:
            info = f"{doctor['full_name']} - {doctor['position']} - {doctor['work_time']}"
            tk.Label(self.root, text=info).pack()
        tk.Button(self.root, text="Назад", command=self.user_menu).pack()

    # Экран записи на прием
    def book_appointment(self):
        self.clear_screen()
        tk.Label(self.root, text="ФИО:").pack()
        self.patient_name = tk.Entry(self.root)
        self.patient_name.pack()
        tk.Label(self.root, text="Номер телефона:").pack()
        self.patient_phone = tk.Entry(self.root)
        self.patient_phone.pack()
        tk.Label(self.root, text="Адрес:").pack()
        self.patient_address = tk.Entry(self.root)
        self.patient_address.pack()
        tk.Label(self.root, text="Проблема:").pack()
        self.patient_problem = tk.Entry(self.root)
        self.patient_problem.pack()

        # Выпадающий список для выбора врача
        tk.Label(self.root, text="Врач:").pack()
        self.doctor_var = StringVar(self.root)
        self.doctor_var.set("Выберите врача")
        doctors = self.schedule.get_doctors()
        doctor_names = [doctor['full_name'] for doctor in doctors]
        self.doctor_menu = OptionMenu(self.root, self.doctor_var, *doctor_names)
        self.doctor_menu.pack()

        tk.Label(self.root, text="Дата и время приема:").pack()
        self.appointment_time = tk.Entry(self.root)
        self.appointment_time.pack()
        tk.Button(self.root, text="Записаться", command=self.submit_appointment).pack()
        tk.Button(self.root, text="Назад", command=self.user_menu).pack()

    # Подтверждение записи на прием
    def submit_appointment(self):
        patient_info = {
            'name': self.patient_name.get(),
            'phone': self.patient_phone.get(),
            'address': self.patient_address.get(),
            'problem': self.patient_problem.get(),
            'doctor': self.doctor_var.get(),
            'appointment_time': self.appointment_time.get()
        }

        # Проверка заполненности всех полей
        if any(value == "" for value in patient_info.values()) or patient_info['doctor'] == "Выберите врача":
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        # Добавление записи на прием в базу данных
        appointment = self.schedule.add_appointment(patient_info)
        messagebox.showinfo("Успех", f"Запись успешно создана для {appointment['name']} к {appointment['doctor']} на {appointment['appointment_time']}")
        self.user_menu()

    # Экран добавления нового врача
    def add_doctor(self):
        self.clear_screen()
        tk.Label(self.root, text="ФИО:").pack()
        self.doctor_name = tk.Entry(self.root)
        self.doctor_name.pack()
        tk.Label(self.root, text="Должность:").pack()
        self.doctor_position = tk.Entry(self.root)
        self.doctor_position.pack()
        tk.Label(self.root, text="Время работы:").pack()
        self.doctor_time = tk.Entry(self.root)
        self.doctor_time.pack()
        tk.Button(self.root, text="Добавить", command=self.submit_doctor).pack()
        tk.Button(self.root, text="Назад", command=self.admin_menu).pack()

    # Подтверждение добавления нового врача
    def submit_doctor(self):
        doctor_info = {
            'full_name': self.doctor_name.get(),
            'position': self.doctor_position.get(),
            'work_time': self.doctor_time.get()
        }

        # Проверка заполненности всех полей
        if any(value == "" for value in doctor_info.values()):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        # Добавление нового врача в базу данных
        doctor = self.schedule.add_doctor(**doctor_info)
        messagebox.showinfo("Успех", f"Врач добавлен: {doctor['full_name']} - {doctor['position']} - {doctor['work_time']}")
        self.admin_menu()

    # Экран выбора врача для редактирования
    def edit_doctor_schedule(self):
        self.clear_screen()
        doctors = self.schedule.get_doctors()
        for idx, doctor in enumerate(doctors):
            info = f"{idx}. {doctor['full_name']} - {doctor['position']} - {doctor['work_time']}"
            tk.Label(self.root, text=info).pack()
        tk.Label(self.root, text="Введите номер врача для редактирования:").pack()
        self.doctor_index = tk.Entry(self.root)
        self.doctor_index.pack()
        tk.Button(self.root, text="Редактировать", command=self.edit_selected_doctor).pack()
        tk.Button(self.root, text="Назад", command=self.admin_menu).pack()

    # Экран редактирования выбранного врача
    def edit_selected_doctor(self):
        try:
            idx = int(self.doctor_index.get())
            doctor = self.schedule.get_doctors()[idx]
        except (ValueError, IndexError):
            messagebox.showerror("Ошибка", "Некорректный номер")
            return

        self.clear_screen()
        tk.Label(self.root, text="Редактировать данные врача:").pack()
        tk.Label(self.root, text="ФИО:").pack()
        self.edit_name = tk.Entry(self.root)
        self.edit_name.insert(0, doctor['full_name'])
        self.edit_name.pack()
        tk.Label(self.root, text="Должность:").pack()
        self.edit_position = tk.Entry(self.root)
        self.edit_position.insert(0, doctor['position'])
        self.edit_position.pack()
        tk.Label(self.root, text="Время работы:").pack()
        self.edit_time = tk.Entry(self.root)
        self.edit_time.insert(0, doctor['work_time'])
        self.edit_time.pack()
        tk.Button(self.root, text="Сохранить", command=lambda: self.submit_edit_doctor(idx)).pack()
        tk.Button(self.root, text="Назад", command=self.admin_menu).pack()

    # Подтверждение изменений данных врача
    def submit_edit_doctor(self, idx):
        full_name = self.edit_name.get()
        position = self.edit_position.get()
        work_time = self.edit_time.get()
        updated_doctor = self.schedule.edit_doctor(idx, full_name, position, work_time)
        messagebox.showinfo("Успех", f"Данные врача обновлены: {updated_doctor}")
        self.admin_menu()

    # Очистка экрана
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicApp(root)
    root.mainloop()
