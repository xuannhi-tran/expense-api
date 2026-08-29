from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def expense_list(request):
    if request.method == 'GET':
        expenses = Expense.objects.filter(
            user = request.user
        )
        category = request.query_params.get('category')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')

        if category:
            expenses = expenses.filter(category=category)
        
        if search:
            expenses = expenses.filter(name__icontains=search)

        if ordering: 
            expenses = expenses.order_by(ordering)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(expenses, request)

        serializer = ExpenseSerializer(result_page, many=True)

        return paginator.get_paginated_response(
            serializer.data
        )
    
    elif request.method == 'POST':
        serializer = ExpenseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(
                user = request.user
            )
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET','DELETE', 'PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk = pk, user=request.user)
    if request.method == 'DELETE':
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'GET': 
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = ExpenseSerializer(
            expense,
            data = request.data,
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        serializer = ExpenseSerializer(
            expense,
            data = request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    






    
