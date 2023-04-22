# Continental  Quiz
#### Video Demo:  https://youtu.be/jUXfu-PbrdY
#### Description:

Continental Quiz is a quiz app made using Flask. It starts off by asking to either log in or register. After this, the user is redirected to the main menu where the user has two options, either to **play** or learn **how to play**. The former option simply takes the user through the basic steps of playing the quiz game. 

If **Play** is pressed, the user is redirected to a map of the world where the user is prompted to click on a continent. Once chosen, the user is taken to the actual quiz where 10 questions about that continent are asked with four options in an MCQ format. The user has the answer each question and then press *next* to move on. The user is not allowed to go back and answer any question that has already been submitted. 

Reloading or going to the page again by pressing on the same continent in the *map* page does not reset the quiz. This is ensured by entering the current progess of the user into the database. 

Once the quiz has been completed, a thank you page is displayed along with the score. The user can also check their score for all of the quizes by going into **Scores** in the navigation bar on the top. Users can also go to **Leaderboard** to check the top scorers for each continent.

### Install Dependencies from requirements.txt 
```
pip install -r requirements.txt
```


### About the files:
---
1. **app.py**: The main code for the program is stored in `app.py`. This includes most of the functions on which the web app runs. Database is also updated through this script, by using cs50's SQL library to connect to and edit the database.

2. **helper.py**: This python file contains only one fuction, the `login_required` function which acts as a decorator function, forcing the user to login before accessing any content[^1].

3. **questions.py**: This stores all of the questions, the options and thec correct answer in the form a 2D-array. It is in the format: question, option-1, option-2, option-3, option-4, correct answer

4. **requirements.txt**: Dependencies needed to run the web app

5. **test.py**: Python script used to create the structure of the database. Has been rendered useless by commenting out a line of code to protect from self-sabotage incase the script is run again by mistake.

6. **templates**: Contains all the html pages rendered through the use of Flask

7. **static**: Contains the CSS and the image used as background in menu

---
[^1]: Other than `leaderboard` page

