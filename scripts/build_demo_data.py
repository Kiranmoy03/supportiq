"""Regenerate the original, hand-authored starter examples (no external data)."""

from __future__ import annotations

import csv
from pathlib import Path

EXAMPLES = {
    "track_order": """
Where can I track my order shipment?
My parcel has not arrived yet, can you locate it?
What is the current status of my online order?
Can I get the tracking number for my purchase?
The package is delayed and I need an update.
How do I find out where my delivery is?
My shipping status has not changed in days.
Could you check the delivery progress of my order?
I ordered shoes last week, are they on their way?
Please tell me when my package will reach me.
The courier tracking link is not updating.
How long until the item arrives at my door?
Can I see the estimated arrival date for my shipment?
My order still says in transit, what does that mean?
I want to know whether my parcel has been dispatched.
The estimated delivery date has already passed.
Has my recent order been shipped yet?
I need information about the whereabouts of my package.
I haven't received any tracking updates for my item.
When should I expect my headphones to be delivered?
Could you provide the latest parcel tracking information?
Can someone check if my order is out for delivery?
The shipment is stuck at the sorting facility.
My package seems lost, where is it now?
Please help me find my missing delivery.
Are there updates from the shipping carrier?
Track the delivery for my recent purchase please.
I need the expected delivery window for my order.
I can't find my shipment tracking details.
What happened to the order I placed on Monday?
Has the courier picked up my parcel?
Why is my delivery taking longer than expected?
I want to follow the progress of my shipped item.
My parcel did not show up on the promised date.
Could you look up the shipping progress for my laptop?
Do you know if my item has reached the local delivery hub?
""",
    "cancel_order": """
I need to cancel the order I just placed.
Please stop my purchase before it is shipped.
How can I cancel an unwanted order?
I bought the wrong product and want to cancel it.
Can you cancel my booking right away?
I changed my mind about my recent order.
Remove the order from my account, please.
I accidentally ordered two items and need one cancelled.
Can I undo a purchase that I made this morning?
I do not want this item anymore, cancel my order.
Is it too late to cancel my purchase?
I selected the wrong color, so please cancel that order.
Please stop processing my order.
I no longer need the item I ordered.
Where is the cancellation option in my order details?
Help me void this order before dispatch.
I'd like to withdraw the order I submitted yesterday.
I made a duplicate purchase by mistake, cancel it.
Can you prevent this order from being fulfilled?
I need to cancel my headphones order urgently.
How do I reverse an order before delivery begins?
I'm trying to cancel a purchase but the button doesn't work.
Please take the item off my order list.
Can I back out of a confirmed order?
I don't need the product, how do I cancel?
Stop the shipment because I ordered by accident.
Cancel the order instead of sending it to me.
I selected the wrong size and want to cancel.
Please help me withdraw my latest purchase.
Can I still cancel even though the order is processing?
I want to abort this order transaction.
I ordered without checking the details and need cancellation.
Is order cancellation available after checkout?
I want the merchant to void my order.
Don't ship my order, please cancel it instead.
I need a way to cancel my submitted purchase.
""",
    "get_refund": """
The product arrived broken and I want a refund.
Can I get my money back for this order?
I need to return the item and request reimbursement.
How do I submit a refund request?
Please refund the payment for my defective headphones.
I received a damaged item and would like my money returned.
What is the process for getting a refund?
I was sent the wrong product, can you reimburse me?
I am unhappy with my purchase and want a refund.
I need to claim a refund for a faulty product.
Please help me initiate a return and refund.
My item doesn't work and I want my money back.
Can you give me a refund for this purchase?
I would like to ask for a full refund.
The goods were not as described, so I need reimbursement.
I want to get a partial refund for the damaged package.
Are refunds possible for an incorrect order?
I need a refund because the item is unusable.
Can I apply for a refund after returning the parcel?
Please tell me how to get reimbursed for my purchase.
I'm requesting my payment back for a faulty charger.
What steps are required to receive a refund?
How can I open a refund case for my order?
The shirt arrived with a tear and I want the amount refunded.
I need to return these shoes and reclaim my money.
Please approve a refund for this defective product.
Can I receive a refund instead of a replacement?
I would prefer my money back over store credit.
I returned an item, how do I request a refund?
I need help asking for a refund on the damaged item.
I purchased the wrong item and would like a refund after return.
What is the refund process for an unsatisfactory purchase?
My new device stopped working and I want a reimbursement.
Can you issue a refund for the product that arrived cracked?
I would like to refund a recent purchase.
Please tell me if I can get the purchase amount back.
""",
    "payment_issue": """
My card was declined while checking out.
The checkout page keeps showing a payment error.
I was charged twice for a single order.
The UPI payment failed but money was deducted.
I cannot complete the transaction for my purchase.
My debit card payment is not going through.
The checkout is stuck on processing payment.
The bank says the charge succeeded but the website says failed.
There is an unexpected duplicate charge on my card.
What should I do about a failed credit card payment?
I can't pay through the available payment gateway.
My transaction was declined for no clear reason.
The payment page freezes when I enter checkout.
I see an error after submitting the payment form.
Please help resolve a billing transaction failure.
Why did the payment system charge me more than once?
The amount was deducted but the order is not confirmed.
My online payment keeps getting rejected.
I can't use my preferred payment method at checkout.
The wallet transaction failed during purchase.
My payment was interrupted midway through checkout.
I am being billed twice for the same purchase.
The app shows payment unsuccessful even though I paid.
A card authorization error prevents me from ordering.
I need help with a payment processing issue.
The payment gateway timed out after I clicked pay.
My credit card charge appears twice on the statement.
Why does checkout say transaction unsuccessful?
I have a billing error when trying to buy something.
Can you check why my payment was not accepted?
Money left my bank account but the payment status is pending.
The website won't accept my payment details.
I received a payment declined notification at checkout.
My net banking transaction returned an error.
I can't place the order because the payment fails.
I was debited even though checkout says the payment failed.
""",
    "recover_password": """
I forgot my login password and cannot sign in.
How can I reset my account password?
I have lost access to my account credentials.
The password I remember no longer works.
Can you send me a link to recover my password?
I am locked out of my profile and need to log in.
Help me regain access to my account.
I can't remember the password for my user account.
Where is the forgot password option?
I need to recover my account after losing my password.
My login is failing because I forgot the passcode.
Please help me reset my sign in details.
I cannot access my account and need a password reset.
How do I change a forgotten account password?
I forgot the credentials required to enter my profile.
The reset password email has not arrived.
I cannot get into my account after forgetting my password.
Please guide me through the password recovery process.
I need a new password for my shopping account.
My old password doesn't let me log in anymore.
How can I unlock my account and sign in again?
I can't sign in to my profile with my current password.
Could you provide instructions for recovering account access?
The password reset link is not working.
I need help logging back into my account.
My account login credentials are missing.
I forgot the password I created during registration.
How do I get back into a locked user profile?
I cannot remember my account password at all.
The password recovery form is not sending an email.
Can you assist with account password restoration?
I don't know my sign-in password anymore.
I am unable to authenticate to my customer account.
I need to regain access because my password is lost.
The login page says my password is incorrect.
I need to update my password but cannot sign in.
""",
    "change_shipping_address": """
I entered the wrong shipping address on my order.
Can I change where my package will be delivered?
Please update the delivery address for my purchase.
I have moved and need the parcel shipped to a different place.
How can I correct my shipping address after checkout?
I forgot my apartment number in the delivery address.
Please redirect my package to my new address.
I want to edit the destination for my order.
My street address is incorrect on the shipment details.
Can I change the postcode on my delivery address?
I need to update my shipping location before dispatch.
The courier has the wrong destination for my parcel.
Please change the city where my item is being delivered.
I used my old address by mistake when ordering.
Where do I modify the address on a confirmed order?
I need to change the shipping address for my headphones.
My house number is wrong on the order delivery details.
Can the parcel be sent to my office instead of home?
I want to replace the delivery location with another address.
The shipping information needs to be corrected.
Can I update my phone address details for this shipment?
My package should go to a different apartment.
I typed the wrong zip code for delivery.
Can you fix the address on my recent order?
I need to reroute the shipment to a new street.
Please update the delivery destination before shipping.
I put the wrong building number for the courier.
How do I amend the shipping information?
I need to switch the delivery address on my purchase.
The address used at checkout is no longer valid.
Can you send the item to my new home address?
I have to correct the delivery postal code.
My order should be shipped to another location.
Please let me change the saved delivery address for this order.
I want to modify the shipping address before the parcel arrives.
I made a mistake entering the recipient address.
""",
}


def main() -> None:
    destination = Path(__file__).resolve().parents[1] / "data" / "demo_tickets.csv"
    with destination.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "intent"])
        writer.writeheader()
        for intent, messages in EXAMPLES.items():
            for message in messages.strip().splitlines():
                writer.writerow({"text": message.strip(), "intent": intent})
    print(f"Wrote {sum(len(v.strip().splitlines()) for v in EXAMPLES.values())} demo examples")


if __name__ == "__main__":
    main()
