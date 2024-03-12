
# Импортируем необходимые модули для создания графического пользовательского интерфейса и работы с файлами .doc и .xls
from tkinter import *
from tkinter import messagebox
# from docx import Document
# from openpyxl import Workbook


# Создаем класс, который будет отображать и обрабатывать основное окно программы
class MainApplication:
    def __init__(self, master):
        self.master = master
        master.title("Элементарные частицы")

        # Создаем метки, поля для ввода и кнопки для каждой элементарной частицы
        self.label_electron = Label(master, text="Электрон")
        self.label_electron.grid(row=0, column=0)
        self.entry_electron = Entry(master)
        self.entry_electron.grid(row=0, column=1)
        self.button_electron = Button(master, text="Рассчитать", command=self.calculate_electron)
        self.button_electron.grid(row=0, column=2)

        self.label_neutron = Label(master, text="Нейтрон")
        self.label_neutron.grid(row=1, column=0)
        self.entry_neutron = Entry(master)
        self.entry_neutron.grid(row=1, column=1)
        self.button_neutron = Button(master, text="Рассчитать", command=self.calculate_neutron)
        self.button_neutron.grid(row=1, column=2)

        self.label_proton = Label(master, text="Протон")
        self.label_proton.grid(row=2, column=0)
        self.entry_proton = Entry(master)
        self.entry_proton.grid(row=2, column=1)
        self.button_proton = Button(master, text="Рассчитать", command=self.calculate_proton)
        self.button_proton.grid(row=2, column=2)

        # Создаем кнопку для сохранения результатов
        self.button_save = Button(master, text="Сохранить результаты", command=self.save_results)
        self.button_save.grid(row=3, column=0, columnspan=3)

        # Создаем метку и поле для вывода результатов расчета удельного заряда и комптоновской длины волны
        self.label_results = Label(master, text="Результаты:")
        self.label_results.grid(row=4, column=0, columnspan=3)
        self.entry_results = Entry(master, state="readonly")
        self.entry_results.grid(row=5, column=0, columnspan=3)

    def calculate_electron(self):
        # Получаем введенное значение массы электрона и конвертируем его во float
        mass = float(self.entry_electron.get())

        # Расчитываем удельный заряд и комптоновскую длину волны для электрона
        specific_charge = -1.76e11
        compton_wavelength = (6.626e-34 / (mass * 9.109e-31)) * 1e9

        # Выводим результаты расчета в поле для результатов
        self.entry_results.configure(state="normal")
        self.entry_results.delete(0, END)
        self.entry_results.insert(0,
                                  f"Удельный заряд: {specific_charge} Кл/кг, Комптоновская длина волны: {compton_wavelength} нм")
        self.entry_results.configure(state="readonly")

    def calculate_neutron(self):
        # Получаем введенное значение массы нейтрона и конвертируем его во float
        mass = float(self.entry_neutron.get())

        # Расчитываем удельный заряд и комптоновскую длину волны для нейтрона
        specific_charge = 0
        compton_wavelength = (6.626e-34 / (mass * 1.675e-27)) * 1e9

        # Выводим результаты расчета в поле для результатов
        self.entry_results.configure(state="normal")
        self.entry_results.delete(0, END)
        self.entry_results.insert(0,
                                  f"Удельный заряд: {specific_charge} Кл/кг, Комптоновская длина волны: {compton_wavelength} нм")
        self.entry_results.configure(state="readonly")

    def calculate_proton(self):
        # Получаем введенное значение массы протона и конвертируем его во float
        mass = float(self.entry_proton.get())

        # Расчитываем удельный заряд и комптоновскую длину волны для протона
        specific_charge = 9.58e7
        compton_wavelength = (6.626e-34 / (mass * 1.673e-27)) * 1e9

        # Выводим результаты расчета в поле для результатов
        self.entry_results.configure(state="normal")
        self.entry_results.delete(0, END)
        self.entry_results.insert(0,
                                  f"Удельный заряд: {specific_charge} Кл/кг, Комптоновская длина волны: {compton_wavelength} нм")
        self.entry_results.configure(state="readonly")

    def save_results(self):
        # Проверяем заполнены ли все поля для результатов
        if self.entry_results.get() == "":
            messagebox.showerror("Ошибка", "Нет результатов для сохранения")
            return

        # Создаем новый документ .doc
        doc = Document()

        # Сохраняем результаты в документ .doc
        doc.add_paragraph("Результаты расчета элементарных частиц:")
        doc.add_paragraph(self.entry_results.get())
        doc.save("results.docx")

        # Создаем новую книгу .xls
        wb = Workbook()
        sheet = wb.active

        # Сохраняем результаты в книгу .xls
        sheet.append(["Результаты расчета элементарных частиц:"])
        sheet.append([self.entry_results.get()])
        wb.save("results.xlsx")

        messagebox.showinfo("Успех", "Результаты сохранены успешно")


# Создаем главное окно программы и запускаем его
root = Tk()
app = MainApplication(root)
root.mainloop()
