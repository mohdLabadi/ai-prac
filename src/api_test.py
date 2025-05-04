import requests
import tkinter as tk
from tkinter import ttk, messagebox

API_BASE = "https://classes.cornell.edu/api/2.0"

def fetch_classes(roster, subject, acad_career, class_levels, crse_attrs):
    try:
        # Build dynamic URL with parameters
        params = {
            "roster": roster,
            "subject": subject
        }
        if acad_career:
            params["acadCareer[]"] = acad_career
        if class_levels:
            params["classLevels[]"] = class_levels
        if crse_attrs:
            params["crseAttrs[]"] = crse_attrs

        response = requests.get(f"{API_BASE}/search/classes.json", params=params)
        response.raise_for_status()
        data = response.json()

        classes = data.get('data', {}).get('classes', [])
        results = []
        for cls in classes:
            title = cls.get("titleShort", "Untitled")
            catalog = cls.get("catalogNbr", "")
            results.append(f"{catalog} - {title}")
        return results
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return []

def load_classes():
    roster = roster_entry.get().strip()
    subject = subject_entry.get().strip()
    acad_career = career_entry.get().strip()
    class_levels = level_entry.get().strip()
    crse_attrs = attr_entry.get().strip()

    class_listbox.delete(0, tk.END)
    courses = fetch_classes(roster, subject, acad_career, class_levels, crse_attrs)
    if courses:
        for course in courses:
            class_listbox.insert(tk.END, course)

# GUI setup
root = tk.Tk()
root.title("Cornell Class Roster Search")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Input fields
ttk.Label(frame, text="Roster (e.g., FA24):").pack(anchor='w')
roster_entry = ttk.Entry(frame)
roster_entry.pack(fill=tk.X)
roster_entry.insert(0, "FA24")

ttk.Label(frame, text="Subject (e.g., CS, MATH):").pack(anchor='w')
subject_entry = ttk.Entry(frame)
subject_entry.pack(fill=tk.X)
subject_entry.insert(0, "CS")

ttk.Label(frame, text="Academic Career (optional, e.g., UG, GR):").pack(anchor='w')
career_entry = ttk.Entry(frame)
career_entry.pack(fill=tk.X)

ttk.Label(frame, text="Class Level (optional, e.g., 6000):").pack(anchor='w')
level_entry = ttk.Entry(frame)
level_entry.pack(fill=tk.X)

ttk.Label(frame, text="Course Attribute (optional, e.g., CU-SBY):").pack(anchor='w')
attr_entry = ttk.Entry(frame)
attr_entry.pack(fill=tk.X)

ttk.Button(frame, text="Load Courses", command=load_classes).pack(pady=5)

class_listbox = tk.Listbox(frame, width=60, height=20)
class_listbox.pack(fill=tk.BOTH, expand=True)

root.mainloop()
