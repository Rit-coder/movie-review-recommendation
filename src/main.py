import numpy as np
import pandas as pd

''' This Dataframe basically contains four things: Movies, User, Rating, Review'''
SESSION = False  # phase which takes true or false according to situation.
CURRENT_USER = ""  # the user who is accessing it currently, will be appended and when logsout this will come back as it is
# Movie Scetion!!!!!!!
MOVIE_PATH = "..\\datastore\\movies.csv"  # the csv folder that I created for movies
movie_columns = ["Name", "Year", "Genre",
                 "Language"]  # columns for movies on the basis of its specifications/ categories.
# User Section!!!!
USER_PATH = "..\\datastore\\users.csv"
user_columns = ["Name", "email_id", "password"]
# Rating Section!!! and we'll go to recommendation system after some lines
RATING_PATH = "..\\datastore\\ratings.csv"
rating_columns = ["Movie Name", "email_id", "Rating"]

GENRE = ["comedy", "horror", "action", "romance", "thriller"]  # subcategories of Genre
LANGUAGE = ["hindi", "english", "kannada", "tamil", "telgu"]  # subcategories of language


# function "add movie" is defined to add movie with specifications as parameters.
def add_movie(name, year, genre, language):
    df_csv_movie = pd.read_csv(MOVIE_PATH)  # the movie from csv file is read and stored in a variable
    # for uniformity i kept all charecter in in smallcase
    if (name.lower().strip() in df_csv_movie['Name'].unique()):
        print(" ============= Movie already exists in Movie datastore!! ============= \n")
    else:
        new_movie = pd.DataFrame([[name.lower(), year, genre.lower(), language.lower()]], columns=movie_columns)
        updated_datastore = df_csv_movie.append(new_movie, ignore_index=True)
        updated_datastore.to_csv(MOVIE_PATH, columns=movie_columns, index=False)
        print(" ============= Movie " + name + " added! ============= \n")


def add_user(name, email, pwd):
    df_csv_user = pd.read_csv(USER_PATH)

    if (email.lower().strip() in df_csv_user['email_id'].unique()):
        print(" ============= Email Id already exists in User datastore!! ============= \n")
    else:
        new_user = pd.DataFrame([[name.lower(), email.lower(), pwd]], columns=user_columns)
        updated_datastore = df_csv_user.append(new_user, ignore_index=True)
        updated_datastore.to_csv(USER_PATH, columns=user_columns, index=False)
        print(" ============= User " + name + " added! ============= \n")


def view_movie():
    df_csv_movie = pd.read_csv(MOVIE_PATH)
    print(df_csv_movie)


def login(eml, pwd):
    df_csv_user = pd.read_csv(USER_PATH)
    global SESSION
    global CURRENT_USER

    ind = df_csv_user.index[df_csv_user['email_id'] == eml]
    if (df_csv_user['password'][ind].unique() == pwd):
        SESSION = True
        CURRENT_USER = eml
        print("Login Successful!!!\n")
    else:
        print("Wrong Credentials!!!\n")


def logout():
    global SESSION
    global CURRENT_USER
    SESSION = False
    CURRENT_USER = ""
    print("Logout Successful!!!\n")


def user_rating(movie_name, rating, user):
    df_csv_movie = pd.read_csv(MOVIE_PATH)
    df_csv_rating = pd.read_csv(RATING_PATH)
    if movie_name.lower().strip() not in df_csv_movie['Name'].unique():
        print(" ============= Movie does not exist, Please add the movie to rate it!! ============= \n")
    else:
        df_dedup_index = df_csv_rating.index[
            (df_csv_rating["Movie Name"] == movie_name.lower()) & (df_csv_rating["email_id"] == user.lower())]
        df_dedup = df_csv_rating.drop(index=df_dedup_index)
        new_rating = pd.DataFrame([[movie_name.lower(), user.lower(), rating]], columns=rating_columns)
        updated_datastore = df_dedup.append(new_rating, ignore_index=True)
        updated_datastore.to_csv(RATING_PATH, columns=rating_columns, index=False)
        print(" ============= You have rated the Movie: " + movie_name.upper() + " ,Rating: " + str(
            rating) + "/5! ============= \n")


