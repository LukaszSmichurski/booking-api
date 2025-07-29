from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI()

# Fake database
available_dates = {
    "2025-08-01",
    "2025-08-02",
    "2025-08-05",
    "2025-08-08",
}

booked_dates = set()


class BookingRequest(BaseModel):
    date: str  # format: YYYY-MM-DD
    name: str
    email: str


@app.get("/available-dates")
def get_available_dates():
    return sorted(list(available_dates - booked_dates))


@app.post("/book-date")
def book_date(request: BookingRequest):
    if request.date not in available_dates:
        raise HTTPException(status_code=400, detail="Data niedostępna.")
    if request.date in booked_dates:
        raise HTTPException(status_code=400, detail="Data już zarezerwowana.")

    booked_dates.add(request.date)
    # W przyszłości: zapisz do bazy lub wyślij e-mail
    return {"message": "Zarezerwowano!", "date": request.date}
