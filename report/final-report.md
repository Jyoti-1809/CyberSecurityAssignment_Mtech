# Advanced Cyber Security Assignment Report

## Cover Page & Submission Form

| Parameter | Details |
| :--- | :--- |
| **Course Title & Code** | SSABZG681: Advanced Cyber Security |
| **Evaluation Component** | EC-1: Expanded Situated Learning Project |
| **Weightage** | 30 Marks |
| **Student 1 Name & ID** | [Jyoti] ([2024ab12529]) - Salesforce Lead |
| **Student 2 Name & ID** | [Shreya] ([2024ab12519]) - SAP Lead |
| **Years of Experience** | [Jyoti - 4yrs, Shreya - 5.5 yrs] |
| **Current Roles** | Salesforce Developer/ SAP EWM/MM Logistics Analyst|
| **Industry Domain** | Enterprise Salesforce Cloud Software & ERP Systems |
| **Selected System Name** | Enterprise Salesforce-to-SAP B2B Commerce Gateway (SS-SAP-IG) |
| **System Type** | Anonymized / Simulated Enterprise Integration Architecture |

**Confidentiality Statement:** This report utilizes an anonymized, simulated enterprise architecture inspired by production-grade Salesforce CRM and SAP S/4HANA integration patterns. No proprietary organizational information, live internal IP addresses, real credentials, or restricted corporate customer data are disclosed. Safe abstraction guidelines have been strictly applied throughout.

---

## Executive Summary

This report delivers an enterprise-grade cyber security architecture evaluation of the **Salesforce-to-SAP B2B Commerce Gateway (SS-SAP-IG)**. The system serves as the mission-critical transactional bridge between customer-facing CRM platforms (Salesforce Experience Cloud & Sales Cloud) and the core backend enterprise resource planning platform (SAP S/4HANA ERP). It handles real-time credit checks, order provisioning, pricing calculations, inventory allocations, and customer master data synchronization.

Because this gateway controls the direct flow from public customer interaction to backend financial and supply chain ledgers, any breach in confidentiality, integrity, or availability introduces severe financial, operational, and regulatory exposure. This evaluation applies C4 architecture modeling, data classification, CIA triad impact analysis, multi-stage threat modeling, CVSS v3.1 risk quantification, defense-in-depth engineering, and enterprise constraint analysis.

The evaluation identifies two high-priority threat vectors: OAuth 2.0 middleware token interception enabling BAPI payload tampering, and unauthenticated OData service exposure leading to financial ledger exfiltration. To eliminate these risks, a four-layer defense-in-depth model is designed, incorporating mTLS, ABAC policy enforcement, cryptographically signed payload tokens, automated SIEM correlation, and HSM-backed key management. The single highest-impact immediate remediation plan establishes enforced mTLS and JSON schema validation at the MuleSoft Integration Gateway within a 5-week phased deployment.

---

## B.2 Anchor: System and Threat Surface Blueprinting

### 1. System Description
The **Salesforce-to-SAP Gateway (SS-SAP-IG)** is an automated enterprise integration platform. It allows B2B customers and internal sales teams working within Salesforce Sales Cloud and Experience Cloud to execute real-time quotes, query inventory availability, place bulk purchase orders, and track invoice status directly from the SAP S/4HANA ERP backend.

* **Primary Business Purpose:** Automate end-to-end B2B order fulfillment, credit authorization, pricing calculations, and customer record synchronization.
* **Key User Groups:** External B2B Enterprise Buyers, Internal Sales Operations Representatives, SAP Inventory Managers, Enterprise Security Operations Center (SOC) Analysts.
* **Operational Importance:** Processing over $15M in daily transactions, system downtime halts global order fulfillment, while integrity violations in pricing or credit limits lead to direct financial fraud.

