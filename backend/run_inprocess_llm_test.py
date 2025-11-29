import traceback
from app import create_app
from app.services.llm_service import generate_response

app = create_app()
with app.app_context():
    try:
        print('Calling generate_response in-process...')
        res = generate_response([{'role':'user','content':'Hi there'}], use_cache=False)
        print('Result:', res)
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()
