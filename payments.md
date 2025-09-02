# Payment Integration Guide - HealthLinkAI

This document provides instructions for integrating payment processing with Flutterwave and Paystack for the HealthLinkAI freemium subscription model.

## Overview

HealthLinkAI uses a freemium model with two tiers:
- **Free**: Limited daily usage (5 symptom checks, 10 MindWell chats, 3 provider lookups)
- **Premium**: Unlimited usage + doctor callbacks + priority support ($9.99/month)

## Flutterwave Integration

### 1. Setup

```bash
pip install flutterwave-python
```

### 2. Environment Variables

Add to your `.env` file:

```env
# Flutterwave Sandbox Keys (Test Mode)
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_TEST-SANDBOXDEMOKEY-X
FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-SANDBOXDEMOKEY-X
FLUTTERWAVE_ENCRYPTION_KEY=FLWSECK_TEST-SANDBOXDEMOKEY-X
FLUTTERWAVE_WEBHOOK_SECRET=your_webhook_secret
```

### 3. Implementation Example

```python
from flutterwave import Flutterwave

# Initialize Flutterwave
fw = Flutterwave(
    public_key=os.getenv('FLUTTERWAVE_PUBLIC_KEY'),
    secret_key=os.getenv('FLUTTERWAVE_SECRET_KEY'),
    encryption_key=os.getenv('FLUTTERWAVE_ENCRYPTION_KEY')
)

@app.route('/payment/flutterwave', methods=['POST'])
def flutterwave_payment():
    user_id = session.get('user_id', 1)  # Get actual user ID
    plan = request.form.get('plan', 'premium')
    
    # Create payment payload
    payload = {
        "tx_ref": f"healthlink_{user_id}_{int(time.time())}",
        "amount": "9.99",
        "currency": "USD",
        "redirect_url": url_for('payment_callback', _external=True),
        "customer": {
            "email": "user@example.com",  # Get from user session
            "phonenumber": "+237600000000",
            "name": "User Name"
        },
        "customizations": {
            "title": "HealthLinkAI Premium Subscription",
            "description": "Monthly Premium Plan",
            "logo": "https://your-domain.com/logo.png"
        }
    }
    
    try:
        response = fw.payment.initiate(payload)
        if response['status'] == 'success':
            return redirect(response['data']['link'])
        else:
            flash('Payment initialization failed', 'error')
            return redirect(url_for('subscribe'))
    except Exception as e:
        flash(f'Payment error: {str(e)}', 'error')
        return redirect(url_for('subscribe'))

@app.route('/payment/callback')
def payment_callback():
    transaction_id = request.args.get('transaction_id')
    tx_ref = request.args.get('tx_ref')
    
    if transaction_id:
        # Verify payment
        response = fw.transaction.verify(transaction_id)
        
        if response['status'] == 'success' and response['data']['status'] == 'successful':
            # Update user subscription
            user_id = tx_ref.split('_')[1]  # Extract user ID from tx_ref
            subscription = get_user_subscription(user_id)
            subscription.plan = 'premium'
            db.session.commit()
            
            flash('Payment successful! Welcome to Premium!', 'success')
            return redirect(url_for('dashboard'))
    
    flash('Payment verification failed', 'error')
    return redirect(url_for('subscribe'))
```

### 4. Webhook Handler

```python
@app.route('/webhook/flutterwave', methods=['POST'])
def flutterwave_webhook():
    # Verify webhook signature
    signature = request.headers.get('verif-hash')
    if signature != os.getenv('FLUTTERWAVE_WEBHOOK_SECRET'):
        return 'Unauthorized', 401
    
    data = request.get_json()
    
    if data['event'] == 'charge.completed':
        tx_ref = data['data']['tx_ref']
        status = data['data']['status']
        
        if status == 'successful':
            # Process successful payment
            user_id = tx_ref.split('_')[1]
            # Update subscription logic here
            pass
    
    return 'OK', 200
```

## Paystack Integration

### 1. Setup

```bash
pip install paystackapi
```

### 2. Environment Variables

Add to your `.env` file:

```env
# Paystack Test Keys
PAYSTACK_PUBLIC_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PAYSTACK_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PAYSTACK_WEBHOOK_SECRET=your_webhook_secret
```

### 3. Implementation Example

