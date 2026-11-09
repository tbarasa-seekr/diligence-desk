# Lumera Pay, Inc. — Information Security Policy (Customer-Shareable Summary)

> **FICTIONAL DOCUMENT — FOR TRAINING USE ONLY.** Lumera Pay, Inc. is an invented company created for SeekrFlow enablement. All names, figures and events are made up. Lumera Pay, Inc. is not affiliated with any similarly named company.

Company: Lumera Pay, Inc. | Document: Information Security Policy | Version 2.3, effective July 1, 2026

## Section 1 — Lumera Pay, Inc. — Overview and Ownership

Company: Lumera Pay, Inc. | Information Security Policy | Section 1 of 6

Lumera Pay, Inc. ("Lumera Pay") provides accounts-payable automation and corporate card software to mid-market finance teams. Lumera Pay was founded in 2023, is headquartered in Richmond, Virginia, and has 28 employees.

Lumera Pay's information security program is owned by the Head of Security, who reports to the Chief Technology Officer. The program is reviewed by leadership twice a year. This document is the customer-shareable summary of that program.

## Section 2 — Lumera Pay, Inc. — Compliance and Assurance

Company: Lumera Pay, Inc. | Information Security Policy | Section 2 of 6

Lumera Pay completed a SOC 2 **Type I** examination; the report was issued in **March 2026** and is available to customers and prospects under NDA. A SOC 2 **Type II** observation period is in progress, with the Type II report expected in **Q1 2027**. Lumera Pay aligns its controls to the AICPA Trust Services Criteria.

## Section 3 — Lumera Pay, Inc. — Access Control and Authentication

Company: Lumera Pay, Inc. | Information Security Policy | Section 3 of 6

- Access follows least privilege. Access rights are reviewed quarterly, and access is removed on the employee's last day.
- **Multi-factor authentication (MFA) is enforced for all Lumera Pay employees on all company systems**, including the production environment, source control and internal tools.
- For customers, single sign-on (**SSO via SAML 2.0**) is available on the **Growth and Enterprise plans**. All customer plans support MFA for end users.

## Section 4 — Lumera Pay, Inc. — Encryption, Logging and Monitoring

Company: Lumera Pay, Inc. | Information Security Policy | Section 4 of 6

- Customer data is encrypted at rest using **AES-256** and in transit using **TLS 1.2 or higher**. Encryption keys are managed in the cloud provider's key management service and rotated annually.
- Security logs from production systems are centralized and retained for **365 days**. Alerts on anomalous activity are monitored by the on-call engineer.

## Section 5 — Lumera Pay, Inc. — Vulnerability Management and Testing

Company: Lumera Pay, Inc. | Information Security Policy | Section 5 of 6

- Automated vulnerability scans run **weekly** across production infrastructure and dependencies. Critical findings are remediated within 15 days.
- An independent third party performs a **penetration test annually**. The most recent test was completed in **May 2026** with no critical findings left open.
- Production changes require **peer code review and passing automated CI checks** before deployment. Emergency changes are reviewed within one business day after deployment.

## Section 6 — Lumera Pay, Inc. — People Security

Company: Lumera Pay, Inc. | Information Security Policy | Section 6 of 6

- All employees complete **security awareness training at hire and annually** thereafter.
- All employees undergo a **background check at hire**, where permitted by law.
- Employees sign confidentiality agreements as a condition of employment.
