# -*- coding: utf-8 -*- 
import urllib
from copy import deepcopy
import codecs
import os.path
#from progressbar import ProgressBar
#pbar = ProgressBar()


# Only set this one to false if you know what you're doing!
# BEWARE - if you set this to false, you will have to deal with your
# computer downloading a lot of txt files. Plan accordingly.
Use_Postprocessed_Data_For_Movies = True

# If you change any assumptions OTHER than race_to_test_enrichment,
# then you'll have to set this one to false. BEWARE - if you do this,
# you will have to deal with your computer downloading a lot of txt files.
# Plan accordingly.
Use_Postprocessed_Data_For_Actors = True

#===============================================================
# OUR ASSUMPTIONS
#===============================================================
English_Movies_Only = False
Discard_Actors_With_Incomplete_Information = True
Use_Top_Six_Featured_Cast_Per_Movie_Only = False
Omit_TV_Movies = True
Race_To_Test_Enrichment = "white"

#===============================================================
# Create an “actor” object for easy management of actor data
#===============================================================
class Actor(object):
    def __init__(self, name):
        self.name = name
        self.gender = ''
        self.race = ''
        self.birthdate = ''
        self.movie_roles = []

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__,self.name)

    def __str__(self):
        return str(self.name)

#===============================================================
# Create a “movie” object for easy management of movie data
# We may want to normalize actors by roles in high-budget movies, domestic movies, etc
#===============================================================
class Movie(object):
    def __init__(self,title):
        self.title = title
        self.runtime = 0
        self.budget = 0
        self.revenue = 0
        self.language = ''
        self.important_cast = []
        self.genre = []

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__,self.title)

    def __str__(self):
        return str(self.title)

#===============================================================
# Data source: TMDB
# https://www.themoviedb.org/
# First step: Mining how many pages of listings exist for movies in 2014
#===============================================================