def get_rating_by_name(movie_name):
    df_csv_movie = pd.read_csv(MOVIE_PATH)
    df_csv_rating = pd.read_csv(RATING_PATH)
    if movie_name.lower().strip() not in df_csv_movie['Name'].unique():
        print(
            " ============= Movie does not exist in our database. You can help us by adding the Movie to our Collection !! ============= \n")

    else:
        rating_list = df_csv_rating[df_csv_rating["Movie Name"] == movie_name.lower()]["Rating"]
        print("Movie " + movie_name + " has got avg Rating of " + str(np.average(rating_list)) + "!!!\n")


def recommendation(genre, language):
    df_csv_rating = pd.read_csv(RATING_PATH)
    df_csv_movie = pd.read_csv(MOVIE_PATH)
    if (genre == "" and language == ""):
        df = df_csv_rating.groupby("Movie Name", sort=True).agg({'Rating': [np.average]})
        print(df["Rating"].sort_values("average", ascending=False))
        print("\n")
    elif (genre != "" and language == ""):
        movie_list_with_genre = df_csv_movie[df_csv_movie["Genre"] == genre]["Name"].tolist()
        df = df_csv_rating[df_csv_rating["Movie Name"].isin(movie_list_with_genre)].groupby("Movie Name",
                                                                                            sort=True).agg(
            {'Rating': [np.average]})
        print(df["Rating"].sort_values("average", ascending=False))
        print("\n")
    elif (genre == "" and language != ""):
        movie_list_with_lanuage = df_csv_movie[df_csv_movie["Language"] == language]["Name"].tolist()
        df = df_csv_rating[df_csv_rating["Movie Name"].isin(movie_list_with_lanuage)].groupby("Movie Name",
                                                                                              sort=True).agg(
            {'Rating': [np.average]})
        print(df["Rating"].sort_values("average", ascending=False))
        print("\n")
    elif (genre != "" and language != ""):
        movie_list_with_genre = df_csv_movie[df_csv_movie["Genre"] == genre]
        movie_list_with_lanuage = movie_list_with_genre[movie_list_with_genre["Language"] == language]["Name"].tolist()
        df = df_csv_rating[df_csv_rating["Movie Name"].isin(movie_list_with_lanuage)].groupby("Movie Name",
                                                                                              sort=True).agg(
            {'Rating': [np.average]})
        print(df["Rating"].sort_values("average", ascending=False))
        print("\n")


while (True):
    try:

        print("\t\t\t************************************")

        while (not SESSION):
            inp = input(
                " ============= Enter 1 to LOGIN!! ============= \n ============= Enter 2 to SIGNUP!! ============= \n")
            if (inp == "1"):
                eml = input("Enter your Email Id: ")
                pwd = input("Enter your Password: ")
                login(eml, pwd)
            if (inp == "2"):
                print("WELCOME TO SIGNUP!!!\n\n")
                movie_name = input("Enter User name! ")
                email = input("Enter email_id! ")
                pwd = input("Enter Password! ")
                add_user(movie_name, email, pwd)

        while (SESSION):
            inp = input(
                " ============= Enter 1 to add a movie!! ============= \n ============= Enter 2 to view Movie Database!! ============= \n" \
                " ============= Enter 3 to Rate a movie!! ============= \n ============= Enter 4 for movie recommendation/rating!! ============= \n" \
                " ============= Enter 5 to Logout!! ============= \n")

            if inp == "1" and SESSION:
                movie_name = input("Enter movie name to add! ")
                year = int(input("Enter released year of the movie!"))
                genre = input("Enter Genre for the movie! HINT: {" + ", ".join(GENRE) + "} ")
                language = input("Enter Language for the movie! HINT: {" + ", ".join(LANGUAGE) + "} ")
                add_movie(movie_name, year, genre, language)

            elif inp == "2":
                view_movie()

            elif inp == "3":
                movie_name = input("Enter Movie name! ")
                rating = float(input("Enter Rating! HINT {1-5} "))
                user_rating(movie_name, rating, CURRENT_USER)

            elif inp == "4":
                inp_rec = input("Enter 1 to get Rating by Movie Name!!\nEnter 2 to get Movie recommendation!! ")
                if (inp_rec == "1"):
                    movie_name = input("Enter a Movie name!! ")
                    get_rating_by_name(movie_name)
                elif (inp_rec == "2"):
                    genre = input("You can enter Genre or proceed...")
                    language = input("You can enter Language or proceed...")
                    recommendation(genre, language)
                else:
                    print("Invalid Input")

            elif inp == "5":
                logout()

            else:
                print("Invalid Input")
    except Exception as e:
        print(e)
