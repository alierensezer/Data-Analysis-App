import locale
import os
import pandas as pd
from tkinter import Text, Tk, LabelFrame
from tkinterdnd2 import TkinterDnD, DND_FILES


locale.setlocale(locale.LC_ALL, '')


window = TkinterDnD.Tk()
window.title("EndKal Veri Analizi Uygulaması")
window.geometry("600x400")


lbl = LabelFrame(window, text="Lütfen dosyayı buraya bırakınız.")
lbl.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=3)
window.grid_columnconfigure(0, weight=1)


text_widget = Text(window, height=10, wrap='none', font=("Courier", 10))
text_widget.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)


def normalize_department_name(name):
    return name.strip().title()

def standardize_column_names(df):
    df.columns = [col.strip().upper() for col in df.columns]

def format_table(df, headers):
    max_lengths = [max(df[col].astype(str).apply(len).max(), len(header)) for col, header in zip(df.columns, headers)]
    formatted_lines = []
    formatted_lines.append(" | ".join(header.ljust(length) for header, length in zip(headers, max_lengths)))
    formatted_lines.append("-" * (sum(max_lengths) + len(headers) * 3 - 1))
    for _, row in df.iterrows():
        formatted_lines.append(" | ".join(str(row[col]).ljust(length) for col, length in zip(df.columns, max_lengths)))
    return "\n".join(formatted_lines)

def on_drop(event):
    try:
        
        file_path = event.data.strip('{}').replace('\\', '/')

        
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path, encoding='utf-8')
            
            
            standardize_column_names(df)
            
            total_count = len(df)
            
            
            if 'SINIF' in df.columns:
                class_summary = df['SINIF'].value_counts().to_frame().reset_index()
                class_summary.columns = ['Sınıf', 'Adet']
                class_summary['Yüzde'] = (class_summary['Adet'] / total_count * 100).round(2)
            else:
                class_summary = pd.DataFrame(columns=['Sınıf', 'Adet', 'Yüzde'])

            
            if 'BÖLÜM' in df.columns:
                df['BÖLÜM'] = df['BÖLÜM'].apply(normalize_department_name)
                department_summary = df['BÖLÜM'].value_counts().to_frame().reset_index()
                department_summary.columns = ['Bölüm', 'Adet']
                department_summary['Yüzde'] = (department_summary['Adet'] / total_count * 100).round(2)
            else:
                department_summary = pd.DataFrame(columns=['Bölüm', 'Adet', 'Yüzde'])

            
            text_widget.delete(1.0, "end")
            text_widget.insert("end", "Sınıf Özeti:\n")
            if not class_summary.empty:
                text_widget.insert("end", format_table(class_summary, ['Sınıf', 'Adet', 'Yüzde']))
            else:
                text_widget.insert("end", "Sınıf bilgisi bulunamadı.\n")
            
            text_widget.insert("end", "\nBölüm Özeti:\n")
            if not department_summary.empty:
                text_widget.insert("end", format_table(department_summary, ['Bölüm', 'Adet', 'Yüzde']))
            else:
                text_widget.insert("end", "Bölüm bilgisi bulunamadı.")
        else:
            text_widget.delete(1.0, "end")
            text_widget.insert("end", "Geçersiz dosya yolu!")
    except Exception as e:
        text_widget.delete(1.0, "end")
        text_widget.insert("end", f"Dosya okunamadı: {e}")


lbl.drop_target_register(DND_FILES)
lbl.dnd_bind('<<Drop>>', on_drop)


window.mainloop()
