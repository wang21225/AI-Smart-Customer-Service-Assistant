from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import success
from app.db.session import get_db
from app.models import CustomerTicket
from app.schemas.ticket import TicketCreate, TicketOut, TicketUpdate
from app.tools.business_tools import create_customer_ticket

router = APIRouter(prefix="/tickets")


@router.get("")
def list_tickets(db: Session = Depends(get_db)):
    items = db.query(CustomerTicket).order_by(CustomerTicket.created_at.desc()).all()
    return success([TicketOut.model_validate(item).model_dump() for item in items])


@router.post("")
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    result = create_customer_ticket(db, payload.category, payload.content, payload.conversation_id)
    item = db.query(CustomerTicket).filter(CustomerTicket.ticket_no == result["ticket_no"]).first()
    return success(TicketOut.model_validate(item).model_dump())


@router.put("/{ticket_id}")
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    item = db.get(CustomerTicket, ticket_id)
    if item:
        if payload.status:
            item.status = payload.status
        if payload.priority:
            item.priority = payload.priority
        db.commit()
        db.refresh(item)
    return success(TicketOut.model_validate(item).model_dump() if item else None)
