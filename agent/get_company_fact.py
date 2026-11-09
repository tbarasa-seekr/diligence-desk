def get_company_fact(company: str, fact_key: str) -> str:
    """Return one exact compliance fact for a named company from its compliance record.

    Use this function only to confirm an exact figure, date, or registry entry after you have
    found the topic in the trust documents with the file search tool. Never quote its output as
    evidence; evidence must come from a document passage. Valid fact_key values: soc2,
    backup_retention, deletion_after_termination, security_log_retention, rto_rpo,
    incident_notification, encryption, sso, eu_data_residency, hosting, subprocessors,
    pen_test, vuln_scans.

    Args:
        company (str): The company's full legal name exactly as the user wrote it, for example "Lumera Pay, Inc.".
        fact_key (str): One of the valid fact_key values listed above.

    Returns:
        str: The exact fact, or "NO RECORD" when the company or key is unknown.
    """
    facts = {
        "lumera pay, inc.": {
            "soc2": "SOC 2 Type I report issued March 2026; Type II report expected Q1 2027",
            "backup_retention": "backups retained for 35 days; restores tested quarterly",
            "deletion_after_termination": "deleted from production systems within 30 days of termination",
            "security_log_retention": "security logs retained for 365 days",
            "rto_rpo": "RTO 4 hours; RPO 1 hour",
            "incident_notification": "customers notified within 48 hours of a confirmed security incident affecting their data",
            "encryption": "AES-256 at rest; TLS 1.2 or higher in transit",
            "sso": "SSO via SAML 2.0 on Growth and Enterprise plans",
            "eu_data_residency": "not offered; customer data remains in US regions",
            "hosting": "AWS us-east-1 with encrypted DR replicas in us-west-2",
            "subprocessors": "AWS (stores all customer data, US); HelpHarbor (support correspondence, US); Mailgrove (names and emails, US); Sightline Analytics (pseudonymized usage events only, US)",
            "pen_test": "annual third-party penetration test; most recent May 2026, no critical findings left open",
            "vuln_scans": "weekly scans; critical findings remediated within 15 days",
        }
    }
    record = facts.get(str(company).strip().lower())
    if record is None:
        return "NO RECORD"
    return record.get(str(fact_key).strip().lower(), "NO RECORD")
