import re
from app.services.explanations import get_explanation, get_optimization_tips

def analyze_solidity(code):
    """Analyze Solidity code for vulnerabilities"""
    vulnerabilities = []
    risk_score = 0
    
    # 1. Reentrancy Detection
    if re.search(r'\.call\(.*\)', code) and re.search(r'balances\[.*\]\s*-=', code):
        vuln_type = "Reentrancy Attack"
        explanation = get_explanation(vuln_type)
        vulnerabilities.append({
            "type": vuln_type,
            "severity": "High",
            "line": "Use of .call() before updating balance",
            "recommendation": "Update balance before making external calls or use reentrancy guard",
            "explanation": explanation["description"],
            "impact": explanation["impact"],
            "fix_example": explanation["fix"],
            "example_code": explanation["example"]
        })
        risk_score += 30
    
    # 2. Integer Overflow/Underflow
    if re.search(r'pragma solidity \^0\.8\.', code):
        pass
    elif re.search(r'(\+=|-=|\*=|\/=)', code):
        vuln_type = "Integer Overflow/Underflow"
        explanation = get_explanation(vuln_type)
        vulnerabilities.append({
            "type": vuln_type,
            "severity": "High",
            "line": "Arithmetic operations without SafeMath",
            "recommendation": "Use Solidity 0.8+ or OpenZeppelin's SafeMath library",
            "explanation": explanation["description"],
            "impact": explanation["impact"],
            "fix_example": explanation["fix"],
            "example_code": explanation["example"]
        })
        risk_score += 25
    
    # 3. Access Control Issues
    if not re.search(r'onlyOwner|onlyAdmin|access control', code, re.IGNORECASE):
        if re.search(r'function\s+\w+\(.*\)\s+public', code):
            vuln_type = "Missing Access Control"
            explanation = get_explanation(vuln_type)
            vulnerabilities.append({
                "type": vuln_type,
                "severity": "Medium",
                "line": "Public function without access modifiers",
                "recommendation": "Add onlyOwner or role-based access control",
                "explanation": explanation["description"],
                "impact": explanation["impact"],
                "fix_example": explanation["fix"],
                "example_code": explanation["example"]
            })
            risk_score += 20
    
    # 4. Unchecked External Calls
    if re.search(r'\.send\(|\.transfer\(', code) and not re.search(r'require\(.*\.send\(', code):
        vuln_type = "Unchecked External Call"
        explanation = get_explanation(vuln_type)
        vulnerabilities.append({
            "type": vuln_type,
            "severity": "Medium",
            "line": "send()/transfer() without checking return value",
            "recommendation": "Use require() to check return value or use call() with reentrancy guard",
            "explanation": explanation["description"],
            "impact": explanation["impact"],
            "fix_example": explanation["fix"],
            "example_code": explanation["example"]
        })
        risk_score += 15
    
    # 5. Gas Optimization Issues
    if re.search(r'for\s*\(.*\)', code):
        if re.search(r'\.push\(', code):
            vuln_type = "Gas Inefficiency"
            explanation = get_explanation(vuln_type)
            vulnerabilities.append({
                "type": vuln_type,
                "severity": "Low",
                "line": "Dynamic array push in loop",
                "recommendation": "Pre-allocate array size or use mapping instead",
                "explanation": explanation["description"],
                "impact": explanation["impact"],
                "fix_example": explanation["fix"],
                "example_code": explanation["example"]
            })
            risk_score += 10
    
    # 6. TX.ORIGIN Usage
    if re.search(r'tx\.origin', code):
        vuln_type = "tx.origin Vulnerability"
        explanation = get_explanation(vuln_type)
        vulnerabilities.append({
            "type": vuln_type,
            "severity": "High",
            "line": "Use of tx.origin for authentication",
            "recommendation": "Use msg.sender instead of tx.origin",
            "explanation": explanation["description"],
            "impact": explanation["impact"],
            "fix_example": explanation["fix"],
            "example_code": explanation["example"]
        })
        risk_score += 35
    
    # 7. Uninitialized Variables
    if re.search(r'address\s+\w+;', code) and not re.search(r'address\s+\w+\s*=', code):
        vuln_type = "Uninitialized Variable"
        explanation = get_explanation(vuln_type)
        vulnerabilities.append({
            "type": vuln_type,
            "severity": "Medium",
            "line": "State variable not initialized",
            "recommendation": "Initialize variables in constructor or directly",
            "explanation": explanation["description"],
            "impact": explanation["impact"],
            "fix_example": explanation["fix"],
            "example_code": explanation["example"]
        })
        risk_score += 15
    
    # 8. Timestamp Dependence
    if re.search(r'block\.timestamp|now\s*[<>=\s]+', code):
        vuln_type = "Timestamp Dependence"
        explanation = get_explanation(vuln_type)
        vulnerabilities.append({
            "type": vuln_type,
            "severity": "Medium",
            "line": "Using block.timestamp for critical logic",
            "recommendation": "Avoid using block.timestamp for randomness or critical conditions",
            "explanation": explanation["description"],
            "impact": explanation["impact"],
            "fix_example": explanation["fix"],
            "example_code": explanation["example"]
        })
        risk_score += 15
    
    # 9. Deprecated Functions
    if re.search(r'throw;|suicide\(', code):
        vuln_type = "Deprecated Function Usage"
        explanation = get_explanation(vuln_type)
        vulnerabilities.append({
            "type": vuln_type,
            "severity": "Low",
            "line": "Using deprecated functions (throw/suicide)",
            "recommendation": "Use 'revert()' instead of 'throw' and 'selfdestruct()' instead of 'suicide'",
            "explanation": explanation["description"],
            "impact": explanation["impact"],
            "fix_example": explanation["fix"],
            "example_code": explanation["example"]
        })
        risk_score += 5
    
    # Get optimization tips
    optimization_tips = get_optimization_tips(code)
    
    # Determine overall risk level
    if risk_score >= 70:
        risk_level = "Critical"
    elif risk_score >= 40:
        risk_level = "High"
    elif risk_score >= 20:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "vulnerabilities": vulnerabilities,
        "total_issues": len(vulnerabilities),
        "optimization_tips": optimization_tips,
        "summary": {
            "high": len([v for v in vulnerabilities if v["severity"] == "High"]),
            "medium": len([v for v in vulnerabilities if v["severity"] == "Medium"]),
            "low": len([v for v in vulnerabilities if v["severity"] == "Low"])
        }
    }