import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timetable Tool")

        self.root.configure(bg="grey")

        self.file_path_var = tk.StringVar()
        self.selected_year_var = tk.StringVar()
        self.selected_code_var = tk.StringVar()

        self.warning_label = tk.Label(root, text="", fg="red", bg="grey")
        self.warning_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        file_label = tk.Label(root, text="CSV File Path:", bg="grey", fg="white", font="italic")
        file_label.grid(row=1, column=0, padx=10, pady=10)

        self.file_entry = tk.Entry(root, textvariable=self.file_path_var, width=30)
        self.file_entry.grid(row=1, column=1, padx=10, pady=10)

        browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        browse_button.grid(row=1, column=2, padx=10, pady=10)

        year_label = tk.Label(root, text="Select Year:", bg="grey", fg="white", font="italic")
        year_label.grid(row=2, column=1, padx=10, pady=10)

        year_combobox = ttk.Combobox(root, textvariable=self.selected_year_var, values=["1", "2", "3", "4"])
        year_combobox.grid(row=3, column=1, padx=10, pady=10)

        code_label = tk.Label(root, text="Department:", bg="grey", fg="white", font="italic")
        code_label.grid(row=2, column=3, padx=10, pady=10)

        code_combobox = ttk.Combobox(root, textvariable=self.selected_code_var, values=["CS", "EE", "UNI"])
        code_combobox.grid(row=3, column=3, padx=10, pady=10)

        display_button = tk.Button(root, text="Display", command=self.display_courses, width=15)
        display_button.grid(row=5, column=1, columnspan=4, padx=10, pady=10)

        courses_label = tk.Label(root, text="Courses :", bg="grey", fg="white", font=("italic", 15))
        courses_label.grid(row=6, column=1, columnspan=1, padx=10, pady=10)

        self.course_listbox = tk.Listbox(root, height=10, width=50, selectmode=tk.MULTIPLE)
        self.course_listbox.grid(row=7, column=1, columnspan=2, padx=10, pady=10)

        add_button = tk.Button(root, text="Add Course", command=self.add_course, font="italic")
        add_button.grid(row=8, column=0, padx=10, pady=10)

        clear_button = tk.Button(root, text="Clear Timetable", command=self.clear_timetable, font="italic")
        clear_button.grid(row=8, column=2, columnspan=3, padx=10, pady=10)

        save_button = tk.Button(root, text="Save Timetable", command=self.save_timetable, font="italic")
        save_button.grid(row=9, column=1, columnspan=2, padx=10, pady=10)

        # List to store timetable data
        self.timetable_data = set()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path_var.set(file_path)

    def display_courses(self):
        file_path = self.file_path_var.get()
        if not file_path:
            self.show_warning("Please choose a file.")
            return

        selected_year = self.selected_year_var.get()
        selected_code = self.selected_code_var.get()

        if not selected_year and not selected_code:
            self.show_warning("Please select a year, code, or both.")
            return

        # Read and process the CSV file
        try:
            with open(file_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                matching_courses = []

                for row in reader:
                    course_code = row[0]
                    course_name = row[1]
                    course_time = row[2]

                    # Check if the course matches the selected criteria
                    if (not selected_year or selected_year in course_code) and (
                            not selected_code or (
                            selected_code.upper() == 'UNI' or selected_code.lower() in course_code.lower())):
                        matching_courses.append((course_code, course_name, course_time))

                # Display matching courses in the listbox
                self.course_listbox.delete(0, tk.END)
                if matching_courses:
                    for course in matching_courses:
                        self.course_listbox.insert(tk.END, f"{course[0]}: {course[1]} ({course[2]})")
                else:
                    self.show_warning(f"No matching courses found for year={selected_year}, code={selected_code}")

                self.show_warning("")  # Clear any previous warnings.
        except Exception as e:
            self.show_warning(f"Error reading CSV file: {str(e)}")

    def add_course(self):
        selected_indices = self.course_listbox.curselection()
        if len(selected_indices) == 0:
            self.show_warning("Please select a course.")
            return

        for index in selected_indices:
            full_course_info = self.course_listbox.get(index)
            # Extract course code, name, and time
            course_parts = full_course_info.split(":")
            course_code = course_parts[0].strip()
            course_info = course_parts[1].split("(")
            course_name = course_info[0].strip()
            course_time = course_info[1].replace(")", "").strip()

            course = (course_code, course_name, course_time)

            if course in self.timetable_data:
                self.show_warning("Course already added to the timetable.")
                return

        if len(self.timetable_data) + len(selected_indices) > 6:
            self.show_warning("You can select at most 6 courses.")
            return

        for index in selected_indices:
            full_course_info = self.course_listbox.get(index)
            # Extract course code, name, and time
            course_parts = full_course_info.split(":")
            course_code = course_parts[0].strip()
            course_info = course_parts[1].split("(")
            course_name = course_info[0].strip()
            course_time = course_info[1].replace(")", "").strip()

            course = (course_code, course_name, course_time)
            self.timetable_data.add(course)

        self.show_warning("")  # Clear any previous warnings

    def clear_timetable(self):
        # Clear the timetable data and the listbox
        self.timetable_data.clear()
        self.course_listbox.delete(0, tk.END)

    def save_timetable(self):
        if not self.timetable_data:
            self.show_warning("Please add courses to the timetable before saving.")
            return

        # Save the timetable data to a CSV file
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if save_path:
            with open(save_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for course in self.timetable_data:
                    writer.writerow(course)
            messagebox.showinfo("Timetable Saved", "Timetable has been saved successfully.")

    def show_warning(self, message):
        self.warning_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()