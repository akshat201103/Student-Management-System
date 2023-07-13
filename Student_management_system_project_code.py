from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.text import Text
from enum import Enum
import matplotlib.pyplot as plt
import os
import pyfiglet
import numpy as np
import time
from rich.progress import Progress
from rich.panel import Panel
from pyfiglet import Figlet

class Action(Enum):
    ADD = "add" 
    REMOVE = "remove" 
    AVG_ATT = "avg att"
    AVG_GEN = "avg gender"
    SHOW_HIGH = "high"
    UPDATE = "update" 
    CLEAR = "clear"
    ENROLL = "enroll"
    SHOW_table="show_table"

class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.console = Console()
        self.next_id = 12221098
        self.console.print(pyfiglet.figlet_format("Student Management System", font="slant"), style="bold red")
        self.course_criteria = {'CSE': 75, 'BBA': 60, 'MCA': 80, 'BCA': 70}

    def add_student(self, name, surname, gender, age, course, attendance, performance, fathers_name, mothers_name, phone_number, parents_phone_number, address):
        rprint( Panel(Text("ADDING NEW STUDENT RECORDS ", justify="center",overflow="fold",style="on black")))
        self.students[self.next_id] = {'name': name.upper(), 
                                        'surname': surname.upper(), 
                                        'gender': gender.upper(),
                                        'age': age, 
                                        'course': course.upper(), 
                                        'attendance': int(attendance), 
                                        'performance': float(performance), 
                                        'fathers_name': fathers_name, 
                                        'mothers_name': mothers_name, 
                                        'phone_number': phone_number, 
                                        'parents_phone_number': parents_phone_number, 
                                        'address': address}
        self.next_id += 1
        rprint(Text(f"Successfully added student: {name}", style="bold green"))

    def remove_student(self, id):
        rprint( Panel(Text("REMOVING STUDENT FROM RECORD ", justify="center",overflow="fold",style="on black")))

        if int(id) in self.students:
            del self.students[int(id)]
            rprint(Text(f"Successfully removed student with ID: {id}", style="bold red"))
        else:
            rprint(Text(f"No student found with ID: {id}", style="bold yellow"))
   

    def update_student(self, id, attribute, new_value):
        rprint( Panel(Text("UPDATING STUDENT DATA IN  RECORD ", justify="center",overflow="fold",style="on black")))

        if int(id) in self.students:
            student = self.students[int(id)]
            if attribute in student:
                student[attribute] = new_value
                rprint(Text(f"Student with ID {id} updated successfully.", style="bold green"))
            else:
                rprint(Text(f"Invalid attribute: {attribute}", style="bold yellow"))
        else:
            rprint(Text(f"No student found with ID: {id}", style="bold yellow"))


    


    def print_students(self):
        print()
        rprint(Panel(Text("SHOWING THE STUDENT RECORDS ", justify="center", overflow="fold", style="underline bold on black")))
        print()
        table = Table(show_header=True, header_style="yellow on black")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Surname")
        table.add_column("Gender")
        table.add_column("Age")
        table.add_column("Course")
        table.add_column("Attendance (%)")
        table.add_column("Performance")
        table.add_column("Father's Name")
        table.add_column("Mother's Name")
        table.add_column("Phone Number")
        table.add_column("Parents Phone Number")
        table.add_column("Address")
    
        for id, student in self.students.items():
            
            row_style = "green on black"
    
            table.add_row(str(id),
                          student['name'],
                          student['surname'],
                          student['gender'],
                          str(student['age']),
                          student['course'],
                          str(student['attendance']),
                          str(student['performance']),
                          student['fathers_name'],
                          student['mothers_name'],
                          student['phone_number'],
                          student['parents_phone_number'],
                          student['address'], style=row_style)
            table.add_row("", "", "", "", "", "", "", "", "", "", "", "", "", end_section=True)
    
        self.console.print(table)
    

    def average_attendance(self):
        rprint( Panel(Text("AVERAGE ATTENDANCE PER COURSE", justify="center",overflow="fold",style="underline bold on black")))

        course_attendance = defaultdict(list)
        for student in self.students.values():
            course_attendance[student['course']].append(student['attendance'])

        avg_attendance = {course: sum(attendance) / len(attendance) for course, attendance in course_attendance.items()}

        # Plotting
        labels = avg_attendance.keys()
        sizes = avg_attendance.values()

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax1.axis('equal')  
        plt.title('Average Attendance by Course')
        plt.show()

    def enroll_student(self):
        rprint(Panel(Text("ENROLLING A NEW STUDENT", justify="center", overflow="fold", style="underline bold on black")))
    
        while True:
            print("Enter student details:")
            name = input("Name: ")
            surname=input("Surname: ")
            age = int(input("Age: "))
            gender = input("Gender: ")
            scholarship = input("Apply for Scholarship? (yes/no): ")
            tenth_grade = float(input("10th Grade(%): "))
            twelfth_grade = float(input("12th Grade(%): "))
    
            avg_grade = (tenth_grade + twelfth_grade) / 2
    
            eligible_courses = [course for course, criteria in self.course_criteria.items() if avg_grade >= criteria]
    
            if eligible_courses:
                rprint(Text(f"Student {name} is eligible for the following courses: {', '.join(eligible_courses)}", style="bold green"))
                course = input("Enter the course to enroll in: ")
                # attendance = "None"
                # performance = "None"
                fathers_name = input("Enter Father's Name: ")
                mothers_name = input("Enter Mother's Name: ")
                phone_number = input("Enter Phone Number: ")
                parents_phone_number = input("Enter Parents Phone Number: ")
                address = input("Enter Address: ")
    
                self.add_student(name, surname, gender, age, course, 0,0 , fathers_name, mothers_name, phone_number, parents_phone_number, address)
            else:
                rprint(Text(f"Sorry, Student {name} is not eligible for any courses.", style="bold red"))
    
            another_student = input("Do you want to enroll another student? (yes/no): ")
            if another_student.lower() != "yes":
                break
       

    def clear_console(self):
        rprint( Panel(Text("CLEARING THE RECORD", justify="center",overflow="fold",style="underline bold on black")))
        os.system('cls' if os.name == 'nt' else 'clear')

    def average_gender(self):
        gender_counts = defaultdict(int)
        for student in self.students.values():
            gender_counts[student['gender']] += 1

        # Plotting
        labels = gender_counts.keys()
        sizes = gender_counts.values()

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax1.axis('equal')  
        plt.title('Average Gender Distribution')
        plt.show()

    def show_highest_performance(self):
        rprint( Panel(Text("HIGHEST PERFORMANCE STUDENT ", justify="center",overflow="fold",style="underline bold on black")))
        max_performance = np.max([student['performance'] for student in self.students.values()])
        highest_performers = {id: student for id, student in self.students.items() if student['performance'] == max_performance}
        rprint(Text(f"Students with highest performance grade ({max_performance}):", style="bold blue"))
        for id, student in highest_performers.items():
            rprint(Text(f"{student['name']} {student['surname']} - Course: {student['course']} - ID: {id}", style="bold blue"))


    def show_lowest_performance(self):
        rprint( Panel(Text("LOWEST PERFORMANCE STUDENT ", justify="center",overflow="fold",style="underline bold on black")))

        max_performance = np.min([student['performance'] for student in self.students.values()])
        highest_performers = {id: student for id, student in self.students.items() if student['performance'] == max_performance}
        rprint(Text(f"Students with highest performance grade ({max_performance}):", style="bold blue"))
        for id, student in highest_performers.items():
            rprint(Text(f"{student['name']} {student['surname']} - Course: {student['course']} - ID: {id}", style="bold blue"))



    def query(self, command):
        # action take the first word as input and remaining input is taken by the *args
        action, *args = command.split(' ')
        # using lower to match it with the action class where ADD = "add" 
        # len(args) is checking the input as when we use add we input 12 entries (name,surname....) 
        if action.lower() == Action.ADD.value and len(args) == 12:    #Action.ADD.value=add 
            self.add_student(*args)
        elif action.lower() == Action.REMOVE.value and len(args) == 1:
            self.remove_student(*args)
        elif action.lower() == Action.UPDATE.value:
            stu_id = input("Enter the student ID: ")
            attribute = input("Enter the attribute to update: ")
            new_val = input("Enter the new value: ")
            self.update_student(stu_id, attribute, new_val)
        elif action.lower() == Action.CLEAR.value:
            self.clear_console()
        elif command.lower() == "avg att":
            self.average_attendance()
        elif command.lower() == "avg gender":
            self.average_gender()
        elif command.lower() == "high":
            self.show_highest_performance()
        elif command.lower() == "low":
            self.show_lowest_performance()
        elif command.lower() == "enroll":
            self.enroll_student()
        elif command.lower()=="show table":
            self.print_students()
        else:
            rprint("[bold red italic]Invalid command !\n[bold green]Please use input in following ways:\n[bold yellow]add <name> <surname> <gender> <age> <course> <attendance> <performance> <fathers_name> <mothers_name> <phone_number> <parents_phone_number> <address>\nremove <id>\nupdate\navg att\navg gender\nhigh\nshow table\nenroll\nlow\nclear")

