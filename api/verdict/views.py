from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import *


@api_view(['GET'])
def get_verdict_content(request):
    data = request.query_params

    verdict_id = data.get('verdict_id')
    # user_id = request.user_id

    verdict = Verdict.objects.get(id=verdict_id)
    total_like = Like.objects.filter(verdict_id=verdict_id).count()
    total_comment = Comment.objects.filter(verdict_id=verdict_id).count()

    # recommendations
    # ....

    return Response({
        'success': True,
        'data': {
            'verdict_id': verdict.id,
            'title': verdict.title,
            'sub_title': verdict.sub_title,
            'ver_title': verdict.ver_title,
            'judgement_date': verdict.judgement_date,
            'result': verdict.result,
            'laws': verdict.laws,
            'url': verdict.url,
            'crime_id': verdict.crime.id,
            'crime_type': verdict.crime.name,
            'total_like': total_like,
            'total_comment': total_comment,
            'create_time': verdict.create_time,
            'recommendations': []
        }
    })


@api_view(['POST'])
def like_verdict(request):
    data = request.data

    verdict_id = data.get('verdict_id')
    email = request.user_id

    try:
        Like.objects.create(verdict_id=verdict_id, email_id=email)
    except IntegrityError:
        return Response({
            'success': True,
            'message': '已按讚過'
        }, status=status.HTTP_409_CONFLICT)

    return Response({
        'success': True,
        'message': '成功'
    }, status=status.HTTP_201_CREATED)


