from bd.connect import add_lesson

lesson_bd_file = open('lesson_bd.txt', 'r', encoding='utf-8')

for line in lesson_bd_file:
    if line != '' and line != '\n':
        add_lesson(line)
