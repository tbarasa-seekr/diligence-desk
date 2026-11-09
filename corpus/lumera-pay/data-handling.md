# Lumera Pay, Inc. — Data Handling & Privacy Standard (Customer-Shareable Summary)

> **FICTIONAL DOCUMENT — FOR TRAINING USE ONLY.** Lumera Pay, Inc. is an invented company created for SeekrFlow enablement. All names, figures and events are made up. Lumera Pay, Inc. is not affiliated with any similarly named company.

Company: Lumera Pay, Inc. | Document: Data Handling & Privacy Standard | Version 1.8, effective July 1, 2026

## Section 1 — Lumera Pay, Inc. — Data Classification

Company: Lumera Pay, Inc. | Data Handling & Privacy Standard | Section 1 of 5

Lumera Pay classifies information in four levels: Public, Internal, Confidential and **Restricted**. All customer data — invoices, payment records, card transactions and the personal information of a customer's users — is classified **Restricted** and receives the strongest controls in this standard.

## Section 2 — Lumera Pay, Inc. — Where Customer Data Lives

Company: Lumera Pay, Inc. | Data Handling & Privacy Standard | Section 2 of 5

- Customer data is stored and processed in **Amazon Web Services (AWS), US East (us-east-1)**. Encrypted replicas are maintained in **US West (us-west-2)** for disaster recovery only.
- **Lumera Pay does not currently offer EU or other non-US data residency.** All customer data remains in the United States regions listed above.
- Customer data is encrypted at rest (AES-256) and in transit (TLS 1.2 or higher), as described in the Information Security Policy.

## Section 3 — Lumera Pay, Inc. — Access to Customer Data

Company: Lumera Pay, Inc. | Data Handling & Privacy Standard | Section 3 of 5

- Employee access to customer data is limited to **support and engineering roles that need it to serve the customer**, and every access is logged.
- **Production customer data is never copied into development or test environments.** Development and testing use synthetic data only.
- Customer data is shared with third parties only as described in the Subprocessor & Vendor List.

## Section 4 — Lumera Pay, Inc. — Retention and Deletion

Company: Lumera Pay, Inc. | Data Handling & Privacy Standard | Section 4 of 5

- During the contract term, customer data is retained for as long as the customer keeps it in the product.
- After contract termination, **customer data is deleted from production systems within 30 days**, and from encrypted backups as those backups expire on their normal schedule. **Written confirmation of deletion is provided on request.**

## Section 5 — Lumera Pay, Inc. — Privacy Commitments

Company: Lumera Pay, Inc. | Data Handling & Privacy Standard | Section 5 of 5

- A **GDPR-aligned Data Processing Addendum (DPA)** is available to all customers and lists the subprocessors in the Subprocessor & Vendor List.
- Lumera Pay acts as a processor of its customers' data; customers remain the controllers of their own records.
- Privacy requests received from a customer's end users are routed to that customer within 5 business days.