if Use_Postprocessed_Data_For_Movies == False:
    i = 1
    TMDB_LINK = "https://www.themoviedb.org/discover/movie?page=" + str(i) + "&year=&primary_release_year=2014&sort_by=&vote_count.gte=&with_genres=&with_keywords=&media_type=movie"
    urllib.urlretrieve(TMDB_LINK, '2014movies_page1.txt')
    f = codecs.open('2014movies_page1.txt','r')
    PageNum = f.read()
    f.close()
    Splitter = "<p class=\"left\" style=\"text-align: left !important;\">Currently on page: 1 of "
    PageNum = PageNum.split(Splitter)[1]
    PageNum = PageNum.split("</p>")[0]
    PageNum = int(PageNum)


    #===============================================================
    # Second step: Mining the movies on each page for the movies in 2014 listing (Results stored in MovieIDs list)
    #===============================================================
    MovieIDs = []
    print "Loading Database..."
    for i in range(0,PageNum):
        TMDB_LINK = "https://www.themoviedb.org/discover/movie?page=" + str(i+1) + "&year=&primary_release_year=2014&sort_by=&vote_count.gte=&with_genres=&with_keywords=&media_type=movie"
        if os.path.isfile('2014movies_page' + str(i+1) + '.txt') == False:
            urllib.urlretrieve(TMDB_LINK, '2014movies_page' + str(i+1) + '.txt')
        f = codecs.open('2014movies_page' + str(i+1) + '.txt','r')
        ActivePage = f.read()
        f.close()
        Raw_MovieLists = ActivePage.split("<div class=\"results\">")[1]
        Raw_MovieLists = Raw_MovieLists.split("/movie/")
        Raw_MovieLists = Raw_MovieLists[1:]
        for j in range(0,len(Raw_MovieLists)):
            Raw_MovieLists[j] = Raw_MovieLists[j][0:8]
            while Raw_MovieLists[j][-1].isdigit() == False:
                Raw_MovieLists[j] = Raw_MovieLists[j][:-1]
        MovieIDs += Raw_MovieLists
    MovieIDs = list(set(MovieIDs))


    #===============================================================
    # Third step: Mining the actors on each page for the movies with the retrieved Movie IDs
    # This is also where we will fill out attribute information for each movie
    #===============================================================
    ActorIDs = []
    All_Actors = []
    All_Movies = []
    print "Fetching Movie Information..."
    for i in range(0,len(MovieIDs)):
        #print i
        # Information for cast ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        CAST_LINK = "https://www.themoviedb.org/movie/"+MovieIDs[i]+"/cast"
        if os.path.isfile('2014actor_page' + str(i+1) + '.txt') == False:
            urllib.urlretrieve(CAST_LINK, '2014actor_page' + str(i+1) + '.txt')

        f = codecs.open('2014actor_page' + str(i+1) + '.txt','r')
        ActivePage = f.read()
        f.close()
        
        ReasonForError = " has not yet been translated to <strong>English (English)</strong>. You can add a new translation by <a href=\"/account/signup?language=en\">signing up</a> for an account and <a href=\"/login?language=en\">logging in</a>.</p>"
        if ReasonForError in ActivePage:
            continue

        ActivePage = ActivePage.split("<a name=\"cast\"></a>")
        Raw_MovieInfo = ActivePage[0]
        Raw_CastInfo = ActivePage[1]

        # The part where we get movie info
        Raw_MovieInfo = Raw_MovieInfo.split("<h3>Release Info<a id=")[0]
        Movie_Title = Raw_MovieInfo.split("<h3>Movie Facts</h3>")[0]
        Movie_Title = Movie_Title.split("<title>")[1]
        Movie_Title = Movie_Title.split(" (2014) - Cast & Crew ")[0]
        Movie_Data = Raw_MovieInfo.split("<h3>Movie Facts</h3>")[1]
        Movie_Data = Movie_Data.split("<p><strong>")[1:]
        for j in range(0,len(Movie_Data)):
            if "Part of the:" in Movie_Data[j] or "Status:" in Movie_Data[j]:
                continue
            elif "Runtime:" in Movie_Data[j]:
                Runtime = Movie_Data[j].split(" />")[1]
                Runtime = Runtime.split("</span>")[0]
            elif "Budget:" in Movie_Data[j]:
                Budget = Movie_Data[j].split("<span id=\"budget\">")[1]
                Budget = Budget.split("</span>")[0]
            elif "Revenue:" in Movie_Data[j]:
                Revenue = Movie_Data[j].split("<span id=\"revenue\">")[1]
                Revenue = Revenue.split("</span>")[0]
            elif "Language:" in Movie_Data[j]:
                Language = Movie_Data[j].split("<span id=\"languages\">")[1]
                Language = Language.split("</span>")[0]           
        Current_Movie = Movie(Movie_Title)
        Current_Movie.runtime = Runtime
        Current_Movie.budget = Budget
        Current_Movie.revenue = Revenue
        Current_Movie.language = Language

        # The part where we get actor names
        Raw_CastInfo = Raw_CastInfo.split("</tbody>")[0]
        Raw_CastInfo = Raw_CastInfo.split("</tr>")
        for j in range(0,len(Raw_CastInfo)-1):
            Temp = Raw_CastInfo[j].split("<td class=\"person\">")[1]
            Temp = Temp.split("<td class=\"character\">")[0]
            Temp = Temp.split(">")[1]
            Temp = Temp.split("<")[0]
            Current_Movie.important_cast += [Temp]
            if Temp in ActorIDs:
                Our_Actor = [o for o in All_Actors if o.name == Temp]
                Actor_Index = All_Actors.index(Our_Actor[0])
                All_Actors[Actor_Index].movie_roles += [Current_Movie.title]
            else:
                ActorIDs += [Temp]
                NewActor = Actor(Temp)
                NewActor.movie_roles += [Current_Movie.title]
                All_Actors += [NewActor]

        # Information for genre ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        GENRE_LINK = "https://www.themoviedb.org/movie/"+MovieIDs[i]
        if os.path.isfile('2014genre_page' + str(i+1) + '.txt') == False:
            urllib.urlretrieve(GENRE_LINK, '2014genre_page' + str(i+1) + '.txt')
        f = codecs.open('2014genre_page' + str(i+1) + '.txt','r')
        ActivePage2 = f.read()
        f.close()

        if ReasonForError in ActivePage2:
            continue
        ActivePage2 = ActivePage2.split("<span id=\"genres\">")[1]
        ActivePage2 = ActivePage2.split("<h3>Production Companies</h3>")[0]
        ActivePage2 = ActivePage2.split("</ul>")[0]
        ActivePage2 = ActivePage2.split("<span itemprop=\"genre\">")[1:]
        ActivePage2 = [j.split("</span>")[0] for j in ActivePage2]
        Current_Movie.genre += ActivePage2
            
        All_Movies += [Current_Movie]

    # Now that we have all of our movie data, let's store it in a friendlier memory-saving form
    out = open('2014_AllMovieData.txt','w')
    for i in range(0,len(All_Movies)):
        out.write(All_Movies[i].title + '\t' + All_Movies[i].runtime + '\t')
        out.write(All_Movies[i].budget + '\t' + All_Movies[i].revenue + '\t')
        out.write(All_Movies[i].language + '\t')
        out.write(','.join(All_Movies[i].important_cast) + '\t')
        out.write(','.join(All_Movies[i].genre))
        if i < len(All_Movies) - 1:
            out.write('\n')
    out.close()

    out = open('2014_ActiveActors_PreData.txt','w')
    for i in range(0,len(All_Actors)):
        out.write(All_Actors[i].name + '\t')
        out.write(','.join(All_Actors[i].movie_roles))
        if i < len(All_Actors) - 1:
            out.write('\n')
    out.close()

