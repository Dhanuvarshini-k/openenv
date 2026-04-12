TICKETS = [
    {
        "ticket_id": "TKT-001",
        "customer_tier": "free",
        "message": "I was charged twice for the same order. Please refund the duplicate charge immediately.",
        "category": "billing",
        "priority": "medium",
        "team": "billing_team",
        "reply_keywords": ["refund", "duplicate", "charge", "billing", "transaction"]
    },
    {
        "ticket_id": "TKT-002",
        "customer_tier": "premium",
        "message": "The app keeps crashing every time I try to upload a file. It shows a fatal error on screen.",
        "category": "technical",
        "priority": "high",
        "team": "tech_team",
        "reply_keywords": ["crash", "upload", "error", "fix", "reinstall"]
    },
    {
        "ticket_id": "TKT-003",
        "customer_tier": "free",
        "message": "I cannot log in to my account. My password reset email is not arriving.",
        "category": "account",
        "priority": "medium",
        "team": "account_team",
        "reply_keywords": ["login", "password", "reset", "email", "account"]
    },
    {
        "ticket_id": "TKT-004",
        "customer_tier": "premium",
        "message": "My package has not arrived. The tracking shows it has been stuck for 5 days.",
        "category": "shipping",
        "priority": "high",
        "team": "shipping_team",
        "reply_keywords": ["package", "tracking", "delivery", "shipping", "investigate"]
    },
    {
        "ticket_id": "TKT-005",
        "customer_tier": "free",
        "message": "Someone hacked my account. I received an OTP I did not request. Unauthorized login detected.",
        "category": "security",
        "priority": "medium",
        "team": "security_team",
        "reply_keywords": ["security", "unauthorized", "otp", "account", "secure"]
    },
    {
        "ticket_id": "TKT-006",
        "customer_tier": "premium",
        "message": "My invoice shows an incorrect amount. I was billed for a plan I did not subscribe to.",
        "category": "billing",
        "priority": "high",
        "team": "billing_team",
        "reply_keywords": ["invoice", "billing", "plan", "amount", "refund"]
    },
    {
        "ticket_id": "TKT-007",
        "customer_tier": "free",
        "message": "The dashboard is loading very slowly. Every page takes more than 30 seconds to load.",
        "category": "technical",
        "priority": "medium",
        "team": "tech_team",
        "reply_keywords": ["slow", "loading", "performance", "dashboard", "fix"]
    },
    {
        "ticket_id": "TKT-008",
        "customer_tier": "free",
        "message": "I need to update the email address linked to my account but the settings page gives an error.",
        "category": "account",
        "priority": "medium",
        "team": "account_team",
        "reply_keywords": ["email", "update", "account", "settings", "verify"]
    },
    {
        "ticket_id": "TKT-009",
        "customer_tier": "premium",
        "message": "My delivery was marked as delivered but I never received the package at my address.",
        "category": "shipping",
        "priority": "high",
        "team": "shipping_team",
        "reply_keywords": ["delivery", "package", "address", "received", "investigate"]
    },
    {
        "ticket_id": "TKT-010",
        "customer_tier": "premium",
        "message": "I see suspicious login activity from a foreign country on my account. Please help secure it.",
        "category": "security",
        "priority": "high",
        "team": "security_team",
        "reply_keywords": ["suspicious", "login", "security", "secure", "unauthorized"]
    },
    {
        "ticket_id": "TKT-011",
        "customer_tier": "free",
        "message": "I requested a refund 10 days ago but still have not received it in my bank account.",
        "category": "billing",
        "priority": "medium",
        "team": "billing_team",
        "reply_keywords": ["refund", "bank", "transaction", "billing", "processing"]
    },
    {
        "ticket_id": "TKT-012",
        "customer_tier": "premium",
        "message": "The API keeps returning a 500 internal server error when I call the export endpoint.",
        "category": "technical",
        "priority": "high",
        "team": "tech_team",
        "reply_keywords": ["api", "error", "server", "endpoint", "fix"]
    },
    {
        "ticket_id": "TKT-013",
        "customer_tier": "free",
        "message": "My account was locked after too many failed login attempts. Please unlock it.",
        "category": "account",
        "priority": "medium",
        "team": "account_team",
        "reply_keywords": ["account", "locked", "login", "unlock", "verify"]
    },
    {
        "ticket_id": "TKT-014",
        "customer_tier": "free",
        "message": "The courier damaged my order during delivery. I want a replacement or a refund.",
        "category": "shipping",
        "priority": "medium",
        "team": "shipping_team",
        "reply_keywords": ["damaged", "delivery", "replacement", "refund", "courier"]
    },
    {
        "ticket_id": "TKT-015",
        "customer_tier": "premium",
        "message": "My two-factor authentication is broken. I am not receiving the security verification codes.",
        "category": "security",
        "priority": "high",
        "team": "security_team",
        "reply_keywords": ["two-factor", "authentication", "verification", "code", "secure"]
    },
    {
        "ticket_id": "TKT-016",
        "customer_tier": "free",
        "message": "I was charged after cancelling my subscription. Please investigate and issue a refund.",
        "category": "billing",
        "priority": "medium",
        "team": "billing_team",
        "reply_keywords": ["charge", "subscription", "cancel", "refund", "billing"]
    },
    {
        "ticket_id": "TKT-017",
        "customer_tier": "premium",
        "message": "The mobile app crashes on launch after the latest update. I have tried reinstalling.",
        "category": "technical",
        "priority": "high",
        "team": "tech_team",
        "reply_keywords": ["crash", "app", "update", "reinstall", "fix"]
    },
    {
        "ticket_id": "TKT-018",
        "customer_tier": "free",
        "message": "I cannot access my account. It says my account has been disabled without any explanation.",
        "category": "account",
        "priority": "medium",
        "team": "account_team",
        "reply_keywords": ["account", "disabled", "access", "verify", "restore"]
    },
    {
        "ticket_id": "TKT-019",
        "customer_tier": "premium",
        "message": "My shipment was sent to the wrong address even though I provided the correct one at checkout.",
        "category": "shipping",
        "priority": "high",
        "team": "shipping_team",
        "reply_keywords": ["shipment", "address", "wrong", "delivery", "reroute"]
    },
    {
        "ticket_id": "TKT-020",
        "customer_tier": "free",
        "message": "I received an email saying my password was changed but I did not make this change.",
        "category": "security",
        "priority": "medium",
        "team": "security_team",
        "reply_keywords": ["password", "changed", "unauthorized", "secure", "account"]
    },
    {
        "ticket_id": "TKT-021",
        "customer_tier": "premium",
        "message": "The payment gateway is declining my card even though my bank confirms no issues.",
        "category": "billing",
        "priority": "high",
        "team": "billing_team",
        "reply_keywords": ["payment", "card", "declined", "billing", "gateway"]
    },
    {
        "ticket_id": "TKT-022",
        "customer_tier": "free",
        "message": "The video player on your platform keeps buffering and does not play any content.",
        "category": "technical",
        "priority": "medium",
        "team": "tech_team",
        "reply_keywords": ["video", "buffering", "player", "fix", "content"]
    },
    {
        "ticket_id": "TKT-023",
        "customer_tier": "premium",
        "message": "I need to merge two accounts under the same email. Please help me with the process.",
        "category": "account",
        "priority": "high",
        "team": "account_team",
        "reply_keywords": ["merge", "account", "email", "verify", "process"]
    },
    {
        "ticket_id": "TKT-024",
        "customer_tier": "free",
        "message": "My order has been in processing state for 2 weeks. No shipping update has been provided.",
        "category": "shipping",
        "priority": "medium",
        "team": "shipping_team",
        "reply_keywords": ["order", "processing", "shipping", "update", "tracking"]
    },
    {
        "ticket_id": "TKT-025",
        "customer_tier": "premium",
        "message": "I found that someone is using my account credentials and placing orders. Please block them.",
        "category": "security",
        "priority": "high",
        "team": "security_team",
        "reply_keywords": ["credentials", "account", "block", "unauthorized", "secure"]
    },
    {
        "ticket_id": "TKT-026",
        "customer_tier": "free",
        "message": "My promo code discount was not applied even though it shows as valid on your website.",
        "category": "billing",
        "priority": "medium",
        "team": "billing_team",
        "reply_keywords": ["promo", "discount", "billing", "code", "apply"]
    },
    {
        "ticket_id": "TKT-027",
        "customer_tier": "premium",
        "message": "The data export feature is broken. Clicking export does nothing and no file is generated.",
        "category": "technical",
        "priority": "high",
        "team": "tech_team",
        "reply_keywords": ["export", "feature", "bug", "file", "fix"]
    },
    {
        "ticket_id": "TKT-028",
        "customer_tier": "free",
        "message": "I want to delete my account and all associated data as per GDPR requirements.",
        "category": "account",
        "priority": "medium",
        "team": "account_team",
        "reply_keywords": ["delete", "account", "data", "gdpr", "process"]
    },
    {
        "ticket_id": "TKT-029",
        "customer_tier": "premium",
        "message": "The delivery driver left my package at the wrong door and a neighbour has it.",
        "category": "shipping",
        "priority": "high",
        "team": "shipping_team",
        "reply_keywords": ["delivery", "package", "wrong", "neighbour", "retrieve"]
    },
    {
        "ticket_id": "TKT-030",
        "customer_tier": "free",
        "message": "I received a phishing email pretending to be from your company asking for my login details.",
        "category": "security",
        "priority": "medium",
        "team": "security_team",
        "reply_keywords": ["phishing", "email", "login", "secure", "report"]
    },
]
