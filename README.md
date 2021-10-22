# Joe's 2021-22 DownGoesBrown Prediction Contest Program

## ABOUT

Each year, [Sean McIndoe (DownGoesBrown, or DGB)](http://www.downgoesbrown.com/) runs a "simple" prediction contest for readers. I'm working on going to school to earn my bachelor's degree in data management & analysis, and have been learning a lot of Python programming this year. At the time that Sean posted the 2021-22 contest, I'd just finished some classes on scraping data from the web, and the thought had occurred to me that it would probably be possible to scrape the contest entries from the comment section at The Athletic and then the data could be wrangled to be a nice, standardized dataframe, where it could be programatically scored out. This started out very much as a "I wonder if I can pull this off..." kind of thing that quickly became a "wow, this is really tough!" situation until it finally turned into a "oh cool, I think I'm getting somewhere!" thing. With the contest entries successfully scraped from a saved copy of the original contest article on The Athletic, I was then able to start wrangling and standardizing the scraped data, so that I could also design a script to automatically score the contest entries.

Given that I'm working on making a career change here, I put my work from this project up on GitHub as another example of my work for prospective employers.

## WHAT CAN I FIND HERE?

This repository hosts the following:
- The copy of the original contest article, including all comments, which I saved at 17:32 Mountain Time on 12 Oct 2021, two minutes after the deadline for contest entries. 
- The full .py script that I wrote, which:
    - Scrapes the comments from the provided html page into a list of authors and associated comments
    - Applies numerous customized fixes to those comments to address those entries which were formatted such that they were incapable of being handled programmatically
    - Generates a dataframe, each row consisting of an author (contestant entrant) and their associated comment (contest entry)
    - Applies numerous customized fixes to the dataframe to address those entries which were able to be handled programmatically, but contained errors
    - Applies standardization operations to each question through the use of several voluminous dictionaries
    - Generate basic reporting and value_counts for each question
    - Generate a .csv file of the entire cleaned and standardized dataframe
- A slideshow summary, containing the reports generated for each question as well as my own notes regarding fun or interesting things that I noticed in the process of handling each question
- A nicely formatted spreadsheet of the entire contest and all entries

## HOW DID YOU HANDLE VAGUE OR UNCLEAR ANSWERS?

Everything was handled in an as permissive and kind a manner as I could, as I was working on this as an independent project prior to bringing it to Sean. This meant that I was operating under the idea that I had no authority to make judgement calls about throwing out entries/answers. Where entries had things mixed up (for example, GM's and coaches jumbled together), I sorted them out and corrected the entry. Where entries had poor formatting, I fixed them. Where entries had unclear answers, I attributed them to the most popular eligible selection (for example, "staal" became "m staal" and not "e staal" or "j staal"). Where entries had unusual answers (for example, picking a hart trophy candidate to be traded), I investigated and corrected where it was clear that this was not the entrant's intent. My position on all of this was to take the kindest and most permissive approach possible, and only be less so if I were given permission by DGB.

## WHAT'S LEFT TO DO?

I still need to generate an autograder script, which should be fairly simple to do. This will require some collaboration to determine what constitutes an ineligible answer (won't count as wrong, but won't count as right) and what constitutes a wrong answer. While I don't expect anyone to be reading this before I get this done, on the off chance that anyone is - please don't bother building this and providing it to me. At this point, I've done all of this myself and I'd like to finish it off myself as well. 

That said, I'm all for improvements to my existing script. Feel free to reach out via [Twitter at @HasekBowsToMe](https://twitter.com/hasekbowstome) if you have a question about your entry, or email at TownsendSignUp on Gmail if you have more broad questions or concerns. 

## ACKNOWLEDGEMENTS

Obviously the biggest thanks has to go to [Sean McIndoe](https://twitter.com/DownGoesBrown) for creating the contest. I was really tired of working on my schoolwork, and this was a nice little diversion for about two weeks. This was a fun little learning experience, even if I probably put way more time into it than I should have. 

[BeautifulSoup's Documentation Page](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), which I got to know quite a bit better than I had in the course of figuring out how to scrape a huuuuuuuge page for the data I needed.

[StackOverflow](https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class) for helping me use "class_" where outdated documentation for BeautifulSoup reflected using "class".

[StackOverflow](https://stackoverflow.com/questions/21997587/beautifulsoup-get-text-from-find-all) for helping me get the data out of my find_all.
