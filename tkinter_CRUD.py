import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi REAL NOT NULL,
            fisika REAL NOT NULL,
            inggris REAL NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_db()


def prediksi_fakultas(bio, fis, ing):
    if bio > fis and bio > ing:
        return "Kedokteran"
    elif fis > bio and fis > ing:
        return "Teknik"
    elif ing > bio and ing > fis:
        return "Bahasa"
    return "Tidak Dapat Ditentukan"

def submit_nilai():
    nama = entry_nama.get().strip()

    try:
        bio = float(entry_bio.get().strip())
        fis = float(entry_fis.get().strip())
        ing = float(entry_ing.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus angka!")
        return

    if not nama:
        messagebox.showerror("Error", "Nama tidak boleh kosong!")
        return

    if not (0 <= bio <= 100):
        messagebox.showerror("Error", "Nilai Biologi harus 0–100!")
        return
    if not (0 <= fis <= 100):
        messagebox.showerror("Error", "Nilai Fisika harus 0–100!")
        return
    if not (0 <= ing <= 100):
        messagebox.showerror("Error", "Nilai Inggris harus 0–100!")
        return

    hasil = prediksi_fakultas(bio, fis, ing)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil))

    conn.commit()
    conn.close()

    load_data()

    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)

def clear_input():
    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)

def load_data():
    for item in table.get_children():
        table.delete(item)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        nama, bio, fis, ing, hasil = row
        table.insert("", tk.END, values=(
            nama,
            f"{bio:.1f}",
            f"{fis:.1f}",
            f"{ing:.1f}",
            hasil
        ))

root = tk.Tk()
root.title("Input Nilai Siswa - SQLite")
root.geometry("880x460")

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

left_frame = tk.LabelFrame(main_frame, text="Form Input", padx=10, pady=10)
left_frame.pack(side="left", fill="y")

tk.Label(left_frame, text="Nama Siswa").pack(anchor="w")
entry_nama = tk.Entry(left_frame, width=25)
entry_nama.pack(pady=3, anchor="w")

tk.Label(left_frame, text="Nilai (0–100):").pack(anchor="w", pady=(10, 3))

nilai_frame = tk.Frame(left_frame)
nilai_frame.pack(pady=5)

tk.Label(nilai_frame, text="Biologi").grid(row=0, column=0, padx=5, sticky="e")
entry_bio = tk.Entry(nilai_frame, width=5)
entry_bio.grid(row=0, column=1, padx=5)

tk.Label(nilai_frame, text="Fisika").grid(row=0, column=2, padx=5, sticky="e")
entry_fis = tk.Entry(nilai_frame, width=5)
entry_fis.grid(row=0, column=3, padx=5)

tk.Label(nilai_frame, text="Inggris").grid(row=0, column=4, padx=5, sticky="e")
entry_ing = tk.Entry(nilai_frame, width=5)
entry_ing.grid(row=0, column=5, padx=5)

btn_frame = tk.Frame(left_frame)
btn_frame.pack(pady=15, anchor="w")

btn_submit = tk.Button(btn_frame, text="Submit", command=submit_nilai, width=10)
btn_submit.grid(row=0, column=0, padx=5)

btn_clear = tk.Button(btn_frame, text="Clear", command=clear_input, width=10)
btn_clear.grid(row=0, column=1, padx=5)


right_frame = tk.LabelFrame(main_frame, text="Data Tersimpan", padx=10, pady=10)
right_frame.pack(side="left", padx=20)

table = ttk.Treeview(
    right_frame,
    columns=("nama", "bio", "fis", "ing", "hasil"),
    show="headings",
    height=15
)
table.pack()

table.heading("nama", text="Nama")
table.heading("bio", text="Biologi")
table.heading("fis", text="Fisika")
table.heading("ing", text="Inggris")
table.heading("hasil", text="Prediksi Fakultas")

table.column("nama", width=150)
table.column("bio", width=70)
table.column("fis", width=70)
table.column("ing", width=70)
table.column("hasil", width=150)

load_data()

root.mainloop()