### 2. Runtime Architecture
The system consists of a hybrid cloud/on-premises architecture:
* **Frontend Layer:** Salesforce Sales Cloud & Experience Cloud (SaaS), utilizing Salesforce Apex and LWC components.
* **Middleware / Integration Layer:** MuleSoft Anypoint Integration Platform deployed on AWS Cloud (iPaaS), acting as API Gateway, OAuth provider, and protocol transformer (REST/JSON to SAP OData/RFC BAPI).
* **Backend Layer:** SAP S/4HANA ERP deployed on-premise / private cloud, running NetWeaver, SAP Gateway, and HANA DB.
* **Identity & Key Management Layer:** Enterprise Identity Provider (Okta / Entra ID) utilizing OIDC/SAML 2.0, with HashiCorp Vault for secrets management.
* **Monitoring Layer:** Cloud-native logging pipeline streaming to Splunk Enterprise SIEM.

---

### 3. Architecture Diagrams (C4 Model)

#### C4 Level 1: System Context Diagram
```plantuml
@startuml
!include [https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml](https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml)
LAYOUT_WITH_LEGEND()

title C4 Level 1: Enterprise Salesforce-to-SAP Integration Gateway Context

Person(b2bCustomer, "B2B Enterprise Buyer", "Places bulk orders and queries quotes via web portal")
Person(salesRep, "Sales Representative", "Manages accounts, quotes, and custom pricing in Salesforce")
Person(secAnalyst, "SOC Analyst", "Monitors security events, anomalous transactions, and API threats")

System(ssGateway, "Salesforce-to-SAP Gateway System", "Orchestrates order placement, pricing, credit checks, and inventory sync")

System_Ext(salesforce, "Salesforce CRM Cloud", "Customer UI, Lead management, Quote generation")
System_Ext(sapERP, "SAP S/4HANA ERP", "Backend financial ledger, inventory master, BAPI execution")
System_Ext(idp, "Enterprise Identity Provider", "Authenticates users via OIDC/SAML 2.0")
System_Ext(siem, "Enterprise SIEM/SOAR", "Centralized security event logging and incident response")

Rel(b2bCustomer, salesforce, "Submits orders & queries stock", "HTTPS / TLS 1.3")
Rel(salesRep, salesforce, "Manages deals & quotes", "HTTPS / TLS 1.3")
Rel(salesforce, ssGateway, "Triggers order execution APIs", "HTTPS / OAuth 2.0 REST")
Rel(ssGateway, sapERP, "Executes BAPI / OData calls", "mTLS / SAP RFC / OData")
Rel(ssGateway, idp, "Validates user & service tokens", "HTTPS / OAuth 2.0")
Rel(ssGateway, siem, "Streams audit & security logs", "Syslog / TLS")
Rel(secAnalyst, siem, "Analyzes alerts & threat streams", "HTTPS")
@enduml

C4 Level 2: Container Diagram
@startuml
!include [https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml](https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml)
LAYOUT_WITH_LEGEND()

title C4 Level 2: Enterprise Salesforce-to-SAP Integration Gateway Containers

Person(salesUser, "Salesforce User / API Client", "Authenticated user or service agent")

System_Boundary(gatewayBoundary, "Salesforce-to-SAP Gateway (SS-SAP-IG)") {
    Container(sfNamedCred, "Salesforce Named Credentials", "Salesforce Security Module", "Stores encrypted outbound endpoints and tokens")
    Container(apiGateway, "MuleSoft API Gateway", "Anypoint Platform / NGINX", "Handles rate limiting, WAF, OAuth token verification, and routing")
    Container(integrationApp, "Order Transformation Microservice", "Mule runtime / Java", "Validates JSON schemas, maps payloads to SAP BAPIs, enforces ABAC")
    Container(vault, "Secrets Manager", "HashiCorp Vault", "Stores SAP service account credentials and private signing keys")
    Container(sapAdapter, "SAP Connector Gateway", "SAP JCo / OData Adapter", "Translates REST requests into SAP RFC/BAPI calls")
}

System_Ext(sapSystem, "SAP S/4HANA ERP Engine", "Main business logic, NetWeaver Gateway, HANA DB")
System_Ext(idp, "Enterprise IdP", "Okta / Entra ID")
System_Ext(siem, "Splunk SIEM", "Security Monitoring")

Rel(salesUser, sfNamedCred, "Initiates action", "Internal SF Protocol")
Rel(sfNamedCred, apiGateway, "Sends REST JSON Request", "HTTPS / TLS 1.3 + OAuth JWT")
Rel(apiGateway, idp, "Validates JWT signature & scopes", "HTTPS / OIDC")
Rel(apiGateway, integrationApp, "Forwards validated request", "mTLS / Internal VPC")
Rel(integrationApp, vault, "Fetches dynamic SAP credentials", "mTLS / HTTPS")
Rel(integrationApp, sapAdapter, "Passes transformed payload", "In-Memory / SEC")
Rel(sapAdapter, sapSystem, "Executes RFC/OData calls", "mTLS / Encrypted SAP SNC")
Rel(integrationApp, siem, "Streams structured audit logs", "Encrypted Syslog")
@enduml

C4 Level 3: Component Diagram (Order Transformation Microservice)
@startuml
!include [https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml](https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml)
LAYOUT_WITH_LEGEND()

title C4 Level 3: Component Diagram - Order Transformation Microservice

Container_Boundary(transService, "Order Transformation Microservice") {
    Component(tokenAuth, "OAuth & JWT Verifier", "Spring Security / Java", "Validates bearer token signatures, expiration, and claims")
    Component(schemaVal, "JSON Schema Validator", "Everit JSON Validator", "Strictly enforces mandatory fields, numerical bounds, and data types")
    Component(abacEngine, "ABAC Policy Engine", "Open Policy Agent (OPA)", "Verifies user roles, deal limits, and tenant boundaries")
    Component(transformer, "Data Mapping Engine", "DataWeave 2.0", "Transforms JSON structures into SAP XML/BAPI parameters")
    Component(replayCheck, "Replay & Nonce Manager", "Redis Cache", "Checks transaction UUIDs to prevent duplicate execution")
    Component(auditComp, "Audit & Security Logger", "Log4j2 / JSON Appender", "Generates immutable audit logs with correlation IDs")
}

Container(apiGw, "API Gateway", "MuleSoft")
Container(sapGateway, "SAP Connector Gateway", "SAP JCo")
Container(siemSys, "Splunk SIEM", "Enterprise Monitoring")

Rel(apiGw, tokenAuth, "Delivers payload", "mTLS")
Rel(tokenAuth, schemaVal, "Authenticated context")
Rel(schemaVal, replayCheck, "Validated structure")
Rel(replayCheck, abacEngine, "Unique request UUID")
Rel(abacEngine, transformer, "Authorized policy decision")
Rel(transformer, sapGateway, "Passes BAPI payload")
Rel(tokenAuth, auditComp, "Logs auth failure/success")
Rel(abacEngine, auditComp, "Logs policy denials")
Rel(auditComp, siemSys, "Streams log events")
@endl

4. Data Flow Mapping

| Source | Destination | Protocol / Transport | Data Type | Trust Boundary | Security Requirements |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Salesforce CRM** | MuleSoft API Gateway | HTTPS / TLS 1.3 | Order JSON, JWT Bearer Token | Public Cloud to Enterprise Middleware Boundary | TLS 1.3, OAuth 2.0, IP Whitelisting |
| **API Gateway** | Transformation Service | mTLS / Private VPC | Authenticated Payload | Middleware Perimeter to Microservice Boundary | Mutual TLS, Rate Limiting, WAF Inspection |
| **Transformation Service** | HashiCorp Vault | HTTPS / TLS 1.3 | Service Credentials, RSA Keys | Application to Secrets Store Boundary | Token-based auth, Dynamic Secret Lease |
| **Transformation Service** | SAP Gateway | mTLS / SAP SNC | Transformed BAPI / OData XML | Cloud iPaaS to On-Premises ERP Boundary | Encrypted SNC, Dedicated IPsec Tunnel, ABAC |
| **SAP Gateway** | SAP S/4HANA Core | Internal SAP RFC / SNC | Native BAPI Calls, SQL Executions | DMZ to Core Financial Ledger Boundary | SAP Authorizations (PFCG), Hardened RFC |
| **All Services** | Splunk SIEM | Syslog over TLS | Audit Logs, Error Telemetry | Enterprise Application to SOC Boundary | Immutable Transport, Log Masking (PII) |

5. Data Classification Matrix

| Asset / Data Element | Description | Criticality | Confidentiality Impact | Integrity Impact | Availability Impact | Data Owner | Regulatory / Policy Mapping | Retention Period | Required Security Controls |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B2B Customer PII & Credentials** | Customer names, tax IDs, email addresses, OAuth tokens | High | High | Medium | Medium | Chief Data Officer | GDPR, DPDP Act, ISO 27001 | 7 Years | AES-256 at rest, TLS 1.3 in transit, Column-level encryption, Anonymization |
| **Financial Ledger & Pricing Master** | Wholesale price books, discount tiers, credit limits, invoices | Critical | High | Critical | High | VP of Finance | SOX, PCI-DSS, SOC 2 | 10 Years | Cryptographic signing, Immutable audit trail, ABAC authorization |
| **SAP Integration Credentials** | System service account keys, Vault tokens, private signing keys | Critical | Critical | Critical | Critical | CISO / Security Ops | NIST SP 800-53, Enterprise Key Mgmt Policy | Rotation: 30 days | HashiCorp Vault storage, Automated rotation, HSM root-of-trust |
| **Order & Inventory Transactions** | B2B orders, inventory status, warehouse fulfillment status | High | Medium | High | High | Global Supply Chain Lead | Enterprise Risk Policy, Internal Audit | 5 Years | Replay protection, JSON schema validation, Non-repudiation logging |

6. Regulatory and Compliance Boundary Mapping
GDPR & DPDP Act: Customer contact details synchronized between Salesforce and SAP must support "Right to be Forgotten" and "Data Minimization". PII transferred across international cloud regions must utilize EU Standard Contractual Clauses (SCCs) and local data isolation.

Sarbanes-Oxley Act (SOX) Section 404: Pricing structures, discount rules, and order postings into SAP directly impact financial statements. Strict separation of duties (SoD) and tamper-proof logging of pricing overrides are legally mandated.

ISO/IEC 27001:2022 & SOC 2 Type II: Enforces controls for zero-trust API architecture, continuous vulnerability scanning, secrets rotation, and centralized security monitoring.

B.3 Apply: Advanced Cyber Security Engineering Pipeline
Task 1: CIA Asset Valuation and Cryptographic Policy
CIA Failure Scenarios & Business Impact
Confidentiality Failure Scenario: An attacker intercepts or extracts unencrypted OData service responses containing customer pricing agreements, tax identifiers, and global B2B discount matrices.

Business Impact: Severe commercial damage, loss of competitive edge, regulatory fines under DPDP/GDPR up to 4% of annual turnover, legal breach notification requirements.

Integrity Failure Scenario: An attacker executes a parameter tampering attack on the Salesforce-to-SAP payload, altering unit price fields from $5,000 to $5, or expanding customer credit limits during BAPI submission.

Business Impact: Immediate direct financial fraud, inventory depletion without payment, operational friction, failure of SOX financial audits.

Availability Failure Scenario: A Distributed Denial of Service (DDoS) attack or XML/JSON parser bomb targets the MuleSoft API Gateway, overwhelming worker threads and severing connection to SAP.

Business Impact: Complete shutdown of global B2B order processing, exceeding $600,000 per hour in lost revenue and breaches of customer SLA agreements.

Security Model Justification
Zero Trust Architecture (ZTA): Network locations offer no implicit trust. Every API request from Salesforce must be explicitly authenticated, authorized, and cryptographically verified before reaching SAP.

Attribute-Based Access Control (ABAC): Dynamic policies evaluate user role, deal threshold, tenant organization ID, customer geography, and request timestamp.

Biba Integrity Model ("No Read Down, No Write Up"): Applied to maintain strict core ERP ledger integrity. Data originating from external unvalidated sources (Salesforce web forms) cannot directly modify high-integrity SAP financial databases without passing through strict validation and sanitizer controls.

Cryptographic Policy Specifications
Data in Transit: TLS 1.3 enforced on all public and cloud perimeter endpoints. TLS 1.2 with strong cipher suites (TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384) mandated for internal VPC connections. Mutual TLS (mTLS) required between Salesforce, MuleSoft, and SAP Gateway.

Data at Rest: All databases, object stores, and message queues encrypted using AES-256-GCM. Column-level encryption applied to customer PII and authentication secrets.

Key Management: Centralized HashiCorp Vault integrated with AWS KMS / HSM. Master keys backed by FIPS 140-2 Level 3 Hardware Security Modules. Automatic rotation enforced every 30 days for service tokens and 90 days for asymmetric signing certificates.

Task 2: Multi-Stage Threat Modeling and Attack Graphs
Threat Scenario 1: Salesforce-to-SAP OAuth Token Interception & BAPI Payload Tampering
Threat Actor: Compromised Third-Party Vendor / Malicious Insider with Salesforce Developer privileges.

Objective: Manipulate B2B purchase orders in SAP to issue goods at zero price and exceed assigned credit lines.

Affected Assets: Salesforce Named Credentials, MuleSoft Integration Engine, SAP S/4HANA Sales Order BAPI.
Threat Scenario 1: Attack Graph Table
**Scenario:** Salesforce-to-SAP OAuth Token Interception & BAPI Payload Tampering

| Stage | Attacker Action | Target Component | Weakness Exploited | Evidence / Logs Generated | Detection Control | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Reconnaissance** | Scans Salesforce Apex code and Named Credentials configuration | Salesforce Org | Over-privileged developer access, visible sandbox credentials | Salesforce Event Monitoring logs, Setup Audit Trail | CI/CD static code review (Checkmarx) | Enforce principle of least privilege, mask credential variables |
| **Initial Access** | Extracts static OAuth Client Secret or session token from Apex memory dump | Salesforce Named Credential | Hardcoded fallback credentials, improper variable scoping | Apex execution logs, unusual credential export | SIEM alert on secret retrieval | Use HashiCorp Vault dynamic secrets, eliminate static keys |
| **Execution** | Intercepts REST call and modifies JSON payload (Unit Cost: $10,000 -> $1.00) | MuleSoft Ingestion API | Missing cryptographic payload signature check | MuleSoft HTTP ingress logs, schema mismatch errors | WAF anomaly alert, JSON schema verification failure | Implement payload signing using RS256 JWT signatures |
| **Lateral Movement** | Forwards tampered JSON payload to integration worker | MuleSoft Worker | Integration worker trusts API gateway without re-checking claims | MuleSoft internal bus logs | Microservice anomaly alert | Enforce end-to-end mTLS and ABAC verification at service layer |
| **Action on Objectives** | Executes `BAPI_SALESORDER_CREATEFROMDAT2` in SAP with fraudulent values | SAP S/4HANA Core | SAP BAPI relies on middleware trust without validating deal limits | SAP Security Audit Log (`SM20`), RFC trace | SAP ETD (Enterprise Threat Detection) alert | Enforce Biba integrity checks and secondary approval workflows in SAP |

PlantUML Attack Graph (Scenario 1)
@startuml
skinparam shadowing false
skinparam backgroundColor #FFFFFF

title MITRE-Aligned Attack Graph Scenario 1: Payload Tampering

start
:Reconnaissance: Scan Salesforce Apex & Named Credentials;
:Initial Access: Extract OAuth Token from memory dump;
:Execution: Intercept REST call & tamper JSON unit price;
:Lateral Movement: Pass tampered payload to MuleSoft Worker;
:Action on Objectives: Execute BAPI_SALESORDER_CREATE in SAP;
stop
@endl

Threat Scenario 2: Unauthenticated SAP OData Service Misconfiguration & ERP Exfiltration
Threat Actor: External Cybercrime Group (Ransomware / Data Extortion).

Objective: Exfiltrate enterprise pricing models, customer databases, and financial ledgers from SAP S/4HANA.

Affected Assets: SAP NetWeaver Gateway, OData REST Services, SAP HANA Database.
Threat Scenario 2: Attack Graph Table
**Scenario:** Unauthenticated SAP OData Service Misconfiguration & ERP Exfiltration

| Stage | Attacker Action | Target Component | Weakness Exploited | Evidence / Logs Generated | Detection Control | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Reconnaissance** | Port scans enterprise external IP ranges for open SAP NetWeaver ports (8000, 50000) | SAP Perimeter Gateway | Misconfigured firewall exposing SAP Gateway directly to internet | Firewall denial/allow logs, Nmap probe spikes | External Attack Surface Management (EASM) scan | Place all SAP NetWeaver endpoints behind strict perimeter WAF/ZTNA |
| **Initial Access** | Exploits default/unauthenticated OData service endpoint (`/sap/opu/odata/`) | SAP NetWeaver OData Service | Default service activated without requiring authentication (`SICF`) | SAP ICM HTTP access logs, 200 OK on sensitive endpoints | SIEM alert on unauthenticated OData access | Disable unused OData services in `SICF`, enforce mandatory authentication |
| **Privilege Escalation** | Leverages SAP generic RFC user privileges to access raw database tables | SAP Authorization Layer | Over-privileged service account assigned `S_TABU_DIS` with `&NC&` | SAP Audit Log (`SM20`), authorization check failures | SAP ETD alert on generic user table reads | Restrict SAP authorizations (PFCG), remove table access rights from service users |
| **Collection** | Executes bulk SQL queries across SAP HANA `KNA1` (Customer Master) and `VBAK` (Orders) | SAP HANA Database | Missing query rate limits or data volume controls | SAP HANA index server trace, excessive memory usage | Database Activity Monitoring (DAM) alert | Implement query caps, DLP inspection, and column-level masking |
| **Exfiltration** | Exfiltrates compressed CSV payload via outbound HTTPS POST requests | External C2 Infrastructure | Weak egress filtering rules on internal SAP subnets | Perimeter Firewall egress logs, High outbound volume | Network DLP / Egress WAF block alert | Enforce strict outbound network filtering and proxy inspection |

PlantUML Attack Graph (Scenario 2)
@startuml
skinparam shadowing false
skinparam backgroundColor #FFFFFF

title MITRE-Aligned Attack Graph Scenario 2: SAP OData Exfiltration

start
:Reconnaissance: Port scan perimeter for exposed SAP NetWeaver ports;
:Initial Access: Access unauthenticated /sap/opu/odata endpoint;
:Privilege Escalation: Abuse generic RFC user table access (S_TABU_DIS);
:Collection: Perform bulk SQL query dumps on SAP HANA tables;
:Exfiltration: Exfiltrate compressed financial data via outbound HTTPS;
stop
@endl

Task 3: Defense-in-Depth Infrastructure Design
Four-Layer Control Stack
+-----------------------------------------------------------------------+
| LAYER 1: DATA & CRYPTOGRAPHIC SECURITY                                |
| • Payload Signing (RS256 JWT)   • AES-256-GCM Encryption at Rest     |
| • HashiCorp Vault Secrets Mgmt  • Envelope Encryption / FIPS 140-2    |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| LAYER 2: NETWORK & PERIMETER SECURITY                                 |
| • ZTNA & Private Endpoints       • Mutual TLS (mTLS) Enforcement       |
| • Cloud WAF with OWASP Rules     • Egress Proxy & Port Filtering       |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| LAYER 3: HOST, APPLICATION & ENDPOINT SECURITY                        |
| • JSON Schema Hardening          • ABAC / Open Policy Agent (OPA)      |
| • SAST/DAST CI/CD Scanning       • Container EDR (Prisma Cloud)       |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| LAYER 4: OPERATIONAL, MANAGERIAL & MONITORING CONTROLS                |
| • Splunk SIEM Security Rules     • Automated SOAR Playbooks           |
| • SAP ETD Anomaly Monitoring    • Quarterly Red Team Exercises        |
+-----------------------------------------------------------------------+
Control-to-Threat Traceability Matrix
#### Control-to-Threat Traceability Matrix

| Threat Scenario | Exploited Attack Stage | Proposed Security Control | Defense Layer | Type (Prevent / Detect / Respond) | Residual Risk Assessment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Scenario 1: Payload Tampering** | Execution (Price Tampering) | RS256 Payload Cryptographic Signing & Schema Validation | Layer 1 & 3 | Prevent | Low - Tampered payloads fail signature validation instantly |
| **Scenario 1: Payload Tampering** | Action on Objectives (BAPI Execution) | ABAC OPA Policy Enforcement & Biba Integrity Check | Layer 3 | Prevent | Low - BAPI execution blocked if deal threshold exceeds user limits |
| **Scenario 2: OData Exfiltration** | Reconnaissance / Initial Access | ZTNA Perimeter & Deactivation of Unused OData Services | Layer 2 & 3 | Prevent | Low - Perimeter hidden; unauthenticated endpoints disabled |
| **Scenario 2: OData Exfiltration** | Collection / Exfiltration | SAP ETD & Splunk SOAR Automated Token Revocation | Layer 4 | Detect & Respond | Medium - Automated playbook halts active sessions within seconds |

B.4 Analyse: Gap Analysis and CVSS Risk Quantification
Baseline vs. Target Architecture Comparison
CURRENT BASELINE ARCHITECTURE
Salesforce ---> [Static OAuth Key] ---> MuleSoft ---> [Unencrypted RFC] ---> SAP ERP
  (Weak validation, static keys, basic RBAC, no payload signatures)

TARGET ARCHITECTURE
Salesforce ---> [mTLS + RS256 Sign] ---> MuleSoft + OPA ---> [IPsec / SNC mTLS] ---> SAP ERP
  (Dynamic Vault secrets, ABAC policies, JSON schema validation, automated SOAR)

Comprehensive Gap Analysis Table

| Domain / Area | Current Baseline State | Proposed Target Architecture State | Gap Severity | Proposed Technical Remediation |
| :--- | :--- | :--- | :--- | :--- |
| **Authentication & Secrets** | Static long-lived OAuth client secrets stored in Salesforce Named Credentials | Dynamic, short-lived secrets provided by HashiCorp Vault with automated rotation | **High** | Integrate HashiCorp Vault with Salesforce using OAuth JWT bearer flows |
| **Data Integrity** | REST JSON payloads sent without cryptographic signatures; schema validated loosely | Every payload cryptographically signed (RS256) and strictly validated against JSON schemas | **Critical** | Implement payload signing in Salesforce Apex and verification in MuleSoft |
| **Authorization** | Basic Role-Based Access Control (RBAC); no dollar-threshold checks at middleware | Attribute-Based Access Control (ABAC) driven by Open Policy Agent (OPA) | **High** | Deploy OPA microservice container within MuleSoft VPC environment |
| **Network Security** | SAP NetWeaver Gateway accessible via public IP with basic firewall rules | Complete ZTNA isolation via AWS DirectConnect; public internet access eliminated | **High** | Re-route SAP Gateway traffic through private transit gateways and ZTNA proxies |
| **Monitoring & Response** | Application logs stored locally; manual incident analysis with delayed response | Centralized Splunk SIEM streaming with automated SOAR playbooks for IP blocking | **Medium** | Deploy Splunk HTTP Event Collectors (HEC) across MuleSoft and SAP ETD |

CVSS v3.1 Risk Quantification Framework
Vulnerability 1: Salesforce-MuleSoft Integration OAuth Token Misconfiguration & Payload Tampering
Vector String: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N

Base Score: 9.1 (Critical)
Detailed Metric Rationale
Attack Vector (AV:N): Exploitable remotely across the network via public Salesforce API endpoints.

Attack Complexity (AC:L): Low complexity; requires no special conditions or complex race conditions once token is intercepted.

Privileges Required (PR:N): None; unauthenticated external actors can exploit intercepted tokens.

User Interaction (UI:N): Completely automated; no human intervention required.

Scope (S:U): Unchanged; impact is contained within the integration gateway and target SAP system.

Confidentiality Impact (C:H): High; allows unauthorized extraction of sensitive B2B price books and order histories.

Integrity Impact (I:H): High; allows direct modification of purchase order values, pricing, and quantities.

Availability Impact (A:N): None; attack does not directly cause application failure or crash worker nodes.

Vulnerability 2: Unauthenticated SAP NetWeaver OData Service Exposure
Vector String: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

Base Score: 9.8 (Critical)

Detailed Metric Rationale
Attack Vector (AV:N): Network accessible over HTTP/HTTPS perimeter ports.

Attack Complexity (AC:L): Low; default service endpoints are well-documented and easily scriptable.

Privileges Required (PR:N): None; default misconfiguration allows unauthenticated requests.

User Interaction (UI:N): None required.

Scope (S:U): Unchanged; affects core SAP ERP components.

Confidentiality Impact (C:H): High; full access to raw database tables (Customer PII, Financials).

Integrity Impact (I:H): High; arbitrary database write operations via exposed BAPIs.

Availability Impact (A:H): High; malicious queries can saturate HANA DB CPU/Memory, crashing ERP services.

Risk Register
RiskID,Threat,Asset,Impact,Likelihood,CVSS_Vector,CVSS_Score,Existing_Control,Proposed_Control,Residual_Risk
R01,Salesforce-to-SAP Payload Tampering,MuleSoft Ingestion API,Critical,High,AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N,9.1,Basic API Key,RS256 Payload Signing & JSON Schema Validation,Low
R02,Unauthenticated SAP OData Exposure,SAP NetWeaver Gateway,Critical,Medium,AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H,9.8,Firewall Rules,ZTNA Private Link & Mandatory OData Auth,Low
R03,Static Integration Secret Leakage,Salesforce Named Credentials,High,High,AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N,6.5,Static OAuth Secret,HashiCorp Vault Dynamic Secrets Rotation,Low
R04,SOX Compliance Pricing Override,SAP Sales Order BAPI,High,Medium,AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:H/A:N,5.3,RBAC Authorization,OPA ABAC Policies & Immutable Audit Logging,Low

B.5 Reflect: Enterprise Constraints and Lifecycle Maintenance
1. Technical Friction
Legacy SAP RFC Protocols: Older SAP NetWeaver instances rely on legacy RFC/BAPI structures that do not natively support modern OAuth 2.0 or JSON Web Tokens (JWT) without additional SAP Gateway configuration.

Salesforce Governor Limits: Salesforce limits outbound HTTP callouts per transaction and daily API executions. Injecting complex cryptographic payload signing directly into Apex must be optimized to prevent hitting Apex CPU time limits.

Latency Overhead: Introducing WAF inspection, JSON schema validation, OPA policy evaluation, and cryptographic verification adds ~35ms latency per transaction, requiring tuning to meet sub-second SLA targets.

2. Organizational Friction
Siloed Engineering Teams: The Salesforce team (Agile cloud developers) and SAP team (traditional enterprise ERP engineers) operate in organizational silos with distinct deployment schedules and security awareness levels.

Budget & Licensing Costs: Implementing HashiCorp Vault Enterprise, MuleSoft Anypoint Security modules, and Splunk SIEM expansion requires an estimated $180,000 in annual licensing investments.

3. Total Cost of Ownership (TCO) Considerations
Capital & Operational Expenditure: Initial implementation cost estimated at $220,000 (engineering hours, security audits, training) plus $180,000 annual recurring infrastructure/licensing cost.

Cost Offset / Risk Reduction: Prevents potential regulatory non-compliance fines ($10M+ under GDPR/DPDP), protects against fraudulent pricing overrides ($15M daily exposure), and reduces manual audit preparation effort by 60% via automated compliance logging.

4. Single Highest-Impact Immediate Remediation Plan
Selected Remediation
Deploy Cryptographic Payload Signing (RS256) and Enforce JSON Schema Validation at the MuleSoft Integration Gateway.

Strategic Justification
This single intervention provides the highest return on investment. It directly mitigates Vulnerability 1 (CVSS 9.1) by ensuring that even if an attacker intercepts an OAuth token or gains access to Salesforce, they cannot alter purchase order values, prices, or account details without invalidating the cryptographic signature.
