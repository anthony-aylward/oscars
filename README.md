# oscars
Assessing the racial bias of the 2014 Oscars

Big Picture Procedure: Hypergeometric Enrichment Test
N: Total number of active actors/actresses in 2014
K: Total number of active actors/actresses in 2014 who are black
n: Total number of actors/actresses nominated for an Oscar for 2014 performances
k: Total number of actors/actresses nominated for an Oscar for 2014 performances who are black

Method for finding N:
Ideas: 
TMDB Data mining using their API: https://www.themoviedb.org/documentation/api


IMDB Data mining using all the patience I can muster http://www.imdb.com/search/title?at=0&countries=us&sort=moviemeter,asc&title_type=feature,tv_series&year=2014,2014
Mine all movie IDs from IMDB using the above search page as a starting point
Mine actor/actress IDs from all IMDB movie pages with the retrieved movie IDs
Mine actor/actress information from all IMDB person pages with retrieved actor IDs


Method for finding K:
Ideas:
If method 2 for finding N is used, use a keyword search in the already-retrieved actor/actress descriptions for ethnic background. If no european or hispanic ancestry is specified, then they are most likely to be black.


Eigenface detection - train a classifier to distinguish black faces from non-black faces and use the trained classifier to detect if an actor is black based on their portrait.
Potential reading material/code inspiration: http://www.mathworks.com/matlabcentral/fileexchange/45915-eigenfaces-algorithm
Consult the workings of a madman: http://www.nndb.com/


Method for finding n and k:
Google “2014 oscar nominees” probably (actually it’d be “2015 oscar nominees” maybe, whatever)






Results

First Run - 2/28/15
The first complete run of the code was completed in the morning of 2/28/2015. These results are severely flawed and can inform us on how to improve our approach.

N = 27498
K = 258
n = 19
k = 0

P_Overrepresentation = 1.0
P_Underrepresentation = 0.9865.

K /  N = 0.00938, a figure that is VERY off. See figure 9 of http://www.bunchecenter.ucla.edu/wp-content/uploads/2014/02/2014-Hollywood-Diversity-Report-2-12-14.pdf

Of our 27498 actors, 24363 of them did not have enough information to be found on NNDB. This could be due to multiple causes:
Their name was not properly formatted (especially true in the case of actors with non-ASCII characters in their name) and they could not be recognized on NNDB.
They do not have an entry on NNDB.

If we re-run the enrichment test such that N = 27498 - 24363 = 3135, we get:

Adjusted P_Overrepresentation = 1.0
Adjused P_Underrepresentation = 0.5283.
Adjusted K / N = 0.0823 (which is closer in agreement with the previously cited figure).

One of our 20 Oscar nominees could not be found in the NNDB. And none of the located nominees were black? Why was I getting told that there was one or two black nominees?
