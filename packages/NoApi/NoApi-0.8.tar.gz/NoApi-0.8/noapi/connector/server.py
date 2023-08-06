import fastapi, uvicorn, threading

from . import Connection



class Server:
	# TODO implement some security maybe

	def __init__(self, port: int):
		"""Open this device for connections"""
		self.port = port
		self.fastapi = fastapi.FastAPI()

		self.connections: set[Connection] = set()

		@self.fastapi.post('/connect')
		def add_client(port: int, request: fastapi.Request):
			client = Connection(request.client.host, port, self.port)
			if client not in self.connections:
				self.connections.add(client)
				client.connect()
				return True
			else:
				return False

		@self.fastapi.get('/test')
		def hello():
			return "Hello!"

		@self.fastapi.exception_handler(Exception)
		async def validation_exception_handler(request, err: Exception):
			return fastapi.responses.JSONResponse(status_code=500,
												  content={'detail': f"{err.__class__.__name__}: {err}"})


	def start(self, log=False):
		if log:
			log_level = None
		else:
			log_level = 'warning'
		uvicorn.run(self.fastapi, host='0.0.0.0', port=self.port, log_level=log_level)

	def start_in_thread(self, log=False):
		threading.Thread(target=self.start, kwargs={'log': log}, daemon=True).start()
