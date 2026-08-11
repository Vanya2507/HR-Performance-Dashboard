from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample dataset for Employee Performance Dashboard
EMPLOYEES = [
    {"id": 101, "name": "Aarav Sharma", "department": "Engineering", "attendance": 95, "task_completion": 92, "productivity": 88, "status": "High Performer"},
    {"id": 102, "name": "Priya Patel", "department": "HR", "attendance": 98, "task_completion": 96, "productivity": 94, "status": "High Performer"},
    {"id": 103, "name": "Rohan Verma", "department": "Marketing", "attendance": 82, "task_completion": 70, "productivity": 65, "status": "Needs Improvement"},
    {"id": 104, "name": "Ananya Singh", "department": "Engineering", "attendance": 91, "task_completion": 88, "productivity": 85, "status": "Good"},
    {"id": 105, "name": "Kabir Mehta", "department": "Sales", "attendance": 78, "task_completion": 60, "productivity": 58, "status": "Needs Improvement"}
]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get data from the 'Add Employee' form
        new_id = EMPLOYEES[-1]['id'] + 1 if EMPLOYEES else 101
        name = request.form.get('name')
        department = request.form.get('department')
        attendance = int(request.form.get('attendance', 0))
        task_completion = int(request.form.get('task_completion', 0))
        productivity = int(request.form.get('productivity', 0))

        # Determine status automatically based on productivity score
        if productivity >= 88:
            status = "High Performer"
        elif productivity >= 75:
            status = "Good"
        else:
            status = "Needs Improvement"

        # Append new employee to list
        EMPLOYEES.append({
            "id": new_id,
            "name": name,
            "department": department,
            "attendance": attendance,
            "task_completion": task_completion,
            "productivity": productivity,
            "status": status
        })
        return redirect(url_for('home'))

    # Calculate Overview Stats Dynamically
    total_employees = len(EMPLOYEES)
    departments_count = len(set(emp['department'] for emp in EMPLOYEES))
    needs_improvement_count = sum(1 for emp in EMPLOYEES if emp['status'] == 'Needs Improvement')
    
    # Calculate Chart Data
    dept_totals = {}
    dept_prod = {}
    for emp in EMPLOYEES:
        dept = emp['department']
        dept_totals[dept] = dept_totals.get(dept, 0) + 1
        dept_prod[dept] = dept_prod.get(dept, []) + [emp['productivity']]

    dept_labels = list(dept_totals.keys())
    dept_counts = list(dept_totals.values())
    prod_scores = [round(sum(scores)/len(scores), 1) for scores in dept_prod.values()]

    return render_template(
        'index.html',
        employees=EMPLOYEES,
        total_employees=total_employees,
        departments_count=departments_count,
        needs_improvement_count=needs_improvement_count,
        dept_labels=dept_labels,
        dept_counts=dept_counts,
        prod_scores=prod_scores
    )

if __name__ == '__main__':
    app.run(debug=True)