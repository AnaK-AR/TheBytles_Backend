from fastapi import FastAPI
from pydantic import BaseModel
from generate_profile_summaries import generate_user_summary
from generate_roles_from_rfp import generate_roles_from_rfp
from generate_keypoints import generate_keypoints
from fastapi.middleware.cors import CORSMiddleware

# Inicializacion de FastAPI
app = FastAPI()

# Configuracion CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://the-bytles-reto.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/")
def read_root():
    return {"message": "Backend is working!"}

# Schemas de Request
class SummaryRequest(BaseModel):
    user_id: str
    
class KeypointsRequest(BaseModel):
    user_id: str

class RoleGenRequest(BaseModel):
    project_id: str

# Endpoints
@app.post("/generate-summary")
async def generate_summary(payload: SummaryRequest):
    user_id = payload.user_id
    success = generate_user_summary(user_id)
    return {"status": "success" if success else "error"}

@app.post("/generate-keypoints")
async def keypoints_request(payload: KeypointsRequest):
    user_id = payload.user_id
    success = generate_keypoints(user_id)
    return {"status": "success" if success else "error"}


@app.post("/generate-roles")
async def generate_roles(request: RoleGenRequest):
    success = generate_roles_from_rfp(request.project_id)
    return { "status": "success" if success else "error"}