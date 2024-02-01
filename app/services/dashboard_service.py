from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository

class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.dashboard_repository = DashboardRepository(db)




