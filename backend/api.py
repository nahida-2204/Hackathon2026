from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
SUPABASE_URL = "https://yrwbupunkzlmnuksnmrh.supabase.co"
# Paste your secure key here (anon/publishable key is fine for GET requests)
SUPABASE_KEY = "SUPABASE_SECRET_KEY_REMOVED" 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize FastAPI
app = FastAPI(
    title="Mauritian Budget Spendings API",
    description="API to fetch public spending extraction data",
    version="1.0.0"
)

# 2. ENABLE CORS (Crucial for Hackathons)
# This allows your frontend (React, Vue, HTML/JS) to make requests to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# ==========================================
# 3. THE GET ENDPOINT
# ==========================================
@app.get("/api/spendings")
def get_all_spendings():
    """
    Fetches all compiled records from the public_spendings table
    and returns them as a structured JSON object.
    """
    try:
        # Query all columns (*) from your target table
        response = supabase.table("public_spendings").select("*").execute()
        
        # Check if we got a response back
        if response.data is None:
            raise HTTPException(status_code=404, detail="No data found in public_spendings table.")
            
        # FastAPI automatically serializes python lists/dicts into clean JSON
        return {
            "status": "success",
            "count": len(response.data),
            "data": response.data
        }
        
    except Exception as e:
        # Gracefully handle database or connection issues
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve data from database: {str(e)}"
        )

# Optional: Root endpoint to verify server is running
@app.get("/")
def read_root():
    return {"message": "Mauritian Budget API is online!"}