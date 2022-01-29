# Django University Website
# https://strykb.pythonanywhere.com/

## Login info
| Account type | Email                            | Password   |
| :----------: | :------------------------------: |:----------:|
| technician   | tech@example<span></span>.com    | 123        |
| tutor        | tutor@example<span></span>.com   | 123        |
| student      | student@example<span></span>.com | 123        |

I recommend using technician's account, since it has the most features.

## Important note
You are free to change or delete any data on this website.  
If something is missing or isn't working properly, click "restore" button on the home page.  

## General info
This project is an university website. It contains a basic university structure (departments, courses etc.) with exams and grades.  
Main features:
  * login/registration with email instead of username
  * three user types:  
    * technician - has the ability to manage users and university structure elements  
      e.g. this user can approve new users as students, create a new department  
        
      | Email                         | Password   |
      | :---------------------------: |:----------:|
      | tech@example<span></span>.com | 123        |  
    * tutor - can create/edit exams and grades, but only if he is assigned to currently chosen module
       
      | Email                          | Password   |
      | :----------------------------: |:----------:|
      | tutor@example<span></span>.com | 123        |  
    * student - can view exams and grades to which he is assigned to
        
      | Email                            | Password   |
      | :------------------------------: |:----------:|
      | student@example<span></span>.com | 123        |  
  * automatically set relationships between models  
    e.g. if user creates course, this course will be automatically linked to department
  * user-friendly forms - instead of using the default admin panel page to manage models, this website uses its own forms with Select2.  
    This enables searching in dropdown form fields.
  * search bar for users list


## Technologies
Project is created with:
* Python
* Django
* Front-End Technologies


## Sources
Department and course descriptions - https://www.ox.ac.uk/
