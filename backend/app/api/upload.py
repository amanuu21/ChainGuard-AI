import logging
import traceback
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.contract import Contract
from app.services.analyzer import analyze_solidity

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/upload")
async def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Received upload request for file: {file.filename}")
    
    try:
        # Check file type
        if not file.filename.endswith('.sol'):
            logger.warning(f"Invalid file type: {file.filename}")
            raise HTTPException(status_code=400, detail="Only .sol files allowed")
        
        # Read file content
        content = await file.read()
        solidity_code = content.decode('utf-8')
        logger.info(f"File read successfully, size: {len(solidity_code)} bytes")
        
        # Analyze the code for vulnerabilities
        logger.info("Starting vulnerability analysis...")
        analysis = analyze_solidity(solidity_code)
        logger.info(f"Analysis complete. Risk score: {analysis.get('risk_score', 'N/A')}")
        
        # Save to database with analysis results
        new_contract = Contract(
            filename=file.filename,
            solidity_code=solidity_code,
            risk_score=analysis.get("risk_score"),
            analysis_result=analysis
        )
        
        logger.info("Saving to database...")
        db.add(new_contract)
        db.commit()
        db.refresh(new_contract)
        logger.info(f"Saved contract with ID: {new_contract.id}")
        
        return {
            "message": "Contract uploaded and analyzed successfully",
            "contract_id": new_contract.id,
            "filename": new_contract.filename,
            "analysis": analysis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.get("/contracts")
def get_all_contracts(db: Session = Depends(get_db)):
    try:
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
    except Exception as e:
        logger.error(f"Error fetching contracts: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contract/{contract_id}")
def get_contract(contract_id: int, db: Session = Depends(get_db)):
    try:
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
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching contract {contract_id}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))