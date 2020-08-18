import os

from reportlab.platypus import Image, Spacer, Table, Paragraph
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing, Polygon, Circle
import utils.charts as charts
from pandas import Series

print(f"Value of color is {charts.BG_COLOR} {type(charts.BG_COLOR)}")

PAGE_WIDTH, PAGE_HEIGHT = A4
TOP_MARGIN = BOTTOM_MARGIN = cm / 4
LEFT_MARGIN = RIGHT_MARGIN = cm
styles = getSampleStyleSheet()
TEXT_H = styles['title']
H4 = styles['Heading4']
SPACE_L = Spacer(100 * cm, cm / 3)
SPACE_M = Spacer(100 * cm, cm / 5)
SPACE_S = Spacer(100 * cm, cm / 10)


def get_charts(data):
    time_chart = charts.time(data=data['Time Spent on question (sec)'],
                             label=data['Question No.'],
                             title="Time spent")
    time = Image(time_chart, width=6 * cm, height=5 * cm)

    time_func = charts.pie(data=data['Time Spent on question (sec)'],
                           label=data['Question No.'],
                           title="Time spent as function of total time.",
                           auto="%1.1f%%")
    time_per = Image(time_func, width=8 * cm, height=4 * cm)

    chart_data: Series = data['Attempt status'].value_counts()
    attempt_chart = charts.pie(chart_data,
                               label=chart_data.index,
                               title="Attempts",
                               auto="%d%%")
    attempts = Image(attempt_chart, width=8 * cm, height=4 * cm)

    chart_data = data[data['Outcome (Correct/Incorrect/Not Attempted)'].isin(['Correct', 'Incorrect'])]
    chart_data: Series = chart_data['Outcome (Correct/Incorrect/Not Attempted)'].value_counts()
    accuracy_chart = charts.pie(chart_data, chart_data.index,
                                title="Accuracy from attempted questions",
                                auto="%1.0f%%",
                                explode=[0.1, 0])
    accuracy = Image(accuracy_chart, width=8 * cm, height=4 * cm)

    chart_data: Series = data['Outcome (Correct/Incorrect/Not Attempted)'].value_counts()
    performance_chart = charts.pie(chart_data,
                                   chart_data.index,
                                   title="Overall Performance Against Test",
                                   auto="%d%%")
    performance = Image(performance_chart, width=8 * cm, height=4 * cm)

    img_grid_style = (
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),
        ('SPAN', (0, -1), (-1, -1)),
    )
    img_grid = (
        (time, time_per),
        (attempts, accuracy),
        (performance,)
    )
    return Table(img_grid, style=img_grid_style)


def title():
    return Paragraph("Wisdom Tests And Math Challenge", style=TEXT_H)


def report_table(data):
    report_table_data = [
        ("Question\nNo.", "Time spent \n on question \n (sec)", 'Score if\n correct', 'Score if\n incorrect', 'Attempt '
                                                                                                              '\nStatus',
         'What you \nmarked', 'Correct \nAnswer', 'Outcome \n(Correct\n/Incorrect/\nNot Attempted)', 'Your \nScore'),
    ]
    for row in data:
        report_table_data.append((f'{row[0]}', f'{row[1]}', f'{row[2]}', f'{row[3]}', f'{row[4]}', f'{row[5]}',
                                  f'{row[6]}', f'{row[7]}', f'{row[8]}'))
    report_table_style = (
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), (Color(0.33, 0.75, 0.80, 1), Color(1, 1, 1, 0)))
    )
    return Table(report_table_data, style=report_table_style)


def totals(marks: int, total: int):
    score_title = Paragraph(f"Total Score : {int(marks)}", style=H4)
    total_percentile = Paragraph(f"Your Overall Percentile:  {(int(marks) * 100) / int(total)}", style=H4)

    return Table([[score_title, total_percentile], ])


def perf_title():
    return Paragraph("Student Performance", style=TEXT_H)


def stu_pic(number: int, img: str):
    logo = Image("logo.png", width=4 * cm, height=2 * cm, hAlign='CENTER')
    pic = Image(f"{img}//{number}.jpg", width=2.5 * cm, height=3 * cm, hAlign="RIGHT")
    data = (
        (logo, pic),
    )
    return Table(data, style=(('VALIGN', (0, 0), (-1, -1), 'TOP'),), hAlign='RIGHT', colWidths=(10 * cm, 3 * cm))


def stu_detail(data):
    for name, reg, grade, gender, school, dob, city, test, country, time in data:
        student_detail = (
            ("Name of Candidate", f"{name}", "Registration No. ", f"{reg}"),
            ("Grade", f"{grade}", "Gender", f"{gender}"),
            ("School Name", f"{school}", "Date of Birth", f"{dob.date()}"),
            ("City Of Residence", f"{city}", "Date Of Test", f"{test.date()}"),
            ("Country Of Residence", f"{country}", "Extra Time Assistance", f"{time}")
        )
        break
    tbl_style = (
        ('FONT', (0, 0), (0, -1), "Helvetica-Bold"),
        ('FONT', (2, 0), (2, -1), "Helvetica-Bold"),
        ('LINEBELOW', (0, 0), (0, -1), 1, (0, 0, 0)),
        ('LINEBELOW', (2, 0), (2, -1), 1, (0, 0, 0)),
    )
    return Table(student_detail, style=tbl_style, colWidths=(None, 6 * cm, None, None))


def border():
    draw = Drawing(1, 1)
    rect = Polygon(points=[-12, cm / 6, (PAGE_WIDTH - (RIGHT_MARGIN + LEFT_MARGIN)), cm / 6,
                           PAGE_WIDTH - (RIGHT_MARGIN + LEFT_MARGIN),
                           -1 * (PAGE_HEIGHT - (TOP_MARGIN + BOTTOM_MARGIN + cm / 2)),
                           -12, -1 * (PAGE_HEIGHT - (TOP_MARGIN + BOTTOM_MARGIN + cm / 2))],
                   strokeColor=Color(*charts.BG_COLOR))
    rect.fillColor = Color(*charts.BG_COLOR, 0.1)
    draw.add(rect)
    draw.add(Circle(100, 90, 5, fillColor=colors.green))
    lab = Label()
    lab.setOrigin(350, -50)
    lab.boxAnchor = 'ne'
    lab.fillColor = Color(*charts.BG_COLOR, 0.15)
    lab.fontSize = 72
    lab.angle = 60
    lab.dx = 0
    lab.dy = 0
    lab.setText('Wisdom Tests')
    draw.add(lab)
    return draw


def all_components(number, data, img_location):
    return [border(),
            title(),
            stu_pic(number, img_location),
            SPACE_M,
            stu_detail(data.filter(items=["Name of Candidate",
                                          "Registration",
                                          "Grade", "Gender", "Name of school", "Date of Birth",
                                          "City of Residence",
                                          "Date and time of test", "Country of Residence",
                                          "Extra time assistance",
                                          ]).head(1).values),
            SPACE_L,
            perf_title(),
            report_table(data.filter(
                items=("Question No.", "Time Spent on question (sec)", "Score if correct",
                       "Score if incorrect",
                       "Attempt status",
                       "What you marked", "Correct Answer",
                       "Outcome (Correct/Incorrect/Not Attempted)",
                       "Your score")).values),
            SPACE_S,
            totals(data.filter(items=('Your score',)).sum(),
                   data.filter(items=('Score if correct',)).sum()),
            SPACE_L,
            get_charts(data),
            ]
