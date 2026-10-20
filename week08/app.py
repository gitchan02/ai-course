import tkinter as tk
from tkinter import ttk, messagebox
from calculator import calculate_parking_fee

class ParkingCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("주차 요금 계산기")
        self.root.geometry("750x550")

        # 데이터 저장용 리스트
        self.data_list = [] 

        self.setup_ui()

    def setup_ui(self):
        # --- 입력 프레임 ---
        input_frame = ttk.LabelFrame(self.root, text="주차 정보 입력", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="입차 시각 (HH:MM):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_entry_time = ttk.Entry(input_frame, width=10)
        self.entry_entry_time.grid(row=0, column=1, padx=5, pady=5)
        self.entry_entry_time.insert(0, "09:00")

        ttk.Label(input_frame, text="출차 시각 (HH:MM):").grid(row=0, column=2, padx=5, pady=5)
        self.entry_exit_time = ttk.Entry(input_frame, width=10)
        self.entry_exit_time.grid(row=0, column=3, padx=5, pady=5)
        self.entry_exit_time.insert(0, "10:00")

        self.extra_days = 0
        self.btn_plus_day = ttk.Button(input_frame, text="+1일", command=self.add_day)
        self.btn_plus_day.grid(row=0, column=4, padx=5, pady=5)
        
        self.lbl_days = ttk.Label(input_frame, text="경과: 0일")
        self.lbl_days.grid(row=0, column=5, padx=5, pady=5)

        self.btn_calculate = ttk.Button(input_frame, text="계산하기", command=self.add_to_history)
        self.btn_calculate.grid(row=0, column=6, padx=10, pady=5)

        # --- 목록 프레임 ---
        list_frame = ttk.LabelFrame(self.root, text="주차 목록", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview 설정
        columns = ("entry", "exit", "duration", "fee")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("entry", text="입차")
        self.tree.heading("exit", text="출차")
        self.tree.heading("duration", text="주차 시간")
        self.tree.heading("fee", text="요금")
        
        self.tree.column("entry", width=80, anchor="center")
        self.tree.column("exit", width=80, anchor="center")
        self.tree.column("duration", width=120, anchor="center")
        self.tree.column("fee", width=100, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # 삭제 버튼 (Treeview에서 선택된 항목 삭제)
        self.btn_delete = ttk.Button(self.root, text="선택 항목 삭제", command=self.delete_selected)
        self.btn_delete.pack(pady=5)

        # --- 하단 합계 프레임 ---
        sum_frame = ttk.Frame(self.root, padding=10)
        sum_frame.pack(fill="x")

        self.lbl_total_sum = ttk.Label(sum_frame, text="오늘 받은 요금 합계: 0원", font=("Arial", 14, "bold"))
        self.lbl_total_sum.pack(side="right")

    def add_day(self):
        self.extra_days += 1
        self.lbl_days.config(text=f"경과: {self.extra_days}일")

    def add_to_history(self):
        entry_val = self.entry_entry_time.get().strip()
        exit_val = self.entry_exit_time.get().strip()

        try:
            # 계산 로직 호출
            _, fee, duration = calculate_parking_fee(entry_val, exit_val, self.extra_days)
            
            # Treeview에 행 추가
            self.tree.insert("", "end", values=(entry_val, exit_val, duration, f"{fee:,}원"))
            
            # 합계 업데이트
            self.update_total_sum()
            
            # 입력값 초기화
            self.reset_inputs()

        except ValueError as e:
            messagebox.showerror("입력 오류", str(e))

    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("알림", "삭제할 항목을 선택해주세요.")
            return

        for item in selected_items:
            self.tree.delete(item)
        
        # 삭제 후 합계 재계산
        self.update_total_sum()

    def update_total_sum(self):
        total = 0
        for child in self.tree.get_children():
            values = self.tree.item(child, 'values')
            # fee column is values[3], format is "1,500원"
            fee_str = values[3].replace(",", "").replace("원", "")
            try:
                total += int(fee_str)
            except ValueError:
                continue
        
        self.lbl_total_sum.config(text=f"오늘 받은 요금 합계: {total:,}원")

    def reset_inputs(self):
        self.extra_days = 0
        self.lbl_days.config(text="경과: 0일")
        self.entry_entry_time.delete(0, tk.END)
        self.entry_entry_time.insert(0, "09:00")
        self.entry_exit_time.delete(0, tk.END)
        self.entry_exit_time.insert(0, "10:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingCalculatorApp(root)
    root.mainloop()