```python
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction

# Initialize Paystack
paystack = Paystack(secret_key=os.getenv('PAYSTACK_SECRET_KEY'))

@app.route('/payment/paystack', methods=['POST'])
def paystack_payment():
    user_id = session.get('user_id', 1)
    plan = request.form.get('plan', 'premium')
    
    # Initialize transaction
    response = Transaction.initialize(
        reference=f"healthlink_{user_id}_{int(time.time())}",
        amount=999,  # Amount in kobo (9.99 * 100)
        email="user@example.com",  # Get from user session
        callback_url=url_for('paystack_callback', _external=True)
    )
    
    if response['status']:
        return redirect(response['data']['authorization_url'])
    else:
        flash('Payment initialization failed', 'error')
        return redirect(url_for('subscribe'))

@app.route('/payment/paystack/callback')
def paystack_callback():
    reference = request.args.get('reference')
    
    if reference:
        # Verify transaction
        response = Transaction.verify(reference)
        
        if response['status'] and response['data']['status'] == 'success':
            # Update user subscription
            user_id = reference.split('_')[1]
            subscription = get_user_subscription(user_id)
            subscription.plan = 'premium'
            db.session.commit()
            
            flash('Payment successful! Welcome to Premium!', 'success')
            return redirect(url_for('dashboard'))
    
    flash('Payment verification failed', 'error')
    return redirect(url_for('subscribe'))
```

### 4. Webhook Handler

```python
import hmac
import hashlib

@app.route('/webhook/paystack', methods=['POST'])
def paystack_webhook():
    # Verify webhook signature
    signature = request.headers.get('x-paystack-signature')
    body = request.get_data()
    
    expected_signature = hmac.new(
        os.getenv('PAYSTACK_WEBHOOK_SECRET').encode(),
        body,
        hashlib.sha512
    ).hexdigest()
    
    if signature != expected_signature:
        return 'Unauthorized', 401
    
    data = request.get_json()
    
    if data['event'] == 'charge.success':
        reference = data['data']['reference']
        # Process successful payment
        user_id = reference.split('_')[1]
        # Update subscription logic here
        pass
    
    return 'OK', 200
```

## Frontend Integration

### 1. Payment Button (Flutterwave)

```html
<script src="https://checkout.flutterwave.com/v3.js"></script>

<button onclick="makePayment()" class="btn-primary">
    Pay with Flutterwave
</button>

<script>
function makePayment() {
    FlutterwaveCheckout({
        public_key: "{{ flutterwave_public_key }}",
        tx_ref: "healthlink_{{ user_id }}_{{ timestamp }}",
        amount: 9.99,
        currency: "USD",
        country: "CM",
        payment_options: "card,mobilemoney,ussd",
        customer: {
            email: "{{ user_email }}",
            phone_number: "{{ user_phone }}",
            name: "{{ user_name }}",
        },
        callback: function (data) {
            console.log(data);
            window.location.href = "/payment/callback?transaction_id=" + data.transaction_id;
        },
        onclose: function() {
            console.log('Payment cancelled!');
        },
        customizations: {
            title: "HealthLinkAI Premium",
            description: "Monthly Premium Subscription",
            logo: "/static/img/logo.png",
        },
    });
}
</script>
```

### 2. Payment Button (Paystack)

```html
<script src="https://js.paystack.co/v1/inline.js"></script>

<button onclick="payWithPaystack()" class="btn-primary">
    Pay with Paystack
</button>

<script>
function payWithPaystack() {
    let handler = PaystackPop.setup({
        key: '{{ paystack_public_key }}',
        email: '{{ user_email }}',
        amount: 999, // Amount in kobo
        ref: 'healthlink_{{ user_id }}_{{ timestamp }}',
        callback: function(response) {
            window.location.href = "/payment/paystack/callback?reference=" + response.reference;
        },
        onClose: function() {
            alert('Payment window closed.');
        }
    });
    handler.openIframe();
}
</script>
```

## Mobile Money Support

Both Flutterwave and Paystack support mobile money payments popular in Cameroon:

### Supported Mobile Money Providers:
- **MTN Mobile Money**
- **Orange Money**
- **Express Union Mobile**

### Configuration:
```python
# For Flutterwave
payment_options = "card,mobilemoney,ussd,banktransfer"

# For Paystack
channels = ["card", "mobile_money", "ussd", "bank_transfer"]
```

## Testing

### Test Cards:

**Flutterwave Test Cards:**
- Successful: 4187427415564246
- Insufficient Funds: 4187427415564246 (amount > 10000)
- CVV: 828, Expiry: 09/32, PIN: 3310

**Paystack Test Cards:**
- Successful: 4084084084084081
- Insufficient Funds: 4084084084084081 (amount > 300000)
- CVV: 408, Expiry: any future date

### Test Mobile Money:
- Use test phone numbers provided in sandbox documentation
- Both providers offer comprehensive test environments

## Security Considerations

1. **Always verify payments server-side** - Never trust client-side confirmations
2. **Use webhook signatures** - Verify all webhook requests
3. **Store sensitive keys securely** - Use environment variables
4. **Implement idempotency** - Handle duplicate webhook calls
5. **Log all transactions** - For debugging and reconciliation

## Production Deployment

1. Replace test keys with live keys
2. Update webhook URLs to production endpoints
3. Implement proper error handling and logging
4. Set up monitoring for failed payments
5. Configure backup payment methods

## Support

- **Flutterwave**: https://developer.flutterwave.com/
- **Paystack**: https://paystack.com/docs/

Both providers offer excellent documentation and developer support for African markets.
