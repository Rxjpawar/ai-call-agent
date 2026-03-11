from .database import SessionLocal
from .models import Appointment
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


def create_appointment(name, email, appointment_time, reason=None):
    db = SessionLocal()
    try:
        dt = datetime.fromisoformat(appointment_time)

        # Conflict check
        existing = db.query(Appointment).filter(
            Appointment.appointment_time == dt
        ).first()

        if existing:
            return "This time slot is already booked."

        appointment = Appointment(
            name=name,
            email=email,
            appointment_time=dt,
            reason=reason
        )

        db.add(appointment)
        db.commit()
        db.refresh(appointment)

        return f"Appointment booked successfully with ID {appointment.id}"

    except SQLAlchemyError as e:
        db.rollback()
        return f"Database error: {str(e)}"

    finally:
        db.close()


def get_appointments():
    db = SessionLocal()
    try:
        appointments = db.query(Appointment).all()

        return [
            {
                "id": a.id,
                "name": a.name,
                "email": a.email,
                "appointment_time": a.appointment_time.isoformat(),
                "reason": a.reason
            }
            for a in appointments
        ]

    finally:
        db.close()


def delete_appointment(appointment_id: int):
    db = SessionLocal()
    try:
        appointment = db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()

        if not appointment:
            return "Appointment not found."

        db.delete(appointment)
        db.commit()

        return "Appointment cancelled successfully."

    finally:
        db.close()