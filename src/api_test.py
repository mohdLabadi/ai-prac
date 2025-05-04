import requests
import tkinter as tk
from tkinter import ttk, messagebox

API_BASE = "https://classes.cornell.edu/api/2.0"

def fetch_math_classes():
    try:
        # Query example: All Math classes in Fall 2014
        url = f"{API_BASE}/search/classes.json?roster=FA24&subject=MATH"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract class titles and catalog numbers
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
    class_listbox.delete(0, tk.END)
    courses = fetch_math_classes()
    if courses:
        for course in courses:
            class_listbox.insert(tk.END, course)

# GUI setup
root = tk.Tk()
root.title("Cornell Class Roster - MATH (FA25)")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Fall 2025 MATH Courses:").pack(anchor='w')

class_listbox = tk.Listbox(frame, width=50, height=20)
class_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

ttk.Button(frame, text="Load Courses", command=load_classes).pack()

root.mainloop()
