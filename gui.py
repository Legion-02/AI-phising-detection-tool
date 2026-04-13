from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from src.predict import predict_text
from src.model_utils import MODEL_PATH


class PhishingDetectorGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title('AI Phishing Detection Tool')
        self.root.geometry('900x700')
        self.root.minsize(800, 620)

        self.status_var = tk.StringVar(value='Ready')
        self.result_var = tk.StringVar(value='Result: Waiting for input')
        self.confidence_var = tk.StringVar(value='Confidence: --')

        self._build_ui()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=16)
        main.pack(fill='both', expand=True)

        header = ttk.Label(
            main,
            text='AI-Based Phishing Detection System',
            font=('Segoe UI', 18, 'bold')
        )
        header.pack(anchor='w')

        subheader = ttk.Label(
            main,
            text='Paste an email or message below and analyze whether it looks like phishing.',
            font=('Segoe UI', 10)
        )
        subheader.pack(anchor='w', pady=(4, 12))

        text_frame = ttk.LabelFrame(main, text='Email / Message Content', padding=10)
        text_frame.pack(fill='both', expand=False)

        self.input_box = scrolledtext.ScrolledText(text_frame, wrap='word', height=12, font=('Consolas', 11))
        self.input_box.pack(fill='both', expand=True)

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill='x', pady=12)

        ttk.Button(btn_frame, text='Analyze', command=self.analyze_text).pack(side='left')
        ttk.Button(btn_frame, text='Clear', command=self.clear_all).pack(side='left', padx=8)
        ttk.Button(btn_frame, text='Load Sample', command=self.load_sample).pack(side='left')

        result_frame = ttk.LabelFrame(main, text='Prediction Summary', padding=12)
        result_frame.pack(fill='x', pady=(0, 12))

        ttk.Label(result_frame, textvariable=self.result_var, font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        ttk.Label(result_frame, textvariable=self.confidence_var, font=('Segoe UI', 11)).pack(anchor='w', pady=(6, 0))

        reasons_frame = ttk.LabelFrame(main, text='Why this result?', padding=10)
        reasons_frame.pack(fill='both', expand=True)

        self.reasons_box = scrolledtext.ScrolledText(reasons_frame, wrap='word', height=10, state='disabled', font=('Segoe UI', 10))
        self.reasons_box.pack(fill='both', expand=True)

        history_frame = ttk.LabelFrame(main, text='Session History', padding=10)
        history_frame.pack(fill='both', expand=True, pady=(12, 0))

        self.history_box = scrolledtext.ScrolledText(history_frame, wrap='word', height=8, state='disabled', font=('Consolas', 10))
        self.history_box.pack(fill='both', expand=True)

        status = ttk.Label(main, textvariable=self.status_var, relief='sunken', anchor='w')
        status.pack(fill='x', pady=(10, 0))

    def _write_box(self, box: scrolledtext.ScrolledText, text: str) -> None:
        box.configure(state='normal')
        box.delete('1.0', tk.END)
        box.insert(tk.END, text)
        box.configure(state='disabled')

    def _append_history(self, text: str) -> None:
        self.history_box.configure(state='normal')
        self.history_box.insert(tk.END, text + '\n' + ('-' * 80) + '\n')
        self.history_box.configure(state='disabled')

    def analyze_text(self) -> None:
        text = self.input_box.get('1.0', tk.END).strip()
        if not text:
            messagebox.showwarning('Missing Input', 'Please paste an email or message first.')
            return

        try:
            result = predict_text(text)
        except FileNotFoundError:
            messagebox.showerror(
                'Model Not Found',
                f'Model file is missing. Please run `python src/train_model.py` first.\n\nExpected path:\n{MODEL_PATH}'
            )
            self.status_var.set('Model file missing')
            return
        except Exception as exc:
            messagebox.showerror('Error', f'Prediction failed:\n{exc}')
            self.status_var.set('Prediction failed')
            return

        self.result_var.set(f"Result: {result['label']}")
        self.confidence_var.set(f"Confidence: {result['confidence']:.2%}")
        self._write_box(self.reasons_box, '\n'.join(f'• {reason}' for reason in result['reasons']))
        preview = text.replace('\n', ' ')[:120]
        history_entry = (
            f"Input: {preview}{'...' if len(text) > 120 else ''}\n"
            f"Prediction: {result['label']} | Confidence: {result['confidence']:.2%}\n"
            f"Reasons: {'; '.join(result['reasons'])}"
        )
        self._append_history(history_entry)
        self.status_var.set('Analysis completed successfully')

    def clear_all(self) -> None:
        self.input_box.delete('1.0', tk.END)
        self._write_box(self.reasons_box, '')
        self.result_var.set('Result: Waiting for input')
        self.confidence_var.set('Confidence: --')
        self.status_var.set('Cleared')

    def load_sample(self) -> None:
        sample = (
            'Urgent: Your company email account will be suspended today. '\
            'Click the link below to verify your password immediately and avoid permanent lockout. '\
            'http://security-check.example/reset'
        )
        self.input_box.delete('1.0', tk.END)
        self.input_box.insert(tk.END, sample)
        self.status_var.set('Sample loaded')


if __name__ == '__main__':
    root = tk.Tk()
    app = PhishingDetectorGUI(root)
    root.mainloop()
