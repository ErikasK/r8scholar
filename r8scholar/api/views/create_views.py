#REST
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
#Project Files
from ..models import Comment, CustomUser, Review, Course, Department, Instructor, Tags
from ..serializers import (CommentSerializer, CreateCommentSerializer, UserSerializer, ReviewSerializer, CreateUserSerializer, CreateReviewSerializer)
from ..email_sender import email_user
#universal python 
import json 
#Profanity Filter
from profanity_filter import ProfanityFilter
pf = ProfanityFilter()

#creates a new custom user
class CreateUserView(APIView): 
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'): 
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            if user: 
                response = serializer.data 
                print(user.verification_code)
                email_user(user.email,user.verification_code)
                return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateComment(APIView):
    def post(self,request,format=None):
        data = json.loads(request.body.decode("utf-8"))

        email = data['email']
        review_id = data['review_id']
        content = data['content']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'Bad Request': 'User does not exist...'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            review = Review.objects.get(review_id=review_id)
        except Review.DoesNotExist:
            return Response({'Bad Request': 'Review does not exist...'}, status=status.HTTP_400_BAD_REQUEST)
            #Censor profanity in content
        content = pf.censor(content)
            #Create a new comment
        comment = Comment(review=review,commenter = user,name=user.nickname,content=content)
        comment.save()
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

#Creates a new review of a course/instructor/department
class CreateReviewView(APIView):
    serializer_class = CreateReviewSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            nickname = serializer.data['nickname']
            subject = serializer.data['subject']
            title = serializer.data['title']
            content = serializer.data['content']
            rating = serializer.data['rating']
            diff_rating = serializer.data['diff_rating']
            would_take_again = serializer.data['would_take_again']
            tag_1 = serializer.data['tag_1']
            tag_2 = serializer.data['tag_2']
            tag_3 = serializer.data['tag_3']
            review_type = serializer.data['review_type']
            #get user who left review and other objects 
            user = CustomUser.objects.get(nickname=nickname)
            my_department = None
            my_instructor = None
            my_course = None
            if review_type == 'course':
                my_course = Course.objects.get(name=subject)
                my_department = my_course.department
            elif review_type == 'instructor':
                my_instructor = Instructor.objects.get(name=subject)
                my_department = my_instructor.department
            else: #review is on a department
                my_department = Department.objects.get(name=subject)
            #Censor profanity in title and content
            title = pf.censor(str(title))
            content = pf.censor(str(content))
            #Create new review
            review = Review(reviewer=user, nickname=nickname, subject=subject, 
            title=title, content=content, rating=rating, diff_rating=diff_rating, would_take_again=would_take_again, department_name=my_department,
            instructor_name=my_instructor, course_name=my_course, review_type=review_type,tag_1=tag_1,tag_2=tag_2,tag_3=tag_3)
            review.save()
            #update rating of the review subject 
            if review_type == 'course':
                my_course.update_rating()
                my_department.update_course_rating()
            elif review_type == 'instructor':
                my_instructor.update_rating()
                my_department.update_instructor_rating()
            else: #review is on a department
                my_department.update_rating()

            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)