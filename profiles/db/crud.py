import json
import logging
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from django.db.models import Q


class CrudFunction:

    def __init__(self) -> None:
        pass

    def crud_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        limit = int(request.query_params.get("limit", 10))  # varsayılan olarak 10
        skip = int(request.query_params.get("skip", 0))  # varsayılan olarak 0
        filter_data = str(request.query_params.get("filter_data", "{}"))
        logging.warning(filter_data)
        try:
            filter_data_json = json.loads(filter_data)
        except json.JSONDecodeError:
            filter_data_json = {}
            raise ValidationError("Bad filtering")
        filters = Q()
        for key, value in filter_data_json.items():
            lookup = key.split("__")
            if len(lookup) > 1:
                filters &= Q(**{f"{lookup[0]}__{lookup[1]}": value})
            else:
                filters &= Q(**{f"{lookup[0]}": value})
        queryset = queryset.filter(filters).order_by("id")[skip : skip + limit]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