if __name__ == "__main__":
    system = StudentManagementSystem()   # Intiating a object of class StudentManagementSystem
    with Progress() as progress:         # Intial Progress bar 
        task1 = progress.add_task("[red]Connecting to server...", total=100)
        task2 = progress.add_task("[green]Fetching Data...", total=100)
        task3 = progress.add_task("[cyan]Warming Up...", total=100)
        while not progress.finished:     
            progress.update(task1, advance=0.5)
            progress.update(task2, advance=0.5)
            progress.update(task3, advance=0.9)
            time.sleep(0.02)
            
    while True:  
        print()   
        rprint("[italic bold white ]-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        console = Console()
        console.print(pyfiglet.figlet_format("                        Operations"), style="bold red")
 
        rprint("[italic bold white ]-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
         
        rprint("[italic bold yellow ]1.Adding a new student: [italic bold white ]add <name> <surname> <gender> <age> <course> <attendance> <performance> <fathers_name> <mothers_name> <phone_number> <parents_phone_number> <address>")
        rprint("[italic bold yellow ]2.Remove a student: [italic bold white]remove <id>")
        rprint("[italic bold yellow ]3.Update student information:[italic bold white]update")
        rprint("[italic bold yellow ]4.Get the average attendance per course:[italic bold white ]avg att ")
        rprint("[italic bold yellow ]5.Get the average of male-female :[italic bold white ]avg att ")
        rprint("[italic bold yellow ]6.Show the highest performance student: [italic bold white ] high")
        rprint("[italic bold yellow ]7.Show the LOWEST performance student:[italic bold white ] low ")
        rprint("[italic bold yellow ]8.Delete all the student records:[italic bold white ]clear ")
        rprint("[italic bold yellow ]9.To enroll in a course:[italic bold white ] enroll ")
        rprint("[italic bold yellow ]10.View the table content:[italic bold white ]show table ")
        print()
        rprint("[italic bold white ]-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print()
        command = input("\nQuery: ")
        system.query(command)      
input()

