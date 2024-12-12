from typing import Dict, List

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from producer import send_message, start_producer, stop_producer

from src.domain.DTO.event_schema import EventCreate, EventUpdateStatus
from src.domain.models.event import Event
from src.repositories import event

router_event = APIRouter()


@router_event.on_event("startup")
async def startup_event():
    await start_producer()


@router_event.on_event("shutdown")
async def shutdown_event():
    await stop_producer()


@router_event.post("/events", response_model=Event)
async def create_event(event_data: EventCreate) -> List[Event]:
    data = event.create_event(event_data)
    await send_message(jsonable_encoder(data))
    return data


@router_event.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: str) -> Event:
    event_data = event.get_event(event_id)
    if not event_data:
        raise HTTPException(status_code=404, detail="Event not found")
    return event_data


@router_event.patch("/events/{event_id}/status", response_model=Event)
async def update_event_status(event_id: str, status_data: EventUpdateStatus) -> Event:
    event_data = event.update_event_status(event_id, status_data.status)
    if not event_data:
        raise HTTPException(status_code=404, detail="Event not found")
    await send_message(jsonable_encoder(event_data))
    return event_data


@router_event.get("/events", response_model=Dict[str, Event])
async def list_events():
    return event.list_events()
