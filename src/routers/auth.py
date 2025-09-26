from fastapi import APIRouter, status


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

@router.get('/healph')
def root():
    return {'status': status.HTTP_200_OK}
