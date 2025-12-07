"""
Email utilities for sending order confirmations and invoices
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .invoice import generate_invoice_pdf
import logging

logger = logging.getLogger(__name__)


def send_order_confirmation_email(order):
    """
    Send order confirmation email with invoice PDF attached
    """
    try:
        # Generate invoice PDF
        invoice_pdf = generate_invoice_pdf(order)
        
        # Prepare email context
        context = {
            'order': order,
            'customer_name': order.customer_name,
            'order_id': order.order_id,
            'total': order.total,
            'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000',
        }
        
        # Render email templates
        subject = f'Order Confirmation - {order.order_id} | LUVORA'
        html_message = render_to_string('shop/emails/order_confirmation.html', context)
        text_message = render_to_string('shop/emails/order_confirmation.txt', context)
        
        # Create email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@luvora.com',
            to=[order.customer_email],
        )
        
        # Add HTML alternative
        email.attach_alternative(html_message, "text/html")
        
        # Attach invoice PDF
        email.attach(
            f'Invoice_{order.order_id}.pdf',
            invoice_pdf.read(),
            'application/pdf'
        )
        
        # Send email
        email.send(fail_silently=False)
        
        logger.info(f"Order confirmation email sent to {order.customer_email} for order {order.order_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send order confirmation email for order {order.order_id}: {str(e)}")
        return False


def send_order_status_update_email(order, message=''):
    """
    Send email when order status is updated
    """
    try:
        context = {
            'order': order,
            'customer_name': order.customer_name,
            'order_id': order.order_id,
            'status': order.get_status_display(),
            'message': message,
            'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000',
        }
        
        subject = f'Order {order.order_id} - Status Update | LUVORA'
        html_message = render_to_string('shop/emails/order_status_update.html', context)
        text_message = render_to_string('shop/emails/order_status_update.txt', context)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@luvora.com',
            to=[order.customer_email],
        )
        
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"Order status update email sent to {order.customer_email} for order {order.order_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send order status update email for order {order.order_id}: {str(e)}")
        return False
