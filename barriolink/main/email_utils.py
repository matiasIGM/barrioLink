from django.shortcuts import render
#render correos


def activation_email_rendered(request):
    return render(request, 'account/email/activation_account_email.html')

def reject_email_rendered(request):
    return render(request, 'account/email/rejection_account_email.html')