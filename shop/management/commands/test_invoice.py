"""
Management command to test invoice generation and email sending
"""
from django.core.management.base import BaseCommand
from shop.models import Order
from shop.invoice import generate_invoice_pdf
from shop.email_utils import send_order_confirmation_email


class Command(BaseCommand):
    help = 'Test invoice generation and email sending for an order'

    def add_arguments(self, parser):
        parser.add_argument(
            'order_id',
            type=str,
            help='Order ID to generate invoice for'
        )
        parser.add_argument(
            '--save',
            action='store_true',
            help='Save PDF to file instead of just testing generation'
        )
        parser.add_argument(
            '--email',
            action='store_true',
            help='Send test email with invoice'
        )

    def handle(self, *args, **options):
        order_id = options['order_id']
        
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Order {order_id} not found'))
            return
        
        self.stdout.write(f'Testing invoice for order: {order.order_id}')
        self.stdout.write(f'Customer: {order.customer_name}')
        self.stdout.write(f'Total: ₹{order.total}')
        self.stdout.write('')
        
        # Generate PDF
        try:
            pdf_buffer = generate_invoice_pdf(order)
            self.stdout.write(self.style.SUCCESS('✓ Invoice PDF generated successfully'))
            
            if options['save']:
                filename = f'invoice_{order.order_id}.pdf'
                with open(filename, 'wb') as f:
                    f.write(pdf_buffer.read())
                self.stdout.write(self.style.SUCCESS(f'✓ Saved to {filename}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Invoice generation failed: {str(e)}'))
            return
        
        # Send email
        if options['email']:
            try:
                send_order_confirmation_email(order)
                self.stdout.write(self.style.SUCCESS(f'✓ Email sent to {order.customer_email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Email sending failed: {str(e)}'))