elif Use_Postprocessed_Data_For_Movies == True:
    f = open('2014_AllMovieData.txt','r')
    AllMovieData = f.read().split('\n')
    f.close()
    All_Movies = []
    ActorIDs = []
    All_Actors = []
    print "Fetching Movie Information..."
    for i in range(0,len(AllMovieData)):
        moviedata_temp = AllMovieData[i].split('\t')
        Current_Movie = Movie(moviedata_temp[0])
        Current_Movie.runtime = moviedata_temp[1]
        Current_Movie.budget = moviedata_temp[2]
        Current_Movie.revenue = moviedata_temp[3]
        Current_Movie.language = moviedata_temp[4]
        Current_Movie.important_cast += moviedata_temp[5].split(',')
        Current_Movie.genre += moviedata_temp[6].split(',')
        All_Movies += [Current_Movie]

    f = open('2014_ActiveActors_PreData.txt','r')
    AllActorData = f.read().split('\n')
    f.close()
    for i in range(0,len(AllActorData)):
        actor_temp = AllActorData[i].split('\t')
        Current_Actor = Actor(actor_temp[0])
        Current_Actor.movie_roles += actor_temp[1].split(',')
        All_Actors += [Current_Actor]
        ActorIDs += actor_temp[0]
                
# If we only want to look at actors in english speaking movies,
# We need to filter out all actors that don't appear in movies with language code 'en'

if Omit_TV_Movies == True:
    import itertools
    All_Movies = [j for j in All_Movies if "TV Movie" not in j.genre]
    NonTV_Actors = [j.important_cast for j in All_Movies]
    NonTV_Actors = list(set(itertools.chain(*NonTV_Actors)))
    All_Actors = [j for j in All_Actors if j.name in NonTV_Actors]
    ActorIDs = [j for j in ActorIDs if j in NonTV_Actors]
    
if English_Movies_Only == True:
    import itertools
    All_Movies = [j for j in All_Movies if "en" in j.language]
    English_Actors = [j.important_cast for j in All_Movies]
    English_Actors = list(set(itertools.chain(*English_Actors)))
    All_Actors = [j for j in All_Actors if j.name in English_Actors]
    ActorIDs = [j for j in ActorIDs if j in English_Actors]

# We can also impose the claim that only the most prominent (the six top-listed stars)
# actors in a movie would ever reasonably be expected to be in the pool for potential nominees
if Use_Top_Six_Featured_Cast_Per_Movie_Only == True:
    import itertools
    Top_Six_Cast = [j.important_cast[0:6] for j in All_Movies]
    Top_Six_Cast = list(set(itertools.chain(*Top_Six_Cast)))
    All_Actors = [j for j in All_Actors if j.name in Top_Six_Cast]
    ActorIDs = [j for j in ActorIDs if j in Top_Six_Cast]



N = len(ActorIDs)



