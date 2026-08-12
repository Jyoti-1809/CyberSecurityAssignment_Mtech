from pathlib import Path

REQUIRED_PATHS = [
    "README.md",
    "report/final-report.md",
    "diagrams/c4-context.puml",
    "diagrams/c4-container.puml",
    "diagrams/c4-component.puml",
    "diagrams/attack-graph-scenario-1.puml",
    "diagrams/attack-graph-scenario-2.puml",
    "risk/risk-register.csv",
    "src/security_gateway.py",
    "presentation/viva-presentation-outline.md"
]

def main():
    root = Path.cwd()
    missing = []
    present = []
    
    for item in REQUIRED_PATHS:
        path = root / item
        if path.exists():
            present.append(item)
        else:
            missing.append(item)
            
    print("\n=== Repository Structure Inspection ===")
    print(f"Present required files: {len(present)} / {len(REQUIRED_PATHS)}")
    
    if present:
        print("\n[OK] Found Files:")
        for item in present:
            print(f"  - {item}")
            
    if missing:
        print("\n[MISSING] Required Files:")
        for item in missing:
            print(f"  - {item}")
        raise SystemExit(1)
    else:
        print("\nSUCCESS: All required files are present and properly positioned!")

if __name__ == "__main__":
    main()
