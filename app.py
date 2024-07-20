import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount'])
if 'budgets' not in st.session_state:
    st.session_state.budgets = pd.DataFrame(columns=['Category', 'Budget'])

def add_expense():
    if st.session_state.amount and st.session_state.category:
        new_expense = pd.DataFrame({
            'Date': [st.session_state.date],
            'Category': [st.session_state.category],
            'Amount': [float(st.session_state.amount)]
        })
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

def add_budget():
    if st.session_state.budget_amount and st.session_state.budget_category:
        new_budget = pd.DataFrame({
            'Category': [st.session_state.budget_category],
            'Budget': [float(st.session_state.budget_amount)]
        })
        st.session_state.budgets = pd.concat([st.session_state.budgets, new_budget], ignore_index=True)

def plot_summary():
    combined = st.session_state.expenses.groupby('Category')['Amount'].sum().reset_index()
    budget_summary = st.session_state.budgets.merge(combined, on='Category', how='left')
    budget_summary['Amount'].fillna(0, inplace=True)
    budget_summary['Difference'] = budget_summary['Budget'] - budget_summary['Amount']
    
    fig, ax = plt.subplots()
    budget_summary.plot(kind='bar', x='Category', y=['Budget', 'Amount'], ax=ax)
    ax.set_ylabel('Amount')
    ax.set_title('Expense vs Budget')
    st.pyplot(fig)

st.title('Expense Tracker Widget')

st.subheader('Add Expense')
st.date_input('Date', key='date')
st.selectbox('Category', options=['Food', 'Entertainment', 'Utilities', 'Other'], key='category')
st.number_input('Amount', min_value=0.0, format='%.2f', key='amount')
st.button('Add Expense', on_click=add_expense)

st.subheader('Set Budget')
st.selectbox('Category', options=['Food', 'Entertainment', 'Utilities', 'Other'], key='budget_category')
st.number_input('Budget Amount', min_value=0.0, format='%.2f', key='budget_amount')
st.button('Set Budget', on_click=add_budget)

st.subheader('Expense and Budget Summary')
plot_summary()

st.subheader('Expenses')
st.dataframe(st.session_state.expenses)

st.subheader('Budgets')
st.dataframe(st.session_state.budgets)
