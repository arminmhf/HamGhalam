---
description: c04-ui-checkout
tags: [ui, incidental, english-brief]
runs: 1
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Glob, Grep, Skill, Agent, Bash]
---

Our checkout React component is still in English. Create src/Checkout.tsx exporting a `fa` object with Persian (semi-formal) versions of these UI strings, keyed exactly like this:

emptyCart: "Your cart is empty"
paymentFailed: "Payment failed. Please try again."
addressSaved: "Address saved"
deliveryHint: "Pick a time when someone will be home to receive the order."
invalidCode: "This discount code is invalid or has expired."
orderConfirmed: "Your order has been placed! We'll text you when it ships."
getStarted: "Get started"
learnMore: "Learn more"
somethingWrong: "Something went wrong"
