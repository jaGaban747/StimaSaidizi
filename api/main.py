from fastapi import FastAPI
from api.routes.customers import router as customers_router
from api.routes.outages import router as outages_router
from api.routes.tokens import router as tokens_router
from api.routes.billing import router as billing_router
from api.routes.support_cases import router as support_cases_router
from api.routes.analytics import router as analytics_router

app = FastAPI(
    title="StimaSaidizi API",
    description="Backend API for the StimaSaidizi electricity customer-support prototype.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "StimaSaidizi API",
        "status": "running",
    }

app.include_router(customers_router)
app.include_router(outages_router)
app.include_router(tokens_router)
app.include_router(billing_router)
app.include_router(support_cases_router)
app.include_router(analytics_router)