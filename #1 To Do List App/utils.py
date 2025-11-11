from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from models import Task

def generate_list_pdf(list_title: str, task_ids: list[str], load_task_func) -> str:
    pdf_path = f"{list_title.replace(' ', '_')}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, f"List: {list_title}")
    y = 700
    for tid in task_ids:
        task = load_task_func(tid)
        if task:
            c.drawString(100, y, f"Title: {task.title}, Desc: {task.description[:50]}..., Pri: {task.priority}, Due: {task.due_date}")
            y -= 30
            if y < 100:
                c.showPage()
                y = 750
    c.save()
    return pdf_path

def generate_task_pdf(task: Task) -> str:
    pdf_path = f"{task.title.replace(' ', '_')}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, f"Task: {task.title}")
    c.drawString(100, 700, f"Description: {task.description}")
    c.drawString(100, 650, f"Priority: {task.priority}")
    c.drawString(100, 600, f"Due Date: {task.due_date}")
    c.save()
    return pdf_path