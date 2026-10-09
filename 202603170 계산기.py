import tkinter as tk
from tkinter import font


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        # 창 기본 설정
        self.title("표준 계산기")
        self.geometry("320 Old Style" if False else "320x480")
        self.resizable(False, False)
        self.configure(bg="#f3f3f3")  # 밝은 회색 배경 (Windows 11 스타일)

        # 계산 상태 변수
        self.current_input = "0"  # 디스플레이에 표시될 현재 값
        self.stored_value = None  # 이전 저장된 숫자
        self.current_operator = None  # 현재 선택된 연산자
        self.reset_screen = False  # 다음 입력 시 화면을 새로 갱신할지 여부

        # GUI 구성
        self.create_widgets()

    def create_widgets(self):
        # 1. 상단 디스플레이 영역 (초기화 버튼 + 결과 창)
        top_frame = tk.Frame(self, bg="#f3f3f3", padx=15, pady=10)
        top_frame.pack(fill="x", side="top")

        # 상단 헤더 (제목 및 초기화 C 버튼)
        header_frame = tk.Frame(top_frame, bg="#f3f3f3")
        header_frame.pack(fill="x", pady=(0, 10))

        title_label = tk.Label(
            header_frame, text="≡  표준", font=("Malgun Gothic", 12, "bold"),
            bg="#f3f3f3", fg="#1b1b1b"
        )
        title_label.pack(side="left")

        # 초기화(C) 버튼 (오른쪽 상단 배치)
        clear_btn = tk.Button(
            header_frame, text="C", font=("Malgun Gothic", 10, "bold"),
            bg="#e5e5e5", fg="#1b1b1b", activebackground="#cccccc",
            bd=0, width=3, cursor="hand2", command=self.clear_all
        )
        clear_btn.pack(side="right")

        # 숫자 표시창 (Display)
        self.display_font = font.Font(family="Segoe UI", size=32, weight="bold")
        self.display_label = tk.Label(
            top_frame, text=self.current_input, font=self.display_font,
            bg="#f3f3f3", fg="#000000", anchor="e", justify="right"
        )
        self.display_label.pack(fill="x", pady=(10, 0))

        # 2. 하단 버튼 그리드 영역
        btn_frame = tk.Frame(self, bg="#f3f3f3", padx=6, pady=6)
        btn_frame.pack(fill="both", expand=True)

        # 그리드 가중치 설정 (모든 버튼이 균등하게 확장되도록)
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(4):
            btn_frame.rowconfigure(i, weight=1)

        # 버튼 배치 데이터 [텍스트, row, col, type]
        buttons = [
            ("7", 0, 0, "num"), ("8", 0, 1, "num"), ("9", 0, 2, "num"), ("×", 0, 3, "op"),
            ("4", 1, 0, "num"), ("5", 1, 1, "num"), ("6", 1, 2, "num"), ("-", 1, 3, "op"),
            ("1", 2, 0, "num"), ("2", 2, 1, "num"), ("3", 2, 2, "num"), ("+", 2, 3, "op"),
            ("+/-", 3, 0, "num"), ("0", 3, 1, "num"), (".", 3, 2, "num"), ("=", 3, 3, "eq")
        ]

        # 버튼 색상 정의 (Windows 11 스타일)
        style_num = {"bg": "#ffffff", "fg": "#000000", "activebg": "#f9f9f9"}
        style_op = {"bg": "#f9f9f9", "fg": "#000000", "activebg": "#f0f0f0"}
        style_eq = {"bg": "#0067c0", "fg": "#ffffff", "activebg": "#005aab"}  # 포인트 파란색

        btn_font = ("Segoe UI", 13)

        for text, r, c, b_type in buttons:
            if b_type == "num":
                bg, fg, abg = style_num["bg"], style_num["fg"], style_num["activebg"]
            elif b_type == "op":
                bg, fg, abg = style_op["bg"], style_op["fg"], style_op["activebg"]
            else:  # 'eq'
                bg, fg, abg = style_eq["bg"], style_eq["fg"], style_eq["activebg"]

            btn = tk.Button(
                btn_frame, text=text, font=btn_font,
                bg=bg, fg=fg, activebackground=abg, activeforeground=fg,
                bd=1, relief="solid", cursor="hand2",
                command=lambda t=text: self.on_button_click(t)
            )
            # 테두리 느낌을 위해 padding 적용
            btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

    def update_display(self, text=None):
        """디스플레이 표기 업데이트 함수"""
        val = text if text is not None else self.current_input
        self.display_label.config(text=val)

    def on_button_click(self, char):
        """버튼 클릭 이벤트 핸들러"""
        # 에러 상태 해제 처리
        if self.current_input == "0으로 나눌 수 없습니다":
            self.clear_all()

        if char in "0123456789":
            self.input_number(char)
        elif char == ".":
            self.input_dot()
        elif char == "+/-":
            self.toggle_sign()
        elif char in ["+", "-", "×", "÷"]:
            self.set_operator(char)
        elif char == "=":
            self.calculate_result()

    def input_number(self, num):
        """숫자 버튼 클릭 처리"""
        if self.current_input == "0" or self.reset_screen:
            self.current_input = num
            self.reset_screen = False
        else:
            self.current_input += num
        self.update_display()

    def input_dot(self):
        """소수점 버튼 클릭 처리"""
        if self.reset_screen:
            self.current_input = "0."
            self.reset_screen = False
        elif "." not in self.current_input:
            self.current_input += "."
        self.update_display()

    def toggle_sign(self):
        """부호 전환(+/-) 처리"""
        if self.current_input == "0":
            return
        if self.current_input.startswith("-"):
            self.current_input = self.current_input[1:]
        else:
            self.current_input = "-" + self.current_input
        self.update_display()

    def set_operator(self, op):
        """연산자 버튼 클릭 처리"""
        if self.stored_value is not None and not self.reset_screen:
            self.calculate_result()

        try:
            self.stored_value = float(self.current_input)
        except ValueError:
            return

        self.current_operator = op
        self.reset_screen = True

    def calculate_result(self):
        """연산(=) 결과 계산 처리"""
        if self.stored_value is None or self.current_operator is None:
            return

        try:
            current_val = float(self.current_input)
            result = 0.0

            if self.current_operator == "+":
                result = self.stored_value + current_val
            elif self.current_operator == "-":
                result = self.stored_value - current_val
            elif self.current_operator == "×":
                result = self.stored_value * current_val
            elif self.current_operator == "÷":
                if current_val == 0:
                    self.current_input = "0으로 나눌 수 없습니다"
                    self.update_display()
                    self.stored_value = None
                    self.current_operator = None
                    self.reset_screen = True
                    return
                result = self.stored_value / current_val

            # 정수로 떨어지는 경우 소수점 제거 (예: 5.0 -> 5)
            if result.is_integer():
                self.current_input = str(int(result))
            else:
                self.current_input = str(round(result, 8))  # 소수점 부동소수점 오차 방지

            self.update_display()
            self.stored_value = None
            self.current_operator = None
            self.reset_screen = True

        except Exception:
            self.current_input = "오류"
            self.update_display()

    def clear_all(self):
        """초기화(Clear) 기능"""
        self.current_input = "0"
        self.stored_value = None
        self.current_operator = None
        self.reset_screen = False
        self.update_display()


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()