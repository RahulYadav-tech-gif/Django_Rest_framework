from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import generics
from .helpers import *
import datetime
import pandas as pd
from django.conf import settings
import uuid

# Create your views here.


@api_view(['GET'])
def get_book(request):
    try:
        book_objs = Book.objects.all()
        serializer = BookSerializer(book_objs, many=True)

        return Response({'status':200, 'payload':serializer.data})
    
    except Exception as e:
        return Response({'status':403, 'message':'something went wrong'})
    

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({'status': 403, 'errors' : serializer.errors, 'message' : 'Something went wrong'})
        
        serializer.save()

        user = User.objects.get(username = serializer.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({'status':200, 'payload':serializer.data, 'refresh': str(refresh), 'access': str(refresh.access_token), 'message':'your data has been saved.',})


class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        student_objs = Student.objects.all()
        serializer = StudentSerializer(student_objs, many=True)
        return Response({'status':200, 'payload':serializer.data})

    def post(self, request):
        data = request.data
        serializer = StudentSerializer(data = request.data)

        if not serializer.is_valid():
            return Response({'status':403, 'error':serializer.errors ,'message':'Something went wrong'})

        serializer.save()
        return Response({'status':200, 'payload':data, 'message':'your data has been saved.'})


    def put(self, request):
        try:
            student_obj = Student.objects.get(id = id)

            serializer = StudentSerializer(student_obj, data=request.data, partial=False)
            if not serializer.is_valid():
                return Response({'status':403, 'error':serializer.errors ,'message':'Something went wrong'})

            serializer.save()

            return Response({'status':200, 'payload':serializer.data, 'message':'your data has been saved.'})
        
        except Exception as e:
            return Response({'status':403, 'message':'invalid id'})
        

    def patch(self, request):
        try:
            student_obj = Student.objects.get(id = request.data['id'])

            serializer = StudentSerializer(student_obj, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({'status':403, 'error':serializer.errors ,'message':'Something went wrong'})

            serializer.save()

            return Response({'status':200, 'payload':serializer.data, 'message':'your data has been saved.'})
        
        except Exception as e:
            return Response({'status':403, 'message':'invalid id'})

    def delete(self, request):
        try:
            id = request.GET.get('id')
            student_obj = Student.objects.get(id = id)
            student_obj.delete()
            return Response({'status':200, 'message':'Student is deleted'})


        except Exception as e:
            return Response({'status':403, 'message':'invalid id'})




class StudentGeneric(generics.ListAPIView, generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer



class StudentGeneric1(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'


class GeneratePdf(APIView):
    def get(self, request):
        student_objs = Student.objects.all()
        params = {
            'today': datetime.date.today(),
            'student_objs' : student_objs
        }
        file_name , status = save_pdf(params)

        if not status:
            return Response({'status' : 400})

        return Response({'status' : 200, 'path' : f'/media/{file_name}'})


class ExportImportExcel(APIView):
    def get(self, request):
        student_objs = Student.objects.all()
        serializer = StudentSerializer(student_objs, many=True)

        df = pd.DataFrame(serializer.data)
        print(df)
        df.to_csv(f"public/excel/{uuid.uuid4()}.csv", encoding="UTF-8", index=False)
        return Response({'status':200})

    def post(self, request):
        uploaded_file = request.FILES.get('files')
        if not uploaded_file:
            return Response({'status': 400, 'error': 'No file uploaded.'})
        exceled_upload_obj = ExcelFileUpload.objects.create(excel_file_upload=request.FILES['files'])
        df = pd.read_csv(f"{settings.BASE_DIR}/public/{exceled_upload_obj.excel_file_upload}")
        print(df.values.tolist())
        return Response({'status':200})







# @api_view(['GET'])
# def home(request):
#     student_objs = Student.objects.all()
#     serializer = StudentSerializer(student_objs, many=True)

#     return Response({'status':200, 'payload':serializer.data})

# @api_view(['POST'])
# def post_student(request):
#     data = request.data
#     serializer = StudentSerializer(data = request.data)

#     # if request.data['age'] < 18:
#     #     return Response({'status':403, 'warning':'Age must be greater than 18'})
#     # As we use DRf, the above logic will be done in 'serializers.py'
#     if not serializer.is_valid():
#         return Response({'status':403, 'error':serializer.errors ,'message':'Something went wrong'})

#     serializer.save()

#     return Response({'status':200, 'payload':data, 'message':'your data has been saved.'})

# @api_view(['PUT'])
# def update_student(request, id):
#     try:
#         student_obj = Student.objects.get(id = id)

#         serializer = StudentSerializer(student_obj, data=request.data, partial=True)
#         if not serializer.is_valid():
#             return Response({'status':403, 'error':serializer.errors ,'message':'Something went wrong'})

#         serializer.save()

#         return Response({'status':200, 'payload':serializer.data, 'message':'your data has been saved.'})
    
#     except Exception as e:
#         return Response({'status':403, 'message':'invalid id'})
    

# @api_view(['DELETE'])
# def delete_student(request, id):
#     try:
#         student_obj = Student.objects.get(id = id)
#         student_obj.delete()
#         return Response({'status':200, 'message':'Student is deleted'})


#     except Exception as e:
#         return Response({'status':403, 'message':'invalid id'})

