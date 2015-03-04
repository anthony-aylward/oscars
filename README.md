# On the Racial Bias of the 2014 Oscars

In this project, we aim to conduct a series of enrichment tests in order to study the probability of racial bias in the selection of Academy Award nominees. Our core procedure is based around the classic Hypergeometric Enrichment Test:

N: Total number of active actors/actresses in 2014

K: Total number of active actors/actresses in 2014 who are of race X

n: Total number of actors/actresses nominated for an Oscar for 2014 performances

k: Total number of actors/actresses nominated for an Oscar for 2014 performances who are of race X


We determine N by examining the cast listings for all movies made in the year 2014. This was done using tMDB (https://www.themoviedb.org/). This product uses the TMDb API but is not endorsed or certified by TMDb.

We determine K by using the listings of personal details on NNDB (http://www.nndb.com/). Likewise, this project is not endorsed or certified by NNDB. We determine n and k from official listings of Academy Award nominations.


## Preliminary Results

Under various criteria, we are consistently observing an over-representation of white actors and actresses in the relevant 2014 Academy Award categories (p < 0.05). Results are not yet finalized.

We're currently using this year's (2015) nominees for Best Lead Actor, Best Lead Actress, Best Supporting Actor, and Best Supporting actress as the foreground dataset. It is notable that this year's nominees for those categories are ALL white, so the fully-fledged hypergeometric test might actually be overkill. In this case, the question "are whites over-represented" boils down to "are at least 99.75 % of nomination-eligible actors white?"


## Some external links
http://www.bunchecenter.ucla.edu/wp-content/uploads/2014/02/2014-Hollywood-Diversity-Report-2-12-14.pdf

http://oscar.go.com/nominees
