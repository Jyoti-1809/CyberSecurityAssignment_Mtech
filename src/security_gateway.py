#!/usr,bin/env python3
"""
Salesforce-to-SAP Security Gateway Verification Engine (POC)
Implements:
1. HMAC-SHA256 Payload Signature Verification
2. JSON Schema Bound Enforcement
3. ABAC Policy Enforcement
4. SIEM Log Stream Formatting
"""

import hmac
import hashlib
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("Salesforce_SAP_Gateway")

VAULT_SHARED_SECRET = b"super-secret-salesforce-sap-signing-key-2026"

ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "order_id": {"type": "string"},
        "customer_id": {"type": "string"},
        "deal_amount": {"type": "number", "minimum": 1.0, "maximum": 500000.0},
        "unit_price": {"type": "number", "minimum": 10.0},
        "quantity": {"type": "integer", "minimum": 1, "maximum": 10000},
        "user_role": {"type": "string"}
    },
    "required": ["order_id", "customer_id", "deal_amount", "unit_price", "quantity", "user_role"]
}

def verify_signature(payload_str: str, signature_header: str) -> bool:
    computed_sig = hmac.new(VAULT_SHARED_SECRET, payload_str.encode('utf-8'), hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_sig, signature_header)

def validate_schema(data: dict) -> tuple[bool, str]:
    for field in ORDER_SCHEMA["required"]:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    if data["unit_price"] < ORDER_SCHEMA["properties"]["unit_price"]["minimum"]:
        return False, f"Unit price ${data['unit_price']} violates minimum bounds."
        
    if data["deal_amount"] > ORDER_SCHEMA["properties"]["deal_amount"]["maximum"]:
        return False, f"Deal amount ${data['deal_amount']} exceeds maximum cap."
        
    return True, "Schema Valid"

def enforce_abac_policy(data: dict) -> tuple[bool, str]:
    user_role = data.get("user_role")
    deal_amount = data.get("deal_amount")

    if user_role == "Sales_Rep" and deal_amount > 100000.0:
        return False, f"ABAC Policy Deny: Role '{user_role}' cannot approve orders over $100,000."
    
    return True, "ABAC Policy Allowed"

def process_salesforce_request(payload_json: str, signature_header: str):
    logger.info("=== Processing Salesforce REST Request ===")
    
    if not verify_signature(payload_json, signature_header):
        logger.error("SECURITY ALERT: Signature verification failed! Payload tampered.")
        return {"status": 401, "message": "Invalid Cryptographic Signature"}
    logger.info("PASS: Payload Signature Verified (Integrity Intact)")

    payload = json.loads(payload_json)

    schema_ok, schema_msg = validate_schema(payload)
    if not schema_ok:
        logger.error(f"SECURITY ALERT: Schema failure - {schema_msg}")
        return {"status": 400, "message": f"Bad Request: {schema_msg}"}
    logger.info("PASS: JSON Schema Structure & Bounds Validated")

    abac_ok, abac_msg = enforce_abac_policy(payload)
    if not abac_ok:
        logger.warning(f"SECURITY ALERT: Policy Violation - {abac_msg}")
        return {"status": 403, "message": f"Forbidden: {abac_msg}"}
    logger.info("PASS: ABAC Policy Decision Granted")

    logger.info(f"SUCCESS: Order {payload['order_id']} dispatched to SAP BAPI.")
    return {"status": 200, "message": "Order Processed into SAP S/4HANA"}

if __name__ == "__main__":
    print("--- RUNNING TEST 1: Valid Salesforce Request ---")
    valid_payload = json.dumps({
        "order_id": "ORD-2026-9981",
        "customer_id": "CUST-SAP-4410",
        "deal_amount": 45000.0,
        "unit_price": 150.0,
        "quantity": 300,
        "user_role": "Sales_Rep"
    })
    valid_sig = hmac.new(VAULT_SHARED_SECRET, valid_payload.encode('utf-8'), hashlib.sha256).hexdigest()
    process_salesforce_request(valid_payload, valid_sig)

    print("\n--- RUNNING TEST 2: Tampered Price Request (Attack Scenario 1) ---")
    tampered_payload = json.dumps({
        "order_id": "ORD-2026-9982",
        "customer_id": "CUST-SAP-4410",
        "deal_amount": 5.0,
        "unit_price": 0.05,
        "quantity": 100,
        "user_role": "Sales_Rep"
    })
    process_salesforce_request(tampered_payload, valid_sig)
