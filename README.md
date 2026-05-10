# University Student Data Dashboard

**Course:** Data Mining — Universidad de la Costa  
**Professor:** José Escorcia-Gutierrez, Ph.D.  
**Author:** Sheila Daniela Hernandez Carrillo - 18038

## Purpose

This project explores university student data to understand trends in admissions, enrollment, retention, and satisfaction. It includes an exploratory analysis and an interactive dashboard built with Streamlit.

## Repository Structure

```
├── app.py                        # Streamlit dashboard
├── requirements.txt              # Dependencies
├── university_student_data.csv   # Dataset
└── README.md
```

## Dataset

The dataset contains information about student applications, admissions, enrollment, retention, and satisfaction across different years and academic terms.

| Column | Meaning |
|---|---|
| `Year` | Academic year |
| `Term` | Spring or Fall semester |
| `Applications` | Number of applications received |
| `Admitted` | Number of students accepted |
| `Enrolled` | Number of students enrolled |
| `Retention Rate (%)` | Percentage of students who continue |
| `Student Satisfaction (%)` | Satisfaction score |
| `Engineering / Business / Arts / Science Enrolled` | Enrollment by department |

## Features

- KPI cards (total enrolled, retention, satisfaction)
- Retention trend over time
- Student satisfaction by year
- Comparison between Spring and Fall
- Enrollment by department
- Interactive filters (year, term, department)

## Live Dashboard

https://university-dashboard-8kawdkdggnwxhliwlg6vju.streamlit.app/
