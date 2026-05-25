from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.contract import Contract
from app.services.analyzer import analyze_solidity

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/upload")
async def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Check file type
    if not file.filename.endswith('.sol'):
        raise HTTPException(status_code=400, detail="Only .sol files allowed")
    
    # Read file content
    content = await file.read()
    solidity_code = content.decode('utf-8')
    
    # Analyze the code for vulnerabilities
    analysis = analyze_solidity(solidity_code)
    
    # Save to database with analysis results
    new_contract = Contract(
        filename=file.filename,
        solidity_code=solidity_code,
        risk_score=analysis["risk_score"],
        analysis_result=analysis
    )
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    
    return {
        "message": "Contract uploaded and analyzed successfully",
        "contract_id": new_contract.id,
        "filename": new_contract.filename,
        "analysis": analysis
    }

@router.get("/contracts")
def get_all_contracts(db: Session = Depends(get_db)):
    contracts = db.query(Contract).all()
    return [
        {
            "id": c.id,
            "filename": c.filename,
            "risk_score": c.risk_score,
            "created_at": str(c.created_at)
        }
        for c in contracts
    ]

@router.get("/contract/{contract_id}")
def get_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return {
        "id": contract.id,
        "filename": contract.filename,
        "solidity_code": contract.solidity_code,
        "analysis_result": contract.analysis_result,
        "risk_score": contract.risk_score,
        "created_at": str(contract.created_at)
    }