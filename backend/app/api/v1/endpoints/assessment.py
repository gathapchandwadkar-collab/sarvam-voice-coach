from fastapi import APIRouter, UploadFile, File, Form
from app.models.schemas import AssessmentResponse
from app.services.pronunciation_eval.scorer import PronunciationScorer

router = APIRouter()

@router.post("/evaluate", response_model=AssessmentResponse)
async def evaluate_pronunciation(
    profile_id: str = Form(...),
    target_text: str = Form(...),
    language_code: str = Form(...),
    audio_file: UploadFile = File(...)
):
    """
    Learner records their attempt at speaking the phrase.
    The system compares acoustic alignment and phonemes against the reference,
    returning an accuracy score, fluency score, and actionable pronunciation tips.
    """
    # Evaluate learner audio against target phonetics
    result = PronunciationScorer.evaluate(
        learner_audio_path="temp_path",
        target_text=target_text,
        language_code=language_code
    )
    return result
