# Lumera Pay, Inc. — Business Continuity & Incident Response Summary (Customer-Shareable)

> **FICTIONAL DOCUMENT — FOR TRAINING USE ONLY.** Lumera Pay, Inc. is an invented company created for SeekrFlow enablement. All names, figures and events are made up. Lumera Pay, Inc. is not affiliated with Lumera Health, Inc. or any other similarly named company.

Company: Lumera Pay, Inc. | Document: Business Continuity & Incident Response Summary | Version 1.4, effective July 1, 2026

## Section 1 — Lumera Pay, Inc. — Resilience Architecture

Company: Lumera Pay, Inc. | Business Continuity & Incident Response | Section 1 of 4

The Lumera Pay platform runs across **multiple availability zones in AWS us-east-1**, with encrypted cross-region replication to **us-west-2** for disaster recovery. The business continuity plan is **tested at least annually**; the most recent tabletop exercise was completed in **June 2026**.

Recovery objectives for a regional failure:

- **Recovery Time Objective (RTO): 4 hours**
- **Recovery Point Objective (RPO): 1 hour**

## Section 2 — Lumera Pay, Inc. — Backups

Company: Lumera Pay, Inc. | Business Continuity & Incident Response | Section 2 of 4

- Production databases are backed up **automatically every day**. Backups are encrypted with the same AES-256 standard as production data.
- **Backups are retained for 35 days** and then destroyed on schedule.
- **Restores are tested quarterly** by recovering a recent backup into an isolated environment and verifying data integrity.

## Section 3 — Lumera Pay, Inc. — Incident Response

Company: Lumera Pay, Inc. | Business Continuity & Incident Response | Section 3 of 4

- Incidents are classified **SEV-1 (critical) through SEV-3 (minor)**, with an **on-call engineer available 24/7**.
- Platform availability incidents are posted to the Lumera Pay status page as they are worked.
- **Customers are notified within 48 hours of a confirmed security incident affecting their data**, with a description of the incident, the data involved and the remediation under way.
- A **post-incident review is completed within 5 business days** of resolution for every SEV-1 and SEV-2 incident, and corrective actions are tracked to completion.

## Section 4 — Lumera Pay, Inc. — Customer Responsibilities

Company: Lumera Pay, Inc. | Business Continuity & Incident Response | Section 4 of 4

Customers are responsible for administering their own users, protecting their own credentials and reporting suspected incidents to Lumera Pay support. Lumera Pay's commitments in this document apply to the Lumera Pay platform and do not extend to systems the customer operates.
