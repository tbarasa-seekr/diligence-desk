# Lumera Health, Inc. — Security & Data Protection Overview (Customer-Shareable)

> **FICTIONAL DOCUMENT — FOR TRAINING USE ONLY.** Lumera Health, Inc. and every vendor named below except Microsoft Azure are invented for SeekrFlow enablement. All names, figures and events are made up. **Lumera Health, Inc. is not affiliated with any similarly named company.**

Company: Lumera Health, Inc. | Document: Security & Data Protection Overview | Version 3.1, effective June 1, 2026

## Section 1 — Lumera Health, Inc. — Company and Compliance

Company: Lumera Health, Inc. | Security & Data Protection Overview | Section 1 of 4

Lumera Health, Inc. ("Lumera Health") provides patient-intake and scheduling software to outpatient clinics. Lumera Health was founded in 2022, is headquartered in Durham, North Carolina, and has 41 employees.

- Lumera Health signs **Business Associate Agreements (BAAs)** with covered-entity customers and operates its program in line with the **HIPAA** Security Rule.
- Lumera Health holds a **SOC 2 Type II report, issued February 2026**, available to customers under NDA.

## Section 2 — Lumera Health, Inc. — Hosting and Encryption

Company: Lumera Health, Inc. | Security & Data Protection Overview | Section 2 of 4

- The platform is hosted in **Microsoft Azure (East US)**.
- Patient data is encrypted at rest using AES-256 and in transit using TLS 1.2 or higher.
- **Multi-factor authentication is enforced for all Lumera Health employees.** Security logs are retained for **180 days**.

## Section 3 — Lumera Health, Inc. — Continuity and Incident Response

Company: Lumera Health, Inc. | Security & Data Protection Overview | Section 3 of 4

- Production databases are backed up daily; **backups are retained for 14 days** with restores tested twice a year.
- Recovery objectives: **RTO 8 hours, RPO 4 hours**.
- Suspected breaches of protected health information are reported to affected covered-entity customers **within 72 hours**, consistent with Lumera Health's BAAs.

## Section 4 — Lumera Health, Inc. — Subprocessors

Company: Lumera Health, Inc. | Security & Data Protection Overview | Section 4 of 4

| Subprocessor | Purpose | Location | Data handled |
| --- | --- | --- | --- |
| Microsoft Azure | Cloud hosting | United States (East US) | Stores all patient data |
| Carepost | Patient appointment messaging | United States | Processes patient names and contact details to deliver reminders |
