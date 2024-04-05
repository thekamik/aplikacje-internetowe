from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages

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


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'pass123':
            # Set session variable to mark user as logged in
            request.session['logged_in'] = True
            return redirect('lab_1')
        else:
            messages.error(request, 'Invalid login credentials')
            # Display an error message to the user
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
    return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        request.session['logged_in'] = False
        return redirect('login')  # Redirect to the login page after logout
    else:
        return render(request, 'logout.html')


def lab_1(request):
    if 'logged_in' in request.session and request.session['logged_in'] == True:
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
    else:
        return redirect('login')

