

from fastapi import APIRouter

from fastapi_modules.modules_another.heart_beat_another.router.implement import router

'''
If you need nested router, use the blow code
'''
# router = APIRouter()
# router.include_router(router, tags=["xxx"], prefix="/xxx")
