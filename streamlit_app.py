import pandas
import streamlit as st
import numpy_financial as npf


st.title("""Leasing kalkylator v1""")

purchase_price = st.sidebar.number_input("Inköpsvärde:    ", value=793000)
down_payment = st.sidebar.number_input("Insats:   ",value=100000)
residual_value = st.sidebar.number_input("Önskat restvärde:   ",value=100000)
loanAmount = purchase_price - down_payment - residual_value

interestRate = st.sidebar.number_input("Låneränta:   ",value=1.25)
nper = st.sidebar.number_input("Antal perioder:   ",value=48)

purchase_price = int(purchase_price)
down_payment = int(down_payment)
interestRate = float(interestRate)/100
interestRate_per_month = interestRate/12

monthlyPayment_np = npf.pmt(interestRate/12, nper, loanAmount);

st.write("Lånesumma: ")
st.write(loanAmount)


st.write("Månatliga kostnaden blir då: ")
st.write(int(monthlyPayment_np))