#===============================================================
# Data source: NNDB
# http://www.nndb.com/
# Fourth step: Consolidating NNDB Information into a local alphabetical listing
#===============================================================
if Use_Postprocessed_Data_For_Actors == False:
    Alphabetical_NNDB = ["http://www.nndb.com/lists/493/000063304/",
                         "http://www.nndb.com/lists/494/000063305/",
                         "http://www.nndb.com/lists/495/000063306/",
                         "http://www.nndb.com/lists/496/000063307/",
                         "http://www.nndb.com/lists/497/000063308/",
                         "http://www.nndb.com/lists/498/000063309/",
                         "http://www.nndb.com/lists/499/000063310/",
                         "http://www.nndb.com/lists/500/000063311/",
                         "http://www.nndb.com/lists/501/000063312/",
                         "http://www.nndb.com/lists/502/000063313/",
                         "http://www.nndb.com/lists/503/000063314/",
                         "http://www.nndb.com/lists/504/000063315/",
                         "http://www.nndb.com/lists/505/000063316/",
                         "http://www.nndb.com/lists/506/000063317/",
                         "http://www.nndb.com/lists/507/000063318/",
                         "http://www.nndb.com/lists/508/000063319/",
                         "http://www.nndb.com/lists/509/000063320/",
                         "http://www.nndb.com/lists/510/000063321/",
                         "http://www.nndb.com/lists/511/000063322/",
                         "http://www.nndb.com/lists/512/000063323/",
                         "http://www.nndb.com/lists/513/000063324/",
                         "http://www.nndb.com/lists/514/000063325/",
                         "http://www.nndb.com/lists/515/000063326/",
                         "http://www.nndb.com/lists/516/000063327/",
                         "http://www.nndb.com/lists/517/000063328/",
                         "http://www.nndb.com/lists/518/000063329/"]
    Alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q",
                "R","S","T","U","V","W","X","Y","Z"]
    NNDB_Listings = {}
    for i in range(0,len(Alphabet)):
        if os.path.isfile("NNDB_"+Alphabet[i]+".txt") == False:
            urllib.urlretrieve(Alphabetical_NNDB[i],"NNDB_"+Alphabet[i]+".txt")
        f = open("NNDB_"+Alphabet[i]+".txt",'r')
        NNDB_Listings[ Alphabet[i] ] = f.read()
        f.close()
    

#===============================================================
# Fifth step: Mining the actor info on each actor page with the retrieved actor IDs (their names)
#===============================================================
print "Fetching Actor Information..."

if Use_Postprocessed_Data_For_Actors == False:
    for i in range(0,len(All_Actors)):
        #print i
        Current_Actor = All_Actors[i].name

        # Dealing with edge cases....
        if Current_Actor == 'Rade \xc5\xa0erbed\xc5\xbeija':
            Current_Actor = "Rade Serbedzija"
            All_Actors[i].name = "Rade Serbedzija"
        elif Current_Actor[-1] == ' ':
            Current_Actor = Current_Actor[:-1]
        Current_Actor_LastInitial = Current_Actor.split(" ")[-1][0]
        if Current_Actor_LastInitial.isalpha() == False:
            continue
        if Current_Actor_LastInitial not in NNDB_Listings:
            continue
        if Current_Actor in NNDB_Listings[ Current_Actor_LastInitial ]:
            Lookup = NNDB_Listings[ Current_Actor_LastInitial ].split("\n")
            Lookup = [j for j in Lookup if Current_Actor in j]
            Lookup = [j for j in Lookup if "a href=" in j]

            # Dealing with edge cases....
            #if Current_Actor == "Hulk Hogan" or Current_Actor == "William Shatner":
                #Lookup = [j for j in Lookup if "a href=" in j]

            if len(Lookup) == 0:
                continue

            ACTOR_URL = Lookup[0].split("<a href=\"")[1].split("\">")[0]
            if os.path.isfile(Current_Actor+".txt") == False:
                urllib.urlretrieve(ACTOR_URL, Current_Actor+".txt")
            f = open(Current_Actor+".txt",'r')
            Temp_ActorInfo = f.read()
            Temp_ActorInfo = Temp_ActorInfo.split("</td></tr><tr><td bgcolor=red height=2></td></tr>")[1]
            Temp_ActorInfo = Temp_ActorInfo.split("\n")[0]
            Temp_ActorInfo = Temp_ActorInfo.split("<b>Born:</b> ")[1]
            
            Temp_DOB = Temp_ActorInfo.split("<b>Gender:</b>")[0]
            Temp_DOB = Temp_DOB.split("</a><br><b>Birthplace:</b>")[0]
            Temp_DOB_Year = Temp_DOB[-4:]
            Temp_DOB_Date = Temp_DOB.split("</a>")[0][-5:]
            Temp_DOB_Final = Temp_DOB_Date + "-" + Temp_DOB_Year
            
            
            Temp_ActorInfo = Temp_ActorInfo.split("<b>Gender:</b> ")[1]
            Temp_Gender = Temp_ActorInfo.split("<b>Race or Ethnicity:</b> ")[0]
            Temp_Gender = Temp_Gender.split("<br>")[0]
            if Current_Actor == "W. Earl Brown":
                Temp_Race = "White"
            else:
                Temp_Race = Temp_ActorInfo.split("<b>Race or Ethnicity:</b> ")[1]
                Temp_Race = Temp_Race.split("<br>")[0]
                if " <" in Temp_Race:
                    Temp_Race = Temp_Race.split(" <")[0]

            All_Actors[i].gender = Temp_Gender
            All_Actors[i].race = Temp_Race
            All_Actors[i].birthdate = Temp_DOB_Final

    out = open('2014_ActiveActors_AllData.txt','w')
    for i in range(0,len(All_Actors)):
        out.write(All_Actors[i].name + '\t')
        out.write(','.join(All_Actors[i].movie_roles))
        out.write('\t')
        out.write(All_Actors[i].gender + '\t' + All_Actors[i].birthdate + '\t')
        out.write(All_Actors[i].race)
        if i < len(All_Actors) - 1:
            out.write('\n')
    out.close()
