from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Dict
from datetime import date, time
from fastapi.middleware.cors import CORSMiddleware # Dodaj ten import

app = FastAPI()

# Dodaj ten blok kodu po inicjalizacji app = FastAPI()
origins = [
    "http://localhost", # Jeśli testujesz lokalnie
    "http://localhost:8000", # Jeśli testujesz lokalnie na innym porcie
    "null", # Czasem potrzebne dla plików otwieranych bezpośrednio z dysku (file://)
    "http://127.0.0.1:5500", # Przykład dla Live Server w VS Code
    # Dodaj tutaj adres URL, pod którym hostujesz swoją stronę front-end
    "https://lukaszsmichurski.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Pozwól na wszystkie metody (GET, POST, PUT, DELETE itp.)
    allow_headers=["*"], # Pozwól na wszystkie nagłówki
)

# Prosta baza danych: dostępne sloty
available_slots: Dict[date, List[time]] = {
    date(2025, 8, 1): [time(9), time(10), time(11)],
    date(2025, 8, 2): [time(12), time(13)],
}

# Zarezerwowane sloty
booked_slots: Dict[date, List[time]] = {}


class BookingRequest(BaseModel):
    date: date
    time: time
    name: str
    email: EmailStr


@app.get("/available-slots")
def get_available_slots():
    result = {}
    for day, hours in available_slots.items():
        booked = booked_slots.get(day, [])
        free = [h.strftime("%H:%M") for h in hours if h not in booked]
        if free:
            result[str(day)] = free
    return result


@app.post("/book-slot")
def book_slot(request: BookingRequest):
    slots = available_slots.get(request.date)
    if not slots or request.time not in slots:
        raise HTTPException(status_code=400, detail="Slot niedostępny.")

    booked_times = booked_slots.setdefault(request.date, [])
    if request.time in booked_times:
        raise HTTPException(status_code=400, detail="Slot już zarezerwowany.")

    booked_times.append(request.time)
    return {"message": f"Zarezerwowano {request.date} o {request.time.strftime('%H:%M')}!"}
