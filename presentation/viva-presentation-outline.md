# Viva Presentation Outline - Salesforce-to-SAP Security Gateway (SS-SAP-IG)

## Slide 1: Cyber Security Assignment
**Course**: SSABZG681 / SEZG681 Advanced Cyber Security
**Project**: Enterprise Salesforce-to-SAP Integration Gateway Architecture Evaluation
**Team**: Jyoti (Salesforce Lead) & Shreya (SAP Lead)
**Declaration**: Anonymized Enterprise Architecture

## Slide 2: System Purpose & Operational Criticality
Operational bridge between Salesforce Sales Cloud and SAP S/4HANA ERP.
Processes $15M daily B2B transactions across pricing, credit checks, and inventory.

## Slide 3: C4 Architecture Blueprint
Overview of C4 Level 1 Context and Level 2 Container Diagrams.
Trust boundaries identified between Public Cloud, iPaaS, and Core ERP.

## Slide 4: Data Classification & CIA Impact
Asset Valuation: Customer PII, Financial Ledgers, SAP Integration Credentials.
Regulatory Scope: SOX 404, GDPR, DPDP Act, ISO 27001.

## Slide 5: Threat Scenario 1 - Payload Tampering (CVSS 9.1)
Interception of OAuth tokens leading to unit price tampering ($10,000 -> $1).
Progression through MuleSoft worker to SAP BAPI execution.

## Slide 6: Threat Scenario 2 - SAP OData Exfiltration (CVSS 9.8)
Unauthenticated access to exposed SAP NetWeaver OData endpoints.
Bulk table extraction (S_TABU_DIS) leading to financial data loss.

## Slide 7: Four-Layer Defense-in-Depth Model
**Layer 1**: RS256 Payload Signing & HashiCorp Vault Dynamic Secrets.
**Layer 2**: ZTNA Private Link & Mutual TLS (mTLS).
**Layer 3**: JSON Schema Bound Validation & OPA ABAC Policies.
**Layer 4**: Splunk SIEM, SAP ETD, and Automated SOAR Playbooks.

## Slide 8: Gap Analysis & CVSS Risk Quantification
CVSS v3.1 Scores: 9.1 (Critical) & 9.8 (Critical).
Risk Register overview and Target Architecture improvements.

## Slide 9: High-Impact Remediation Strategy
Priority Action: RS256 Cryptographic Payload Signing & JSON Schema Validation.
5-Week phased deployment plan.

## Slide 10: Technical & Organizational Reflection
Balancing developer velocity, Salesforce Governor limits, and legacy SAP RFCs.
TCO and ROI justification for business leadership.
