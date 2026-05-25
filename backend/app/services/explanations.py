# Pre-written expert explanations for each vulnerability type

EXPLANATIONS = {
    "Reentrancy Attack": {
        "description": "An attacker can repeatedly withdraw funds before the contract updates its balance.",
        "impact": "Loss of all funds in the contract. This is how the famous DAO hack happened ($60M lost).",
        "fix": "Update balances BEFORE making external calls, or use OpenZeppelin's ReentrancyGuard.",
        "example": "function withdraw(uint amount) nonReentrant { require(balance[msg.sender] >= amount); balance[msg.sender] -= amount; (bool success,) = msg.sender.call{value: amount}(''); require(success); }"
    },
    "Integer Overflow/Underflow": {
        "description": "Arithmetic operations can wrap around to unexpected values when exceeding limits.",
        "impact": "Attackers can manipulate balances or break contract logic.",
        "fix": "Use Solidity 0.8+ (built-in checks) or OpenZeppelin's SafeMath library.",
        "example": "using SafeMath for uint256; balance = balance.add(amount);"
    },
    "Missing Access Control": {
        "description": "Sensitive functions can be called by anyone, not just authorized users.",
        "impact": "Attackers can steal funds, change ownership, or destroy the contract.",
        "fix": "Add onlyOwner modifier or role-based access control.",
        "example": "modifier onlyOwner() { require(msg.sender == owner, 'Not owner'); _; } function withdraw() public onlyOwner { ... }"
    },
    "Unchecked External Call": {
        "description": "send() or transfer() can fail without being detected.",
        "impact": "Contract state becomes inconsistent, potentially locking funds.",
        "fix": "Always check return values or use require().",
        "example": "require(addr.send(amount), 'Transfer failed');"
    },
    "Gas Inefficiency": {
        "description": "Poorly optimized code costs more gas than necessary.",
        "impact": "Users pay higher transaction fees; contract may hit gas limits.",
        "fix": "Cache array length, use uint256, avoid unnecessary storage writes.",
        "example": "uint len = arr.length; for(uint i; i < len; i++) { ... }"
    },
    "tx.origin Vulnerability": {
        "description": "Using tx.origin instead of msg.sender for authentication.",
        "impact": "Attackers can trick contracts into performing unauthorized actions.",
        "fix": "Always use msg.sender for authentication.",
        "example": "require(msg.sender == owner, 'Not owner');"
    },
    "Uninitialized Variable": {
        "description": "State variables are used without being initialized.",
        "impact": "Unpredictable behavior or security holes.",
        "fix": "Initialize variables in constructor or directly.",
        "example": "uint256 public value = 0; address public owner = msg.sender;"
    }
}

def get_explanation(vulnerability_type):
    """Get detailed explanation for a vulnerability"""
    return EXPLANATIONS.get(vulnerability_type, {
        "description": "Security issue detected in your smart contract.",
        "impact": "Could lead to unexpected behavior or security risks.",
        "fix": "Review the code and implement proper security patterns.",
        "example": "Follow best practices for smart contract development."
    })

def get_optimization_tips(contract_code):
    """Generate gas optimization tips based on code patterns"""
    tips = []
    
    if "for(" in contract_code or "for (" in contract_code:
        tips.append("💡 Use `unchecked` blocks in loops to save gas (Solidity 0.8+).")
    
    if "storage" in contract_code.lower():
        tips.append("💡 Use `calldata` instead of `memory` for read-only function parameters.")
    
    if "++" in contract_code or "--" in contract_code:
        tips.append("💡 Use `unchecked{++i;}` for loop counters to save gas.")
    
    if "require(" in contract_code:
        tips.append("💡 Order require statements from cheapest to most expensive gas cost.")
    
    if len(contract_code) > 5000:
        tips.append("💡 Consider splitting large contracts into smaller libraries.")
    
    if not tips:
        tips.append("💡 Your code looks gas-efficient! Consider using immutable variables for constants.")
    
    return tips