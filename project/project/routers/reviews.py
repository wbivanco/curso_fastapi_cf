from fastapi import HTTPException, APIRouter

from typing import List

from ..database import UserReview, User, Movie
from ..schemas import ReviewRequestModel, ReviewResponseModel, ReviewRequestPutModel


router = APIRouter(prefix='/reviews')

@router.post('', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):

    if User.select().where(User.id == user_review.user_id).exists():
        raise HTTPException(404, 'El usuario no existe.')
    
    if Movie.select().where(Movie.id == user_review.movie_id).exists():
        raise HTTPException(404, 'La película no existe.')
    
    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score 
    )

    return user_review

@router.get('', response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1,limit: int = 10):
    reviews = UserReview.select().paginate(page, limit)

    return [user_review for user_review in reviews]


@router.get('/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(404, 'La reseña no existe.')

    return user_review


@router.put('/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(404, 'La reseña no existe.')
    
    user_review.review = review_request.review
    user_review.score = review_request.score

    user_review.save()

    return user_review

@router.delete('/{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(404, 'La reseña no existe.')
    
    user_review.delete_instance()

    return user_review