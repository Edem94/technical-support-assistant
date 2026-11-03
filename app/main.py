@asynccontextmanager
def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
