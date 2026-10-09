import streamlit as st

st.set_page_config(page_title="표준 계산기", layout="centered")

st.title("≡ 표준 계산기")

# Инициализация состояния
if "input" not in st.session_state:
    st.session_state.input = "0"
if "stored" not in st.session_state:
    st.session_state.stored = None
if "operator" not in st.session_state:
    st.session_state.operator = None
if "reset" not in st.session_state:
    st.session_state.reset = False

# Отображение экрана калькулятора
st.markdown(
    f"<h1 style='text-align: right; background-color: #f3f3f3; padding: 10px; border-radius: 5px;'>{st.session_state.input}</h1>",
    unsafe_allow_html=True,
)

# Кнопка очистки
if st.button("C (Clear)", use_container_width=True):
    st.session_state.input = "0"
    st.session_state.stored = None
    st.session_state.operator = None
    st.session_state.reset = False
    st.rerun()


def click_num(num):
    if st.session_state.input == "0" or st.session_state.reset:
        st.session_state.input = str(num)
        st.session_state.reset = False
    else:
        st.session_state.input += str(num)


def click_op(op):
    st.session_state.stored = float(st.session_state.input)
    st.session_state.operator = op
    st.session_state.reset = True


def calculate():
    if st.session_state.stored is not None and st.session_state.operator:
        curr = float(st.session_state.input)
        prev = st.session_state.stored
        op = st.session_state.operator

        if op == "+":
            res = prev + curr
        elif op == "-":
            res = prev - curr
        elif op == "×":
            res = prev * curr
        elif op == "÷":
            if curr == 0:
                st.session_state.input = "0으로 나눌 수 없습니다"
                st.session_state.stored = None
                st.session_state.operator = None
                st.session_state.reset = True
                return
            res = prev / curr

        if res.is_integer():
            st.session_state.input = str(int(res))
        else:
            st.session_state.input = str(round(res, 8))

        st.session_state.stored = None
        st.session_state.operator = None
        st.session_state.reset = True


# Сетка кнопок 4x4
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("7", use_container_width=True):
        click_num(7)
        st.rerun()
    if st.button("4", use_container_width=True):
        click_num(4)
        st.rerun()
    if st.button("1", use_container_width=True):
        click_num(1)
        st.rerun()
    if st.button("+/-", use_container_width=True):
        if st.session_state.input.startswith("-"):
            st.session_state.input = st.session_state.input[1:]
        elif st.session_state.input != "0":
            st.session_state.input = "-" + st.session_state.input
        st.rerun()

with col2:
    if st.button("8", use_container_width=True):
        click_num(8)
        st.rerun()
    if st.button("5", use_container_width=True):
        click_num(5)
        st.rerun()
    if st.button("2", use_container_width=True):
        click_num(2)
        st.rerun()
    if st.button("0", use_container_width=True):
        click_num(0)
        st.rerun()

with col3:
    if st.button("9", use_container_width=True):
        click_num(9)
        st.rerun()
    if st.button("6", use_container_width=True):
        click_num(6)
        st.rerun()
    if st.button("3", use_container_width=True):
        click_num(3)
        st.rerun()
    if st.button(".", use_container_width=True):
        if "." not in st.session_state.input:
            st.session_state.input += "."
        st.rerun()

with col4:
    if st.button("×", use_container_width=True):
        click_op("×")
        st.rerun()
    if st.button("-", use_container_width=True):
        click_op("-")
        st.rerun()
    if st.button("+", use_container_width=True):
        click_op("+")
        st.rerun()
    if st.button("=", type="primary", use_container_width=True):
        calculate()
        st.rerun()
