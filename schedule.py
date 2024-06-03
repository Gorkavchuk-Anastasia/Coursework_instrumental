from database import load_database, save_database

class Schedule:
    def __init__(self):
        self.db = load_database()

    def add_doctor(self, full_name, position, work_time):
        new_doctor = {
            'full_name': full_name,
            'position': position,
            'work_time': work_time
        }
        self.db['doctors'].append(new_doctor)
        save_database(self.db)
        return new_doctor

    def edit_doctor(self, doctor_index, full_name=None, position=None, work_time=None):
        doctor = self.db['doctors'][doctor_index]
        if full_name:
            doctor['full_name'] = full_name
        if position:
            doctor['position'] = position
        if work_time:
            doctor['work_time'] = work_time
        save_database(self.db)
        return doctor

    def get_doctors(self):
        return self.db['doctors']

    def add_appointment(self, patient_info):
        self.db['appointments'].append(patient_info)
        save_database(self.db)
        return patient_info

    def get_appointments(self):
        return self.db['appointments']