elif Use_Postprocessed_Data_For_Actors == True:
    f = open('2014_ActiveActors_AllData.txt','r')
    AllActorData = f.read().split('\n')
    f.close()
    for i in range(0,len(AllActorData)):
        actor_temp = AllActorData[i].split('\t')
        Current_Actor = Actor(actor_temp[0])
        Current_Actor.movie_roles += actor_temp[1].split(',')
        Current_Actor.gender = actor_temp[2]
        Current_Actor.birthdate = actor_temp[3]
        Current_Actor.race = actor_temp[4]
        All_Actors += [Current_Actor]
        ActorIDs += actor_temp[0]    


if Discard_Actors_With_Incomplete_Information == True:
    All_Actors = [i for i in All_Actors if i.race != '']
    N = len(All_Actors)

Black_Actors = [i for i in All_Actors if "Black" in i.race]
White_Actors = [i for i in All_Actors if "White" in i.race]

if Race_To_Test_Enrichment == "black":
    K = len(Black_Actors)
elif Race_To_Test_Enrichment == "white":
    K = len(White_Actors)

#===============================================================
# Data source: ABC
# http://oscar.go.com/nominees
# Sixth step: Listing out the oscar nominees
#===============================================================
Nominees = ["Steve Carell","Bradley Cooper","Benedict Cumberbatch","Michael Keaton","Eddie Redmayne",
            "Robert Duvall","Ethan Hawke","Edward Norton","Mark Ruffalo","J.K. Simmons",
            "Marion Cotillard","Felicity Jones","Julianne Moore","Rosamund Pike","Reese Witherspoon",
            "Patricia Arquette","Laura Dern","Keira Knightley","Emma Stone","Meryl Streep"]

Nominees_in_Database = [i for i in All_Actors if i.name in Nominees]
Black_Nominees = [i for i in Nominees_in_Database if "Black" in i.race]
White_Nominees = [i for i in Nominees_in_Database if "White" in i.race]

n = len(Nominees_in_Database)

if Race_To_Test_Enrichment == "black":
    k = len(Black_Nominees)
elif Race_To_Test_Enrichment == "white":
    k = len(White_Nominees)


#===============================================================
# Seventh step: Hypergeometric Enrichment!
# Way to interpret:
# A significant value for P_Value_OverRepresentation means that our feature is over-represented in our selection
# A significant value for P_Value_UnderRepresentation means that our feature is under-represented in our selection
#===============================================================
import scipy.stats as stats
P_Value_OverRepresentation = stats.hypergeom.sf(int(k) - 1,int(N),int(K),int(n))
P_Value_UnderRepresentation = stats.hypergeom.cdf(int(k) + 1,int(N),int(K),int(n))

#===============================================================
# OUTPUT
#===============================================================
print " "
print "Overrepresentation p-value: " + str(P_Value_OverRepresentation)
print "Underrepresentation p-value: " + str(P_Value_UnderRepresentation)
print " "
print "ASSUMPTIONS:"
if Race_To_Test_Enrichment == "black":
    print "Values are examining representation of black actors."
elif Race_To_Test_Enrichment == "white":
    print "Values are examining representation of white actors."
if Discard_Actors_With_Incomplete_Information == True:
    print "We are ignoring actors that do not have available racial information."
else:
    print "We are NOT ignoring actors that do not have available racial information."  
if English_Movies_Only == True:
    print "We are ignoring actors cast in non-English movies."
else:
    print "We are NOT ignoring actors cast in non-English movies."
if Use_Top_Six_Featured_Cast_Per_Movie_Only == True:
    print "We are only considering the top six credited actors of the movie on TMDB."
else:
    print "We are considering all credited actors of the movie on TMDB."
if Omit_TV_Movies == True:
    print "We are excluding TV Movies."
else:
    print "We are INCLUDING TV Movies."
