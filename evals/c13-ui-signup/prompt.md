---
description: c13-ui-signup (held out: no copywriter example uses this brief)
tags: [heldout]
runs: 1
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Glob, Grep, Skill, Agent, Bash]
---

Our signup/login React component is still in English. Create src/Auth.tsx exporting a `fa` object with Persian (semi-formal) versions of these UI strings, keyed exactly like this:

phonePlaceholder: "Enter your mobile number"
codeSent: "We've sent a 5-digit code to your phone."
wrongCode: "That code is incorrect. Please try again."
resendCode: "Resend code"
accountCreated: "Your account has been created!"
logoutConfirm: "Are you sure you want to log out?"
getStarted: "Get started"
learnMore: "Learn more"
networkError: "Something went wrong. Check your connection and try again."
