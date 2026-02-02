from django.views.generic import TemplateView


class ContactView(TemplateView):
    """Contact page with form submission"""
    template_name = 'contact/index.html'
    
    def post(self, request, *args, **kwargs):
        from django.core.mail import send_mail
        from django.contrib import messages
        from django.shortcuts import redirect
        from django.conf import settings
        
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validate required fields
        if not all([first_name, last_name, email, message]):
            messages.error(request, 'Wszystkie pola są wymagane.')
            return redirect('contact')
        
        # Compose email
        subject = f'Nowa wiadomość od {first_name} {last_name}'
        email_message = f"""
        Nowa wiadomość z formularza kontaktowego:

        Imię: {first_name}
        Nazwisko: {last_name}
        Email: {email}

        Wiadomość:
        {message}
        """
        
        try:
            send_mail(
                subject=subject,
                message=email_message,
                from_email=settings.EMAIL_HOST_USER,  # Use authenticated Gmail account
                recipient_list=['banaszekk123@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Twoja wiadomość została wysłana pomyślnie!')
        except Exception as e:
            messages.error(request, f'Wystąpił błąd podczas wysyłania wiadomości. Spróbuj ponownie później.')
            print(f"Email error: {e}")  # Log the error for debugging
        
        return redirect('contact')
