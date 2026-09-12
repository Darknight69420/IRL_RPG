from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, character, activities, creatures, quest_chains, chronicle, achievements
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(character.router, prefix="/character", tags=["Character & Progression"])
api_router.include_router(activities.router, prefix="/activities", tags=["Activities & Habits"])
api_router.include_router(creatures.router, prefix="/creatures", tags=["Creatures & Lifedex"])
api_router.include_router(quest_chains.router, prefix="/quest-chains", tags=["Goal Quest Chains"])
api_router.include_router(chronicle.router, prefix="/chronicle", tags=["Chronicle Stream"])
api_router.include_router(achievements.router, prefix="/achievements", tags=["Achievements"])
