# Create your views here
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import generate_incremental_chfid

@api_view(['GET'])
def get_new_chfid(request):
    new_chfid = generate_incremental_chfid()
    return Response({'new_chfid': new_chfid})
