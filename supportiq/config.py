"""Shared intent metadata for the demo."""

from __future__ import annotations

INTENTS = {
    "track_order": {
        "label": "Order tracking",
        "icon": "📦",
        "action": "Ask for the order reference and check the carrier's tracking page.",
        "template": "I can help check your order status. Please share your order number so our team can look up the latest tracking details.",
    },
    "cancel_order": {
        "label": "Order cancellation",
        "icon": "🛑",
        "action": "Check whether the order has shipped and whether cancellation is allowed.",
        "template": "I can help with cancellation. Please provide the order number; we'll check whether the order is eligible to cancel.",
    },
    "get_refund": {
        "label": "Refund request",
        "icon": "↩️",
        "action": "Review refund eligibility and ask for the order reference.",
        "template": "I can help you start a refund request. Please share the order number and a short explanation of the problem.",
    },
    "payment_issue": {
        "label": "Payment problem",
        "icon": "💳",
        "action": "Check payment status safely; never ask for passwords, PINs or card details.",
        "template": "Sorry you're having trouble paying. Please tell us the error message and payment method used, without sharing sensitive card information.",
    },
    "recover_password": {
        "label": "Account access",
        "icon": "🔐",
        "action": "Direct the user to the official password-reset flow.",
        "template": "You can recover access using the 'Forgot password' option on the sign-in page. If that doesn't work, our team can help verify your account securely.",
    },
    "change_shipping_address": {
        "label": "Address update",
        "icon": "📍",
        "action": "Verify the order status before attempting an address change.",
        "template": "I can help with a shipping-address change. Please share your order number; our team will check whether the address can still be updated.",
    },
}

SAMPLES = {
    "track_order": "My order hasn't arrived yet. Can you tell me where the package is?",
    "cancel_order": "I placed an order by mistake and need to cancel it before shipping.",
    "get_refund": "The item arrived damaged and I want my money back.",
    "payment_issue": "The checkout charged my card twice. How can I fix the payment?",
    "recover_password": "I can't sign in because I forgot my password.",
    "change_shipping_address": "I entered the wrong delivery address. Can I update it?",
}
