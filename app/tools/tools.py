from langchain_core.tools import tool
from app.database.crud import create_appointment, get_appointments, delete_appointment
from videosdk.agents import function_tool
from datetime import datetime
import pytz

@function_tool
async def book_appointment(
    name: str,
    email: str,
    appointment_time: str,
    reason: str
):
    """
    Book a new appointment.

    Args:
        name: Name of the person
        email: Email address of the user
        appointment_time: Appointment time in ISO format
        reason: Reason for the appointment
    """
    return create_appointment(name, email, appointment_time, reason)


@function_tool
async def list_appointments():
    """
    List all booked appointments.
    """
    return get_appointments()


@function_tool
async def cancel_appointment(appointment_id: int):
    """
    Cancel an appointment using its ID.

    Args:
        appointment_id: The ID of the appointment
    """
    return delete_appointment(appointment_id)


@function_tool
async def get_current_date_time():
    """
    Returns the current date and time in India (Asia/Kolkata timezone).
    """
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)
    return now.isoformat()