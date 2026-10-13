# On-call Process

- **Rotation:** weekly, primary and secondary, with handoff on Monday at 10:00 local time.
- **Acknowledge** pages within 5 minutes. Escalate to the secondary at 15 minutes and to the engineering manager at 30.
- **Severity**
  - **SEV1**: customer-facing outage or SLO fast burn. All hands, status page, updates every 30 minutes.
  - **SEV2**: degraded service or slow burn. On-call owns it and updates hourly.
  - **SEV3**: no customer impact. Ticket, handled next business day.
- **Handoff notes:** open incidents, noisy alerts, risky changes planned this week.
- **Toil budget:** if any alert fires more than 3 times a week without action, fix or delete it.
