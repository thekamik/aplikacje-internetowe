from django.shortcuts import render
from django import forms


# Home Page
def index(request):
    return render(request, "index.html")


# Laboratorium nr 1
class LoanCalculatorForm(forms.Form):
    loan_amount = forms.DecimalField(label='Kwota kredytu', max_digits=10, decimal_places=2)
    interest_rate = forms.DecimalField(label='Oprocentowanie (w %)', max_digits=5, decimal_places=2)
    repayment_period = forms.IntegerField(label='Okres spłaty (w latach)')

def calculate_monthly_payment(loan_amount, interest_rate, repayment_period):
    monthly_interest_rate = (interest_rate / 100) / 12
    total_payments = repayment_period * 12
    monthly_payment = (monthly_interest_rate * loan_amount) / (1 - (1 + monthly_interest_rate) ** (-total_payments))
    return monthly_payment

def calculate_total_payment(monthly_payment, repayment_period):
    total_payments = repayment_period * 12
    total_payment = monthly_payment * total_payments
    return total_payment

def lab_1(request):

    form = LoanCalculatorForm()

    if request.method == 'POST':

        form = LoanCalculatorForm(request.POST)
        if form.is_valid():
            # Read the values from the form
            loan_amount = form.cleaned_data['loan_amount']
            interest_rate = form.cleaned_data['interest_rate']
            repayment_period = form.cleaned_data['repayment_period']

            monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, repayment_period)
            total_payment = calculate_total_payment(monthly_payment, repayment_period)

            summary_data = {
                "monthly_payment": monthly_payment,
                "total_payment": total_payment
            }
        else:
            summary_data = None
    else:
        summary_data = None
        
    
    return render(request, 'lab_1.html', {'form': form, "summary_data": summary_data})

