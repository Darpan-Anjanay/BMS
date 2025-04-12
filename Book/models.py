from django.db import models
from django.contrib.auth.models import User

# class User(AbstractUser):
#     USER_TYPE_CHOICES = (
#         ('student', 'Student'),
#         ('faculty', 'Faculty'),
#         ('librarian', 'Librarian'),
#         ('guest', 'Guest'),
#     )
#     UserType = models.CharField(max_length=50,choices=USER_TYPE_CHOICES)
#     ProfileImage = models.ImageField(upload_to='ProfileImage', null=True, blank=True)
   



class Department(models.Model):
    DepartmentName = models.CharField(max_length=255,verbose_name='Department Name')
    User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.DepartmentName


class Book(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE) 
    Title = models.CharField(max_length=255)
    Author = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=13, unique=True)
    PublicationDate = models.DateField(null=True, blank=True)
    Edition = models.CharField(max_length=50, blank=True)
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)  
    TotalCopies = models.PositiveIntegerField(default=0)
    AvailableCopies = models.PositiveIntegerField(default=0)
    CoverImage = models.ImageField(upload_to='book', null=True, blank=True)
    Description = models.TextField()

    def __str__(self):
        return self.Title
    


class Student(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE) 
    StudentID = models.AutoField(primary_key=True) 
    Department = models.ForeignKey(Department, on_delete=models.CASCADE) 
    Year = models.PositiveIntegerField()

    def __str__(self):
        return self.User.username

class BorrowedBook(models.Model):  
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    BorrowDate = models.DateField(auto_now_add=True)  
    ReturnDate = models.DateField(null=True, blank=True)
    Actual_return_Date = models.DateField(null=True, blank=True)
    Returned = models.BooleanField(default=False)
    FineAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0) 

    def __str__(self):
        return f'{self.Student.User.username} - {self.Book.Title}'

    

class Fine(models.Model):
    BorrowedBook = models.OneToOneField(BorrowedBook, on_delete=models.CASCADE) 
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    PaymentDate = models.DateField(null=True, blank=True)
    Paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Fine for {self.BorrowedBook.Student.User.username} - {self.BorrowedBook.Book.Title}' 
    
