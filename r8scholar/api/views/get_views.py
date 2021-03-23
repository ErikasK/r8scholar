#Project Files
from ..models import CustomUser, Review, Course, Department, Instructor
from ..serializers import (UserSerializer, ReviewSerializer, CourseSerializer, DepartmentSerializer, 
InstructorSerializer)
#REST
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
#Python
import json

#get views 
class GetUser(APIView):
    serializer_class = UserSerializer
    lookup_url_kwarg = 'email'
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        email = request.GET.get(self.lookup_url_kwarg)
        if email != None:
            user = CustomUser.objects.filter(email=email)
            if len(user) > 0:
                data = UserSerializer(user[0]).data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'User Not Found': 'Invalid User Email.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Email not found in request'}, status=status.HTTP_400_BAD_REQUEST)

#returns all reviews on a specific subject 
class GetReviewsView(APIView): 
    serializer_class = ReviewSerializer
    lookup_url_kwarg = 'subject'
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        subject = request.GET.get(self.lookup_url_kwarg)
        if subject != None:
            reviews = Review.objects.filter(subject=subject)
            if len(reviews) > 0:
                data = []
                for review in reviews: 
                    data.append(ReviewSerializer(review).data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'Review(s) Not Found': 'Invalid Review Subject.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'No Subject to Query'}, status=status.HTTP_400_BAD_REQUEST)

class GetCourseView(APIView): 
    serializer_class = CourseSerializer
    lookup_url_kwarg = 'name'
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        name = request.GET.get(self.lookup_url_kwarg)
        if name != None:
            course = Course.objects.filter(name=name)
            if len(course) > 0:
                data = self.serializer_class(course[0]).data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'Course Not Found': 'Invalid Course Name.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'No Subject to Query'}, status=status.HTTP_400_BAD_REQUEST)

class GetDepartmentView(APIView): 
    serializer_class = DepartmentSerializer
    lookup_url_kwarg = 'name'
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        name = request.GET.get(self.lookup_url_kwarg)
        if name != None:
            department = Department.objects.filter(name=name)
            if len(department) > 0:
                data = self.serializer_class(department[0]).data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'Department Not Found': 'Invalid department name.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'No Subject to Query'}, status=status.HTTP_400_BAD_REQUEST)

class GetInstructorView(APIView): 
    serializer_class = InstructorSerializer
    lookup_url_kwarg = 'name'
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        name = request.GET.get(self.lookup_url_kwarg)
        if name != None:
            instructor = Instructor.objects.filter(name=name)
            if len(instructor) > 0:
                data = self.serializer_class(instructor[0]).data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'Instructor Not Found': 'Invalid instructor name.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'No Subject to Query'}, status=status.HTTP_400_BAD_REQUEST)

class getTopCourses(APIView): #im only going to comment this one because instructors is the exact same 
    permission_classes = (permissions.AllowAny,)
    def post(self,request):
        data = json.loads(request.body.decode("utf-8")) #info is given by a post request
        department = data['department']#since we need both a departmant and an amount 
        amt = int(data['amount'])
        my_department = None
        if department != 'any':
            my_department = Department.objects.get(name=department) #find the department

        if my_department is not None or department=="any":#if not goto else and return that we dont have that department 
            top_courses = [None]*amt
            courses = None#find the courses the belong to the department 
            if department=="any":
                courses = Course.objects.all()
                if len(courses) >= amt: #cannot request more courses than we have 
                    #Get list of instructors sorted by rating
                    courses_sorted_rating = Course.objects.order_by('-rating')
                    for i in range(amt):
                        top_courses[i] = courses_sorted_rating[i]
                    #serialize the final choices 
                    for c in range(amt): #cannot do this before because we need to compared the ratings constantly 
                        top_courses[c] = CourseSerializer(top_courses[c]).data
                    return Response(top_courses, status=status.HTTP_200_OK) 
                else:
                    return Response({"Invalid Request":"Too many courses requested"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                courses = Course.objects.all()
                if len(courses) >= amt: #cannot request more courses than we have 
                    #Get list of instructors sorted by rating
                    courses_sorted_rating = Course.objects.filter(department=my_department).order_by('-rating')
                    for i in range(amt):
                        top_courses[i] = courses_sorted_rating[i]
                    #serialize the final choices 
                    for c in range(amt): #cannot do this before because we need to compared the ratings constantly 
                        top_courses[c] = CourseSerializer(top_courses[c]).data
                    return Response(top_courses, status=status.HTTP_200_OK)
                else:
                    return Response({"Invalid Request":"Too many courses requested"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Invalid Request":"Courses not found"}, status=status.HTTP_404_NOT_FOUND)

class getTopInstructors(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self,request):
        data = json.loads(request.body.decode("utf-8"))
        department = data['department']
        amt = int(data['amount'])
        my_department = None
        if department != 'any':
            my_department = Department.objects.get(name=department) #find the department
        
        if my_department is not None or department=="any":
            top_instructors = [None]*amt
            instructors = None
            if department == "any":
                instructors = Instructor.objects.all()
                if len(instructors) >= amt:
                    #Get list of instructors sorted by rating
                    instructors_sorted_rating = Instructor.objects.order_by('-rating')#minus sign orders by descending
                    for i in range(amt):
                        top_instructors[i] = instructors_sorted_rating[i]
                    #serialize the final choices 
                    for i in range(amt):
                        top_instructors[i] = InstructorSerializer(top_instructors[i]).data
                    return Response(top_instructors, status=status.HTTP_200_OK)
                else:
                    return Response({"Invalid Request":"Too many instructors requested"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                instructors = Instructor.objects.filter(department=my_department)
                if len(instructors) >= amt:
                    #Get list of instructors sorted by rating
                    instructors_sorted_rating = Instructor.objects.filter(department=my_department).order_by('-rating')#minus sign orders by descending
                    for i in range(amt):
                        top_instructors[i] = instructors_sorted_rating[i]
                    #serialize the final choices 
                    for i in range(amt):
                        top_instructors[i] = InstructorSerializer(top_instructors[i]).data
                    return Response(top_instructors, status=status.HTTP_200_OK)
                else:
                    return Response({"Invalid Request":"Too many instructors requested"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Invalid Request":"Courses not found"}, status=status.HTTP_404_NOT_FOUND)

class getTopDepartments(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = DepartmentSerializer
    lookup_url_kwarg = 'amount'

    def get(self, request, format=None):
        amt = int(request.GET.get(self.lookup_url_kwarg))
        top_departments=[None]*amt
        departments = Department.objects.all()
        if len(departments) >= amt:
            departments_sorted_rating = Department.objects.order_by('-rating')#minus sign orders by descending
            for i in range(amt):
                top_departments[i] = departments_sorted_rating[i]
            #serialize final list
            for i in range(amt):
                top_departments[i] = self.serializer_class(top_departments[i]).data
            return Response(top_departments, status=status.HTTP_200_OK)
        else:
            return Response({"Invalid Request":"Too many departments requested"}, status=status.HTTP_400_BAD_REQUEST)