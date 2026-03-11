import asyncio
import logging
import os
import traceback
from videosdk.agents import Agent,AgentSession,JobContext,Options,RealTimePipeline,RoomOptions,WorkerJob
from videosdk.plugins.google import GeminiLiveConfig, GeminiRealtime
from tools.tools import book_appointment , list_appointments ,cancel_appointment , get_current_date_time
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
class MyVoiceAgent(Agent):
	def __init__(self):
		super().__init__(
			instructions=(
				"You are a helpful voice assistant that can help users "
                "book appointments, list appointments, "
                "cancel appointments and check the current time."
			),
			tools=[book_appointment,list_appointments,cancel_appointment,get_current_date_time],
		)

	async def on_enter(self) -> None:
		await self.session.say("Hello! I'm your real-time assistant. How can I help you today?")

	async def on_exit(self) -> None:
		await self.session.say("Goodbye! It was great talking with you!")


async def start_session(context: JobContext):
	
	model = GeminiRealtime(
		model="gemini-2.5-flash-native-audio-preview-12-2025",
		api_key=os.getenv("GOOGLE_API_KEY"),
		config=GeminiLiveConfig(
			voice="Leda",
			response_modalities=["AUDIO"],
		),
	)
	pipeline = RealTimePipeline(model=model)
	session = AgentSession(agent=MyVoiceAgent(), pipeline=pipeline)

	try:
		await context.connect()
		await session.start()
		await asyncio.Event().wait()
	finally:
		await session.close()
		await context.shutdown()


def make_context() -> JobContext:
	room_options = RoomOptions()
	return JobContext(room_options=room_options)


if __name__ == "__main__":
	try:
		
		options = Options(
			agent_id="MyTelephonyAgent",
			register=True,  
			max_processes=10,
			host="localhost",
			port=8081,
		)
		job = WorkerJob(entrypoint=start_session, jobctx=make_context, options=options)
		job.start()
	except Exception:
		traceback.print_exc()