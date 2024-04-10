import os
import time

def validiateLines(data):
    if len(data) != 8:
        print("Invalid data format")
        exit()
    if not data[2].isdigit():
        print("Invalid grade level")
        exit()
    if not data[4].isdigit():
        print("Invalid bus route")
        exit()
    try :
        float(data[5])
    except ValueError:
        print("Invalid GPA")
        exit()

def parseFile():
    # data schema: last_name, first_name, grade, classroom, bus, GPA, teacher_last_name, teacher_first_name
    # the last_name dictionary will store the last name as the key and all the infomation stored for students with that last name
    last_name = {}
    # class_roster will store the teacher's last name as the key and all the students in that class
    class_roster = {}
    # bus_route will store the bus route as the key and all the students that take that bus
    bus_route = {}
    # students_in_grade will store the grade as the key and all the students in that grade
    students_in_grade = {}

    with open("students.txt", 'r') as file:
        for line in file:
            data = line.split(',')
            data[-1] = data[-1].strip()

            validiateLines(data)

            if data[0] in last_name:
                last_name[data[0]].append(data)
            else:
                last_name[data[0]] = []
                last_name[data[0]].append(data)

            if data[6] in class_roster:
                class_roster[data[6]].append(data)
            else:
                class_roster[data[6]] = []
                class_roster[data[6]].append(data)

            if int(data[4]) in bus_route:
                bus_route[int(data[4])].append(data)
            else:
                bus_route[int(data[4])] = []
                bus_route[int(data[4])].append(data)

            if int(data[2]) in students_in_grade:
                students_in_grade[int(data[2])].append(data)
            else:
                students_in_grade[int(data[2])] = []
                students_in_grade[int(data[2])].append(data)
        
    return last_name, class_roster, bus_route, students_in_grade

def textOutline():
    print("==============================================")
    print("SchoolSearch: The all knowing school database for Grades 1 - 6")
    print("==============================================\n")
    
    print("----------------------------------------------")
    print("< > denotes mandatory arguments")
    print("[ ] denotes optional arguments")
    print("Note: commands are case and whitespace sensitive")
    print("----------------------------------------------")
    print("Valid Commands:")
    print("S <last name> [B]: Searches for a student by last name and \'B\' will display the student's bus route as well")
    print("T <last name>: Searches for a teacher by last name and displays all students in that teacher's class")
    print("B <route number>: Searches for a specfic bus route and the students that take that bus")
    print("G <grade level> [H\L]: Will display the students in the provided grade and \'H\' or \'L\' will display the students with a highest and lowest GPA in that grade respctively")
    print("A <grade level>: Will display the average GPA for students in the provided grade")
    print("I: Will display the number of students in each grade level")
    print("C: Will clear the terminal")
    print("Q: Quits the program")


def parseUserInput(lastNameDict, classRosterDict, busRouteDict, gradeLevelDict):
    print("Welcome to SchoolSearch: The all knowing school database")
    print("Please wait while the program loads")
    time.sleep(1)
    os.system('clear')
    textOutline()

    while True:
        user_input = input("\nEnter a command: ")
        user_input = user_input.split(' ')

        if user_input[0] == 'S' and len(user_input) > 1 and len(user_input) < 4:
            if user_input[1] in lastNameDict:
                print("\nStudent found!")
                student = lastNameDict[user_input[1]][0]
                print("Student name: " + student[1] + " " + student[0])
                if len(user_input) == 3 and user_input[2] == 'B':
                    print("Bus route: " + student[4])
                else:
                    print("Grade Level: " + student[2])
                    print("Classroom: " + student[3])
                    print("Teacher: " + student[7] + " " + student[6])
            else:
                print("No student with that last name found or invalid command")
        
        elif user_input[0] == 'T' and len(user_input) == 2:
            if user_input[1] in classRosterDict:
                print("\nTeacher found!")
                studentLst = classRosterDict[user_input[1]]
                print("Teacher name: " + studentLst[0][7] + " " + studentLst[0][6])
                print("Students in class: ")
                i = 1
                for student in studentLst:
                    print(str(i) + ". " + student[1] + " " + student[0])
                    i += 1
            else:
                print("No teacher with that last name found or invalid command")
        
        elif user_input[0] == 'B' and len(user_input) == 2:
            if int(user_input[1]) in busRouteDict:
                print("\nBus route found!")
                studentLst = busRouteDict[int(user_input[1])]
                print("Students on bus route " + user_input[1] + ": ")
                i = 1
                for student in studentLst:
                    print(str(i) + ". " + student[1] + " " + student[0] + ", Grade: " + student[2] + ", Classroom: " + student[3])
                    i += 1
            else:
                print("No bus route with that number found or invalid command")

        elif user_input[0] == 'A' and len(user_input) == 2:
            if int(user_input[1]) in gradeLevelDict:
                studentLst = gradeLevelDict[int(user_input[1])]
                totalGPA = 0
                for student in studentLst:
                    totalGPA += float(student[5])
                avgGPA = totalGPA / len(studentLst)
                print("Average GPA for students is grade " + user_input[1] + " is " + str(round(avgGPA, 2)))
            else:
                print("No students in that grade level or invalid command")

        elif user_input[0] == 'G' and len(user_input) > 1 and len(user_input) < 4:
            gradeLevel = int(user_input[1])
            if gradeLevel in gradeLevelDict:
                studentLst = gradeLevelDict[gradeLevel]
                
                if len(user_input) == 2:
                    print("\nStudents in grade " + user_input[1] + ": ")
                    i = 1
                    for student in studentLst:
                        print(str(i) + ". " + student[1] + " " + student[0])    
                        i += 1
                else:
                    studentLst.sort(key=lambda x: x[5], reverse=True)
                    if user_input[2] == 'H':
                        print("\nStudent with the highest GPA in grade " + user_input[1] + "is " + studentLst[0][1] + " " + studentLst[0][0] + ", GPA: " + studentLst[0][5] )
                    elif user_input[2] == 'L':
                        print("\nStudent with the lowest GPA in grade " + user_input[1] + "is " + studentLst[-1][1] + " " + studentLst[-1][0] + ", GPA: " + studentLst[-1][5])
                    else:
                        print("Invalid command")
            else:
                print("No students in that grade level or invalid command")

        elif user_input[0] == 'I' and len(user_input) == 1:
            print("\nNumber of students in each grade level: ")
            gradeLevelDict = dict(sorted(gradeLevelDict.items()))
            highestGrade = max(gradeLevelDict.keys())
            i = 1
            while i <= highestGrade:
                if i in gradeLevelDict:
                    print("Grade " + str(i) + ": " + str(len(gradeLevelDict[i])))
                else:
                    print("Grade " + str(i) + ": 0")
                i += 1
        
        elif user_input[0] == 'C' and len(user_input) == 1:
            print("Clearing terminal...")
            os.system('clear')
            time.sleep(0.5)
            textOutline()
        elif user_input[0] == 'Q' and len(user_input) == 1:
            print("Exiting program")
            time.sleep(1)
            os.system('clear')
            break
        else: 
            print("Invalid command! Please try again!")
            time.sleep(1)
        

def main():
    lastNameDict, classRosterDict, busRouteDict, gradeLevelDict = parseFile()
    
    parseUserInput(lastNameDict, classRosterDict, busRouteDict, gradeLevelDict)

if __name__ == '__main__':
    main()