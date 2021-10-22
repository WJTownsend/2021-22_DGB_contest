from bs4 import BeautifulSoup
from bs4.element import TemplateString
import numpy as np
import pandas as pd


def entry_scraper(source_html):
    """Provided a string for a source html page (saved to disk, rather than queried
    from a site), this function scrapes contest entry comments by identifying comments
    which are 8+ lines long into a list of authors and comments. Returns two lists,
    one being the authors of each comment and the other being the comments. As an
    example, authors[14] wrote comments[14]. This function will check for duplicated 
    author names, and will update any duplicates by appending the index of their 
    comment to the author name. A list of duplicate authors will be printed as a 
    warning to the user.
    """
    # Pulling data from file, rather than requerying web page each attempt
    with open(source_html, 'r', encoding='utf8') as raw:
        # Read contents of web page
        contents = raw.read()
        # Make some soup out of those contents
        soup = BeautifulSoup(contents, "html.parser")
        # Pull only the comments from the entire HTML page
        comment_soup = soup.find(id="parent-comment-container")
        # Extract comment author names from the comments
        authors = [x.get_text()
                   for x in comment_soup.find_all(class_="comment-author-text")]
        # Extract comment text from the comments
        comments = [x.get_text().lstrip().lower()
                    for x in comment_soup(class_="comment-text-container")]
        print(f"This comment section has {len(authors)} authors")
        print(f"This comment section has {len(comments)} comments")
        # Before continuing, verify both lists are equal in length for joining
        # If not, script quits running
        if len(authors) != len(comments):
            print("List of Authors and List of Comments are not equal length")
            print("Something seems to be wrong, ending script")
            quit()
        # Remove comments that are not at least 8 lines long, by finding
        # Index of each failing case and placing them in a list to be handled
        filter_index = 0
        indexes_to_pop = []
        print("Searching for comments of less than 8 lines...")
        for comment in comments:
            new_lines = comment.count('\n')
            if new_lines < 8:
                indexes_to_pop.append(filter_index)
            filter_index += 1
        # Notify how many comments are to be removed
        print(f"{len(indexes_to_pop)} comments found with less than 8 lines.")
        print("Removing those comments...")
        # Reverse list of indexes, so we pop from the back, not the front
        # This avoids moving the list's indexes as we're removing items
        indexes_to_pop.reverse()
        # Iterate through list to pop, and remove corresponding items
        # From both comments and authors
        for pop_index in indexes_to_pop:
            comments.pop(pop_index)
            authors.pop(pop_index)
        # Check for duplicate authors, to avoid overwriting any authors w same name
        # If duplicate author name exists, rename the author
        temp_index = 0
        duped_authors = []
        for author in authors:
            if authors.count(author) > 1:
                duped_authors.append(author)
                mod_author = author + " entry # " + str(temp_index)
                authors[temp_index] = mod_author
            elif author in duped_authors:
                mod_author = author + " entry # " + str(temp_index)
                authors[temp_index] = mod_author
            temp_index += 1
        # If duplicate authors exist, notify of such
        if len(duped_authors) > 0:
            print("NOTICE: Duplicated authors were found.")
            print("The following authors have been modified due to duplicates:")
            print(set(duped_authors))
        # Comment gathering is finished
        print("This is the end of comment gathering operations.")
        print(f"A total of {len(authors)} authors have been pulled.")
        print(f"These authors made {len(comments)} comments in this set.")
        return authors, comments


def comment_fixer(authors, comments):
    """ Because of a lack of standardization regarding formatting of answers, 
    contest entries have a wide variety of formats, and many answers are very
    poorly or inconsistently formatted, preventing automated handling with a
    script. Given the list of authors and the associated list of comments, 
    this function has been customized to edit comments that were not able to
    be handled programmatically, so that they may be handled in such fashion.
    Returns a modified list of authors and a modified list of comments, and 
    a count of how many comments required "major surgery".

    Note that this function will have to be re-written and customized for
    future prediction contests. This is one of the most time-intensive parts
    of generating this program.  
    """
    major_surgery_count = 0
    # Many entries are poorly formatted and done in such a way that trying
    # to identify them through an if/then will end up negatively impacting other entries
    # These readers' entries must be manually edited, and their names cursed for all time
    print("Manually editing certain comments to fix issues that otherwise cannot be filtered...")
    # Julian M dropped extra line breaks in answers, I'll have to rewrite the entry
    print("Julian M, I fixed your entry")
    major_surgery_count += 1
    comments[73] = "1. veg, col, nyi, tbl, tor\n2. buf, ari, ana, sjs, cbj\n3. cooper, brind'amour, quenneville, trotz, smith\n4. lamoriello, francis, yzerman, guerin, brisebois\n5. demko, vasilevskiy, lehner, markstrom, hellebuyck\n6. caufield, seider, zegras, knight, byram\n7. fox, makar, hedman, ekblad\n8. mcdavid, mackinnon, hellebuyck, makar, pettersson\n9. eichel, kessel, rakell, korpisalo, juolevi\n10. 0"
    # Philipp R. had commentary before his entry which was interpreted as an answer.
    # Cutting out the front of his entry to start at his answers.
    print("Philipp R, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[135]
    temp_comment = temp_comment[134:]
    comments[135] = temp_comment
    # Michael L had extra line breaks in his entry, which messed up reading it by line
    print("Michael L, I fixed your entry")
    major_surgery_count += 1
    comments[149] = "1. tbl, fla, nyi, veg, col\n2. buf, ott, cbj, ana, det\n3. cooper, trotz, quenneville, cassidy, maurice\n4. brisebois, sakic, lamoriello, sweeney, mclellan\n5. hart, lehner, shesterkin, vasilevskiy, hellebuyck\n6. caufield, seider, pinto, knight, zegras\n7. hedman, heiskanen, makar, fox, mcavoy\n8. mcdavid, mackinnon, matthews, kucherov, panarin\n9. eichel, gaudreau, kessel\n10. draisaitl"
    # Evan L got his questions mixed up and listed GM's for question 3 (not coaches)
    # and listed coaches for question 4 instead of GM's. I'll be generous and fix it.
    print("Evan L, I saved your entry!")
    major_surgery_count += 1
    print("You swapped Q3 & Q4 and I fixed it for you.")
    print("I can't help you with the fact that you specifically picked Bill Armstrong, though")
    comments[170] = "1. col, tor, veg, tbl, fla\n2. buf, ari, det, ana, cbj\n3. cooper, keefe, quenneville, brind'amour, trotz\n4. yzerman, brisebois, dorion, guerin, b armstrong\n5. vasilevskiy, kuemper, lehner, gibson, hellebuyck\n6. zegras, knight, nedeljkovic\n7. makar, hedman, ekblad, hamilton\n8. crosby, matthews, mcdavid, mackinnon, hellebuyck\n9. dermott, beagle, galchenyuk, hertl\n10. mackinnon"
    # Mitch G used spaces as his separator for only the first two lines of his entry
    # Cannot use spaces without inadvertently handling other non-answer first lines
    print("Mitch G, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[174]
    temp_comment = temp_comment.replace(
        "1. tbl car vgk col bos", "1. tbl, car, veg, col, bos")
    temp_comment = temp_comment.replace(
        "2. buf ott sjs cbj det", "2. buf, ott, sjs, cbj, det")
    comments[174] = temp_comment
    # Rick C used periods as his separator for the entire entry. Cannot use periods
    # without inadvertently handling other non-answer first lines
    print("Rick C, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[218]
    temp_comment = temp_comment.replace(".", ",")
    comments[218] = temp_comment
    # Shahzaib Hassain I. included a bunch of new lines in his entry
    # I need each answer on a line, not straddling two
    print("Shahzaib Hassain I., I fixed your entry")
    comments[229] = "1. tbl, col, veg, tor, edm\n2. buf, det, ari, cbj, ana\n3. trotz, cooper, ducharme, brind'amour, gallant\n4. yerman, sakic, brisebois, guerin, zito\n5. saros, gibson, hellebuyck, vasilevskiy\n6. caufield, knight, zegras\n7. hedman, makar, fox, mcavoy, q hughes\n8. mcdavid, matthews, mackinnon, kucherov, draisaitl\n9. forsberg, giroux, domi, hertl, kessel\n10. draisaitl"
    # Ryan L used both "-" and "," in his entry, I will replace the leading "-"
    print("Ryan L, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[263]
    temp_comment = temp_comment.replace("-", "")
    comments[263] = temp_comment
    # Matthew K used spaces as his separator for the entire entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("Matthew K, I fixed your entry")
    major_surgery_count += 1
    comments[264] = "1. tbl, col, tor, nyi, fla\n2. buf, ott, ari, lak, det\n3. cooper, smith, cassidy, ducharme, bednar\n4. sweeney, brisebois, bergevin, zito, dubas\n5. vasilevskiy, fleury, hellebuyck, demko, bobrovsky, lehner\n6. raymond, raddysh, vilardi, kahkonen, cal foote\n7. hedman, fox, josi, carlson, mcavoy\n8. mcdavid, kucherov, mackinnon, vasilevskiy, draisaitl\n9.eichel, w nylander, ullmark, pk subban, byfield\n10. kucherov"
    # Joseph T used spaces as his separator for the entire entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("Joseph T, I fixed your entry")
    major_surgery_count += 1
    comments[266] = "1. tbl, tor, veg, col, edm\n2. buf, ari, det, ana, ott\n3. keefe, cooper, trotz, brind'amour, quenneville\n4. brisebois, yzerman, dorion, cheveldayoff, mccrimmon\n5. vasilevskiy, fleury, hellebuyck, binnington, saros\n6. caufield, seider\n7. makar, hamilton, hedman, mcavoy\n8. mcdavid, matthews, draisaitl, mackinnon\n9. kessel, stralman, eichel\n10. marner"
    # Danny D used spaces as his separator for half of his entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("Danny D, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[282]
    temp_comment = temp_comment[138:]
    temp_comment = "1. tbl, col, veg, nyi, tor\n2. buf, ari, det, sjs, ana\n3. cooper, trotz, brind'amour, quenneville, bednar\n" + temp_comment
    comments[282] = temp_comment
    # Alex K used spaces as his separator for the entire entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("Alex K, I fixed your entry")
    major_surgery_count += 1
    comments[306] = "1. col, veg, tor, fla, wpg\n2. det, buf, ana, ari, cbj\n3. trotz, cooper, brind'amour, quenneville, smith\n4. sakic, brisebois, mccrimmon, yzerman, blake\n5. vasilevskiy, grubauer, demko, hellebuyck, markstrom\n6. caufield, knight\n7. makar, mcavoy, fox\n8. mcdavid, matthews, mackinnon, barkov\n9. tarasenko, kessel, pk subban\n10. draisaitl"
    # Arthur M put extra line breaks in his entry, added extra '-', etc.
    print("Arthur M, I fixed your entry")
    major_surgery_count += 1
    comments[340] = "1. tbl, veg, nyi, col, edm\n2. ana, arz, buf, cbj, det\n3. cooper, trotz, brind'amour, quenneville, evason\n4. sakic, guerin, brisebois, yzerman, lamoriello\n5. hellebuyck, vasilevskiy, saros, lehner, fleury\n6. caufield, zegras\n7. makar, josi, hedman, mcavoy\n8. mcdavid, matthews, mackinnon, panarin, draisaitl\n9. eichel, kessel\n10. draisaitl"
    # Lewis D used spaces as his separator for the entire entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("Lewis D, I fixed your entry")
    major_surgery_count += 1
    comments[344] = "1. tbl, veg, col, bos, edm\n2. det, lak, buf, ott, ana\n3. cooper, trotz, deboer, bednar, cassidy\n4. brisebois, lamoriello, mccrimmon, sakic, sweeney\n5. hellebuyck, grubauer, vasilevskiy\n6. caufield, zegras\n7. hedman, makar, fox\n8. mcdavid, mackinnon, draisaitl, matthew, kane\n9. eichel, kessel\n10. mackinnon"
    # Rob B used a pile of '-' and ',' in his entry
    # I just have to rewrite the comment
    print("Rob B, I fixed your entry")
    major_surgery_count += 1
    comments[354] = "1. tbl, tor, fla, col, nyi\n2. buf, ari, ana, cbj, ott\n3. cooper, bednar, trotz, brind'amour, quenneville\n4. guerin, francis, yzerman, lamoriello, dubas\n5. vasilevskiy, lehner, hellebuyck, grubauer, kuemper\n6. bunting, rossi, byfield, zegras, caufield\n7. mcavoy, theodore, muzzin, makar, slavin\n8. mcdavid, matthews, mckinnon, kucherov, draisaitl\n9. eichel, hertl, c brown"
    # Curtis R used both "-" and "," in his entry, I will replace the leading "-"
    print("Curtis R, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[366]
    temp_comment = temp_comment.replace("-", "")
    comments[366] = temp_comment
    # Garret F uses periods and commas as separators in his entry,
    # I can't fix this without doing it manually, so here we go...
    print("Garret F, I fixed your entry")
    major_surgery_count += 1
    comments[390] = "1. col, veg, tbl, nyi\n2. buf, det, ari, ana\n3. cooper, trotz, brind'amour, sullivan\n4. sakic, yzerman, lamoriello, francis, brisebois\n5. vasilevskiy, saros, fleury, lehner\n6. caufield, newhook, rossi\n7. makar, fox, mcavoy, ekblad\n8. mcdavid, mackinnon, hellebuyck, crosby, makar\n9. kessel, forsberg"
    # Bernhard J started each line with "# - ", and the "-" got caught as a separator
    # for part of the answers. Removing "-" from entry
    print("Bernhard J, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[391]
    temp_comment = temp_comment.replace("-", "")
    comments[391] = temp_comment
    # Jeff C. randomly interspersed his entry with periods and commas and misnumbered the questions.
    # I can't fix this without doing it manually, so here we go...
    print("Jeff C, I fixed your entry")
    major_surgery_count += 1
    comments[392] = "1. tbl, col, veg, edm, tor\n2. buf, ari, ott, det, cbj\n3. trotz, cooper, cassidy, quenneville, brind'amour\n4. sakic, yzerman, francis, guerin, drury\n5. hellebuyck, saros, vasilevskiy, demko, markstrom\n6. caufield, zegras, swayman, seider\n7. hedman, fox, makar, hamilton, nurse\n8. mcdavid, draisaitl, mackinnon, kucherov, matthews\n9. eichel, tarasenko\n10. draisaitl"
    # James H used spaces as his separator for the entire entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("James H, I fixed your entry")
    major_surgery_count += 1
    print("INTERPRETATION WARNING: James H wrote in 'Brisbois Montreal GM Sweeney'")
    print("This was read as 'Montreal GM' (Bergevin) rather than George McPhee")
    comments[404] = "1. tbl, nyi, veg, col, pit\n2. det, buf, van, ari\n3. sullivan, trotz, cassidy\n4. brisebois, bergevin, sweeney\n5. hellebuyck, kuemper\n6. caufield\n7. hedman, makar\n8. mcdavid, crosby, matthews, mackinnon\n9. eichel"
    # Nick Z stopped using commas partway through his entry, only using spaces.
    # Can't filter for spaces effectively without causing other problems.
    print("Nick Z, I saved your entry")
    major_surgery_count += 1
    print("INTERPRETATION WARNING: Nick Z selected 'armstrong' as a GM")
    print("This was read as 'd armstrong' (eligible) instead of 'b armstrong' (ineligible)")
    comments[451] = "1. edm, tbl, col, fla, bos\n2. buf, det, ott, ana, sjs\n3. cooper, maurice, quenneville, brind'amour, trotz\n4. holland, d armstrong, mcphee, sakic, sweeney\n5. hellebuyck, vasilevskiy, peterson, demko, gibson\n6. newhook, podkolzin, zegras, caufield\n7. nurse, fox, makar, doughty, pietrangelo\n8. mcdavid, draisaitl, mackinnon, kucherov\n9. eichel, lebanc, bjork, m staal\n10. draisaitl"
    # Michael F. had commentary before his entry which was interpreted as an answer.
    # Cutting out the front of his entry to start at his answers.
    print("Michael F, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[455]
    temp_comment = temp_comment[41:]
    comments[455] = temp_comment
    # Félix F. entered his label ahead of his entry, and used a "-" to do
    # which got read as part of an answer
    print("Félix F., I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[461]
    temp_comment = temp_comment[10:]
    comments[461] = temp_comment
    # Jonathan Willis had commentary before his entry which was interpreted as an answer.
    # Cutting out the front of his entry to start at his answers.
    print("Jonathan Willis, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[511]
    temp_comment = temp_comment[152:]
    comments[511] = temp_comment
    # Kevin J used spaces as his separator for only the first two lines of his entry
    # Cannot use spaces without inadvertently handling other non-answer first lines
    print("Kevin J, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[526]
    temp_comment = temp_comment.replace(
        "1. tor vgk col car tbl", "1. tor, veg, col, car, tbl")
    temp_comment = temp_comment.replace(
        "2. det buf cbj ari ott", "2. det, buf, cbj, ari, ott")
    comments[526] = temp_comment
    # Александр started each line with "# - ", and the "-" got caught as a separator
    # for part of the answers. Removing "-" from entry
    print("Александр, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[535]
    temp_comment = temp_comment.replace("-", "")
    comments[535] = temp_comment
    # Craig C started each line with "# - ", and the "-" got caught as a separator
    # for part of the answers. Removing "-" from entry
    print("Craig C, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[542]
    temp_comment = temp_comment.replace("-", "")
    comments[542] = temp_comment
    # Taylor R used spaces as his separator for the entire entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("Taylor R, I fixed your entry")
    major_surgery_count += 1
    comments[583] = "1. nyi, col, veg, tbl, car\n2. buf, cbj, det, ari, ana\n3. cooper, brind'amour, trotz, quenneville, deboer\n4. lamoriello, yzerman, cheveldayoff, blake, sakic\n5. hellebuyck, fleury, kuemper, vasilevskiy, lehner\n6. caufield, knight, zegras, nedeljkovic, drysdale\n7. hedman, pietrangelo, fox, makar, hamilton\n8. mcdavid, mackinnon, vasilevskiy, matthews, stone\n9. hertl, korpisalo, forsberg, carter, leddy\n10. draisaitl"
    # David S. started each line with "# - ", and the "-" got caught as a separator
    # for part of the answers. Removing "-" from entry
    print("David S, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[600]
    temp_comment = temp_comment.replace("-", "")
    comments[600] = temp_comment
    # Drew D used spaces as his separator for the entire entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("Drew D, I fixed your entry")
    major_surgery_count += 1
    comments[605] = "1. tbl, col, veg, tor, car\n2. buf, ari, ana, det, ott\n3. cooper, trotz, hakstol, deboer, bednar\n4. b armstrong, d armstrong, mccrimmon, sakic, waddell\n5. binnington, lehner, hellebuyck, gibson, demko\n6. caufield\n7. pietrangelo, fox, makar\n8. mcdavid, kucherov, mackinnon, crosby\n9. eichel, tarasenko\n10. kucherov"
    # MIKE R included extra line breaks in an answer, which didn't play nice with
    # my line by line iteration
    print("MIKE R, I fixed your entry")
    major_surgery_count += 1
    comments[622] = "1. nyi, tbl, col, veg\n2. buf, ari, sjs, cbj\n3. trot, quenneville, cooper, bednar\n4. lamoriello, yzerman, sakic, brisebois\n5. vasilevskiy, hellebuyck, gibson\n6. caufield, knight, zegras, seider\n7. makar, fox, hedman\n8. mcdavid, matthews, mackinnon\n9. leddy, tierney, hertl\n10. mackinnon"
    # Kevin D included extra line breaks in questions, breaks the automatic handling of successive lines
    print("Kevin D, I fixed your entry")
    major_surgery_count += 1
    comments[649] = "1. col, veg, tbl, tor, nyi\n2. ari, buf, ana\n3. cooper, bednar, trotz, cassidy\n4. doug armstrong, yzerman, sakic, sweeney, lamoriello\n5. binnington, vasilevskiy, hellebuyck, saros\n6. caufield, zegras\n7. pietrangelo, fox, makar, hedman\n8. mcdavid, mackinnon, matthews, draisaitl\n9. eichel, hertl\n10. draisaitl"
    # Andy D. had commentary before his entry which was interpreted as an answer.
    # Cutting out the front of his entry to start at his answers.
    print("Andy D, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[666]
    temp_comment = temp_comment[17:]
    comments[666] = temp_comment
    # Levi T has 2 coaches, 3 GMs in Q2, and 3 GMs 2 coaches in Q3
    # I feel merciful (and don't have permission to start scrapping people's answers)
    # So I'll swap them around (the sixth GM will get picked up by the cheat filter)
    print("Levi T, I saved your entry!")
    major_surgery_count += 1
    print("I can't change the fact that you picked an ineligible GM though")
    comments[679] = "1. tbl, fla, col, veg, bos\n2. det, ari, buf, ana, lak\n3. cooper, keefe, quenneville, deboer\n4. zito, yzerman, mccrimmon, sakic, brisebois, dubas\n5. binnington, hellebuyck, gibson, vasilevskiy, lehner\n6. caufield, zegras, newhook\n7. makar, hedman, mcavoy, fox\n8. mcdavid, matthews, barkov, hellebuyck\n9. eichel, tarasenko, kessel, holtby, mikheyev\n10. mackinnon"
    # James S. used a "-" while tagging at the start of his entry, which got read as an
    # Answer. Cutting out the front of his entry to start at his answers.
    print("James S, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[719]
    temp_comment = temp_comment[5:]
    comments[719] = temp_comment
    # Jack F used spaces as his separator for half of his entry, cannot use spaces
    # without inadvertently causing a whoooole bunch of other problems
    print("Jack F, I fixed your entry")
    major_surgery_count += 1
    comments[728] = "1. tbl, col, veg\n2. buf, det, ari, sjs, cbj\n3. cooper, trotz\n4. brisebois, sakic, yzerman\n5. vasilevskiy, fleury, hellebuyck\n6. caufield, seider, knight\n7. hedman, makar, fox, hamilton\n8. mcdavid, kucherov, pastrnak, matthews\n9. eichel, hertl, kessel"
    # Kyle A included a comment before his entry that got interpreted as
    # his answer to question 1
    print("Kyle A, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[778]
    temp_comment = temp_comment[27:]
    comments[778] = temp_comment
    # Jeff N. used a "-" in his first line which got read as an answer, fixing this
    print("Jeff N, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[784]
    temp_comment = temp_comment[13:]
    comments[784] = temp_comment
    # Brian L. used "1.)" instead of one or the other. He also has a bunch of periods for first initials.
    # Replacing all "." with "" in his entry
    print("Brian L, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[858]
    temp_comment = temp_comment.replace(".", "")
    comments[858] = temp_comment
    # Bill E had extra periods, commas, and line breaks in his entry
    # I could fix the other stuff, but I can't fix the line breaks easily
    print("Bill E, I fixed your entry")
    major_surgery_count += 1
    comments[864] = "1. tbl, col, veg, fla, tor\n2. buf, cbj, ana, det, ari\n3. brind'amour, cooper, trotz, quenneville, bednar\n4. guerin, yzerman\n5. vasilevskiy, hellebuyck, shesterkin\n6. caufield, zegras, newhook\n7. makar, fox, q hughes\n8. mcdavid, mackinnon, matthews, kucherov, point\n9. tarasenko, hertl\n10. draisaitl"
    # Tyler V. used "1.)" instead of one or the other.
    # Replacing all ")" with "" in his entry
    print("Tyler V, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[869]
    temp_comment = temp_comment.replace(")", "")
    comments[869] = temp_comment
    # James L entered every single answer on a new line and did not follow the rules.
    # I will be generous and fix his entry.
    print("James L, I saved your entry. Next time, read the rules.")
    major_surgery_count += 1
    comments[899] = "1. col, tor, tbl, veg\n2. ari, buf, det\n3. trotz, cooper, bednar\n4. sakic, yzerman, blake, brisebois\n5. vasilevskiy, hellebuyck, talbot\n6. caufield\n7. makar, hedman, fox, heiskanen\n8. mcdavid, draisaitl, mackinnon, barkov, vasilevskiy\n9. tarasenko, eichel"
    # Josh P used spaces as his separator for the entire entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("Josh P, I fixed your entry")
    major_surgery_count += 1
    print("INTERPRETATION WARNING: Josh P selected 'armstrong' as a GM")
    print("This was read as 'd armstrong' (eligible) instead of 'b armstrong' (ineligible)")
    comments[941] = "1. tbl, col, tor, veg, nyi\n2. buf, ott, det, ana, ari\n3. cooper, bednar, keefe, trotz, brind'amour\n4. yzerman, brisebois, sakic, d armstrong, waddell\n5. hellebuyck, vasilevskiy, gibson, lehner, saros\n6. podkolzin, caufield, zegras\n7. hedman, makar, hamilton, mcavoy, theodore\n8. matthews, mcdavid, mackinnon, barkov, stone\n9. glendening\n 10. draisaitl"
    # Cal G stopped using commas and used "and" partway through the questions, I'm just gonna
    # Rewrite the entry in a usable format
    print("Cal G, I fixed your entry")
    major_surgery_count += 1
    comments[1010] = "1. col, veg, tbl, tor, nyi\n2. buf, cbj, ari, ana, ott\n3. cooper, quenneville, maurice, evason, cassidy\n4. mccrimmon, yzerman, brisebois, guerin, francis\n5. vasilevskiy, lehner, fleury, hellebuyck, binnington\n6. caufield, seider, zegras\n7. makar, hedman, theodore\n8. mcdavid, crosby, mackinnon, stone, point\n9. hertl, rakell, kessel, fleury, ekholm\n"
    # R W. didn't follow the rules and copied the entire question into his answers
    # I will be generous and fix his entry
    print("R W. I saved your entry. Next time, read the rules.")
    major_surgery_count += 1
    comments[1020] = "1. tor, nyi, fla, veg, col\n2. buf, sea, det, ari\n3. trotz, cooper, keefe\n4. sakic, yzerman, lamoriello\n5. hellebuyck, vasilevskiy, bobrovsky\n6. sillinger, caufield, zegras\n7. werenski, fox, makar, ekblad \n8. mcdavid, matthews, barkov\n9. eichel, domi, tarasenko\n10. marner"
    # Jeffrey M stopped using commas and used "and" partway through the questions, and had
    # numerous illegible answers, entering this one by hand
    print("Jeffrey M, I fixed your entry")
    major_surgery_count += 1
    print("INTERPRETATION WARNING: Jeffrey M listed coach 'bed are' norris trophy 'herman', and traded player 'jessel'")
    print("These were interpreted as 'bednar', 'hamilton', and 'kessel'")
    print("You were thiiiiiis close to getting noah juulsen instead of kessel because I was looking at names starting with j")
    comments[1032] = "1. tbl, col, veg, edm, wpg\n2. buf, ari, cbj, det, ana\n3. bednar, cooper, quenneville, trotz, tippett\n4. yzerman, sakic, mccrimmon, cheveldayoff, brisebois\n5. vasilevskiy, hellebuyck, saros, markstrom, kuemper\n6. zegras, caufield\n7. makar, hamilton, theodore\n8. mcdavid, mackinnon, barkov, kucherov\n9. kessel, eichel\n10. draisaitl"
    # Sean McIndoe entered a bunch of commentary before his entry, which got interpreted
    # as an answer. Fixing your answer, Sean!
    print("Down Goes Brown, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[1046]
    temp_comment = temp_comment[120:]
    comments[1046] = temp_comment
    # Cole R used both "-" and "," in his entry, I will replace the leading "-"
    print("Cole R, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[1048]
    temp_comment = temp_comment.replace("-", "")
    comments[1048] = temp_comment
    # Gordon C used spaces as his separator for the entire entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("Gordon C, I fixed your entry")
    major_surgery_count += 1
    comments[1052] = "1. col, veg, fla, tgl, nyi\n2. buf, det, ari, sjs, ana\n3. quenneville, cooper, trotz, brind'amour, bednar\n4. brisebois, sakic, yzerman, zito, lamoriello\n5. lehner, vasilevskiy, hellebuyck, demko, saros\n6. caufield, seider, a kaliyev, knight, rossi\n7. makar, fox, hedman, hamilton, theodore\n8. mcdavid, matthews, mckinnon, draisaitl, barkov\n9. kessel, hertl, palat, manson, pavelski\n10. draisaitl"
    # Ellay H started each line with "# - ", and the "-" got caught as a separator
    # for part of the answers. Removing "-" from entry
    print("Ellay H, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[1127]
    temp_comment = temp_comment.replace("-", "")
    comments[1127] = temp_comment
    # John G. used periods off and on throughout his entry, along with comma separators.
    # Cannot filter through this as his separator for the entire entry. I'll just rewrite it.
    print("John G, I fixed your entry")
    major_surgery_count += 1
    print("INTERPRETATION WARNING: John G selected 'armstrong' as a GM")
    print("I chose 'd armstrong' (eligible) instead of 'b armstrong' (inelgible)")
    comments[1143] = "1. col, veg, fla, tor, nyi\n2. buf, ari, cbj, ana, det\n3. cooper, quenneville, trotz, brind'amour, berube\n4. brisebois, zito, lamoriello, waddell, d armstrong\n5. saros, hellebuyck, demko, markstrom, kuemper\n6. caufield, zegras, seider, newhook\n7. makar, hughes, theodore. fox\n8. mcdavid, matthews, point, mackinnon\n9. borowiecki, leddy, c miller, crouse, edler"
    # Daryl H used both ")" and "." after his numbers, I'll replace the ")" with ""
    print("Daryl H, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[1148]
    temp_comment = temp_comment.replace(")", "")
    comments[1148] = temp_comment
    # Jesse H used a pile of commas and semicolons to identify all of his players and teams
    # I just have to rewrite the whole comment
    print("Jesse H, I fixed your entry")
    major_surgery_count += 1
    comments[1171] = "1. tbl, fla, veg, col, tor\n2. buf, ana, ari, sjs, det\n3. cooper,\n4. yzerman, brisebois, sakic, kekalainen, lamoriello\n5. gibson, hellebuyck, markstrom, kuemper, lehner\n6. caufield, zegras, knight\n7. makar, fox, mcavoy, hamilton, theodore\n8. mcdavid, mackinnon, marchand, barkov, matthews\n9. eichel, kessel, hertl\n10. draisaitl"
    # Bradley P somehow had tabs inserted into the start of his answers. He also wrote numbers like
    # "1.)" rather than using one or the other
    print("Bradley P, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[1214]
    temp_comment = temp_comment.replace("\t", "")
    temp_comment = temp_comment.replace(")", "")
    comments[1214] = temp_comment
    # David F used both "-" and "," in his entry, I will replace the leading "-"
    print("David F, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[1227]
    temp_comment = temp_comment.replace("-", "")
    comments[1227] = temp_comment
    # Steven B skipped a question and put a bunch of stuff in the wrong slots
    # I just gotta write this one out manually
    print("Steven B, I fixed your entry")
    major_surgery_count += 1
    comments[1261] = "1. tbl, nyi, tor, wsh, col\n2. det, buf, ari, ott, sjs\n3. cooper, quenneville, trotz, laviolette, deboer\n4. yzerman, waddell, sakic, guerin, blake\n5. vasilevskiy, hellebuyck\n6. 0 \n7. makar, hedman, carlson\n8. mcdavid, mackinnon, draisaitl\n9. gaudreau, eichel, kessel"
    # Nick D used both "-" and "," in his entry, I will replace the leading "-"
    print("Nick D, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[1271]
    temp_comment = temp_comment.replace("-", "")
    comments[1271] = temp_comment
    # Matt B made two entries in one comment, one for him and one for his dad
    # I'm inclined to not allow this, but it's ultimately DGB's call. I'll generate them for now.
    print("Matt B, I fixed your entry (and your dad's)")
    major_surgery_count += 1
    comments[1282] = "1. col, veg, tbl, tor, car\n2. njd, ana, sjs, buf, ari\n3. cooper, bednar, keefe, brind'amour, cassidy\n4. brisebois, sweeney, mccrimmon, dubas, lamoriello\n5. vasilevskiy, hellebuyck, gibson, lehner, fleury\n6. caufield, zegras, seider, raymond, drysdale\n7. fox, hedman, makar, hamilton, mcavoy\n8. panarin, mcdavid, mackinnon, kucherov, draisaitl\n10. kucherov"
    matts_dad = "Matt B entry # 1282's dad"
    authors.append(matts_dad)
    major_surgery_count += 1
    matts_dad_entry = "1. col, veg, tor, wsh, nyi\n2. buf, ott, det, njd, ari\n3. trotz, cassidy, bednar, cooper, maurice\n4. sweeney, poile, dubas, murray, blake\n5. shesterkin, hart, vasilevskiy, binnington, hellebuyck\n6. caufield, zegras, knight, seider, byfield\n7. jones, fox, makar, mcavoy, burns\n8. matthews, mcdavid, draisaitl, panarin, ovechkin\n9. gaudreau, kessel, tarasenko, koskinen, shattenkirk\n10. draisaitl"
    comments.append(matts_dad_entry)
    # Taralynn D. used both spaces and periods as separators, cannot use spaces without causing
    # lots of other problems, I'm fixing it
    print("Taralynn D, I fixed your entry")
    major_surgery_count += 1
    comments[1316] = "tbl, col, veg, tor, nyi\n2. buf, ari, ana, det, cbj\n3. cooper, brind'amour, smith, quenneville, hakstol\n4. brisebois, francis, dorion, sakic, blake\n5. vasilevskiy, hellebuyck, saros, markstrom, demko\n6. caufield, zegras, knight, seider, drysdale\n7. hedman, fox, makar, hamilton, mcavoy\n8. mcdavid, mackinnon, matthews, barkov, draisaitl\n9. eichel, roussel, c miller, manson, stetcher\n10. draisaitl"
    # Scott D had multiple lines of commentary before his entry
    print("Scott D, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[1335]
    temp_comment = temp_comment[66:]
    comments[1335] = temp_comment
    # Nav S used periods as the separator for the entire entry, cannot use periods
    # without inadvertently causing some other problems
    print("Nav S, I fixed your entry")
    major_surgery_count += 1
    comments[1348] = "1. car, col, tbl, tor, veg\n2. ana, ari, buf, det, ott\n3. brind'amour, cooper, trotz, evason, keefe\n4. francis, yzerman, brisebois, lamoriello, blake\n5. demko, vasilevskiy, hellebuyck, saros, markstrom\n6. caufield, knight, zegras, byram\n7. makar, hedman, fox, ekblad, slavin\n8. mcdavid, matthews, draisaitl, mackinnon\n9. eichel, hertl, c miller, m staal, leddy"
    # JEFFREY R made only one pick per question, which I can't work around, so
    # I'll fix his entry for him
    print("JEFFREY R, I fixed your entry")
    major_surgery_count += 1
    comments[1366] = "1. veg, \n2. buf,\n3. trotz,\n4. sakic,\n5. hellebuyck,\n6. zegras,\n7. makar,\n8. mcdavid,\n9. rakell,"
    # Andrew James L. used spaces and commas as separators throughout his entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("Andrew James L., I fixed your entry")
    major_surgery_count += 1
    comments[1389] = "1. col, tbl, vgk, tor, min\n2. buf, ana, cbj, det, ari\n3. cooper, trotz, maurice, keefe, brind'amour\n4. brisebois, guerin, yzerman, d armstrong\n5. hellebuyck, vasilevskiy, markstrom, saros\n6. caufield, zegras, seider\n7. makar, hedman, mcavoy, fox, weegar\n8. mcdavid, matthews, mackinnon, kucherov, marchand\n9. kessel\n10. rantanen"
    # George K started each line with "# - ", and the "-" got caught as a separator
    # for part of the answers. Removing "-" from entry
    print("George K, I fixed your entry")
    major_surgery_count += 1
    temp_comment = comments[1432]
    temp_comment = temp_comment.replace("-", "")
    comments[1432] = temp_comment
    # Christopher B added comments before his entry.
    print("Christopher B, I fixed your entry")
    major_surgery_count += 1
    comments[1462] = "1. tbl, col, veg, fla, car\n2. buf, ana, det, ari, sjs\n3. cooper, deboer, trotz, quenneville, brind'amour\n4. yzerman, maclellan, sakic, blake, lamoriello\n5. hellebuyck, vasilevskiy, saros, kuemper, gibson\n6. caufield, knight, zegras, seider, krebs\n7. makar, fox, hedman, pietrangelo, hughes\n8. mcdavid, mackinnon, draisaitl, crosby, pastrnak\n9. kessel, nyquist, henrique, leddy, zucker\n10. draisaitl"
    # Phil G used spaces as his separator for the entire entry, cannot use spaces
    # without inadvertently causing a whooooooole bunch of other problems
    print("Phil G, I fixed your entry")
    major_surgery_count += 1
    comments[1495] = "1. tbl, tor, col, veg\n2. ott, det, buf, ari, ana\n3. brind'amour, trotz, cooper, maurice\n4. francis, sakic, brisebois, yzerman, blake\n5. vasilevskiy, hellebuyck, demko\n6. zegras, caufield, knight\n7. makar, mcavoy, hamilton\n8. mcdavid, mackinnon, kucherov, matthews\n9. kessel, hertl, forsberg, eichel\n10. matthews"
    # Elliott W made only one pick per question, which I can't work around, so
    # I'll fix his entry for him
    print("Elliott W, I fixed your entry")
    major_surgery_count += 1
    comments[1552] = "1. nyi,\n2. buf,\n3. cooper,\n4. yzerman,\n5. vasilevskiy,\n6. byram,\n7. fox,\n8. matthews,\n9. kessel,\n10. marner "
    print("All 'major surgery' operations performed on comments")
    print(f"{major_surgery_count} comments had to be handled in this fashion.")
    print("All comments are now ready to be programmatically handled as contest entries.")
    return major_surgery_count, authors, comments


def generate_dataframe(authors, comments):
    """ This function takes a list of authors and a corresponding and
    equal list of comments and generates a dataframe from the two. Each
    line consists of the author (e.g. author[42]) and the 46 potential
    answers provided by that author (e.g. comment[42]). This is done by 
    splitting each comment into lines and reading through them to find
    the first "answer" line (some entries are preceded by non-answers), 
    and iterating through the lines to generate all 46 answers to 10
    questions. Returns a dataframe with each contest entry on a row.
    This function will print out lots of information about its handling
    of each new index, including certain edge cases that apply.

    Note that this function includes numerous special-case handling 
    operations, due to a *wide* variety of entry formats in the absence
    of an enforced standard. This function may be rewritten with an 
    enforced formatting standard, which may also dramatically reduce
    the number of entries needing manual intervention. 
    """
    # Generate a dataframe, which we'll add the answers to
    col_names = ['author', 'q1a1', 'q1a2', 'q1a3', 'q1a4', 'q1a5', 'q2a1', 'q2a2', 'q2a3', 'q2a4', 'q2a5', 'q3a1', 'q3a2', 'q3a3', 'q3a4', 'q3a5', 'q4a1', 'q4a2', 'q4a3', 'q4a4', 'q4a5', 'q5a1', 'q5a2', 'q5a3', 'q5a4',
                 'q5a5', 'q6a1', 'q6a2', 'q6a3', 'q6a4', 'q6a5', 'q7a1', 'q7a2', 'q7a3', 'q7a4', 'q7a5', 'q8a1', 'q8a2', 'q8a3', 'q8a4', 'q8a5', 'q9a1', 'q9a2', 'q9a3', 'q9a4', 'q9a5', 'q10a1']
    df = pd.DataFrame(columns=col_names)
    # Iterate through the lists of authors and corresponding comments, together:
    for i in range(len(authors)):
        print(f"Handling index {i}, author: {authors[i]}...")
        # Start list with author name, list to eventually be placed in dataframe
        this_entry = [authors[i]]
        # Track which question we're on for specific filtering operations
        question_line = 0
        # Handling x author, handle x comment as well, and split that comment
        # into lines to be processed one at a time
        for line in comments[i].splitlines():
            # If stripped line is empty, skip to next line
            if not line.strip():
                continue
            # A handful of people used '&' instead of ',', replace those
            if "&" in line:
                line = line.replace("&", ",")
            # Another handful of people used ';' instead of ',', replace those
            if ";" in line:
                line = line.replace(";", ",")
            # Special situation - "marc-andre fleury" messes up replacing '-' with ','
            # Also have to account for 'andré', and for "fluery", apparently
            # Also apparently have to account for hypenation between "andre" and "fleury", I guess
            # Also apparently have to account for "marc-andre f", I guess
            # Also apparently have to account for "marc andre-flurry" too, I guess
            # Also apparently have to account for "andre-fleury" too, I guess
            # Also apparently have to account for "m-a fleury" too, I guess
            # Also apparently have to account for "marc andre-feury" too, I guess
            # If Flower retires, that'd be convenient...
            if "marc-andre fleury" in line:
                line = line.replace("marc-andre fleury", "fleury")
            if "marc-andré fleury" in line:
                line = line.replace("marc-andré fleury", "fleury")
            if "marc-andre fluery" in line:
                line = line.replace("marc-andre fluery", "fleury")
            if "marc-andré fluery" in line:
                line = line.replace("marc-andré fluery", "fleury")
            if "marc andre-fleury" in line:
                line = line.replace("marc andre-fleury", "fleury")
            if "marc andré-fleury" in line:
                line = line.replace("marc andré-fleury", "fleury")
            if "marc andre-fluery" in line:
                line = line.replace("marc andre-fluery", "fleury")
            if "marc andré-fluery" in line:
                line = line.replace("marc andré-fluery", "fleury")
            if "marc andre-feury" in line:
                line = line.replace("marc andre-feury", "fleury")
            if "marc-andre f" in line:
                line = line.replace("marc-andre f", "fleury")
            if "marc andré-f" in line:
                line = line.replace("marc andré-f", "fleury")
            if "marc andre-flurry" in line:
                line = line.replace("marc andre-flurry", "fleury")
            if "andre-fleury" in line:
                line = line.replace("andre-fleury", "fleury")
            if "m-a fleury" in line:
                line = line.replace("m-a fleury", "fleury")
            # Yet another handful of people used '-' instead of ',', replace those
            if "-" in line:
                line = line.replace("-", ",")
            # And yet more people used '/' instead of ',', replace those
            if "/" in line:
                line = line.replace("/", ",")
            # If we aren't in the middle of question lines AND no commas
            # are present, skip to next line
            if (question_line == 0) and (line.find(",") == -1):
                continue
            # If we haven't failed out, this line is an answer to a question
            # Increment the question counter to reflect active question
            question_line += 1
            # Now that we know we're in the answers, substitute " and " that people
            # included in their answers. Including spaces saves names like "andy", "andrei", etc.
            # Replacing " and " done with an oxford comma (good grammar!)
            if ", and " in line:
                line = line.replace(", and ", ", ")
            # Replacing " and " done without an oxford comma, if it wasn't already replaced above
            if " and " in line:
                line = line.replace(" and ", ",")
            # Someone managed to insert a "hard" space in their entry instead of a normal space
            # Turning any hard space encountered into a normal space
            if "\xa0" in line:
                line = line.replace("\xa0", " ")
            # Some people added lines to the bottom of their entry, if we're in
            # these lines, get out!
            if question_line > 10:
                continue
            # If line starts with "10", then slice off first 3 characters
            if line.startswith("10"):
                line = line[3:]
            # If line starts with "bonus" instead of "10" (some people did this)
            # Then slice off the first 6 characters
            if line.startswith("bonus"):
                line = line[6:]
            # Placed this check into a try block because some people wrote in Q10
            # but left it blank, causing a crash
            try:
                # If line starts off with a digit (and wasn't already identified as
                # '10'), then slice off first 2 characters
                if line[0].isdigit():
                    line = line[2:]
            except:
                print(
                    "NOTIFICATION: line appears blank, cannot slice index 0")
                print(
                    f"Please check index {i} by author {authors[i]} to verify this behavior")
            # Remove any trailing/leading spaces
            line = line.strip()
            # Edge case: If line ends with comma, remove it to prevent creating
            # additional list elements that are empty (I did this)
            if line.endswith(","):
                line = line[:-1]
            # Edge case: If line ends with period, remove it so I don't have to fix it later
            if line.endswith("."):
                line = line[:-1]
            # Split the line into its constituent answers, by comma
            answers = line.split(",")
            # Make sure line does not have more than five answers
            # If so, take only their first 5 answers and snitch on them
            if len(answers) > 5:
                print(
                    f"SNITCHING: {this_entry[0]} on entry {i} had more than 5 entries in question {question_line}!")
                print("Only taking their first 5 answers for this question")
                answers = answers[0:5]
            # If we are not on question # 10 (only 1 possible answer), then
            # check if there aren't 5 answers in the line, and if there are not,
            # pad it out to contain 5 answers with NaN values
            if question_line != 10:
                while len(answers) < 5:
                    answers.append(np.nan)
            # If we are on question 10 and for some reason you used a comma in your
            # entry (e.g. "nope, not trying"), take only first element of the list
            if question_line == 10 and len(answers) > 1:
                answers = answers[:1]
            # Now take the five answers and append each to this_entry list
            for answer in answers:
                # Some people's formatting led to white space inside list, strip it
                # Checking for type == string to avoid trying to strip NaNs and crashing
                if type(answer) == str:
                    answer = answer.strip()
                this_entry.append(answer)

        # Some people didn't include a line for Q10 if they didn't answer it
        # Check for if we've finished and are still on Q9
        # If so, add a NaN for Q10
        if question_line == 9:
            this_entry.append(np.nan)

        # With all answers now packaged in list with author, convert list
        # To Series, using df.column names as index
        entry_line = pd.Series(this_entry, index=df.columns)
        print("Appending entry to dataframe...")
        # Append the Series to the DF
        df = df.append(entry_line, ignore_index=True)
    # Notify that dataframe generation is complete
    print("**********DATAFRAME HAS BEEN GENERATED**********")
    print(f"This dataframe contains {df.shape[0]} lines!")
    return df


def dataframe_fixer(df):
    """ While some entries had formatting issues that prevented
    programmatic handling and required 'major surgery' as a
    result, many other entries required only minor corrections,
    again due to inconsistent formatting. A common example is 
    a period instead of a comma, which leads to two answers 
    lumped into a single location in the dataframe. This 
    function takes a dataframe, and returns a modified version
    of that dataframe, as well as a count of how many entries
    required such 'minor surgery'. 

    Again, this function was customized to correct these issues 
    and would have to be rewritten for subsequent contests. 
    """
    minor_surgery_count = 0
    # Luca D included multiple lines of commentary in his answer
    print("Luca D, I fixed your entry")
    minor_surgery_count += 1
    df.at[1, 'q8a4'] = np.nan
    df.at[1, 'q9a1'] = np.nan
    df.at[1, 'q9a2'] = np.nan
    df.at[1, 'q10a1'] = "giroux"
    # Emma G selected "bernard" as a coach
    print("Emma G, I fixed your entry")
    minor_surgery_count += 1
    print("INTERPRETATION WARNING: Emma G wrote in 'bernard' as one of her coaches")
    print("Not sure if this is Bednar (seems like an autocorrect) or Berube (same start of word)")
    print("Bednar is the more popular pick, so she gets Bednar")
    df.at[7, 'q3a4'] = "bednar"
    # Anthony F forgot a comma
    print("Anthony F, I fixed your entry")
    minor_surgery_count += 1
    df.at[16, 'q6a3'] = "rossi"
    df.at[16, 'q6a5'] = "newhook"
    # Brendan M dropped an extra period into one of his answers
    print("Brendan M, I fixed your entry")
    minor_surgery_count += 1
    df.at[24, 'q4a1'] = "sakic"
    df.at[24, 'q4a2'] = "dubas"
    # Brandon K dropped an extra period into two of his answers
    print("Brandon K, I fixed your entry")
    minor_surgery_count += 1
    df.at[31, 'q2a4'] = "ari"
    df.at[31, 'q2a5'] = "cbj"
    df.at[31, 'q3a1'] = "cooper"
    df.at[31, 'q3a5'] = "trotz"
    # David B had an explanation of picking ron francis
    print("David B, I fixed your entry")
    minor_surgery_count += 1
    df.at[36, 'q4a1'] = "francis"
    # Brant G. tagged each line with a prompt ("playoffs:", etc., along with some commentary)
    print("Brant G, I fixed your entry")
    minor_surgery_count += 1
    df.at[45, "q1a1"] = "tbl"
    df.at[45, "q1a5"] = "car"
    df.at[45, "q2a1"] = "ari"
    df.at[45, "q3a1"] = "trotz"
    df.at[45, "q4a1"] = "waddell"
    df.at[45, "q5a1"] = "vasilevskiy"
    df.at[45, "q6a1"] = "caufield"
    df.at[45, "q6a3"] = "nedeljkovic"
    df.at[45, "q7a1"] = "fox"
    df.at[45, "q8a1"] = "mcdavid"
    df.at[45, "q9a1"] = "kessel"
    df.at[45, "q10a1"] = np.nan
    # Joe R included an extra period in an answer, then had some commentary
    # Joe R also stated he wasn't sure if Panarin is calder-eligible but maybe would select him
    # Not adding him to his entry, I've been being very permissive on keeping people in the contest
    # Without any directions from Sean to the contrary
    print("Joe R, I fixed your entry")
    minor_surgery_count += 1
    df.at[52, 'q6a3'] = "podkolzin"
    df.at[52, 'q6a4'] = np.nan
    df.at[52, 'q6a5'] = np.nan
    # Ben H didn't enter anything for Q9 or Q10
    print("Ben H, I fixed your entry")
    minor_surgery_count += 1
    df.at[63, 'q9a1'] = np.nan
    df.at[63, 'q9a2'] = np.nan
    df.at[63, 'q10a1'] = np.nan
    # Paul G dropped an extra period in an answer
    print("Paul G, I fixed your entry")
    minor_surgery_count += 1
    df.at[93, 'q6a1'] = "zegras"
    df.at[93, 'q6a3'] = "caufield"
    # Damian H added commentary to some of his answers
    print("Damian H, I fixed your entry")
    df.at[156, 'q6a3'] = np.nan
    df.at[156, 'q9a1'] = "eichel"
    df.at[156, 'q10a1'] = "kucherov"
    # Dylan C had an explanation of picking ron francis
    print("Dylan C, I fixed your entry")
    minor_surgery_count += 1
    df.at[180, 'q4a5'] = "francis"
    # Alexx M dropped a semicolon into one of his answers and used some mysterious punctuation on Markstrom
    print("Alexx M, I fixed your entry")
    minor_surgery_count += 1
    df.at[188, 'q2a2'] = "ari"
    df.at[188, 'q2a5'] = "sjs"
    df.at[188, 'q5a3'] = "markstrom"
    # Andre D dropped an extra period into one of his answers
    print("Andre D, I fixed your entry")
    minor_surgery_count += 1
    df.at[200, 'q2a1'] = "buf"
    df.at[200, 'q2a5'] = "ari"
    # Tim S included commentary in an answer
    print("Tim S, I fixed your entry")
    minor_surgery_count += 1
    df.at[228, 'q8a5'] = "marchand"
    # Nick L didn't enter anything for Q9 or Q10
    print("Nick L, I fixed your entry")
    minor_surgery_count += 1
    df.at[233, 'q9a1'] = np.nan
    # Max A selected "miller" as a player to be traded
    # There are two active Millers, I've been interpreting these as the more popular one, in this case colin miller
    print("Max A, I fixed your entry")
    minor_surgery_count += 1
    print("INTERPRETATION WARNING: Entry specifies 'miller' to get traded, this is interpreted as c miller")
    df.at[270, 'q9a4'] = "c miller"
    # Liam A dropped a period in instead of a comma
    print("Liam A, I fixed your entry")
    minor_surgery_count += 1
    df.at[278, 'q8a2'] = "matthews"
    df.at[278, 'q8a5'] = "mackinnon"
    # Julien G dropped extra commas in an answer
    print("Julien G, I fixed your entry")
    minor_surgery_count += 1
    df.at[304, 'q8a3'] = "draisaitl"
    df.at[304, 'q8a4'] = np.nan
    df.at[304, 'q10a1'] = np.nan
    # ED P. used a letter to start each line, instead of a number
    print("ED P, I fixed your entry")
    minor_surgery_count += 1
    df.at[309, "q1a1"] = "col"
    df.at[309, "q2a1"] = "buf"
    df.at[309, "q3a1"] = "cooper"
    df.at[309, "q4a1"] = "brisebois"
    df.at[309, "q5a1"] = "hellebuyck"
    df.at[309, "q6a1"] = "zegras"
    df.at[309, "q7a1"] = "makar"
    df.at[309, "q8a1"] = "mcdavid"
    df.at[309, "q9a1"] = "hertl"
    df.at[309, "q10a1"] = "draisaitl"
    # Edward A dropped an extra comma in an answer
    print("Edward A, I fixed your entry")
    minor_surgery_count += 1
    df.at[315, 'q8a1'] = "mcdavid"
    df.at[315, 'q8a2'] = "barkov"
    # Chris H dropped an extra period in an answer
    print("Chris H, I fixed your entry")
    minor_surgery_count += 1
    df.at[316, 'q6a2'] = "zegras"
    df.at[316, 'q6a4'] = "knight"
    # Jacob G couldn't be bothered to list his coaches or gm's and just said "the ones from the teams in Q1"
    # Fortunately for Jacob G, I'm not eliminating anyone, that's up to Sean
    print("Jacob G, I'm fixing your entry... reluctantly")
    minor_surgery_count += 1
    print("I can't help that you ended up with an ineligible GM though")
    df.at[328, 'q3a1'] = "cooper"
    df.at[328, 'q3a2'] = "cassidy"
    df.at[328, 'q3a3'] = "bednar"
    df.at[328, 'q3a4'] = "deboer"
    df.at[328, 'q3a5'] = "quenneville"
    df.at[328, 'q4a1'] = "brisebois"
    df.at[328, 'q4a2'] = "sweeney"
    df.at[328, 'q4a3'] = "sakic"
    df.at[328, 'q4a4'] = "mccrimmon"
    df.at[328, 'q4a5'] = "zito"
    # Chayim S didn't enter anything for Q9
    print("Chayim S, I fixed your entry")
    minor_surgery_count += 1
    df.at[332, 'q9a1'] = np.nan
    # Alex W left question 5 blank
    print("Alex W, I fixed your entry")
    minor_surgery_count += 1
    df.at[347, 'q5a1'] = np.nan
    # Derek R had a leading space before his numbering in Q9
    print("Derek R, I fixed your entry")
    minor_surgery_count += 1
    df.at[352, 'q9a1'] = "eichel"
    df.at[352, 'q10a1'] = np.nan
    # Jesse E didn't enter anything for Q9 or Q10
    print("Jesse E, I fixed your entry")
    minor_surgery_count += 1
    df.at[355, 'q9a1'] = np.nan
    df.at[355, 'q10a1'] = np.nan
    # Jordi A dropped an extra period into an answer
    print("Jordi A, I fixed your entry")
    minor_surgery_count += 1
    df.at[377, 'q4a1'] = "sweeney"
    df.at[377, 'q4a5'] = "bowman"
    # Whistler B picked marner for Q10
    print("Whistler B, I fixed your entry")
    minor_surgery_count += 1
    df.at[387, 'q10a1'] = "marner"
    # David B listed one of his nonplayoff teams as "set"
    print("David B, I fixed your entry")
    minor_surgery_count += 1
    print("INTERPRETATION WARNING: David B listed one of his non-playoff teams as 'set'")
    print("This is being interpreted as Seattle")
    df.at[393, 'q2a2'] = "sea"
    # Ryder S forgot a couple of commas in his answers
    print("Ryder S, I fixed your entry")
    minor_surgery_count += 1
    df.at[410, 'q3a4'] = "brind'amour"
    df.at[410, 'q3a5'] = "keefe"
    df.at[410, 'q4a4'] = "lamoriello"
    df.at[410, 'q4a5'] = "mccrimmon"
    # Andrew B didn't answer multiple questions
    print("Andrew B, I fixed your entry")
    minor_surgery_count += 1
    df.at[422, 'q6a1'] = np.nan
    df.at[422, 'q7a1'] = np.nan
    df.at[422, 'q9a1'] = np.nan
    # Steven E included commentary on some answers
    print("Steven E, I fixed your entry")
    minor_surgery_count += 1
    df.at[423, 'q5a2'] = np.nan
    df.at[423, 'q10a1'] = np.nan
    # Michael S had an explanation of picking ron francis
    print("Michael S, I fixed your entry")
    minor_surgery_count += 1
    minor_surgery_count += 1
    df.at[445, 'q4a5'] = "francis"
    # David J dropped an extra comma in Q9
    print("David J, I fixed your entry")
    minor_surgery_count += 1
    df.at[462, 'q9a3'] = "rakell"
    df.at[462, 'q9a4'] = np.nan
    # Daniel A passed on a couple of questions
    print("Daniel A, I fixed your entry")
    minor_surgery_count += 1
    df.at[472, 'q6a1'] = np.nan
    df.at[472, 'q10a1'] = np.nan
    # Tyler S dropped an extra period into an answer
    print("Tyler S, I fixed your entry")
    minor_surgery_count += 1
    df.at[491, 'q4a4'] = "lamoriello"
    df.at[491, 'q4a5'] = "hextall"
    # Zachary P. picked caufield and then lamented Calder trophy voting
    print("Zachary P, I fixed your entry")
    minor_surgery_count += 1
    df.at[503, 'q6a1'] = "caufield"
    df.at[503, 'q6a2'] = np.nan
    # Chris S did not answer Q9
    print("Chris S, I fixed your entry")
    minor_surgery_count += 1
    df.at[507, 'q9a1'] = np.nan
    # Mike M looks like he swapped his answers for question 7 (norris) and question 8 (hart)
    # I'll fix it for him
    print("Mike M, I fixed your entry")
    minor_surgery_count += 1
    df.at[541, 'q7a1'] = "makar"
    df.at[541, 'q7a2'] = "hedman"
    df.at[541, 'q7a3'] = "theodore"
    df.at[541, 'q7a4'] = np.nan
    df.at[541, 'q7a5'] = np.nan
    df.at[541, 'q8a1'] = "matthews"
    df.at[541, 'q8a2'] = "mcdavid"
    df.at[541, 'q8a3'] = "mackinnon"
    df.at[541, 'q8a4'] = "barkov"
    df.at[541, 'q8a5'] = "kucherov"
    # Hank F didn't name specific goalies and instead named "tb g" and "nyr g"
    # I think this is cheating and wouldn't give credit, but I'll be kind until Sean tells me different
    print("Hank F, I fixed your entry")
    minor_surgery_count += 1
    print("INTERPRETATION WARNING: Hank listed goalies 'tb g' and 'nyr g', I think this is cheating")
    print("But I'm generously interpreting these as 'vasilevskiy' and 'shesterkin' unless Sean says otherwise")
    df.at[556, 'q5a1'] = "vasilevskiy"
    df.at[556, 'q5a2'] = "shesterkin"
    # Samuel T insisted on using numerous different types of ' & " on brind'amour
    print("Samuel T, I fixed your entry")
    minor_surgery_count += 1
    df.at[569, 'q3a2'] = "brind'amour"
    # Brendan G mixed up questions 6 and 7, I'll fix it
    print("Brendan G, I fixed your entry")
    minor_surgery_count += 1
    df.at[604, 'q6a1'] = "caufield"
    df.at[604, 'q6a2'] = "zegras"
    df.at[604, 'q6a3'] = np.nan
    df.at[604, 'q6a4'] = np.nan
    df.at[604, 'q6a5'] = np.nan
    df.at[604, 'q7a1'] = "makar"
    df.at[604, 'q7a2'] = "hedman"
    df.at[604, 'q7a3'] = "mcavoy"
    df.at[604, 'q7a4'] = "hamilton"
    df.at[604, 'q7a5'] = "fox"
    # Matt S dropped an extra period into one of his answers
    print("Matt S, I fixed your entry")
    minor_surgery_count += 1
    df.at[610, 'q2a2'] = "ott"
    df.at[610, 'q2a5'] = "ana"
    # Ryan M included commentary on his pick of Ron Francis
    print("Ryan M, I fixed your entry")
    minor_surgery_count += 1
    df.at[615, 'q4a2'] = "francis"
    df.at[615, 'q4a3'] = "brisebois"
    # Erin H selected "richelieu" to be traded
    # There is no richelieu on hockey reference or on elite prospects
    # I'm going to be kind and interpret this as rickard rakell, cause I can't think of anything else
    print("Erin H, I fixed your entry")
    minor_surgery_count += 1
    print("INTERPRETATION WARNING: Entry specifies 'richelieu' to get traded, this is interpreted as rakell")
    df.at[619, 'q9a1'] = "rakell"
    # Joseph B skipped a comma when picking both doug and bill armstrong
    print("Joseph B, I fixed your entry")
    minor_surgery_count += 1
    df.at[621, 'q4a1'] = "d armstrong"
    df.at[621, 'q4a2'] = "b armstrong"
    # Jonathan M selected "smith" as a player to be traded
    # There are four active Smiths, I've been interpreting these as the more popular one, in this case r smith
    # I initially thought Mike Smith would be the one people thought would get traded (and assumed this meant Mike)
    # But it seems that Reilly Smith is a somewhat popular pick to get traded, so that's the call here
    print("Jonathan M, I fixed your entry")
    minor_surgery_count += 1
    print("INTERPRETATION WARNING: Entry specifies 'smith' to get traded, this is interpreted as r smith")
    df.at[623, 'q9a5'] = "r smith"
    # John F left a prompt ("playoffs:") in one question
    print("John F, I fixed your entry")
    minor_surgery_count += 1
    df.at[698, 'q5a1'] = "hellebuyck"
    df.at[698, 'q5a2'] = "vasilevskiy"
    df.at[698, 'q5a3'] = "fleury"
    df.at[698, 'q5a4'] = np.nan
    df.at[698, 'q5a5'] = np.nan
    # Michael R included commentary on his pick
    print("Michael R, I fixed your entry")
    minor_surgery_count += 1
    df.at[700, 'q9a3'] = "hart"
    # Anthony B dropped a period into one of his answers
    print("Anthony B, I fixed your entry")
    minor_surgery_count += 1
    df.at[701, 'q2a3'] = "det"
    df.at[701, 'q2a5'] = "ari"
    # Ray M included commentary on one answer
    print("Ray M, I fixed your entry")
    minor_surgery_count += 1
    df.at[706, 'q6a3'] = "tomasino"
    df.at[706, 'q6a4'] = np.nan
    # David R accidentally dropped in a space on answer 2 that didn't play nice
    print("David R, I fixed your entry")
    minor_surgery_count += 1
    df.at[715, 'q2a1'] = "det"
    # Joe C didn't enter anything for Q9
    print("Joe C, I fixed your entry")
    minor_surgery_count += 1
    df.at[735, 'q9a1'] = np.nan
    # Jérémie R included an extra comma
    print("Jérémie R, I fixed your entry")
    minor_surgery_count += 1
    df.at[766, 'q8a4'] = "kucherov"
    df.at[766, 'q8a5'] = np.nan
    # Kevin C had some lines starting with a ' '
    print("Kevin C, I fixed your entry")
    minor_surgery_count += 1
    df.at[771, 'q5a1'] = 'hellebuyck'
    df.at[771, 'q6a1'] = 'caufield'
    # Uziel S had an explanation of picking ron francis
    print("Uziel S, I fixed your entry")
    minor_surgery_count += 1
    df.at[798, 'q4a1'] = "francis"
    # Kyle B forgot a comma
    print("Kyle B, I fixed your entry")
    minor_surgery_count += 1
    df.at[802, 'q9a3'] = "ekholm"
    df.at[802, 'q9a5'] = "kessel"
    # Johnny M dropped an extra space in an answer
    print("Johnny M, I fixed your entry")
    minor_surgery_count += 1
    df.at[820, 'q8a1'] = "mcdavid"
    # Cal R forgot a comma
    print("Cal R, I fixed your entry")
    minor_surgery_count += 1
    df.at[859, 'q9a1'] = "forsberg"
    df.at[859, 'q9a3'] = "domi"
    # Jeffrey C. used a period instead of a comma once
    print("Jeffrey C, I fixed your entry")
    minor_surgery_count += 1
    df.at[860, "q1a4"] = "edm"
    df.at[860, "q1a5"] = "tbl"
    # Sean Shapiro entered commentary for Q9
    print("Sean Shapiro, I fixed your entry")
    minor_surgery_count += 1
    df.at[897, 'q9a1'] = np.nan
    # Benjamin N forgot a comma
    print("Benjamin N, I fixed your entry")
    minor_surgery_count += 1
    df.at[909, 'q7a4'] = "mcavoy"
    df.at[909, 'q7a5'] = "theodore"
    # C J. added commentary to a selection of Ron Francis
    print("C J., I fixed your entry")
    minor_surgery_count += 1
    df.at[926, 'q4a4'] = "francis"
    df.at[926, 'q4a5'] = "d armstrong"
    # Hai T selected "pitlick" as a player to be traded
    # There are two active Pitlicks, I've been interpreting these as the more popular one, in this case t pitlick
    print("Hai T, I fixed your entry")
    minor_surgery_count += 1
    print("INTERPRETATION WARNING: Entry specifies 'pitlick' to get traded, this is interpreted as t pitlick")
    df.at[931, 'q9a5'] = "t pitlick"
    # Matthew F forgot some commas throughout several answers
    print("Matthew F, I fixed your entry")
    minor_surgery_count += 1
    df.at[936, 'q7a1'] = "hedman"
    df.at[936, 'q7a2'] = "josi"
    df.at[936, 'q7a3'] = "fox"
    df.at[936, 'q7a4'] = "makar"
    df.at[936, 'q7a5'] = "heiskanen"
    df.at[936, 'q8a1'] = "mcdavid"
    df.at[936, 'q8a4'] = "matthews"
    df.at[936, 'q8a5'] = "mackinnon"
    df.at[936, 'q9a1'] = "hertl"
    df.at[936, 'q9a2'] = "kessel"
    df.at[936, 'q9a3'] = "rakell"
    # Kevin S entered commentary for Q9 & Q10
    print("Kevin S, I fixed your entry")
    minor_surgery_count += 1
    df.at[942, 'q9a1'] = np.nan
    df.at[942, 'q10a1'] = np.nan
    # Logan F skipped Question 9 entirely, so #10 became #9 when read by the script
    print("Logan F, I fixed your entry")
    minor_surgery_count += 1
    df.at[947, 'q9a1'] = np.nan
    df.at[947, 'q10a1'] = "draisaitl"
    # Ryan M used accents or dashes that my filtering didn't recognize for Fleury
    print("Ryan M, I fixed your entry")
    minor_surgery_count += 1
    df.at[954, 'q5a2'] = "kuemper"
    df.at[954, 'q5a5'] = np.nan
    # Matt H forgot a comma
    print("Matt H, I fixed your entry")
    minor_surgery_count += 1
    df.at[980, 'q5a1'] = "hellebuyck"
    df.at[980, 'q5a5'] = "vasilevskiy"
    # Daniel F dropped an extra period in an answer
    print("Daniel F, I fixed your entry")
    minor_surgery_count += 1
    df.at[993, 'q5a4'] = "saros"
    df.at[993, 'q5a5'] = "fleury"
    # Andrew R included commentary amongst answers
    print("Andrew R, I fixed your entry")
    minor_surgery_count += 1
    df.at[1012, 'q6a2'] = "seider"
    df.at[1012, 'q9a4'] = "stepan"
    df.at[1012, 'q9a5'] = np.nan
    # Kevin L forgot a comma in one of his answers
    print("Kevin L, I fixed your entry")
    minor_surgery_count += 1
    df.at[1029, 'q4a2'] = "yzerman"
    df.at[1029, 'q4a5'] = "blake"
    # Ryan L forgot a comma
    print("Ryan L, I fixed your entry")
    minor_surgery_count += 1
    df.at[1035, 'q6a4'] = "seider"
    df.at[1035, 'q6a5'] = "podkolzin"
    # Glenn I selected "miller" as a player to be traded
    # There are two active Millers, I've been interpreting these as the more popular one, in this case colin miller
    print("Glenn I, I fixed your entry")
    minor_surgery_count += 1
    print("INTERPRETATION WARNING: Entry specifies 'miller' to get traded, this is interpreted as c miller")
    df.at[1075, 'q9a4'] = "c miller"
    # ALEXANDER W included some extra periods, made some commentary, etc.
    print("ALEXANDER W, I fixed your entry")
    minor_surgery_count += 1
    df.at[1080, 'q4a1'] = "guerin"
    df.at[1080, 'q4a2'] = "sakic"
    df.at[1080, 'q4a3'] = "yzerman"
    df.at[1080, 'q5a5'] = np.nan
    df.at[1080, 'q6a1'] = np.nan
    df.at[1080, 'q6a2'] = np.nan
    df.at[1080, 'q6a3'] = np.nan
    df.at[1080, 'q6a4'] = np.nan
    df.at[1080, 'q6a5'] = np.nan
    # David S included some extra periods in answers
    print("David S, I fixed your entry")
    minor_surgery_count += 1
    df.at[1087, 'q5a1'] = "hellebuyck"
    # Joe M forgot a comma in an answer
    print("Joe M, I fixed your entry")
    minor_surgery_count += 1
    df.at[1092, 'q4a3'] = "guerin"
    df.at[1092, 'q4a5'] = "sakic"
    # Neil W. tagged each line with how many answers he was giving ("(5)", etc.)
    print("Neil W, I fixed your entry")
    minor_surgery_count += 1
    df.at[1102, "q1a1"] = "col"
    df.at[1102, "q2a1"] = "buf"
    df.at[1102, "q3a1"] = "cooper"
    df.at[1102, "q4a1"] = "yzerman"
    df.at[1102, "q5a1"] = "vasilevskiy"
    df.at[1102, "q6a1"] = "knight"
    df.at[1102, "q7a1"] = "fox"
    df.at[1102, "q8a1"] = "mcdavid"
    df.at[1102, "q9a1"] = "eichel"
    df.at[1102, "q10a1"] = "marner"
    # Jason Z dropped an extra period in an answer, generated a blank answer
    print("Jason Z, I fixed your entry")
    minor_surgery_count += 1
    df.at[1137, 'q6a4'] = np.nan
    # Bret L didn't enter anything for Q9
    print("Bret L, I fixed your entry")
    minor_surgery_count += 1
    df.at[1142, 'q9a1'] = np.nan
    # John G accidentally used a period instead of a comma
    print("John G, I fixed your entry")
    minor_surgery_count += 1
    df.at[1143, 'q7a3'] = "theodore"
    df.at[1143, 'q7a4'] = "fox"
    # Jared M didn't enter anything for Q9
    print("Jared M, I fixed your entry")
    minor_surgery_count += 1
    df.at[1147, 'q9a1'] = np.nan
    # Bobby B selected "staal" as a player to be traded
    # There are quite famously 3 Staals, I've been interpreting these as the more popular one, in this case m staal
    print("Bobby B, I fixed your entry")
    minor_surgery_count += 1
    print("INTERPRETATION WARNING: Entry specifies 'staal' to get traded, this is interpreted as m staal")
    df.at[1158, 'q9a2'] = "m staal"
    # Anthony T. tagged each line with a prompt ("playoffs:", etc.)
    print("Anthony T, I fixed your entry")
    minor_surgery_count += 1
    df.at[1179, "q1a1"] = "col"
    df.at[1179, "q2a1"] = "det"
    df.at[1179, "q3a1"] = "trotz"
    df.at[1179, "q4a1"] = "lamoriello"
    df.at[1179, "q5a1"] = "hellebuyck"
    df.at[1179, "q6a1"] = "caufield"
    df.at[1179, "q7a1"] = "makar"
    df.at[1179, "q8a1"] = "mackinnon"
    df.at[1179, "q9a1"] = "eichel"
    df.at[1179, "q10a1"] = "draisaitl"
    # Sean B accidentally dropped an extra comma in Q9
    print("Sean B, I fixed your entry")
    minor_surgery_count += 1
    df.at[1212, 'q9a4'] = "leddy"
    # James B. tagged each line with a prompt ("playoffs:", etc.) and did so inconsistently
    print("James B, I fixed your entry")
    minor_surgery_count += 1
    df.at[1228, "q1a1"] = "car"
    df.at[1228, "q2a1"] = "cbj"
    df.at[1228, "q3a1"] = "trotz"
    df.at[1228, "q4a1"] = "blake"
    df.at[1228, "q5a1"] = "markstrom"
    df.at[1228, "q5a5"] = np.nan
    df.at[1228, "q6a1"] = "knight"
    df.at[1228, "q6a5"] = np.nan
    df.at[1228, "q7a1"] = "carlson"
    df.at[1228, "q8a1"] = "mcdavid"
    df.at[1228, "q9a1"] = "hertl"
    df.at[1228, "q10a1"] = np.nan
    # Peter G forgot a comma
    print("Peter G, I fixed your entry")
    minor_surgery_count += 1
    df.at[1241, 'q8a4'] = "marchand"
    df.at[1241, 'q8a5'] = "draisaitl"
    # Connor N put a space in before numbering
    print("Connor N, I fixed your entry")
    minor_surgery_count += 1
    df.at[1246, 'q8a1'] = "mcdavid"
    # Chris S forgot a comma
    print("Chris S, I fixed your entry")
    minor_surgery_count += 1
    df.at[1247, 'q7a4'] = "slavin"
    df.at[1247, 'q7a5'] = "josi"
    # Bryan l included commentary in one of his answers
    print("Bryan L, I fixed your entry")
    minor_surgery_count += 1
    df.at[1257, 'q6a4'] = np.nan
    # Samantha P used a '-' in brind'amour, which split it into two answers
    print("Samantha P, I fixed your entry")
    minor_surgery_count += 1
    df.at[1278, 'q3a2'] = "brind'amour"
    df.at[1278, 'q3a3'] = "smith"
    # Matt B skipped Question 9 entirely, so #10 became #9 when read by the script
    print("Matt B, I fixed your entry")
    minor_surgery_count += 1
    df.at[1282, 'q9a1'] = np.nan
    df.at[1282, 'q10a1'] = "kucherov"
    # Morgan J left multiple questions blank
    print("Morgan J, I fixed your entry")
    minor_surgery_count += 1
    df.at[1295, 'q5a1'] = np.nan
    df.at[1295, 'q6a1'] = np.nan
    # Clint R dropped an extra period in an answer
    print("Clint R, I fixed your entry")
    minor_surgery_count += 1
    df.at[1296, 'q8a5'] = np.nan
    # Cam P forgot a comma, two of his answers got combined
    print("Cam P, I fixed your entry")
    df.at[1322, 'q3a2'] = "cooper"
    df.at[1322, 'q3a5'] = "keefe"
    # Suraj D dropped an extra period into one of his answers
    print("Suraj D, I fixed your entry")
    minor_surgery_count += 1
    df.at[1324, 'q3a3'] = "bednar"
    df.at[1324, 'q3a5'] = "cooper"
    # Jon H used a '-' in brind'amour, which split it into two answers
    print("Jon H, I fixed your entry")
    minor_surgery_count += 1
    df.at[1338, 'q3a2'] = "brind'amour"
    df.at[1338, 'q3a3'] = "maurice"
    # Will B left a question empty
    print("Will B, I fixed your entry")
    minor_surgery_count += 1
    df.at[1353, 'q6a1'] = np.nan
    df.at[1353, 'q10a1'] = np.nan
    # David S used a '-' in brind'amour, which split it into two answers
    print("David S, I fixed your entry")
    minor_surgery_count += 1
    df.at[1374, 'q3a2'] = "brind'amour"
    df.at[1374, 'q3a3'] = "smith"
    # Brian H didn't enter anything for Q9
    print("Brian H, I fixed your entry")
    minor_surgery_count += 1
    df.at[1378, 'q9a1'] = np.nan
    # A.J. M. tagged each line with a prompt ("playoffs:", etc., along with some extra notes)
    print("A. J. M., I fixed your entry")
    minor_surgery_count += 1
    df.at[1381, "q1a1"] = "tbl"
    df.at[1381, "q2a1"] = "ari"
    df.at[1381, "q3a1"] = "keefe"
    df.at[1381, "q3a5"] = "cooper"
    df.at[1381, "q4a1"] = "francis"
    df.at[1381, "q4a4"] = "brisebois"
    df.at[1381, "q5a1"] = "vasilevskiy"
    df.at[1381, "q6a1"] = "nedeljkovic"
    df.at[1381, "q6a5"] = "seider"
    df.at[1381, "q7a1"] = "hedman"
    df.at[1381, "q8a1"] = "mcdavid"
    df.at[1381, "q9a1"] = "kessel"
    df.at[1381, "q10a1"] = "draisaitl"
    # Tony M dropped an extra comma in an answer
    print("Tony M, I fixed your entry")
    minor_surgery_count += 1
    df.at[1382, 'q5a5'] = "saros"
    # Sandy K forgot a comma and got teams merged together as a result
    print("Sandy K, I fixed your entry")
    minor_surgery_count += 1
    df.at[1383, "q1a2"] = "col"
    df.at[1383, "q1a5"] = "tor"
    # James B. tagged each line with a prompt ("playoffs:", etc.)
    print("James B, I fixed your entry")
    minor_surgery_count += 1
    df.at[1406, "q1a1"] = "col"
    df.at[1406, "q2a1"] = "cbj"
    df.at[1406, "q3a1"] = "cooper"
    df.at[1406, "q4a1"] = "brisebois"
    df.at[1406, "q5a1"] = "vasilevskiy"
    df.at[1406, "q6a1"] = "caufield"
    df.at[1406, "q7a1"] = "hedman"
    df.at[1406, "q8a1"] = "mcdavid"
    df.at[1406, "q9a1"] = "eichel"
    df.at[1406, "q10a1"] = "draisaitl"
    # Pete D dropped an extra comma in his answers
    print("Pete D, I fixed your entry")
    minor_surgery_count += 1
    df.at[1445, 'q3a4'] = "brind'amour"
    # Pat E forgot a comma between two answers
    print("Pat E, I fixed your entry")
    minor_surgery_count += 1
    df.at[1452, "q1a1"] = "tor"
    df.at[1452, "q1a5"] = "col"
    # Josh M dropped a period into one of his answers
    print("Josh M, I fixed your entry")
    minor_surgery_count += 1
    df.at[1457, 'q2a3'] = "buf"
    df.at[1457, 'q2a5'] = "cbj"
    # Mike V included an explanation of his picking ron francis
    print("Mike V, I fixed your entry")
    minor_surgery_count += 1
    df.at[1414, 'q4a5'] = "francis"
    # Dylan J dropped an extra comma into one of his answers
    print("Dylan J, I fixed your entry")
    minor_surgery_count += 1
    df.at[1501, 'q4a3'] = "mccrimmon"
    df.at[1501, 'q4a4'] = "sweeney"
    # Peter E had no spaces or ".", ")", etc. after his numbering, cutting off the first letter of each set of answers
    print("Peter E, I fixed your entry")
    minor_surgery_count += 1
    df.at[1520, 'q1a1'] = "tbl"
    df.at[1520, 'q2a1'] = "van"
    df.at[1520, 'q3a1'] = "tippett"
    df.at[1520, 'q4a1'] = "mccrimmon"
    df.at[1520, 'q5a1'] = "price"
    df.at[1520, 'q6a1'] = "caufield"
    df.at[1520, 'q7a1'] = "hedman"
    df.at[1520, 'q8a1'] = "mcdavid"
    df.at[1520, 'q9a1'] = "kessel"
    df.at[1520, 'q10a1'] = np.nan
    # David S used an emoji that I dont think will work in my dictionaries
    print("David S, I fixed your entry")
    minor_surgery_count += 1
    df.at[1524, 'q10a1'] = "draisaitl"
    # Faizal S dropped an extra period in one of his answers
    print("Faizal S, I fixed your entry")
    minor_surgery_count += 1
    df.at[1525, 'q2a1'] = "buf"
    # Steve M led some lines with spaces
    print("Steve M, I fixed your entry")
    minor_surgery_count += 1
    df.at[1526, 'q5a1'] = "hellebuyck"
    # Ian B chose "kuemper" among his norris selections
    # The only active "kuemper" in the league is Darcy Kuemper
    # This doesnt appear to be a mistake of swapping answers - Ian correctly put goalies (3 of them) in question 5,
    # Rookies in 6 (1 of them), and defense in 7 (3, including Kuemper). I'll put it in 5 for him.
    print("Ian B, I fixed your entry")
    minor_surgery_count += 1
    df.at[1532, 'q5a4'] = "kuemper"
    df.at[1532, 'q7a3'] = np.nan
    # Joel C dropped some extra periods in answers
    print("Joel C, I fixed your entry")
    minor_surgery_count += 1
    df.at[1541, 'q6a1'] = "caufield"
    df.at[1541, 'q7a1'] = "hedman"
    # Bryce C forgot a comma in one of his answers
    print("Bryce C, I fixed your entry")
    minor_surgery_count += 1
    df.at[1542, 'q3a2'] = "quenneville"
    df.at[1542, 'q3a5'] = "cooper"
    # Marc B included an explanation of his picking ron francis
    print("Marc B, I fixed your entry")
    minor_surgery_count += 1
    df.at[1580, 'q4a5'] = "francis"
    # Jon C wrote a very long explanation of his picks, which was long enough and used
    # enough puncuation to be picked up as a very bad entry to the contest. His reply
    # is deleted after all repairs are made via indexing.
    minor_surgery_count += 1
    print("Dropping index 849 - is not an entry, is an explanation of Jon C's entry")
    df.drop(849, axis=0, inplace=True)
    # Kevin A submitted his entry twice, then replied to one of his entries to make an amended entry
    # Because he forgot to enter anyone for Q9. Deleting his two prior entries.
    minor_surgery_count += 1
    print("Dropping outdated entry from Kevin A")
    df.drop(1223, axis=0, inplace=True)
    minor_surgery_count += 1
    print("Dropping another outdated entry from Kevin A")
    df.drop(1281, axis=0, inplace=True)
    return df, minor_surgery_count


def standardization_operations(df, authors):
    """ In order to facilitate automatic grading of the
    contest entries, all answers in all entries must be
    standardized. In this way, "tbl" can be graded, instead
    of "Tampa Bay", "Lightning", "Tampa", etc. This function
    takes a dataframe and goes through each question, using
    customized dictionaries to replace all answers with a 
    standardized answer. Returns a standardized dataframe.

    2021-22 note: This function also takes a list of authors
    for use during the special "armstrong" GM check. This 
    MUST be modified for next year, when the second GM named
    "armstrong" becomes a viable answer.

    Note that for future contests, these dictionaries can be
    a starting point, but will have to be very closely 
    checked to make sure they remain accurate.
    """
    # Start standardizing entries by replacing values with a standard value
    # Dictionary to match team cities with three letter abbreviation
    city_name_dict = {
        "anaheim": "ana",
        "arizona": "ari",
        "phoenix": "ari",
        "az": "ariz",
        "boston": "bos",
        "buffalo": "buf",
        "carolina": "car",
        "columbus": "cbj",
        "cbus": "cbj",
        "clb": "cbj",
        "calgary": "cgy",
        "chicago": "chi",
        "colorado": "col",
        "dallas": "dal",
        "detroit": "det",
        "edmonton": "edm",
        "florida": "fla",
        "los angeles": "lak",
        "minnesota": "min",
        "mn": "min",
        "montreal": "mtl",
        "new jersey": "njd",
        "nj": "njd",
        "nashville": "nsh",
        "new york islanders": "nyi",
        "ny islanders": "nyi",
        "new york (islanders)": "nyi",
        "nyislanders": "nyi",
        "new york rangers": "nyr",
        "new york (rangers)": "nyr",
        "ny rangers": "nyr",
        "ottawa": "ott",
        "philadelphia": "phi",
        "pittsburgh": "pit",
        "san jose": "sjs",
        "sj": "sjs",
        "seattle": "sea",
        "st louis": "stl",
        "st. louis": "stl",
        "tampa bay": "tbl",
        "tampa": "tbl",
        "toronto": "tor",
        "vancouver": "van",
        "las vegas": "veg",
        "vegas": "veg",
        "winnipeg": "wpg",
        "washington": "wsh"
    }
    # Dictionary to match team names with three letter abbreviation
    team_name_dict = {
        "mighty ducks": "ana",
        "ducks": "ana",
        "coyotes": "ari",
        "yotes": "ari",
        "bruins": "bos",
        "sabres": "buf",
        "hurricanes": "car",
        "canes": "car",
        "'canes": "car",
        "blue jackets": "cbj",
        "jackets": "cbj",
        "bjs": "cbj",
        "flames": "cgy",
        "blackhawks": "chi",
        "black hawks": "chi",
        "avalanche": "col",
        "avs": "col",
        "stars": "dal",
        "red wings": "det",
        "wings": "det",
        "oilers": "edm",
        "oil": "edm",
        "panthers": "fla",
        "kings": "lak",
        "wild": "min",
        "canadiens": "mtl",
        "canadians": "mtl",
        "devils": "njd",
        "predators": "nsh",
        "preds": "nsh",
        "islanders": "nyi",
        "isles": "nyi",
        "rangers": "nyr",
        "senators": "ott",
        "sens": "ott",
        "flyers": "phi",
        "penguins": "pit",
        "sharks": "sjs",
        "kraken": "sea",
        "blues": "stl",
        "lightning": "tbl",
        "bolts": "tbl",
        "maple leafs": "tor",
        "leafs": "tor",
        "canucks": "van",
        "golden knights": "veg",
        "knights": "veg",
        "jets": "wpg",
        "capitals": "wsh",
        "caps": "wsh"
    }
    teams_other_dict = {
        "0": np.nan,
        "anaheim ducks": "ana",
        "annehiem": "ana",
        "anahiem": "ana",
        "anh": "ana",
        "ani": "ana",
        "ana ducks": "ana",
        "arizona coyotes": "ari",
        "az coyotes": "ari",
        "phoenix coyotes": "ari",
        "arz": "ari",
        "ariz": "ari",
        "'zona": "ari",
        "arizona..": "ari",
        "azc": "ari",
        "phx": "ari",
        "boston bruins": "bos",
        "buffalo sabres": "buf",
        "sabers": "buf",
        "sabre's": "buf",
        "sabre’s": "buf",
        "bufallo sabres": "buf",
        "sables": "buf",
        "buff.": "buf",
        "buff": "buf",
        "buf sabres": "buf",
        "carolina hurricanes": "car",
        "columbus blue jackets": "cbj",
        "clm": "cbj",
        "colombus blue jackets": "cbj",
        "colombus": "cbj",
        "blue jax": "cbj",
        "coumbus": "cbj",
        "the cbj": "cbj",
        "calgary flames": "cgy",
        "cal": "cgy",
        "chicago blackhawks": "chi",
        "chicago black hawks": "chi",
        "colorado avalanche": "col",
        "col avalanche": "col",
        "coloardo": "col",
        "colarado": "col",
        "avalance": "col",
        "aves": "col",
        "avalanches": "col",
        "crl": "col",
        "dallas stars": "dal",
        "detroit red wings": "det",
        "redwings": "det",
        "drw": "det",
        "det.": "det",
        "det red wings": "det",
        "detroit redwings": "det",
        "edmonton oilers": "edm",
        "oliers": "edm",
        "florida panthers": "fla",
        "floride": "fla",
        "flo": "fla",
        "fl": "fla",
        "flp": "fla",
        "los angeles kings": "lak",
        "l.a. kings": "lak",
        "la kings": "lak",
        "l.a kings": "lak",
        "la": "lak",
        "minnesota wild": "min",
        "minn": "min",
        "montreal canadiens": "mtl",
        "montreal canadians": "mtl",
        "candiens": "mtl",
        "habs": "mtl",
        "nashville predators": "nsh",
        "nash": "nsh",
        "nas": "nsh",
        "nshville": "nsh",
        "new jersey devils": "njd",
        "ney york islanders": "nyi",
        "new york isles": "nyi",
        "new york i": "nyi",
        "ottawa senators": "ott",
        "sentaors": "ott",
        "philadelphia flyers": "phi",
        "philedelphia": "phi",
        "san jose sharks": "sjs",
        "sj sharks": "sjs",
        "sharkes": "sjs",
        "san josé sharks": "sjs",
        "sam jose": "sjs",
        "sanjose": "sjs",
        "seattle kraken": "sea",
        "krakken": "sea",
        "st louis blues": "stl",
        "st. louis blues": "stl",
        "st": "stl",
        "tampa bay lightning": "tbl",
        "tb lightning": "tbl",
        "tb": "tbl",
        "mike m 1. lightning": "tbl",
        "tampa bay lightening": "tbl",
        "lightining": "tbl",
        "ligntning": "tbl",
        "lighting": "tbl",
        "lightening": "tbl",
        "lightnings": "tbl",
        "tampa lightning": "tbl",
        "tamp bay": "tbl",
        "tgl": "tbl",
        "toronto maple leafs": "tor",
        "mapleleafs": "tor",
        "leaf's": "tor",
        "leaf’s": "tor",
        "tor maple leafs": "tor",
        "tml": "tor",
        "maples leafs": "tor",
        "vancouver canucks": "van",
        "las vegas golden knights": "veg",
        "vegas golden knights": "veg",
        "vgk": "veg",
        "dillon h. 1. vegas": "veg",
        "de 1. golden knights": "veg",
        "golden knight": "veg",
        "goldn knights": "veg",
        "goldn knight": "veg",
        "g knights": "veg",
        "g. knights": "veg",
        "golden nights": "veg",
        "las.vegas": "veg",
        "vgn": "veg",
        "lvk": "veg",
        "lv": "veg",
        "lvg": "veg",
        "vgs": "veg",
        "vkg": "veg",
        "the vgk": "veg",
        "winnipeg jets": "wpg",
        "win": "wpg",
        "washington capitals": "wsh",
        "was": "wsh",
    }
    # Generate list of columns for question 1 to iterate through
    q1 = ['q1a1', 'q1a2', 'q1a3', 'q1a4', 'q1a5']
    for question in q1:
        print(f"Standardizing the answers for column {question}...")
        # Replace by city name
        df[question].replace(to_replace=city_name_dict,
                             value=None, inplace=True)
        # Replace by team name
        df[question].replace(to_replace=team_name_dict,
                             value=None, inplace=True)
        # Replace by other criteria (combined city & team name, misspellings, etc.)
        df[question].replace(to_replace=teams_other_dict,
                             value=None, inplace=True)
        print("Done!")
    q2 = ['q2a1', 'q2a2', 'q2a3', 'q2a4', 'q2a5']
    for question in q2:
        print(f"Standardizing the answers for column {question}")
        # Replace by city name
        df[question].replace(to_replace=city_name_dict,
                             value=None, inplace=True)
        # Replace by team name
        df[question].replace(to_replace=team_name_dict,
                             value=None, inplace=True)
        # Replace by other criteria (combined city & team name, misspellings, etc.)
        df[question].replace(to_replace=teams_other_dict,
                             value=None, inplace=True)
        print("Done!")
    # Dictionary of variations of coaches names for standardization
    coaches_dict = {
        "0": np.nan,

        "jared bednar": "bednar",
        "j. bednar": "bednar",
        "j bednar": "bednar",
        "bednar (col)": "bednar",
        "bednar(col)": "bednar",
        "jared bednar (col)": "bednar",
        "j. bednard": "bednar",
        "bed ar": "bednar",
        "colorado": "bednar",
        "jared bendar": "bednar",
        "col coach": "bednar",
        "richard bednar": "bednar",
        "bednard": "bednar",
        "bednar col": "bednar",
        "j.bednar": "bednar",
        "col": "bednar",
        "j benar": "bednar",
        "bedner": "bednar",

        "craig berube": "berube",
        "c. berube": "berube",
        "c berube": "berube",
        "berube (stl)": "berube",
        "berube(stl)": "berube",

        "jeff blashill": "blashill",
        "j. blashill": "blashill",
        "j blashill": "blashill",
        "blashill (det)": "blashill",
        "blashill(det)": "blashill",
        "detroit": "blashill",
        "det": "blashill",

        "bob boughner": "boughner",
        "b. boughner": "boughner",
        "b boughner": "boughner",
        "boughner (sjs)": "boughner",
        "boughner (sj)": "boughner",
        "boughner(sjs)": "boughner",
        "boughner(sj)": "boughner",

        "rick bowness": "bowness",
        "r. bowness": "bowness",
        "r bowness": "bowness",
        "bowness (dal)": "bowness",
        "bowness(dal)": "bowness",

        "rod brind'amour": "brind'amour",
        "rod brind’amour": "brind'amour",
        "r. brind'amour": "brind'amour",
        "r. brind’amour": "brind'amour",
        "r brind'amour": "brind'amour",
        "r brind’amour": "brind'amour",
        "rod brindamour": "brind'amour",
        "r. brindamour": "brind'amour",
        "r brindamour": "brind'amour",
        "brindamour": "brind'amour",
        "brind’amour": "brind'amour",
        "brind’amour(car)": "brind'amour",
        "brindamore": "brind'amour",
        "rba": "brind'amour",
        "rodthebod": "brind'amour",
        "rod “the bod” brind’amour": "brind'amour",
        "rod bind’amour": "brind'amour",
        "brand'amour": "brind'amour",
        "rod brind‘amour": "brind'amour",
        "rob brind'amour": "brind'amour",
        "brind‘amour": "brind'amour",
        "rod": "brind'amour",
        "brindamor": "brind'amour",
        "brindamore car": "brind'amour",
        "brind ‘amour ": "brind'amour",
        "brind amour": "brind'amour",
        "brind amor": "brind'amour",
        "brind'amor": "brind'amour",
        "rod bindamour": "brind'amour",
        "brind'amur": "brind'amour",
        "ron brind’amour": "brind'amour",
        "brind ‘amour": "brind'amour",
        "r brind amour": "brind'amour",
        'rob "the bod"': "brind'amour",
        "rod brid'amour": "brind'amour",
        "rod the bod": "brind'amour",
        "brind a’mour": "brind'amour",
        "rod brind'amour (car)": "brind'amour",
        "brind’amor": "brind'amour",
        "car": "brind'amour",
        "brind'omour": "brind'amour",
        "rod brind`amour": "brind'amour",
        "brind'amour (car)": "brind'amour",
        "rod brind’ amour": "brind'amour",
        "rod ‘the bod’ brind’amour": "brind'amour",
        "brind' amour ": "brind'amour",
        "rod brind’amor": "brind'amour",
        "robert brindamour": "brind'amour",
        "rob brind’amour": "brind'amour",
        "brinda’amour": "brind'amour",
        "rob brinda'mour": "brind'amour",
        "bind’amour": "brind'amour",
        "rod brind amour": "brind'amour",
        "rod  brind'amour": "brind'amour",
        "rod brind'amor": "brind'amour",
        "brind’amour (car)": "brind'amour",
        "brind a'mour": "brind'amour",
        "rob brindamour": "brind'amour",
        "canes coach": "brind'amour",
        "brind' amour": "brind'amour",
        "brind’amore": "brind'amour",
        "rod 'the bod' brind'amour": "brind'amour",

        "bruce cassidy": "cassidy",
        "b. cassidy": "cassidy",
        "b cassidy": "cassidy",
        "cassidy (bos)": "cassidy",
        "cassidy(bos)": "cassidy",
        "cassidy bos": "cassidy",
        "bos coach": "cassidy",
        "butch cassidy": "cassidy",
        "kassidy": "cassidy",
        "cassiday": "cassidy",
        "bos": "cassidy",

        "jeremy colliton": "colliton",
        "j. colliton": "colliton",
        "j colliton": "colliton",
        "colliton (chi)": "colliton",
        "colliton(chi)": "colliton",
        "collison": "colliton",
        "jeremy collington": "colliton",

        "jon cooper": "cooper",
        "j. cooper": "cooper",
        "j cooper": "cooper",
        "cooper (tb)": "cooper",
        "cooper(tb)": "cooper",
        "john cooper": "cooper",
        "cooper (tbl)": "cooper",
        "cooper(tbl)": "cooper",
        "tbl": "cooper",
        "tb": "cooper",
        "cooper tb": "cooper",
        "ooper": "cooper",
        "tb coach": "cooper",
        "tbl coach": "cooper",
        "tampa coach": "cooper",
        "jon cooper (tb)": "cooper",
        "jon cooper (tbl)": "cooper",
        "j.cooper": "cooper",
        "job cooper": "cooper",
        "tampa bay": "cooper",
        "jon copper": "cooper",
        "jonathon cooper": "cooper",
        "cooper.": "cooper",

        "peter deboer": "deboer",
        "pete deboer": "deboer",
        "peter de boer": "deboer",
        "pete de boer": "deboer",
        "p. deboer": "deboer",
        "p. de boer": "deboer",
        "p deboer": "deboer",
        "p de boer": "deboer",
        "deboer (veg)": "deboer",
        "deboer (vgk)": "deboer",
        "pete deboer (vgk)": "deboer",
        "deboer (lv)": "deboer",
        "de boer (veg)": "deboer",
        "de boer (vgk)": "deboer",
        "de boer (lv)": "deboer",
        "vgk coach": "deboer",
        "vgk": "deboer",
        "deboer vgk": "deboer",
        "lv coach": "deboer",
        "doboer": "deboer",
        "de boer": "deboer",
        "debour": "deboer",
        "peter debour": "deboer",
        "deboar": "deboer",
        "vegas coach": "deboer",

        "dominique ducharme": "ducharme",
        "dom ducharme": "ducharme",
        "d. ducharme": "ducharme",
        "d ducharme": "ducharme",
        "ducharme (mtl)": "ducharme",
        "ducharme(mtl)": "ducharme",
        "dominic duscharme": "ducharme",

        "dallas eakins": "eakins",
        "d. eakins": "eakins",
        "d eakins": "eakins",
        "eakins (ana)": "eakins",
        "eakins(ana)": "eakins",

        "dean evason": "evason",
        "d. evason": "evason",
        "d evason": "evason",
        "evason (min)": "evason",
        "evason(min)": "evason",
        "dean evanson": "evason",
        "evanson": "evason",
        "dean evenson": "evason",
        "d.evason": "evason",
        "evenson": "evason",
        "minnesota coach": "evason",
        "dean eaveson": "evason",

        "gerard gallant": "gallant",
        "g. gallant": "gallant",
        "g gallant": "gallant",
        "gallant (nyr)": "gallant",
        "gallant(nyr)": "gallant",
        "gerrard gallant": "gallant",
        "galland": "gallant",
        "garrard gallant": "gallant",
        "g.gallant": "gallant",

        "don granato": "granato",
        "d. granato": "granato",
        "d granato": "granato",
        "granato (buf)": "granato",
        "granato(buf)": "granato",

        "travis green": "green",
        "t. green": "green",
        "t green": "green",
        "green (van)": "green",
        "green(van)": "green",
        "t.green": "green",
        "todd green": "green",
        "trent green": "green",

        "dave hakstol": "hakstol",
        "d. hakstol": "hakstol",
        "d hakstol": "hakstol",
        "hakstol (sea)": "hakstol",
        "hakstol(sea)": "hakstol",
        "dave hakstall": "hakstol",
        "hasktoil": "hakstol",
        "hakstoll": "hakstol",
        "kraken coach": "hakstol",
        "halston": "hakstol",
        "dave hakstoll": "hakstol",

        "john hynes": "hynes",
        "j. hynes": "hynes",
        "j hynes": "hynes",
        "hynes (nsh)": "hynes",
        "hynes(nsh)": "hynes",

        "sheldon keefe": "keefe",
        "s. keefe": "keefe",
        "s keefe": "keefe",
        "keefe (tor)": "keefe",
        "keefe(tor)": "keefe",
        "tor": "keefe",
        "toronto": "keefe",
        "sheldon keef": "keefe",
        "sheldon keefe(tor)": "keefe",
        "keafe": "keefe",
        "keefe (tml)": "keefe",
        "seldon keefe": "keefe",

        "brad larsen": "larsen",
        "b. larsen": "larsen",
        "b larsen": "larsen",
        "larsen (cbj)": "larsen",
        "larsen(cbj)": "larsen",
        "cbj": "larsen",

        "peter laviolette": "laviolette",
        "p. laviolette": "laviolette",
        "p laviolette": "laviolette",
        "laviolette (wsh)": "laviolette",
        "laviolette(wsh)": "laviolette",
        "peter_laviolette": "laviolette",
        "laviollette": "laviolette",
        "laviollete": "laviolette",

        "paul maurice": "maurice",
        "p. maurice": "maurice",
        "p maurice": "maurice",
        "maurice (wpg)": "maurice",
        "maurice(wpg)": "maurice",
        "paul maurice (wpg)": "maurice",

        "todd mclellan": "mclellan",
        "t. mclellan": "mclellan",
        "t mclellan": "mclellan",
        "mclellan (lak)": "mclellan",
        "mclellan (la)": "mclellan",
        "mclellan(lak)": "mclellan",
        "mclellan(la)": "mclellan",
        "mclennan": "mclellan",
        "todd mclellan (lak)": "mclellan",
        "mcllellan": "mclellan",
        "lak": "mclellan",
        "maclellan": "mclellan",
        "mcclellan": "mclellan",

        "joel quenneville": "quenneville",
        "j. quenneville": "quenneville",
        "j quenneville": "quenneville",
        "quenneville (fla)": "quenneville",
        "quenneville(fla)": "quenneville",
        "coach q": "quenneville",
        "queenville": "quenneville",
        "quinville": "quenneville",
        "j.quenneville": "quenneville",
        "quennville": "quenneville",
        "qunneville": "quenneville",
        "joel quinville": "quenneville",
        "joel queneville": "quenneville",
        "joel quenneville (fla)": "quenneville",
        "q": "quenneville",
        "joel quennville": "quenneville",
        "joel quenville": "quenneville",
        "queenneville": "quenneville",
        "joel quennenville": "quenneville",
        "florida coach": "quenneville",
        "quineville": "quenneville",
        "j. quennville": "quenneville",
        "joe q": "quenneville",
        "fla coach": "quenneville",
        "quenville": "quenneville",
        "queneville": "quenneville",
        "john quenneville": "quenneville",
        "joel quennevile": "quenneville",
        "quennville (fla)": "quenneville",
        "joe quenneville": "quenneville",
        "quinneville": "quenneville",
        "quenneville fla": "quenneville",
        "john quenville": "quenneville",
        "joe quinville": "quenneville",
        "joel qenneville": "quenneville",
        "queeneville": "quenneville",
        "joel quinneville": "quenneville",
        "quennveville": "quenneville",
        "quennenville": "quenneville",
        "joel quennvile": "quenneville",
        "joel q (fla)": "quenneville",
        "joel qunneville": "quenneville",
        "john quennville": "quenneville",
        "j. quenville": "quenneville",
        "joel quennveville": "quenneville",


        "lindy ruff": "ruff",
        "l. ruff": "ruff",
        "l ruff": "ruff",
        "ruff (njd)": "ruff",
        "ruff (nj)": "ruff",
        "ruff(njd)": "ruff",
        "ruff(nj)": "ruff",
        "ruff nj": "ruff",
        "new jersey coach": "ruff",

        "d. j. smith": "smith",
        "d j smith": "smith",
        "d.j. smith": "smith",
        "dj smith": "smith",
        "smith (ott)": "smith",
        "smith(ott)": "smith",
        "dj smith (ott)": "smith",
        "d.j. smith (ott)": "smith",
        "d.j smith": "smith",
        "ottawa coach": "smith",
        "ott coach": "smith",
        "djsmith": "smith",
        "tj smith": "smith",

        "mike sullivan": "sullivan",
        "m. sullivan": "sullivan",
        "m sullivan": "sullivan",
        "sullivan (pit)": "sullivan",
        "sullivan(pit)": "sullivan",
        "sullivan (pitt)": "sullivan",

        "daryl sutter": "sutter",
        "d. sutter": "sutter",
        "d sutter": "sutter",
        "sutter (cgy)": "sutter",
        "sutter(cgy)": "sutter",
        "darryl sutter": "sutter",
        "cgy coach": "sutter",

        "dave tippett": "tippett",
        "d. tippett": "tippett",
        "d tippett": "tippett",
        "tippett (edm)": "tippett",
        "tippett(edm)": "tippett",
        "dave tippet": "tippett",
        "d. tippet": "tippett",
        "d tippet": "tippett",
        "tippet (edm)": "tippett",
        "tippet(edm)": "tippett",
        "edmonton": "tippett",
        "edm": "tippett",
        "tippet": "tippett",
        "edm coach": "tippett",
        "tippette": "tippett",
        "d.tippett": "tippett",
        "tippit": "tippett",
        "tipett": "tippett",

        "andre tourigny": "tourigny",
        "a. tourigny": "tourigny",
        "a tourigny": "tourigny",
        "tourigny (ari)": "tourigny",
        "tourigny(ari)": "tourigny",
        "arizona": "tourigny",
        "ari": "tourigny",
        "phx": "tourigny",

        "barry trotz": "trotz",
        "b. trotz": "trotz",
        "b trotz": "trotz",
        "trotz (nyi)": "trotz",
        "trotz(nyi)": "trotz",
        "ny islanders": "trotz",
        "nyi": "trotz",
        "trots": "trotz",
        "rotz": "trotz",
        "barrty trotz": "trotz",
        "barry trotz (nyi)": "trotz",
        "tortz": "trotz",
        "b.trotz": "trotz",
        "trott": "trotz",
        "trotz nyi": "trotz",
        "nyi coach": "trotz",
        "barry trots": "trotz",


        "alain vigneault": "vigneault",
        "a. vigneault": "vigneault",
        "a vigneault": "vigneault",
        "vigneault (phi)": "vigneault",
        "vigneault(phi)": "vigneault",
        "alain vignealt": "vigneault",
    }
    q3 = ['q3a1', 'q3a2', 'q3a3', 'q3a4', 'q3a5']
    for question in q3:
        print(f"Standardizing the answers for column {question}")
        # Replace by various names of coaches
        df[question].replace(to_replace=coaches_dict, value=None, inplace=True)
        print("Done!")
    # Dictionary of variations of GM names for standardization
    gms_dict = {
        "0": np.nan,

        "kevyn adams": "adams",
        "k. adams": "adams",
        "k adams": "adams",
        "adams (buf)": "adams",
        "adams(buf)": "adams",
        "buf": "adams",

        "bill armstrong": "b armstrong",
        "bill armstrong (ari)": "b armstrong",
        "bill armstrong (az)": "b armstrong",
        "b armstrong (ari)": "b armstrong",
        "b armstrong (az)": "b armstrong",
        "b. armstrong": "b armstrong",
        "armstrong (ari)": "b armstrong",
        "armstrong (az)": "b armstrong",
        "phx": "b armstrong",
        "ari": "b armstrong",
        "armstrong (coyotes)": "b armstrong",
        "armstrong(coyotes)": "b armstrong",
        "ari gm": "b armstrong",
        "bill armstong": "b armstrong",
        "armstrong(az)": "b armstrong",

        "doug armstrong": "d armstrong",
        "doug armstrong (stl)": "d armstrong",
        "d armstrong (stl)": "d armstrong",
        "d. armstrong (stl)": "d armstrong",
        "d. armstrong": "d armstrong",
        "armstrong (stl)": "d armstrong",
        "armstrong(stl)": "d armstrong",
        "stl": "d armstrong",
        "armstrong(blues)": "d armstrong",
        "armstrong (st. l)": "d armstrong",
        "armstrong (doug)": "d armstrong",
        "doug armstrong stl": "d armstrong",

        "jim benning": "benning",
        "j. benning": "benning",
        "j benning": "benning",
        "benning (van)": "benning",
        "benning(van)": "benning",
        "van": "benning",

        "marc bergevin": "bergevin",
        "mark bergevin": "bergevin",
        "marc bergevin (mtl)": "bergevin",
        "mark bergevin (mtl)": "bergevin",
        "m. bergevin": "bergevin",
        "m bergevin": "bergevin",
        "bergevin (mtl)": "bergevin",
        "bergevin(mtl)": "bergevin",
        "mtl": "bergevin",
        "bergevin mtl": "bergevin",

        "rob blake": "blake",
        "rob blake (lak)": "blake",
        "rob blake (la)": "blake",
        "r. blake": "blake",
        "r blake": "blake",
        "blake (lak)": "blake",
        "blake (la)": "blake",
        "lak": "blake",
        "la": "blake",
        "rod blake": "blake",
        "r.blake": "blake",
        "kings gm": "blake",

        "stan bowman": "bowman",
        "stan bowman (chi)": "bowman",
        "s. bowman": "bowman",
        "s. bowman (chi)": "bowman",
        "s bowman (chi)": "bowman",
        "s bowman": "bowman",
        "bowman (chi)": "bowman",
        "bowman(chi)": "bowman",
        "chi": "bowman",

        "julien brisebois": "brisebois",
        "julian brisebois": "brisebois",
        "julien brise bois": "brisebois",
        "julian brise bois": "brisebois",
        "julien brisebois (tbl)": "brisebois",
        "julian brisebois (tbl)": "brisebois",
        "julien brisebois (tb)": "brisebois",
        "julian brisebois (tb)": "brisebois",
        "j. brisebois (tbl)": "brisebois",
        "j. brisebois (tb)": "brisebois",
        "j. brisebois": "brisebois",
        "j brisebois (tbl)": "brisebois",
        "j brisebois (tb)": "brisebois",
        "j brisebois": "brisebois",
        "brisebois (tbl)": "brisebois",
        "brisebois (tb)": "brisebois",
        "brisebois(tbl)": "brisebois",
        "brisebois(tb)": "brisebois",
        "tbl gm": "brisebois",
        "tb gm": "brisebois",
        "tbl": "brisebois",
        "tb": "brisebois",
        "julien brisbois": "brisebois",
        "j. brisbois": "brisebois",
        "j brisbois": "brisebois",
        "julien briseboise": "brisebois",
        "j. briseboise": "brisebois",
        "j briseboise": "brisebois",
        "j.brisebois": "brisebois",
        "j.brisbois": "brisebois",
        "j.brisboise": "brisebois",
        "bisebois": "brisebois",
        "birsbouis": "brisebois",
        "julien briesebois": "brisebois",
        "biseboise": "brisebois",
        "juilen brisebos": "brisebois",
        "juloen brisbois": "brisebois",
        "julian briseboes": "brisebois",
        "j. briesbois": "brisebois",
        "brisebouis": "brisebois",
        "john brisebois": "brisebois",
        "julia brisebois": "brisebois",
        "broisebois": "brisebois",
        "julien briesbois": "brisebois",
        "julian briesbois": "brisebois",
        "brisbios": "brisebois",
        "briesbois": "brisebois",
        "jbb": "brisebois",
        "brisbois": "brisebois",
        "julien brisbrois": "brisebois",
        "tampa gm": "brisebois",
        "julien brizebois": "brisebois",
        "biresbois": "brisebois",
        "birsebois": "brisebois",
        "julien brisebous": "brisebois",
        "briseboise": "brisebois",
        "brisboi": "brisebois",
        "brisebios": "brisebois",
        "brisebrois": "brisebois",
        "briesebois": "brisebois",
        "julian briesebois": "brisebois",
        "julian birsbois": "brisebois",
        "breisbois": "brisebois",
        "brisebois tb": "brisebois",
        "tampa bay": "brisebois",
        "julien birsbois": "brisebois",
        "brisboise": "brisebois",
        "julien brisbeois": "brisebois",
        "julien brisebrois": "brisebois",

        "kevin cheveldayoff": "cheveldayoff",
        "kevin cheveldayof": "cheveldayoff",
        "kevin cheveldayov": "cheveldayoff",
        "kevin cheveldayoff (wpg)": "cheveldayoff",
        "kevin cheveldayoff (win)": "cheveldayoff",
        "k. cheveldayoff (wpg)": "cheveldayoff",
        "k. cheveldayoff (win)": "cheveldayoff",
        "k. cheveldayoff": "cheveldayoff",
        "k cheveldayoff (wpg)": "cheveldayoff",
        "k cheveldayoff (win)": "cheveldayoff",
        "k cheveldayoff": "cheveldayoff",
        "cheveldayoff (wpg)": "cheveldayoff",
        "cheveldayoff (win)": "cheveldayoff",
        "cheveldayoff(wpg)": "cheveldayoff",
        "cheveldayoff(win": "cheveldayoff",
        "chevy": "cheveldayoff",
        "wpg": "cheveldayoff",
        "win": "cheveldayoff",
        "kevin chevyldayoff": "cheveldayoff",
        "kevin chevaldeyoff": "cheveldayoff",
        "kevin cheveladayoff": "cheveldayoff",
        "chevelydayoff": "cheveldayoff",
        "chevaldayoff": "cheveldayoff",
        "kevin chevaldayof": "cheveldayoff",
        "wpg gm": "cheveldayoff",
        "chevelodayoff": "cheveldayoff",
        "cheveldayof": "cheveldayoff",

        "pierre dorion": "dorion",
        "pierre dorian": "dorion",
        "pierre dorion (ott)": "dorion",
        "p. dorion (ott)": "dorion",
        "p. dorion": "dorion",
        "p dorion (ott)": "dorion",
        "p dorion": "dorion",
        "dorion (ott)": "dorion",
        "dorion(ott)": "dorion",
        "ott": "dorion",
        "doiron": "dorion",
        "dorian": "dorion",
        "pierre doriane": "dorion",
        "ott gm": "dorion",

        "chris drury": "drury",
        "chris drury (nyr)": "drury",
        "chris drury (ny)": "drury",
        "c. drury (nyr)": "drury",
        "c. drury (ny)": "drury",
        "c. drury": "drury",
        "c drury (nyr)": "drury",
        "c drury (ny)": "drury",
        "c drury": "drury",
        "drury (nyr)": "drury",
        "drury (ny)": "drury",
        "drury(nyr)": "drury",
        "drury(ny)": "drury",
        "nyr": "drury",
        "ny rangers": "drury",

        "kyle dubas": "dubas",
        "kyle dubas (tor)": "dubas",
        "kyle dubas (tml)": "dubas",
        "k. dubas (tor)": "dubas",
        "k. dubas (tml)": "dubas",
        "k. dubas": "dubas",
        "k dubas (tor)": "dubas",
        "k dubas (tml)": "dubas",
        "k dubas": "dubas",
        "dubas (tor)": "dubas",
        "dubas (tml)": "dubas",
        "dubas(tor)": "dubas",
        "dubas(tml)": "dubas",
        "tor": "dubas",
        "tml": "dubas",
        "k.dubas": "dubas",

        "tom fitzgerald": "fitzgerald",
        "tom fitzgerald (njd)": "fitzgerald",
        "tom fitzgerald (nj)": "fitzgerald",
        "t. fitzgerald (njd)": "fitzgerald",
        "t. fitzgerald (nj)": "fitzgerald",
        "t. fitzgerald": "fitzgerald",
        "t fitzgerald (njd)": "fitzgerald",
        "t fitzgerald (nj)": "fitzgerald",
        "t fitzgerald": "fitzgerald",
        "fitzgerald (njd)": "fitzgerald",
        "fitzgerald (nj)": "fitzgerald",
        "fitzgerald(njd)": "fitzgerald",
        "fitzgerald(nj)": "fitzgerald",
        "njd": "fitzgerald",
        "nj": "fitzgerald",

        "chuck fletcher": "fletcher",
        "chuck fletcher (phi)": "fletcher",
        "c. fletcher (phi)": "fletcher",
        "c. fletcher": "fletcher",
        "c fletcher (phi)": "fletcher",
        "c fletcher": "fletcher",
        "fletcher (phi)": "fletcher",
        "fletcher(phi)": "fletcher",
        "phi": "fletcher",
        "fletcher phi": "fletcher",
        "phi gm": "fletcher",

        "ron francis": "francis",
        "ron francis (sea)": "francis",
        "r. francis (sea)": "francis",
        "r. francis": "francis",
        "r francis (sea)": "francis",
        "r francis": "francis",
        "francis (sea)": "francis",
        "francis(sea)": "francis",
        "francis (hired july 2019)": "francis",
        "sea": "francis",
        "seattle gm": "francis",
        "ron francis (if he counts he was technically hired early enough)": "francis",
        "r.francis": "francis",
        "kraken gm": "francis",
        "franics": "francis",
        "sea gm": "francis",

        "bill guerin": "guerin",
        "bill guerin (min)": "guerin",
        "b. guerin (min)": "guerin",
        "b. guerin": "guerin",
        "b guerin (min)": "guerin",
        "b guerin": "guerin",
        "guerin (min)": "guerin",
        "guerin(min)": "guerin",
        "min": "guerin",
        "guerrin": "guerin",
        "guerin (minn)": "guerin",
        "minnesota gm": "guerin",
        "geurin": "guerin",
        "b.guerin": "guerin",
        "billy guerin": "guerin",
        "bill geurin": "guerin",
        "bill gudrun": "guerin",
        "bill guerrin": "guerin",

        "ron hextall": "hextall",
        "ron hextall (pit)": "hextall",
        "r. hextall (pit)": "hextall",
        "r. hextall": "hextall",
        "r hextall (pit)": "hextall",
        "r hextall": "hextall",
        "hextall (pit)": "hextall",
        "hextall(pit)": "hextall",
        "pit": "hextall",

        "ken holland": "holland",
        "ken holland (edm)": "holland",
        "k. holland (edm)": "holland",
        "k. holland": "holland",
        "k holland (edm)": "holland",
        "k holland": "holland",
        "holland (edm)": "holland",
        "holland(edm)": "holland",
        "edm": "holland",
        "ken hollland": "holland",
        "oilers gm": "holland",

        "jarmo kekalainen": "kekalainen",
        "jarmo kekalainen (cbj)": "kekalainen",
        "jarmo kekalainen (cb)": "kekalainen",
        "j. kekalainen (cbj)": "kekalainen",
        "j. kekalainen (cb)": "kekalainen",
        "j. kekalainen": "kekalainen",
        "j kekalainen (cbj)": "kekalainen",
        "j kekalainen (cb)": "kekalainen",
        "j kekalainen": "kekalainen",
        "kekalainen (cbj)": "kekalainen",
        "kekalainen (cb)": "kekalainen",
        "kekalainen(cbj)": "kekalainen",
        "kekalainen(cb)": "kekalainen",
        "cbj gm": "kekalainen",
        "cb gm": "kekalainen",
        "clb gm": "kekalainen",
        "cbj": "kekalainen",
        "clb": "kekalainen",
        "cb": "kekalainen",
        "kekalaninen": "kekalainen",
        "columbus": "kekalainen",
        "kekalainan": "kekalainen",
        "jarmmo kekalaien": "kekalainen",
        "jarmo kekäläinen": "kekalainen",
        "jermo kekailainen": "kekalainen",
        "jarmo": "kekalainen",
        "kekalanien": "kekalainen",
        "kekäläinen": "kekalainen",
        "jarmok": "kekalainen",
        "kekalaainen": "kekalainen",
        "jarmo kekelainen": "kekalainen",

        "lou lamoriello": "lamoriello",
        "lou lamoriello (nyi)": "lamoriello",
        "lou lamoriello (ny)": "lamoriello",
        "l. lamoriello (nyi)": "lamoriello",
        "l. lamoriello (ny)": "lamoriello",
        "l. lamoriello": "lamoriello",
        "l lamoriello (nyi)": "lamoriello",
        "l lamoriello (ny)": "lamoriello",
        "l lamoriello (nyi)": "lamoriello",
        "l lamoriello (ny)": "lamoriello",
        "l lamoriello": "lamoriello",
        "lamoriello (nyi)": "lamoriello",
        "lamoriello (ny)": "lamoriello",
        "lamoriello(nyi)": "lamoriello",
        "lamoriello(ny)": "lamoriello",
        "nyi gm": "lamoriello",
        "nyi": "lamoriello",
        "lamarello": "lamoriello",
        "lou lamorello(sry dont know his spellin)": "lamoriello",
        "lou lamorello": "lamoriello",
        "lou lamerello": "lamoriello",
        "lou lamerillo": "lamoriello",
        "lamourello": "lamoriello",
        "lamorilleo": "lamoriello",
        "lamarillo": "lamoriello",
        "ny islanders": "lamoriello",
        "lamoreillo": "lamoriello",
        "lou lamariello": "lamoriello",
        "lou lamirello": "lamoriello",
        "lamorillo": "lamoriello",
        "lamiorello": "lamoriello",
        "lamoreiello": "lamoriello",
        "lou lam": "lamoriello",
        "lou l": "lamoriello",
        "lou lamarello": "lamoriello",
        "lou lamierello": "lamoriello",
        "lamerello": "lamoriello",
        "lamorielllo (nyi)": "lamoriello",
        "lamorello": "lamoriello",
        "lamariello": "lamoriello",
        "lamourillo": "lamoriello",
        "lou": "lamoriello",
        "lamouriello": "lamoriello",
        "lamoille": "lamoriello",
        "l.lamoriello": "lamoriello",
        "lou lamoirello": "lamoriello",
        "lou lamarillo": "lamoriello",
        "luo lamoriello": "lamoriello",
        "lammoriello": "lamoriello",
        "uncle lou": "lamoriello",
        "lou lamiorello": "lamoriello",
        "lou lameriello": "lamoriello",
        "lamerllo": "lamoriello",
        "lamorinello": "lamoriello",
        "lou lamorielo": "lamoriello",

        "brian maclellan": "maclellan",
        "brian maclellan (wsh)": "maclellan",
        "b. maclellan (wsh)": "maclellan",
        "b. maclellan": "maclellan",
        "b maclellan (wsh)": "maclellan",
        "b maclellan": "maclellan",
        "maclellan (wsh)": "maclellan",
        "maclellan(wsh)": "maclellan",
        "wsh gm": "maclellan",
        "wsh": "maclellan",
        "was gm": "maclellan",
        "mcclellan": "maclellan",
        "mclellan": "maclellan",
        "brian mcclellan": "maclellan",
        "brian mclellan": "maclellan",
        "mclelland": "maclellan",
        "macclellan": "maclellan",
        "maclellan (was)": "maclellan",
        "brian macclellan": "maclellan",

        "kelly mccrimmon": "mccrimmon",
        "kelly mccrimmon (veg)": "mccrimmon",
        "kelly mccrimmon (vgk)": "mccrimmon",
        "kelly mccrimmon (lv)": "mccrimmon",
        "k. mccrimmon (veg)": "mccrimmon",
        "k. mccrimmon (vgk)": "mccrimmon",
        "k. mccrimmon (lv)": "mccrimmon",
        "k. mccrimmon": "mccrimmon",
        "k mccrimmon (veg)": "mccrimmon",
        "k mccrimmon (vgk)": "mccrimmon",
        "k mccrimmon (lv)": "mccrimmon",
        "k mccrimmon": "mccrimmon",
        "mccrimmon (veg)": "mccrimmon",
        "mccrimmon (vgk)": "mccrimmon",
        "mccrimmon (lv)": "mccrimmon",
        "mccrimmon(veg)": "mccrimmon",
        "mccrimmon(vgk)": "mccrimmon",
        "mccrimmon(lv)": "mccrimmon",
        "vegas gm": "mccrimmon",
        "vegas": "mccrimmon",
        "veg": "mccrimmon",
        "vgk gm": "mccrimmon",
        "vgk": "mccrimmon",
        "lv gm": "mccrimmon",
        "lv": "mccrimmon",
        "lvk": "mccrimmon",
        "kelly mcrimmon": "mccrimmon",
        "k.mccrimmon": "mccrimmon",
        "knights gm (kelly mccrimmon)": "mccrimmon",
        "mcgrimmon": "mccrimmon",
        "kelly maccrimmon": "mccrimmon",
        "mcrimmon": "mccrimmon",
        "mckrimmon": "mccrimmon",
        "kelly m": "mccrimmon",
        "kelly mckrimmon": "mccrimmon",

        "bob murray": "murray",
        "bob murray (ana)": "murray",
        "b. murray (ana)": "murray",
        "b. murray": "murray",
        "b murray (ana)": "murray",
        "b murray": "murray",
        "murray (ana)": "murray",
        "murray(ana)": "murray",
        "ana": "murray",

        "jim nill": "nill",
        "jim nill (dal)": "nill",
        "j. nill (dal)": "nill",
        "j. nill": "nill",
        "j nill (dal)": "nill",
        "j nill": "nill",
        "nill (dal)": "nill",
        "nill(dal)": "nill",
        "dal": "nill",

        "david poile": "poile",
        "david poile (nash)": "poile",
        "david poile (nsh)": "poile",
        "d. poile (nash)": "poile",
        "d. poile (nsh)": "poile",
        "d. poile": "poile",
        "d poile (nash)": "poile",
        "d poile (nsh)": "poile",
        "d poile": "poile",
        "poile (nash)": "poile",
        "poile (nsh)": "poile",
        "poile(nash)": "poile",
        "poile(nsh)": "poile",
        "nash": "poile",
        "nsh": "poile",
        "poille": "poile",

        "joe sakic": "sakic",
        "joe sakic (col)": "sakic",
        "j. sakic (col)": "sakic",
        "j. sakic": "sakic",
        "j sakic (col)": "sakic",
        "j sakic": "sakic",
        "sakic (col)": "sakic",
        "sakic(col)": "sakic",
        "col gm": "sakic",
        "col": "sakic",
        "sackic": "sakic",
        "salic": "sakic",
        "j.sakic": "sakic",
        "joe sackic": "sakic",
        "sacic": "sakic",
        "joseph sakic": "sakic",
        "burnaby joe": "sakic",
        "sakic col": "sakic",
        "avalanche gm": "sakic",
        "sakick": "sakic",
        "jow sakic": "sakic",
        "jose sakic": "sakic",

        "don sweeney": "sweeney",
        "don sweeney (bos)": "sweeney",
        "don sweeny": "sweeney",
        "don sweeny (bos)": "sweeney",
        "d. sweeney (bos)": "sweeney",
        "d. sweeny (bos)": "sweeney",
        "d. sweeney": "sweeney",
        "d. sweeny": "sweeney",
        "d sweeney (bos)": "sweeney",
        "d sweeny (bos)": "sweeney",
        "d sweeney": "sweeney",
        "d sweeny": "sweeney",
        "sweeny": "sweeney",
        "sweeney (bos)": "sweeney",
        "sweeny (bos)": "sweeney",
        "sweeney(bos)": "sweeney",
        "sweeny(bos)": "sweeney",
        "bos gm": "sweeney",
        "bos": "sweeney",
        "sweeney bos": "sweeney",

        "brad treliving": "treliving",
        "brad treliving (cgy)": "treliving",
        "b. treliving (cgy)": "treliving",
        "b. treliving": "treliving",
        "b treliving (cgy)": "treliving",
        "b treliving": "treliving",
        "treliving (cgy)": "treliving",
        "treliving(cgy)": "treliving",
        "cgy gm": "treliving",
        "cgy": "treliving",

        "don waddell": "waddell",
        "don waddell (car)": "waddell",
        "don waddle": "waddell",
        "d. waddell (car)": "waddell",
        "d. waddle": "waddell",
        "d. waddell": "waddell",
        "d waddell (car)": "waddell",
        "d waddle": "waddell",
        "d waddell": "waddell",
        "waddell (car)": "waddell",
        "waddell(car)": "waddell",
        "car gm": "waddell",
        "car": "waddell",
        "waddel": "waddell",
        "don waddel": "waddell",
        "waddell car": "waddell",
        "wadell": "waddell",
        "donwaddell": "waddell",
        "carolina gm": "waddell",

        "doug wilson": "wilson",
        "doug wilson (sjs)": "wilson",
        "doug wilson (sj)": "wilson",
        "d. wilson (sjs)": "wilson",
        "d. wilson (sj)": "wilson",
        "d. wilson": "wilson",
        "d wilson (sjs)": "wilson",
        "d wilson (sj)": "wilson",
        "d wilson": "wilson",
        "wilson (sjs)": "wilson",
        "wilson (sj)": "wilson",
        "wilson(sjs)": "wilson",
        "wilson(sj)": "wilson",
        "sjs gm": "wilson",
        "sj gm": "wilson",
        "sjs": "wilson",
        "sj": "wilson",

        "steve yzerman": "yzerman",
        "steve yzerman (det)": "yzerman",
        "s. yzerman (det)": "yzerman",
        "s. yzerman": "yzerman",
        "s yzerman (det)": "yzerman",
        "s yzerman": "yzerman",
        "yzerman (det)": "yzerman",
        "yzerman(det)": "yzerman",
        "stevie y": "yzerman",
        "det gm": "yzerman",
        "det": "yzerman",
        "yzermam": "yzerman",
        "steve yserman": "yzerman",
        "steven yzerman": "yzerman",
        "detroit gm": "yzerman",
        "detroit": "yzerman",
        "steve yzermam": "yzerman",
        "steve y": "yzerman",
        "yerman": "yzerman",
        "yzerman det": "yzerman",
        "s.yzerman": "yzerman",
        "stevie yzerman": "yzerman",

        "bill zito": "zito",
        "bill zito (fla)": "zito",
        "bill zito (fl)": "zito",
        "b. zito (fla)": "zito",
        "b. zito (fl)": "zito",
        "b. zito": "zito",
        "b zito (fla)": "zito",
        "b zito (fl)": "zito",
        "b zito": "zito",
        "zito (fla)": "zito",
        "zito (fl)": "zito",
        "zito(fla)": "zito",
        "zito(fl)": "zito",
        "fla gm": "zito",
        "fla": "zito",
        "fl gm": "zito",
        "fl": "zito",
        "bill zeto": "zito",
    }
    q4 = ['q4a1', 'q4a2', 'q4a3', 'q4a4', 'q4a5']
    for question in q4:
        print(f"Standardizing the answers for column {question}")
        # Replace by various names of gms
        df[question].replace(to_replace=gms_dict, value=None, inplace=True)
        print("Done!")

    print("Running special 'armstrong' check for GM's. Many people entered 'armstrong' as an entry, but there are two armstrongs.")
    print("'d armstrong' of St Louis is eligible this year, but 'b armstrong' of Arizona is not.")
    print("In the entries I've had to fix so far, I've defaulted to giving people credit for 'd armstrong' based on his eligibility.")
    print("This will need to be clarified next year.")
    armstrong_count = 0
    for question in q4:
        for index in range(len(df)):
            if df[question].iloc[index] == "armstrong":
                temp_author = authors[index]
                armstrong_count += 1
                print(f"{temp_author}, I fixed your entry")
                print(
                    f"INTERPRETATION WARNING: {temp_author} listed 'armstrong' in their GMs. Interpreting this as 'd armstrong'")
                df.at[index, question] = "d armstrong"

    print(f"This check fixed {armstrong_count} entries.")
    print("This is in addition to some other entries with the same problem fixed previously in this script")
    # Dictionary of variations of goalie names for standardization
    goalie_dict = {
        "0": np.nan,

        "jake allen": "allen",
        "j. allen": "allen",
        "j allen": "allen",
        "j.allen": "allen",

        "frederik andersen": "andersen",
        "frederik anderson": "andersen",
        "freddie andersen": "andersen",
        "freddie andersen": "andersen",
        "f. andersen": "andersen",
        "f. anderson": "andersen",
        "f andersen": "andersen",
        "f anderson": "andersen",
        "anderson": "andersen",
        "f.andersen": "andersen",
        "fred anderson": "andersen",
        "frederick andersen": "andersen",

        "craig anderson": "anderson",

        "jordan binnington": "binnington",
        "j. binnington": "binnington",
        "j binnington": "binnington",
        "binington": "binnington",
        "binnington (stl)": "binnington",
        "bennington": "binnington",
        "bininngton": "binnington",
        "binnigton": "binnington",
        "jordan binnington (stl)": "binnington",
        "j.binnington": "binnington",

        "sergei bobrovsky": "bobrovsky",
        "sergei bobrovski": "bobrovsky",
        "sergei bobrofski": "bobrovsky",
        "s. bobrovsky": "bobrovsky",
        "s. bobrovski": "bobrovsky",
        "s. bobrofski": "bobrovsky",
        "s bobrovsky": "bobrovsky",
        "s bobrovski": "bobrovsky",
        "s bobrofski": "bobrovsky",
        "bob": "bobrovsky",

        "jack campbell": "campbell",
        "j. campbell": "campbell",
        "j campbell": "campbell",

        "thatcher demko": "demko",
        "t. demko": "demko",
        "t demko": "demko",
        "thatcher d": "demko",
        "t. demko": "demko",
        "semko": "demko",
        "dempko": "demko",

        "marc-andre fleury": "fleury",
        "marc andre fleury": "fleury",
        "mark andre fleury": "fleury",
        "marc andrew fleury": "fleury",
        "mark andrew fleury": "fleury",
        "m. a. fleury": "fleury",
        "m.a. fleury": "fleury",
        "m a fleury": "fleury",
        "ma fleury": "fleury",
        "fluery": "fleury",
        "flower": "fleury",
        "feury": "fleury",
        "fleury (chi)": "fleury",
        "flurry": "fleury",
        "maf": "fleury",
        "marc andre fluery": "fleury",
        "m.a fleury": "fleury",
        "m.afleury": "fleury",

        "john gibson": "gibson",
        "j. gibson": "gibson",
        "j gibson": "gibson",
        "jon gibson": "gibson",
        "j.gibson": "gibson",

        "philipp grubauer": "grubauer",
        "philip grubauer": "grubauer",
        "phil grubauer": "grubauer",
        "p. grubauer": "grubauer",
        "p grubauer": "grubauer",
        "phillip grubauer": "grubauer",
        "phillipp grubauer": "grubauer",
        "philipp grabauer": "grubauer",

        "carter hart": "hart",
        "carter heart": "hart",
        "c. hart": "hart",
        "c. heart": "hart",
        "c hart": "hart",
        "c heart": "hart",

        "connor hellebuyck": "hellebuyck",
        "conner hellebuyck": "hellebuyck",
        "c. hellebuyck": "hellebuyck",
        "c hellebuyck": "hellebuyck",
        "hellebucyck": "hellebuyck",
        "c. hellebyuck": "hellebuyck",
        "hellebuyk": "hellebuyck",
        "connor hellybuck": "hellebuyck",
        "hellybuck": "hellebuyck",
        "helly": "hellebuyck",
        "connor hellyebuck": "hellebuyck",
        "helebyuk": "hellebuyck",
        "hellebucyk": "hellebuyck",
        "connor hellebyuck": "hellebuyck",
        "connor hellebuyck (wpg)": "hellebuyck",
        "connor hellebuyc": "hellebuyck",
        "hellebuyuk": "hellebuyck",
        "conor h": "hellebuyck",
        "conor hellebuyck": "hellebuyck",
        "connor helleybuck": "hellebuyck",
        "connor h": "hellebuyck",
        "hellabuck": "hellebuyck",
        "hellebuych": "hellebuyck",
        "c helleybuck": "hellebuyck",
        "c.hellebuyck": "hellebuyck",
        "conner hellebucyk": "hellebuyck",
        "connor heelebuyck": "hellebuyck",
        "connor hellbuyck": "hellebuyck",
        "connor hellebuck": "hellebuyck",
        "connor hellebucyk": "hellebuyck",
        "connor hellebuyk": "hellebuyck",
        "connor hellebyck": "hellebuyck",
        "connor hellebyuck (wpg)": "hellebuyck",
        "connor helleybuyck": "hellebuyck",
        "connor hellybuyck": "hellebuyck",
        "conor hellybuck": "hellebuyck",
        "hellyubuk": "hellebuyck",
        "hellebuyck (wpg)": "hellebuyck",
        "hellebuyuck": "hellebuyck",
        "hellebuyuck (wpg)": "hellebuyck",
        "hellebyck": "hellebuyck",
        "hellebyuck": "hellebuyck",
        "hellenbuyck": "hellebuyck",
        "hellenbyck": "hellebuyck",
        "helleybuck": "hellebuyck",
        "helleybuyck": "hellebuyck",
        "helllebucyk": "hellebuyck",
        "helllebuyck": "hellebuyck",
        "hellybuyck": "hellebuyck",
        "hellyebuck": "hellebuyck",
        "hellyebuyck": "hellebuyck",
        "hellyubuk": "hellebuyck",
        "heebuyck": "hellebuyck",
        "helabyuck": "hellebuyck",
        "helebucyk": "hellebuyck",
        "helebuyck": "hellebuyck",
        "hellbuyck": "hellebuyck",
        "hellbyuck": "hellebuyck",
        "hellebuck": "hellebuyck",
        "hullybuck": "hellebuyck",

        "adin hill": "hill",
        "a. hill": "hill",
        "a hill": "hill",
        "hill (sjs)": "hill",
        "hill (sj)": "hill",

        "carter hutton": "hutton",
        "c. hutton": "hutton",
        "c hutton": "hutton",
        "hutton (ari)": "hutton",

        "joonas korpisalo": "korpisalo",
        "jonas korpisalo": "korpisalo",
        "j. korpisalo": "korpisalo",
        "j korpisalo": "korpisalo",
        "korpi": "korpisalo",

        "darcy kuemper": "kuemper",
        "darcy kemper": "kuemper",
        "d. kuemper": "kuemper",
        "d. kemper": "kuemper",
        "d kuemper": "kuemper",
        "d kemper": "kuemper",
        "kemper": "kuemper",
        "keumper": "kuemper",
        "kempur": "kuemper",
        "darcey kuemper": "kuemper",
        "darcy kuemper (col)": "kuemper",

        "kevin lankinen": "lankinen",
        "k. lankinen": "lankinen",
        "lankinen": "lankinen",

        "robin lehner": "lehner",
        "r. lehner": "lehner",
        "r lehner": "lehner",
        "lehener": "lehner",
        "lehner (vgk)": "lehner",
        "lehrer": "lehner",
        "robin lehner (wgk)": "lehner",
        "lehnar": "lehner",
        "lenher": "lehner",
        "robin l": "lehner",
        "robin l.": "lehner",
        "robin lehner (vgk)": "lehner",
        "robin lehrner": "lehner",
        "robyn l": "lehner",

        "jacob markstrom": "markstrom",
        "jacob markström": "markstrom",
        "jacob marksrom": "markstrom",
        "j. markstrom": "markstrom",
        "j. markström": "markstrom",
        "j markstrom": "markstrom",
        "j markström": "markstrom",
        "markström": "markstrom",
        "jakob markstrom": "markstrom",
        "marsktrom": "markstrom",
        "jakov markstom": "markstrom",
        "markstrom (cgy)": "markstrom",
        "markstrom (cal)": "markstrom",
        "markstron": "markstrom",
        "markstrum": "markstrom",
        "j.markstrom": "markstrom",
        "jacob m": "markstrom",
        "jacob markstrom (cgy)": "markstrom",
        "jakob markstom": "markstrom",
        "jakob markstorm": "markstrom",
        "j.markström": "markstrom",
        "jacob markström (cgy)": "markstrom",

        "elvis merzlikins": "merzlikins",
        "e. merzlikins": "merzlikins",
        "e merzlikins": "merzlikins",
        "merzlinkis": "merzlikins",

        "matt murray": "murray",
        "m. murray": "murray",
        "m murray": "murray",

        "alex nedeljkovic": "nedeljkovic",
        "a. nedeljkovic": "nedeljkovic",
        "a nedeljkovic": "nedeljkovic",
        "nedjelkovic": "nedeljkovic",
        "nedelijkovic": "nedeljkovic",
        "nedeljkovich": "nedeljkovic",
        "alex nedelkjovic": "nedeljkovic",

        "calvin petersen": "petersen",
        "calvin peterson": "petersen",
        "cal petersen": "petersen",
        "cal peterson": "petersen",
        "c. petersen": "petersen",
        "c. peterson": "petersen",
        "c petersen": "petersen",
        "c peterson": "petersen",
        "peterson": "petersen",
        "cal pederson": "petersen",

        "carey price": "price",
        "c. price": "price",
        "c price": "price",

        "james reimer": "reimer",
        "james riemer": "reimer",
        "j. reimer": "reimer",
        "j. riemer": "reimer",
        "j reimer": "reimer",
        "j riemer": "reimer",
        "riemer": "reimer",

        "juuse saros": "saros",
        "juicy saros": "saros",
        "juice saros": "saros",
        "j. saros": "saros",
        "j saros": "saros",
        "jusee saros": "saros",
        "sarros": "saros",
        "suros": "saros",
        "soros": "saros",
        "saaros": "saros",
        "saros (nsh)": "saros",
        "jusse saros": "saros",
        "jussi saaros": "saros",
        "jussi sarros": "saros",
        "jusso saros": "saros",
        "juuso saros": "saros",

        "igor shesterkin": "shesterkin",
        "i. shesterkin": "shesterkin",
        "i shesterkin": "shesterkin",
        "shesterskin": "shesterkin",
        "shersterkin": "shesterkin",
        "sheshterkin": "shesterkin",
        "shestyorkin": "shesterkin",
        "igor s": "shesterkin",
        "igor shersterkin": "shesterkin",
        "igor sherstorkin": "shesterkin",
        "igor sheshterkin": "shesterkin",

        "mike smith": "smith",
        "m. smith": "smith",
        "m smith": "smith",

        "cam talbot": "talbot",
        "c. talbot": "talbot",
        "c talbot": "talbot",

        "linus ullmark": "ullmark",
        "linus ulmark": "ullmark",
        "l. ullmark": "ullmark",
        "l. ulmark": "ullmark",
        "l ullmark": "ullmark",
        "l ulmark": "ullmark",
        "ulmark": "ullmark",

        "semyon varlamov": "varlamov",
        "varlarmov": "varlamov",

        "andrei vasilevskiy": "vasilevskiy",
        "andre vasilevskiy": "vasilevskiy",
        "andrei vasilevski": "vasilevskiy",
        "a. vasilevskiy": "vasilevskiy",
        "a vasilevskiy": "vasilevskiy",
        "vasilskiey": "vasilevskiy",
        "vasi": "vasilevskiy",
        "vasy": "vasilevskiy",
        "andre vaislevskiy": "vasilevskiy",
        "vaislevskiy": "vasilevskiy",
        "andre vasileskiy": "vasilevskiy",
        "vasileskiy": "vasilevskiy",
        "andre vassilevsky": "vasilevskiy",
        "vassilevsky": "vasilevskiy",
        "andrei vaselevskiy": "vasilevskiy",
        "vaselevskiy": "vasilevskiy",
        "andrei vasilesvksiy (tbl)": "vasilevskiy",
        "andrei vaseilevskiy (tbl)": "vasilevskiy",
        "vasilevakiy": "vasilevskiy",
        "visilievsky": "vasilevskiy",
        "vasilevaky": "vasilevskiy",
        "andrei vasilevskiy": "vasilevskiy",
        "vasielevskiy": "vasilevskiy",
        "andrei vasileviskiy": "vasilevskiy",
        "vasilevskyi": "vasilevskiy",
        "vasilevslky": "vasilevskiy",
        "andrei vasilievskey": "vasilevskiy",
        "andrei vasilesvkiy": "vasilevskiy",
        "andrei vasiliesky": "vasilevskiy",
        "vasilevkiy": "vasilevskiy",
        "andrei vasilesvkiy (tbl)": "vasilevskiy",
        "andrei vasilevskiy (tbl)": "vasilevskiy",
        "vazilevskiy": "vasilevskiy",
        "andrea vasilevsky": "vasilevskiy",
        "vaslievskiy": "vasilevskiy",
        "vasilievski": "vasilevskiy",
        "vas": "vasilevskiy",
        "vasilievsky": "vasilevskiy",
        "andrei vasilevskey": "vasilevskiy",
        "a vasilevsky": "vasilevskiy",
        "a.vasilevsky": "vasilevskiy",
        "anderi vasilevskiy": "vasilevskiy",
        "andre vasileskly": "vasilevskiy",
        "andre vasilevesky": "vasilevskiy",
        "andre vasilevsky": "vasilevskiy",
        "andrei v": "vasilevskiy",
        "andrei vasikevski": "vasilevskiy",
        "andrei vasilevesky": "vasilevskiy",
        "andrei vasilevsky": "vasilevskiy",
        "andrei vasilievskiy": "vasilevskiy",
        "andrei vasilievsky": "vasilevskiy",
        "andrei vasiliievski": "vasilevskiy",
        "andrei vasivleskiy": "vasilevskiy",
        "andrei vesalevskey": "vasilevskiy",
        "andrej vasilevski": "vasilevskiy",
        "andrew vasilevskiy": "vasilevskiy",
        "andrew vasilevskiy (tbl)": "vasilevskiy",
        "andrew vasilevsky": "vasilevskiy",
        "andriy vasilevskiy": "vasilevskiy",
        "vaselevski": "vasilevskiy",
        "vaselevskii": "vasilevskiy",
        "vasi tb": "vasilevskiy",
        "vasielevski": "vasilevskiy",
        "vasikevskiy": "vasilevskiy",
        "vasile skin": "vasilevskiy",
        "vasilekskiy": "vasilevskiy",
        "vasileski": "vasilevskiy",
        "vasilesky": "vasilevskiy",
        "vasilesky (tb)": "vasilevskiy",
        "vasilesvkiy": "vasilevskiy",
        "vasilevesky": "vasilevskiy",
        "vasilevksiy": "vasilevskiy",
        "vasilevskey": "vasilevskiy",
        "vasilevski": "vasilevskiy",
        "vasilevski (tbl)": "vasilevskiy",
        "vasilevskiey": "vasilevskiy",
        "vasilevskiy (tbl)": "vasilevskiy",
        "vasilevskiy hellebuyck": "vasilevskiy",
        "vasilevsky": "vasilevskiy",
        "vasiliesky": "vasilevskiy",
        "vasiljevsky": "vasilevskiy",
        "vasilveskiy": "vasilevskiy",
        "vasilvesky": "vasilevskiy",
        "vaslevskiy": "vasilevskiy",
        "vaslievsky": "vasilevskiy",
        "vasylevski": "vasilevskiy",

        "vitek vanecek": "vanecek",
        "vitek vanacek": "vanecek",
        "v. vanecek": "vanecek",
        "v. vanacek": "vanecek",
        "v vanecek": "vanecek",
        "v vanacek": "vanecek",
        "vanacek": "vanecek",


    }
    q5 = ['q5a1', 'q5a2', 'q5a3', 'q5a4', 'q5a5']
    for question in q5:
        print(f"Standardizing the answers for column {question}")
        # Replace by various names of goalies
        df[question].replace(to_replace=goalie_dict, value=None, inplace=True)
        print("Done!")
    # Dictionary of variations of rookie names for standardization
    rookie_dict = {
        "0": np.nan,

        "matty beniers": "beniers",
        "beniers": "beniers",
        "m. beniers": "beniers",

        "matthew boldy": "boldy",
        "mattew boldy": "boldy",
        "matt boldy": "boldy",
        "boldy": "boldy",
        "m. boldy": "boldy",
        "m.boldy": "boldy",
        "m boldy": "boldy",

        "evan bouchard": "bouchard",
        "bouchard": "bouchard",
        "e. bouchard": "bouchard",
        "e bouchard": "bouchard",

        "michael bunting": "bunting",
        "bunting": "bunting",
        "m bunting": "bunting",

        "quinton byfield": "byfield",
        "byfield": "byfield",
        "q byfield": "byfield",
        "q. byfield": "byfield",
        "q.byfield": "byfield",
        "quentin byfield": "byfield",
        "quinton byfeld": "byfield",
        "quiton byfield": "byfield",
        "quninton byfield": "byfield",

        "bowen byram": "byram",
        "byram": "byram",
        "bowan byram": "byram",
        "bowen bryan": "byram",
        "bowen byran": "byram",
        "b. byram": "byram",
        "bo byram": "byram",
        "bynam": "byram",
        "byram (col)": "byram",
        "byrom": "byram",
        "byrum": "byram",

        "alexandre carrier": "carrier",
        "alexander carrier": "carrier",
        "alex carrier": "carrier",
        "carrier": "carrier",
        "a. carrier": "carrier",

        "cole caufield": "caufield",
        "caufield": "caufield",
        "c caufield": "caufield",
        "c caulfield": "caufield",
        "c. caufield": "caufield",
        "c. caulfield": "caufield",
        "c.caufield": "caufield",
        "calufield": "caufield",
        "canfield": "caufield",
        "caufeild": "caufield",
        "caufeld": "caufield",
        "caufield (mon)": "caufield",
        "caufield (mtl)": "caufield",
        "caufiled": "caufield",
        "caufiueld": "caufield",
        "cauflield": "caufield",
        "caulfeld": "caufield",
        "caulfied": "caufield",
        "caulfield": "caufield",
        "caulfired": "caufield",
        "claufield": "caufield",
        "coke caufeild": "caufield",
        "cole c": "caufield",
        "cole canfield": "caufield",
        "cole caufeild": "caufield",
        "cole caufeild (mtl)": "caufield",
        "cole caufied": "caufield",
        "cole caufield (mtl)": "caufield",
        "cole caulfield": "caufield",
        "cole claufield": "caufield",
        "goal caufield": "caufield",

        "yegor chinakhov": "chinakhov",
        "chinakhov": "chinakhov",
        "chinakov": "chinakhov",

        "jamie drysdale": "drysdale",
        "drysdale": "drysdale",
        "jamie  drysdale": "drysdale",
        "jaime drysdale": "drysdale",
        "j. drysdale": "drysdale",
        "drysdale (ana)": "drysdale",

        "william eklund": "eklund",
        "eklund": "eklund",
        "ekland": "eklund",
        "w. eklund": "eklund",
        "englund": "eklund",

        "filip gustavsson": "gustavsson",
        "gustavsson": "gustavsson",
        "f. gustavsson": "gustavsson",

        "cal foote": "c foote",
        "foote": "c foote",

        "alexander holtz": "holtz",
        "alexandre holtz": "holtz",
        "alex holtz": "holtz",
        "holtz": "holtz",
        "a. holtz": "holtz",
        "a.holtz": "holtz",
        "a holtz": "holtz",

        "jacob peterson": "peterson",
        "peterson": "peterson",

        "seth jarvis": "jarvis",
        "jarvis": "jarvis",

        "kaapo kahkonen": "kahkonen",
        "kahkonen": "kahkonen",

        "arthur kaliyev": "kaliyev",
        "kaliyev": "kaliyev",
        "a kaliyev": "kaliyev",

        "knight": "knight",
        "specer knight": "knight",
        "spencer k": "knight",
        "spencer knight": "knight",
        "spencer knight (fla)": "knight",
        "spencer knightr": "knight",
        "spenser knight": "knight",
        "s knight": "knight",
        "s. knight": "knight",
        "s.knight": "knight",
        "knight (fla)": "knight",
        "knight (spencer)": "knight",

        "vitaly kravtsov": "kravtsov",
        "kravtsov": "kravtsov",
        "kravstov": "kravtsov",

        "peyton krebs": "krebs",
        "krebs": "krebs",

        "hendrix lapierre": "lapierre",
        "lapierre": "lapierre",

        "anton lundell": "lundell",
        "lundell": "lundell",

        "connor mcmichael": "mcmichael",
        "mcmichael": "mcmichael",
        "c mcmichael": "mcmichael",

        "dawson mercer": "mercer",
        "mercer": "mercer",
        "dawson mercer baby!": "mercer",

        "nedeljkovic": "nedeljkovic",
        "ned in drw": "nedeljkovic",
        "nedejlkovic": "nedeljkovic",
        "nedelijokic": "nedeljkovic",
        "nedeljkovich": "nedeljkovic",
        "nedelkovic": "nedeljkovic",
        "nedelkovich": "nedeljkovic",
        "nedjelkovic": "nedeljkovic",
        "nejdelkovic": "nedeljkovic",
        "a nedjelkovic": "nedeljkovic",
        "a. nedeljkovic": "nedeljkovic",
        "alex nedeljkovic": "nedeljkovic",
        "alex nedeljkovic (det)": "nedeljkovic",
        "alex nedjelkovic": "nedeljkovic",

        "jake neighbours": "neighbours",
        "neighbours": "neighbours",
        "neighbors": "neighbours",

        "alex newhook": "newhook",
        "newhook": "newhook",
        "a. newhook": "newhook",

        "nils lundkvist": "lundkvist",
        "lundkvist": "lundkvist",
        "nils lundquist": "lundkvist",

        "owen power": "power",
        "power": "power",
        "o. power": "power",

        "cole perfetti": "perfetti",
        "perfetti": "perfetti",

        "john peterka": "peterka",
        "peterka": "peterka",

        "shane pinto": "pinto",
        "pinto": "pinto",
        "shane pinkto": "pinto",
        "s.pinto": "pinto",
        "sane pinto": "pinto",

        "vasily podkolzin": "podkolzin",
        "podkolzin": "podkolzin",
        "v. podkolzin": "podkolzin",
        "valery podkolzin": "podkolzin",
        "vasili podkolzin": "podkolzin",
        "vasiliy podkolzin": "podkolzin",
        "vasily p": "podkolzin",
        "vasily podklzin": "podkolzin",
        "vasily podzilkin": "podkolzin",
        "vasily podzkolin": "podkolzin",
        "podkolzn": "podkolzin",
        "podzolkin": "podkolzin",

        "taylor raddysh": "raddysh",
        "raddysh": "raddysh",

        "jack rathbone": "rathbone",
        "rathbone": "rathbone",

        "lucas raymond": "raymond",
        "raymond": "raymond",
        "lucas raymond (det)": "raymond",
        "raymond (det)": "raymond",

        "lukas reichel": "reichel",
        "reichel": "reichel",

        "nick robertson": "robertson",
        "robertson": "robertson",
        "n robertson": "robertson",

        "marco rossi": "rossi",
        "rossi": "rossi",
        "m rossi": "rossi",

        "scott perunovich": "perunovich",
        "perunovich": "perunovich",

        "moritz seider": "seider",
        "seider": "seider",
        "mo seider": "seider",
        "moreitz seider": "seider",
        "moritz seider (det)": "seider",
        "moritz sieder": "seider",
        "m. seider": "seider",
        "m seider": "seider",
        "m.seider": "seider",
        "mortiz seider": "seider",
        "zeider": "seider",
        "seider (det)": "seider",
        "sieder": "seider",
        "seidel": "seider",
        "seoder": "seider",

        "cole sillinger": "sillinger",
        "sillinger": "sillinger",
        "c. sillinger": "sillinger",

        "jeremy swayman": "swayman",
        "swayman": "swayman",
        "jeremey swayman": "swayman",
        "jeremy s": "swayman",
        "swaymam": "swayman",

        "vladimir tkachev": "tkachev",
        "tkachev": "tkachev",
        "tkachyov": "tkachev",

        "philip tomasino": "tomasino",
        "tomasino": "tomasino",
        "tomassino": "tomasino",

        "trevor zegras": "zegras",
        "zegras": "zegras",
        "travis zegras": "zegras",
        "trevor segras": "zegras",
        "trevor z": "zegras",
        "trevor zagras": "zegras",
        "trevor zegas": "zegras",
        "trevor zegras (ana)": "zegras",
        "trevor zegres": "zegras",
        "trevor zigras": "zegras",
        "t zegras": "zegras",
        "t. zegras": "zegras",
        "t.zegras": "zegras",
        "zebras": "zegras",
        "zegra": "zegras",
        "segras": "zegras",
        "zegras (ana)": "zegras",
        "zegres": "zegras",
        "zeigras": "zegras",
        "zergas": "zegras",
        "zehra’s": "zegras",

    }
    q6 = ['q6a1', 'q6a2', 'q6a3', 'q6a4', 'q6a5']
    for question in q6:
        print(f"Standardizing the answers for column {question}")
        # Replace by various names of calder candidates
        df[question].replace(to_replace=rookie_dict, value=None, inplace=True)
        print("Done!")
    # Dictionary of variations of defense names for standardization
    dmen_dict = {
        "0": np.nan,

        "sebastian aho": "aho (d)",
        "aho (d)": "aho (d)",

        "tyson barrie": "barrie",
        "barrie": "barrie",

        "brent burns": "burns",
        "burns": "burns",

        "john carlson": "carlson",
        "carlson": "carlson",
        "carlson (wsh)": "carlson",
        "j. carlson": "carlson",
        "j. carlson (wsh)": "carlson",

        "thomas chabot": "chabot",
        "chabot": "chabot",

        "jakob chychrun": "chychrun",
        "chychrun": "chychrun",
        "jacob chychrun": "chychrun",

        "rasmus dahlin": "dahlin",
        "dahlin": "dahlin",

        "drew doughty": "doughty",
        "doughty": "doughty",

        "aaron ekblad": "ekblad",
        "ekblad": "ekblad",

        "mario ferraro": "ferraro",
        "ferraro": "ferraro",

        "adam fox": "fox",
        "fox": "fox",
        "adam fox (nyr)": "fox",
        "andy fox": "fox",
        "a fox": "fox",
        "a. fox": "fox",
        "a.fox": "fox",
        "adam f": "fox",
        "fox (nyr)": "fox",

        "mark giordano": "giordano",
        "giordano": "giordano",

        "samuel girard": "girard",
        "girard": "girard",
        "sam girard": "girard",

        "dougie hamilton": "hamilton",
        "hamilton": "hamilton",
        "doug hamilton": "hamilton",
        "douggie hamilton": "hamilton",
        "dougie": "hamilton",
        "dougie hamilton (njd)": "hamilton",
        "d hamilton": "hamilton",
        "d hamlton": "hamilton",
        "d. hamilton": "hamilton",
        "d.hamilton": "hamilton",
        "hamiliton": "hamilton",
        "hamilston": "hamilton",
        "hamiltom": "hamilton",
        "hamilton (njd)": "hamilton",

        "noah hanifin": "hanifin",
        "hanifin": "hanifin",

        "miro heiskanen": "heiskanen",
        "heiskanen": "heiskanen",
        "miro heskainen": "heiskanen",
        "miro heskinen": "heiskanen",
        "miro hieskanan": "heiskanen",
        "m heiskenan": "heiskanen",
        "m. heiskanen": "heiskanen",
        "heiskenan": "heiskanen",
        "heiskenen": "heiskanen",
        "heiskenin": "heiskanen",
        "heiskinen": "heiskanen",
        "heskinan": "heiskanen",
        "heskinen": "heiskanen",
        "hieskanen": "heiskanen",

        "quinn hughes": "q hughes",
        "hughes": "q hughes",
        "quin hughes": "q hughes",
        "quinn h": "q hughes",
        "q hughes": "q hughes",
        "q. hughes": "q hughes",
        "q.hughes": "q hughes",
        "hughes (q)": "q hughes",

        "roman josi": "josi",
        "josi": "josi",
        "roman jossi": "josi",
        "roman jossie": "josi",
        "r. josi": "josi",
        "r.josi": "josi",

        "erik karlsson": "karlsson",
        "karlsson": "karlsson",
        "e. karlsson": "karlsson",

        "duncan keith": "keith",
        "keith": "keith",

        "kris letang": "letang",
        "letang": "letang",

        "cale makar": "makar",
        "makar": "makar",
        "cale makar (col)": "makar",
        "cale maker": "makar",
        "cole makar": "makar",
        "cole makar (col)": "makar",
        "cole maker": "makar",
        "cal makar": "makar",
        "cale m": "makar",
        "c makar": "makar",
        "c.makar": "makar",
        "c. makar": "makar",
        "makar (col)": "makar",
        "makarov": "makar",
        "maker": "makar",
        "makes": "makar",
        "makkar": "makar",
        "całe makar": "makar",

        "charlie mcavoy": "mcavoy",
        "mcavoy": "mcavoy",
        "charlie macavoy": "mcavoy",
        "charlie macvoy": "mcavoy",
        "charlie mcavoy (bos)": "mcavoy",
        "charlie m": "mcavoy",
        "c mcavoy": "mcavoy",
        "c. mcavoy": "mcavoy",
        "mcavoy (bos)": "mcavoy",
        "macavoy": "mcavoy",
        "mccavoy": "mcavoy",
        "mccovoy": "mcavoy",
        "mcevoy": "mcavoy",
        "mcovoy": "mcavoy",

        "jake muzzin": "muzzin",
        "muzzin": "muzzin",

        "darnell nurse": "nurse",
        "nurse": "nurse",
        "nurse (edm)": "nurse",

        "colton paryako": "parayko",
        "parakyo": "parayko",

        "adam pelech": "pelech",
        "pelech": "pelech",

        "jeff petry": "petry",
        "petry": "petry",
        "perry": "petry",

        "alex pietrangelo": "pietrangelo",
        "pietrangelo": "pietrangelo",
        "alex pieterangelo": "pietrangelo",
        "alex pieteranglo": "pietrangelo",
        "a pietrangelo": "pietrangelo",
        "peitrangelo": "pietrangelo",
        "peterangelo": "pietrangelo",
        "petro": "pietrangelo",
        "piatrangelo": "pietrangelo",
        "pieterangelo": "pietrangelo",
        "pietranglo": "pietrangelo",
        "pietriangelo": "pietrangelo",

        "ivan provorov": "provorov",
        "provorov": "provorov",

        "ryan pulock": "pulock",
        "pulock": "pulock",

        "morgan rielly": "rielly",
        "rielly": "rielly",
        "morgan reilly": "rielly",
        "reilly": "rielly",

        "mikhail sergachev": "sergachev",
        "sergachev": "sergachev",

        "seth jones": "jones",
        "jones": "jones",
        "seth j": "jones",
        "s jones": "jones",
        "s. jones": "jones",
        "(seth) jones": "jones",

        "shea theodore": "theodore",
        "theodore": "theodore",
        "shea theadore": "theodore",
        "sheatheodore": "theodore",
        "s. theodore": "theodore",
        "theadore": "theodore",
        "thedore": "theodore",
        "theordore": "theodore",

        "jaccob slavin": "slavin",
        "slavin": "slavin",
        "jacob slavin": "slavin",
        "slavvin": "slavin",

        "jared spurgeon": "spurgeon",
        "spurgeon": "spurgeon",

        "devon toews": "d toews",
        "toews": "d toews",
        "d. toews": "d toews",

        "victor hedman": "hedman",
        "hedman": "hedman",
        "victim hedman": "hedman",
        "victor h": "hedman",
        "victor headman": "hedman",
        "victor hedamn": "hedman",
        "victor hedman (tbl)": "hedman",
        "victor hedmen": "hedman",
        "victor herman": "hedman",
        "viktor hedman": "hedman",
        "viktor heman": "hedman",
        "v hedman": "hedman",
        "v. hedman": "hedman",
        "v.hedman": "hedman",
        "headman": "hedman",
        "herman": "hedman",
        "hedmam": "hedman",
        "hedman (tb)": "hedman",
        "hedman (tbl)": "hedman",
        "hedmon": "hedman",
        "heldman": "hedman",

        "mackenzie weegar": "weegar",
        "weegar": "weegar",
        "m. weegar": "weegar",
        "m.weegar": "weegar",
        "weeger": "weegar",
        "wegar": "weegar",

        "zach werenski": "werenski",
        "werenski": "werenski",
    }
    q7 = ['q7a1', 'q7a2', 'q7a3', 'q7a4', 'q7a5']
    for question in q7:
        print(f"Standardizing the answers for column {question}")
        # Replace by various names of norris candidates
        df[question].replace(to_replace=dmen_dict, value=None, inplace=True)
        print("Done!")
    # Dictionary of variations of hart candidate names for standardization
    hart_dict = {
        "0": np.nan,

        "sebastian aho": "aho (f)",
        "aho": "aho (f)",
        "aho (car)": "aho (f)",

        "aleksander barkov": "barkov",
        "barkov": "barkov",
        "alexander barkov": "barkov",
        "alexander barskov": "barkov",
        "alexsander barkov": "barkov",
        "aleksandar barkov": "barkov",
        "aleksander barkkov": "barkov",
        "aleksandr barkov": "barkov",
        "alex barkov": "barkov",
        "alex barkov (fla)": "barkov",
        "a. barkov": "barkov",
        "barkiv": "barkov",
        "barkov (fla)": "barkov",
        "sasha barkov": "barkov",
        "barlow": "barkov",

        "mathew barzal": "barzal",
        "barzal": "barzal",
        "matthew barzal": "barzal",

        "sean coutourier": "coutourier",
        "couturier": "coutourier",

        "sidney crosby": "crosby",
        "crosby": "crosby",
        "sidney c": "crosby",
        "sydney crosby": "crosby",
        "s crosby": "crosby",
        "crosby (pit)": "crosby",

        "leon draisaitl": "draisaitl",
        "draisaitl": "draisaitl",
        "leon draisaital": "draisaitl",
        "leon draisaitil": "draisaitl",
        "leon draisaitl (edm)": "draisaitl",
        "leon draisatl": "draisaitl",
        "leon draisitl": "draisaitl",
        "leon draistaitl": "draisaitl",
        "leon drasaitl": "draisaitl",
        "leon dreisaitl": "draisaitl",
        "leon d": "draisaitl",
        "leon d.": "draisaitl",
        "l draisaitl": "draisaitl",
        "l. draisaitl": "draisaitl",
        "leon": "draisaitl",
        "draisaitl (edm)": "draisaitl",
        "draisaitle": "draisaitl",
        "draisatil": "draisaitl",
        "draisatl": "draisaitl",
        "draisetal": "draisaitl",
        "draisital": "draisaitl",
        "draisitl": "draisaitl",
        "draistail": "draisaitl",
        "draistaitl": "draisaitl",
        "draistatl": "draisaitl",
        "draistl": "draisaitl",
        "drasaitl": "draisaitl",
        "drasital": "draisaitl",
        "dreisaitl": "draisaitl",
        "driasaittl": "draisaitl",
        "drai": "draisaitl",
        "draisailt": "draisaitl",
        "draisaital": "draisaitl",
        "draisaitil": "draisaitl",

        "aaron ekblad": "ekblad",
        "ekblad": "ekblad",

        "marc andre fleury": "fleury",
        "fleury": "fleury",

        "adam fox": "fox",
        "fox": "fox",

        "victor hedman": "hedman",
        "hedman": "hedman",

        "connor hellebuyck": "hellebuyck",
        "hellebuyck": "hellebuyck",
        "connor hellyebuck": "hellebuyck",
        "c. hellebuyck": "hellebuyck",
        "hellebuck": "hellebuyck",

        "roope hintz": "hintz",
        "hintz": "hintz",

        "jack hughes": "hughes",
        "j hughes": "hughes",

        "jonathan huberdeau": "huberdeau",
        "huberdeau": "huberdeau",

        "seth jones": "jones",
        "s.jones": "jones",

        "patrick kane": "kane",
        "kane": "kane",
        "kane (patrick)": "kane",
        "patty kane": "kane",
        "pkane": "kane",
        "p kane": "kane",
        "p. kane": "kane",
        "p. kane (initial probably unnecessary)": "kane",
        "p.kane": "kane",
        "kane88": "kane",

        "kirill kaprizov": "kaprizov",
        "kaprizov": "kaprizov",
        "kiril kaprizov": "kaprizov",
        "kirill kaprisov": "kaprizov",
        "kaprisov": "kaprizov",
        "karprizov": "kaprizov",
        "kiprizov": "kaprizov",

        "nikita kucherov": "kucherov",
        "kucherov": "kucherov",
        "nikita kucharov": "kucherov",
        "nikita kucherov (tbl)": "kucherov",
        "nikita kuscherov": "kucherov",
        "n kucherov": "kucherov",
        "n. kucherov": "kucherov",
        "kucherov (tbl)": "kucherov",
        "kuchorov": "kucherov",
        "kuckerov": "kucherov",
        "kusherov": "kucherov",

        "anders lee": "lee",
        "lee": "lee",

        "nathan mackinnon": "mackinnon",
        "mackinnon": "mackinnon",
        "nathan mackinnon (col)": "mackinnon",
        "nathan mackinon": "mackinnon",
        "nathan makinnon": "mackinnon",
        "nathan mckinnion": "mackinnon",
        "nathan mckinnon": "mackinnon",
        "nate mackinnon": "mackinnon",
        "n mackinnon": "mackinnon",
        "n. mackinnon": "mackinnon",
        "n. mackinon": "mackinnon",
        "n.mackinnon": "mackinnon",
        "nathan m": "mackinnon",
        "mackininon": "mackinnon",
        "mackinnin": "mackinnon",
        "makinnon": "mackinnon",
        "mackinnion": "mackinnon",
        "mackinnon (col)": "mackinnon",
        "mackinon": "mackinnon",
        "mckinnon": "mackinnon",
        "mckinnon (col)": "mackinnon",
        "mckinon": "mackinnon",
        "mckìnnon": "mackinnon",

        "cale makar": "makar",
        "makar": "makar",
        "c. makar": "makar",

        "brad marchand": "marchand",
        "marchand": "marchand",
        "b marchand": "marchand",

        "mitch marner": "marner",
        "marner": "marner",
        "mitchell marner": "marner",
        "m. marner": "marner",

        "auston matthews": "matthews",
        "matthews": "matthews",
        "austin matthews": "matthews",
        "austen matthews": "matthews",
        "austin mathews": "matthews",
        "auston mathews": "matthews",
        "auston matthews (tor)": "matthews",
        "austonmatthews": "matthews",
        "austin m": "matthews",
        "a matthews": "matthews",
        "a. matthews": "matthews",
        "a.matthews": "matthews",
        "matthews (austin)": "matthews",
        "matthews (tor)": "matthews",
        "mathews": "matthews",
        "matthew": "matthews",
        "matthew's": "matthews",
        "auston matthew’s": "matthews",
        "matthew’s": "matthews",

        "connor mcdavid": "mcdavid",
        "mcdavid": "mcdavid",
        "conner mcdavid": "mcdavid",
        "connor m david": "mcdavid",
        "connor mcdavid (edm)": "mcdavid",
        "conor mcdavid": "mcdavid",
        "connor m": "mcdavid",
        "mcdaddy": "mcdavid",
        "c mcdavid": "mcdavid",
        "c. mcdavid": "mcdavid",
        "c.mcdavid": "mcdavid",
        "macdavid": "mcdavid",
        "macdavid (edm)": "mcdavid",
        "mcdavid (edm)": "mcdavid",
        "mcjesus": "mcdavid",
        "david": "mcdavid",

        "ryan o'reilly": "o'reilly",
        "o'reilly": "o'reilly",

        "alex ovechkin": "ovechkin",
        "ovechkin": "ovechkin",

        "artemi panarin": "panarin",
        "panarin": "panarin",
        "artem panarin": "panarin",
        "artemi panerin": "panarin",
        "artemis panarin": "panarin",
        "artermi panarin": "panarin",
        "artrmi panarin": "panarin",
        "a.panarin": "panarin",
        "panerin": "panarin",
        "panirin": "panarin",
        "pannarin": "panarin",
        "planarian": "panarin",
        "bread": "panarin",

        "david pastrnak": "pastrnak",
        "pastrnak": "pastrnak",
        "david pasternak": "pastrnak",
        "david pastranak": "pastrnak",
        "d pastrnak": "pastrnak",
        "pastranak": "pastrnak",

        "elias pettersson": "pettersson",
        "pettersson": "pettersson",
        "elias petterson": "pettersson",
        "e. petterson": "pettersson",
        "petterrson": "pettersson",
        "pettersen": "pettersson",

        "brayden point": "point",
        "point": "point",
        "b.point": "point",

        "mikko rantanen": "rantanen",
        "rantanen": "rantanen",
        "m. rantanen": "rantanen",

        "juuse saros": "saros",
        "saros": "saros",

        "mark scheifele": "scheifele",
        "scheifele": "scheifele",

        "mark stone": "stone",
        "stone": "stone",
        "m.stone": "stone",

        "andrei vasilevskiy": "vasilevskiy",
        "vasilevskiy": "vasilevskiy",
        "andrei v": "vasilevskiy",
        "andrei vasilevsky": "vasilevskiy",
        "andrei vasilievskiy": "vasilevskiy",
        "vasilevsky": "vasilevskiy",
        "vasi": "vasilevskiy",
        "vasilevski": "vasilevskiy",

        "mika zibanejad": "zibanejad",
        "zibanejad": "zibanejad",

    }
    q8 = ['q8a1', 'q8a2', 'q8a3', 'q8a4', 'q8a5']
    for question in q8:
        print(f"Standardizing the answers for column {question}")
        # Replace by various names of hart candidates
        df[question].replace(to_replace=hart_dict, value=None, inplace=True)
        print("Done!")
    # Dictionary of variations of players to be traded names for standardization
    trade_dict = {
        "0": np.nan,

        "michael amadio": "amadio",
        "amadio": "amadio",

        "craig anderson": "anderson",
        "c anderson": "c anderson",

        "andreas athanasiou": "athanasiou",
        "athanasiou": "athanasiou",

        "jay beagle": "beagle",
        "beagle": "beagle",

        "jonathan bernier": "bernier",
        "bernier": "bernier",

        "matthew benning": "benning",
        "benning": "benning",

        "tyler bertuzzi": "bertuzzi",
        "bertuzzi": "bertuzzi",
        "t. bertuzzi": "bertuzzi",

        "alex biega": "biega",
        "biega": "biega",

        "anders bjork": "bjork",
        "bjork": "bjork",

        "colin blackwell": "blackwell",
        "blackwell": "blackwell",

        "sergei bobrovsky": "bobrovsky",
        "bobrovsky": "bobrovsky",

        "brock boeser": "boeser",
        "boeser": "boeser",

        "nick bonino": "bonino",
        "bonino": "bonino",

        "mark borowiecki": "borowiecki",
        "borowiecki": "borowiecki",
        "mark boroweicki": "borowiecki",

        "will borgen": "borgen",
        "borgen": "borgen",

        "johnny boychuk": "boychuk",
        "boychuk": "boychuk",

        "brian boyle": "boyle",
        "boyle": "boyle",

        "derick brassard": "brassard",
        "brassard": "brassard",

        "connor brown": "c brown",
        "c brown": "c brown",

        "dustin brown": "d brown",
        "d brown": "d brown",

        "josh brown": "j brown",
        "j brown": "j brown",

        "andre burakovsky": "burakovsky",
        "burakovsky": "burakovsky",
        "burakowsky": "burakovsky",

        "will butcher": "butcher",
        "butcher": "butcher",
        "w. butcher": "butcher",

        "quinton byfield": "byfield",
        "byfield": "byfield",

        "paul byron": "byron",
        "byron": "byron",

        "jeff carter": "carter",
        "carter": "carter",

        "zdeno chara": "chara",
        "chara": "chara",

        "ben chariot": "chiarot",
        "ben chiarot": "chiarot",
        "chiarot": "chiarot",

        "kyle clifford": "clifford",
        "clifford": "clifford",

        "andrew cogliano": "cogliano",
        "cogliano": "cogliano",

        "andrew copp": "copp",
        "copp": "copp",

        "nick cousins": "cousins",
        "cousins": "cousins",
        "n. cousins": "cousins",

        "lawson crouse": "crouse",
        "crouse": "crouse",

        "rasmus dahlin": "dahlin",
        "dahlin": "dahlin",

        "dante fabbro": "fabbro",
        "fabbro": "fabbro",

        "jake debrusk": "debrusk",
        "debrusk": "debrusk",

        "calvin de haan": "de haan",
        "dehaan": "de haan",

        "danny dekeyser": "dekeyser",
        "dekeyser": "dekeyser",
        "d. dekeyser": "dekeyser",

        "nic deslauriers": "deslauriers",
        "deslauriers": "deslauriers",

        "travis dermott": "dermott",
        "dermott": "dermott",

        "max domi": "domi",
        "domi": "domi",
        "m. domi": "domi",
        "m.domi": "domi",

        "matt dumba": "dumba",
        "dumba": "dumba",

        "ryan dzingel": "dzingel",
        "dzingel": "dzingel",
        "dzingle": "dzingel",
        "r.dzingel": "dzingel",

        "cody eakin": "eakin",
        "eakin": "eakin",
        "cody eakins": "eakin",
        "c. eakin": "eakin",
        "c.eakin": "eakin",

        "jordan eberle": "eberle",
        "eberle": "eberle",

        "alexander edler": "edler",
        "edler": "edler",
        "a. edler": "edler",
        "alex edler": "edler",

        "jack eichel": "eichel",
        "eichel": "eichel",
        "jack eichel (buf)": "eichel",
        "jack eickel": "eichel",
        "j. eichel": "eichel",
        "j eichel": "eichel",
        "eichel (buf)": "eichel",
        "eicher": "eichel",
        "eichle": "eichel",

        "mattias ekholm": "ekholm",
        "ekholm": "ekholm",
        "matthias ekholm": "ekholm",
        "eckholm": "ekholm",

        "tyler ennis": "ennis",
        "ennis": "ennis",
        "ennis (ott)": "ennis",

        "eric comrie": "comrie",
        "comrie": "comrie",

        "loui eriksson": "eriksson",
        "eriksson": "eriksson",
        "loui erikkson": "eriksson",
        "louie eriksson": "eriksson",
        "louis eriksson": "eriksson",
        "ericksson": "eriksson",

        "robby fabbri": "fabbri",
        "fabbri": "fabbri",
        "robbi fabbri": "fabbri",

        "kevin fiala": "fiala",
        "fiala": "fiala",

        "filip forsberg": "forsberg",
        "forsberg": "forsberg",
        "filip forsberg (nsh)": "forsberg",
        "filip forsbog": "forsberg",
        "flip forsberg": "forsberg",
        "flip forsburg": "forsberg",
        "forsberg (filip)": "forsberg",
        "forsberg (nas)": "forsberg",
        "forserg": "forsberg",
        "fosberg": "forsberg",
        "f forsberg": "forsberg",
        "f.  forsberg": "forsberg",
        "f. forsberg": "forsberg",
        "f.forsberg": "forsberg",
        "forsberg": "forsberg",
        "fforsberg": "forsberg",

        "marc andre fleury": "fleury",
        "ma fleury": "fleury",
        "maf": "fleury",
        "fleury": "fleury",
        "fluery": "fleury",

        "cam fowler": "fowler",
        "fowler": "fowler",

        "sam gagner": "gagner",
        "gagner": "gagner",
        "sam gagne": "gagner",
        "ganger": "gagner",

        "alex galchenyuk": "galchenyuk",
        "galchenyuk": "galchenyuk",

        "jake gardiner": "gardiner",
        "gardiner": "gardiner",

        "johnny gaudreau": "gaudreau",
        "gaudreau": "gaudreau",
        "johnny gaudreau (cgy)": "gaudreau",
        "j. gaudreau": "gaudreau",

        "aleksandar georgiev": "georgiev",
        "alexander georgiev": "georgiev",
        "georgiev": "georgiev",

        "ryan getzlaf": "getzlaf",
        "getzlaf": "getzlaf",

        "shayne gostisbehere": "gostisbehere",
        "gostisbehere": "gostisbehere",
        "ghostisbehere": "gostisbehere",

        "john gibson": "gibson",
        "gibson": "gibson",

        "mark giordano": "giordano",
        "giordano": "giordano",
        "m. giordano": "giordano",

        "zemgus girgensons": "girgensons",
        "girgensons": "girgensons",
        "girgensuns": "girgensons",

        "claude giroux": "giroux",
        "giroux": "giroux",

        "luke glendening": "glendening",
        "glendening": "glendening",

        "alex goligoski": "goligoski",
        "goligoski": "goligoski",

        "jordan greenway": "greenway",
        "greenway": "greenway",

        "thomas greiss": "greiss",
        "greiss": "greiss",

        "rocco grimaldi": "grimaldi",
        "grimaldi": "grimaldi",

        "erik gudbranson": "gudbranson",
        "gudbranson": "gudbranson",

        "carl hagelin": "hagelin",
        "hagelin": "hagelin",

        "robert hagg": "hagg",
        "hagg": "hagg",

        "libor hajek": "hajek",
        "hajek": "hajek",

        "jaroslav halak": "halak",
        "halak": "halak",

        "travis hamonic": "hamonic",
        "hamonic": "hamonic",

        "connor hellebuyck": "hellebuyck",
        # This is legitimate - I checked and this is an answer to Q9
        "hellebuyck": "hellebuyck",

        "adam henrique": "henrique",
        "henrique": "henrique",

        "tomas hertl": "hertl",
        "hertl": "hertl",
        "thomas hertl": "hertl",
        "t hertl": "hertl",
        "t. hertl": "hertl",
        "t.hertl": "hertl",
        "hertl (sj)": "hertl",
        "hertl (sjs)": "hertl",
        "hertle": "hertl",
        "hertz": "hertl",
        "hertel": "hertl",
        "tomáš hertl": "hertl",

        "thomas hickey": "hickey",
        "hickey": "hickey",

        "vinnie hinostroza": "hinostroza",
        "hinostroza": "hinostroza",
        "vinnie hinestroza": "hinostroza",
        "vinnie hinistroza": "hinostroza",
        "vinny hinostroza": "hinostroza",
        "v. hinostroza": "hinostroza",
        "hinistroza": "hinostroza",

        "nick holden": "holden",
        "holden": "holden",
        "n. holden": "holden",

        "braden holtby": "holtby",
        "holtby": "holtby",

        "carter hutton": "c hutton",
        "c hutton": "c hutton",
        "hutton": "c hutton",

        "mattias janmark": "janmark",
        "janmark": "janmark",

        "dmitrij jaskin": "jaskin",
        "jaskin": "jaskin",

        "marcus johansson": "johansson",
        "johansson": "johansson",

        "ross johnston": "r johnston",
        "r johnston": "r johnston",

        "martin jones": "m jones",
        "m jones": "m jones",

        "seth jones": "s jones",
        "s jones": "s jones",
        "s.jones": "s jones",
        "(seth) jones": "s jones",

        "roman josi": "josi",
        "josi": "josi",

        "olli juolevi": "juolevi",
        "juolevi": "juolevi",

        "nazem kadri": "kadri",
        "kadri": "kadri",

        "kaapo kakko": "kakko",
        "kakko": "kakko",

        "evander kane": "e kane",
        "e kane": "e kane",
        "kane": "e kane",
        "e. kane": "e kane",
        "e.kane": "e kane",
        "ekane": "e kane",

        "ondrej kase": "kase",
        "kase": "kase",

        "zack kassian": "kassian",
        "kassian": "kassian",

        "clayton keller": "keller",
        "keller": "keller",

        "michal kempny": "kempny",
        "kempny": "kempny",

        "alex kerfoot": "kerfoot",
        "kerfoot": "kerfoot",

        "ryan kesler": "kesler",
        "kesler": "kesler",
        "ryan kessler": "kesler",

        "phil kessel": "kessel",
        "kessel": "kessel",
        "phi kessel": "kessel",
        "phil \"the thrill\" kessel": "kessel",
        "phil kessel (ari)": "kessel",
        "phil kessell": "kessel",
        "philip kessel": "kessel",
        "phill kessel": "kessel",
        "phillip kessel": "kessel",
        "phil k": "kessel",
        "p kessel": "kessel",
        "kessel (ari)": "kessel",
        "p. kassel": "kessel",
        "p. kessel": "kessel",
        "p.kessel": "kessel",
        "kessell": "kessel",
        "2x stanley cup champion phil kessel": "kessel",

        "anton khudobin": "khudobin",
        "khudobin": "khudobin",

        "john klingberg": "klingberg",
        "klingberg": "klingberg",
        "klinger": "klingberg",

        "leo komarov": "komarov",
        "komarov": "komarov",
        "komorov": "komarov",

        "anze kopitar": "kopitar",
        # This is legitimate - I checked and this is an answer to Q9
        "kopitar": "kopitar",

        "joonas korpisalo": "korpisalo",
        "korpisalo": "korpisalo",

        "mikko koskinen": "koskinen",
        "koskinen": "koskinen",

        "jesperi kotkaniemi": "kotkaniemi",
        "kotkaniemi": "kotkaniemi",

        "vitaly kravtsov": "kravtsov",
        "kravtsov": "kravtsov",
        "vitali kravstov": "kravtsov",
        "vitali kravtsov": "kravtsov",

        "nikita kucherov": "kucherov",
        # This is legitimate - There were two entries, I checked and 1 was a legit answer to #9, the other was a mistake
        "kucherov": "kucherov",

        "darcy kuemper": "kuemper",
        "kuemper": "kuemper",

        "brett kulak": "kulak",
        "kulak": "kulak",

        "dean kukan": "kukan",
        "kukan": "kukan",

        "evgeny kuznetsov": "kuznetsov",
        "kuznetsov": "kuznetsov",
        "evgeni kuznetzov": "kuznetsov",
        "evgeny kuznetzov": "kuznetsov",
        "kutzentsov": "kuznetsov",

        "andrew ladd": "ladd",
        "ladd": "ladd",

        "patrik laine": "laine",
        "laine": "laine",
        "patrick laine": "laine",
        "laine (cbj)": "laine",

        "kevin labanc": "labanc",
        "labanc": "labanc",
        "lebanc": "labanc",

        "johan larsson": "jo larsson",
        "jo larsson": "jo larsson",

        "nick leddy": "leddy",
        "leddy": "leddy",
        "n. leddy": "leddy",
        "n leddy": "leddy",
        "leddy\\": "leddy",

        "kris letang": "letang",
        "letang": "letang",

        "trevor lewis": "lewis",
        "lewis": "lewis",

        "hampus lindholm": "lindholm",
        "lindholm": "lindholm",
        "h lindholm": "lindholm",
        "h. lindholm": "lindholm",

        "ilya lyubushkin": "lyubushkin",
        "lyubushkin": "lyubushkin",

        "olli maatta": "maatta",
        "maatta": "maatta",
        "maata": "maatta",

        "evgeni malkin": "malkin",
        "malkin": "malkin",

        "josh manson": "manson",
        "manson": "manson",
        "j manson": "manson",

        "ryan macinnis": "macinnis",
        "macinnis": "macinnis",

        "timo meier": "meier",
        "meier": "meier",

        "ilya mikheyev": "mikheyev",
        "mikheyev": "mikheyev",
        "ilya mickheyev": "mikheyev",
        "ilya mikeyev": "mikheyev",
        "micheyev": "mikheyev",
        "mikeyhev": "mikheyev",

        "colin miller":  "c miller",
        "c miller":  "c miller",
        "collin miller":  "c miller",
        "c. miller":  "c miller",
        "c.miller":  "c miller",
        "(colin) miller":  "c miller",

        "mitch marner": "marner",
        "marner": "marner",

        "sean monahan": "monahan",
        "monahan": "monahan",

        "sam montembeault": "montembeault",
        "montembeault": "montembeault",

        "john moore": "j moore",
        "j moore": "j moore",

        "connor murphy": "murphy",
        "murphy": "murphy",

        "vladislav namestnikov": "namestnikov",
        "namestnikov": "namestnikov",
        "vlad namestnikov": "namestnikov",
        "namestnikov (det)": "namestnikov",
        "namestikov": "namestnikov",
        "namestnekov": "namestnikov",

        "james neal": "neal",
        "neal": "neal",
        "j neal": "neal",

        "nino niederreiter": "niederreiter",
        "niederreiter": "niederreiter",

        "markus nutivaara": "nutivaara",
        "nutivaara": "nutivaara",

        "william nylander": "w nylander",
        "w nylander": "w nylander",

        "gustav nyquist": "nyquist",
        "nyquist": "nyquist",

        "victor olofsson": "olofsson",
        "olofsson": "olofsson",

        "ondrej palat": "palat",
        "palat": "palat",

        "nic petan": "petan",
        "petan": "petan",

        "greg pateryn": "pateryn",
        "pateryn": "pateryn",

        "cedric paquette": "paquette",
        "paquette": "paquette",

        "joe pavelski": "pavelski",
        "pavelski": "pavelski",

        "mathieu perreault": "perreault",
        "perreault": "perreault",

        "marcus pettersson": "m pettersson",
        "m pettersson": "m pettersson",
        "marcus petterson": "m pettersson",

        "pierre engvall": "engvall",
        "engvall": "engvall",

        "mark pysyk": "pysyk",
        "pysyk": "pysyk",

        "jonathan quick": "quick",
        "quick": "quick",

        "alexander radulov": "radulov",
        "radulov": "radulov",

        "rickard rakell": "rakell",
        "rakell": "rakell",
        "richard rackell": "rakell",
        "richard rakell": "rakell",
        "rikard rakell": "rakell",
        "rikard rakkel": "rakell",
        "rickard rackell": "rakell",
        "rickard rakell (ana)": "rakell",
        "rakell (ana)": "rakell",
        "rakkell": "rakell",
        "r rakell": "rakell",
        "r. rakell": "rakell",
        "r.rakell": "rakell",
        "rackel": "rakell",
        "rackell": "rakell",
        "racker": "rakell",
        "rickell": "rakell",
        "robert rakell": "rakell",

        "victor rask": "v rask",
        "rask": "v rask",
        "v. rask": "v rask",

        "morgan rielly": "rielly",
        "rielly": "rielly",
        "morgan reilly": "rielly",
        "morgan rielly (tor)": "rielly",
        "m.reilly": "rielly",
        "m. reilly": "rielly",
        "m. rielly": "rielly",
        "reilly": "rielly",
        "reilly(tor)": "rielly",

        "james reimer": "reimer",
        "reimer": "reimer",

        "sam reinhart": "reinhart",
        "reinhart": "reinhart",

        "rasmus ristolainen": "ristolainen",
        "ristolainen": "ristolainen",

        "jack roslovic": "roslovic",
        "roslovic": "roslovic",

        "antoine roussel": "roussel",
        "roussel": "roussel",
        "antoine roussell": "roussel",
        "rousell": "roussel",

        "bryan rust": "rust",
        "rust": "rust",

        "jan rutta": "rutta",
        "rutta": "rutta",

        "zachary sanford": "sanford",
        "sanford": "sanford",

        "justin schultz": "schultz",
        "schultz": "schultz",

        "andrej sekera": "sekera",
        "sekera": "sekera",

        "damon severson": "severson",
        "severson": "severson",

        "kevin shattenkirk": "shattenkirk",
        "shattenkirk": "shattenkirk",

        "riley sheahan": "sheahan",
        "sheahan": "sheahan",

        "jakob silfverberg": "silfverberg",
        "silfverberg": "silfverberg",

        "reilly smith": "r smith",
        "r smith": "r smith",

        "vladimir sobotka": "sobotka",
        "sobotka": "sobotka",

        "eric staal": "e staal",
        "e staal": "e staal",

        "marc staal": "m staal",
        "m staal": "m staal",
        "mark staal": "m staal",
        "m. staal": "m staal",

        "paul stastny": "stastny",
        "stastny": "stastny",

        "derek stepan": "stepan",
        "stepan": "stepan",

        "troy stecher": "stecher",
        "stecher": "stecher",
        "t. stecher": "stecher",
        "troy stetcher": "stecher",
        "stetcher": "stecher",

        "anton stralman": "stralman",
        "stralman": "stralman",
        "anton strahlman": "stralman",
        "a.stralman": "stralman",
        "stalman": "stralman",
        "strahlman": "stralman",
        "anton strålman": "stralman",

        "ryan strome": "r strome",
        "r strome": "r strome",

        "dylan strome": "d strome",
        "d strome": "d strome",
        "d. strome": "d strome",
        "strome": "d strome",
        "strome (chi)": "d strome",

        "malcolm subban": "m subban",
        "m subban": "m subban",

        "pk subban": "pk subban",
        "subban": "pk subban",
        "p.k. subban": "pk subban",
        "p. k. subban": "pk subban",
        "p.k. suban": "pk subban",
        "pk suban": "pk subban",
        "suban": "pk subban",

        "vladimir tarasenko": "tarasenko",
        "tarasenko": "tarasenko",
        "vlad tarasenko": "tarasenko",
        "vladamir tarasenko": "tarasenko",
        "vladimer tarasenko": "tarasenko",
        "vladimir taransenko": "tarasenko",
        "vladimir tarasanko": "tarasenko",
        "vladimir tarasenko (stl)": "tarasenko",
        "vladimir terasenko": "tarasenko",
        "valdimir tarasenko": "tarasenko",
        "v tarasenko": "tarasenko",
        "v. tarasenko": "tarasenko",
        "v.tarasenko": "tarasenko",
        "tarensanko": "tarasenko",
        "taresenko": "tarasenko",
        "taraenko": "tarasenko",
        "tarasanko": "tarasenko",

        "tomas tatar": "tatar",
        "tatar": "tatar",

        "joe thornton": "thornton",
        "thornton": "thornton",
        "jumbo joe": "thornton",

        "chris tierney": "tierney",
        "tierney": "tierney",
        "chris tierny": "tierney",
        "c. tierney": "tierney",
        "tiereny (ott)": "tierney",
        "tierney (ott)": "tierney",
        "tierny": "tierney",
        "tirney": "tierney",

        "brady tkachuk": "b tkachuk",
        "b tkachuk": "b tkachuk",

        "matthew tkachuk": "m tkachuk",
        "m tkachuk": "m tkachuk",

        "dustin tokarski": "tokarski",
        "tokarski": "tokarski",

        "vincent trocheck": "trocheck",
        "trocheck": "trocheck",

        "kyle turris": "turris",
        "turris": "turris",

        "linus ullmark": "ullmark",
        "ullmark": "ullmark",

        "james van riemsdyk": "van riemsdyk",
        "j van riemsdyk": "van riemsdyk",

        "frank vatrano": "vatrano",
        "vatrano": "vatrano",

        "jake walman": "walman",
        "walman": "walman",

        "zach whitecloud": "whitecloud",
        "whitecloud": "whitecloud",

        "miles wood": "wood",
        "wood": "wood",

        "keith yandle": "yandle",
        "yandle": "yandle",

        "nikita zadorov": "zadorov",
        "zadorov": "zadorov",
        "zadarov": "zadorov",
        "n.zadorov": "zadorov",

        "mika zibanejad": "zibanejad",
        "zibanejad": "zibanejad",

        "jason zucker": "zucker",
        "zucker": "zucker",
    }
    q9 = ['q9a1', 'q9a2', 'q9a3', 'q9a4', 'q9a5']
    for question in q9:
        print(f"Standardizing the answers for column {question}")
        # Replace by various names of hart candidates
        df[question].replace(to_replace=trade_dict, value=None, inplace=True)
        print("Done!")
    # Dictionary of variations of 100-point scorer's names for standardization
    bonus_dict = {
        "barkov": "barkov",

        "sam bennett (yes": "bennett",

        "sidney crosby": "crosby",

        "leon draisaitl": "draisaitl",
        "draisaitl": "draisaitl",
        "leon draisatl": "draisaitl",
        "leon draisaitil": "draisaitl",
        "l. draisaitl": "draisaitl",
        "draisaital": "draisaitl",
        "draistaitl": "draisaitl",
        "leon draistaitl": "draisaitl",
        "draisaitl (edm)": "draisaitl",
        "leon": "draisaitl",
        "draisatl": "draisaitl",
        ": draisatl": "draisaitl",
        "draisitl": "draisaitl",
        "draisetal": "draisaitl",
        "l.draisaitl": "draisaitl",
        "leon d": "draisaitl",
        "10. draisaitl": "draisaitl",
        "optional bonus question: draisaitl": "draisaitl",
        "leon draisatil": "draisaitl",
        "draistatl": "draisaitl",
        "drasatail": "draisaitl",
        "draissaitl": "draisaitl",
        "draisaitl for the win!": "draisaitl",
        "l draisaitl": "draisaitl",
        "drasaitl": "draisaitl",
        "draisitl (edm)": "draisaitl",
        "l draisaital": "draisaitl",
        "leon draisaital": "draisaitl",
        "leon drausaitl": "draisaitl",
        "neon leon draisaitl baby": "draisaitl",
        "bonus: l. draisaitl": "draisaitl",
        "the other half of the oiler offense (a.k.a leon draisaitl)": "draisaitl",
        "draisaitil": "draisaitl",
        "draistail": "draisaitl",

        "giroux": "giroux",

        "roope hintz": "hintz",

        "jonathan huberdeau": "huberdeau",
        "huberdeau": "huberdeau",

        "patrick kane": "p kane",
        "p kane": "p kane",

        "kaprizov": "kaprizov",
        "kaprisov": "kaprizov",

        "nikita kucherov": "kucherov",
        "kucherov": "kucherov",
        "kucherov gonna go brrrrrrr": "kucherov",
        "kucherov*": "kucherov",
        "optional bonus question: nikita kucherov": "kucherov",
        "kucherov. i already own the book anyway (it's great)": "kucherov",
        "kucherov (could tank my whole entry": "kucherov",
        "question: kucherov": "kucherov",

        "nathan mackinnon": "mackinnon",
        "mackinnon": "mackinnon",
        "nate mackinnon": "mackinnon",
        "mckinnon": "mackinnon",
        "nate mckinnon": "mackinnon",
        "nathan mackinnon (col)": "mackinnon",
        "n. mackinnon": "mackinnon",
        "nathan mckinnon": "mackinnon",
        "bonus: mackinnon": "mackinnon",

        "brad marchand": "marchand",
        "marchand": "marchand",

        "mitch marner": "marner",
        "marner": "marner",
        "bonus: marner": "marner",
        "m. marner": "marner",
        "marner *insert elmo_fire_chaos.gif*": "marner",

        "auston matthews": "matthews",
        "matthews": "matthews",
        "austin mathews": "matthews",
        "auston matthews             bpb": "matthews",
        "auston matthews (for a bonus signed six pack of labatt": "matthews",
        "matthews bang!": "matthews",

        "artemi panarin": "panarin",
        "panarin": "panarin",
        "panarin the bread man": "panarin",
        ". panarin": "panarin",
        "panerin": "panarin",
        "artemi panerin": "panarin",
        "panarin (praying for no second pandemic)": "panarin",
        "bread man artemi panarin": "panarin",

        "david pastrnak": "pastrnak",
        "pastrnak": "pastrnak",

        "brayden point": "point",
        "point": "point",

        "mikko rantanen": "rantanen",
        "rantanen": "rantanen",
        "rantanen mikko": "rantanen",

        "mark scheifele": "scheifele",
        "scheifele": "scheifele",

        "0": np.nan,
        "": np.nan,
        "no answer": np.nan,
        "pass": np.nan,
        "no thank you": np.nan,
        "nope": np.nan,
        "no way": np.nan,
        "hell no. not falling for this one": np.nan,
        "too risky": np.nan,
        "n": np.nan,
        "i know nothing about hockey so everyone should beat me": np.nan,
        "no": np.nan,
        "jcs": np.nan,
        "r.s": np.nan,
        "nick d": np.nan,
        "kjl": np.nan,
        "jwm": np.nan,
        "jl": np.nan,
        "ben from portland": np.nan,
        "none": np.nan,
        "jon n": np.nan,
        "lol do you think i'm a sucker?": np.nan,
        "tag so i can find my entry: jl96": np.nan,
        "no bonus answer.....go jackets!!!": np.nan,
        "tim t. lgrw": np.nan,
        "gw": np.nan,
        "carl12345": np.nan,
        "ryan m": np.nan,
        "ellay 'vanilla thunder' heys": np.nan,
        "i think my autocorrect now hates me as much as i hate it": np.nan,
        "waaaaaaay too scared to risk this one": np.nan,
        "couple possibilities but no one i'm gonna risk it all on": np.nan,
        "rnw": np.nan,
        "tae": np.nan,
        "with five minutes to spare baby! blk": np.nan,
        "not gonna do it..": np.nan,
        "gm": np.nan,
        "jb0202": np.nan,
        "nope nope nope": np.nan,
        "sn": np.nan,
        "lets go buffalo": np.nan,
        "nope. nope nope nope. not touching that": np.nan,
        "jar": np.nan,
        "bradley o": np.nan,
        "efk (nyc)": np.nan,
        "man am i going to look awful at the end": np.nan,
        "nobody": np.nan,
        "rl": np.nan,
        "rga": np.nan,
        "riley b": np.nan,
        "not a chance": np.nan,
        "risk it all": np.nan,
        "travis c": np.nan,
        "bwd": np.nan,
        "moods": np.nan,
        "saruman": np.nan,
        "paul lang": np.nan,
        "oh": np.nan,
        "srl": np.nan,
        "ajm": np.nan,
        ">": np.nan,
        "\"b.	marner\"": np.nan,
        "pg13": np.nan,
        "b$": np.nan,
        "no way iâ€™ll risk it": np.nan,
        "my wife's entry": np.nan,
        "ty stortz": np.nan,
        "hopefully i'll do better than last year. thanks alot lafreniere..": np.nan,
        "when mackinnon sprains his ankle": np.nan,
        "mtw": np.nan,
        "rg": np.nan,
        "kaj": np.nan,
        "mcl": np.nan,
        "rjp": np.nan,
        "dcrjmr": np.nan,
        "woj": np.nan,
        "cga": np.nan,
        "since wayne": np.nan,
        "tim b": np.nan,
        "eht": np.nan,
        "sonny": np.nan,
        "jtk": np.nan,
        "ccc": np.nan,
        "i am not falling into this trap": np.nan,
        "jrb716": np.nan,
        "submmited by jammer": np.nan,
        "phil j": np.nan,
        "rocco m": np.nan,
        "robkd": np.nan,
        "dt": np.nan,
        "not participating": np.nan,
        "kevin y": np.nan,
        "jzs": np.nan,
        "bonud": np.nan,
        "ross hamm": np.nan,
        "dfh": np.nan,
        "thank you sean": np.nan,
        "bz": np.nan,
        "macki....can't risk the entire entry. not submitting for q #10": np.nan,
        "justin zentai": np.nan,
        "bjb": np.nan,
        "decline bonus": np.nan,
        "wg2": np.nan,
        "ekb": np.nan,
        "no thanks!": np.nan,
        "ajv": np.nan,
        "jwc": np.nan,
        "not going for the optional suic": np.nan,
        "kevin durant": np.nan,
        "085 alj": np.nan,
        "bonus": np.nan,
        "japanada": np.nan,
        "fetterov": np.nan,
        "cd11": np.nan,
        "jsa": np.nan,
        "~wsd": np.nan,
        "[pass]": np.nan,
        "aj ~ go wings!": np.nan,
        "irbull": np.nan,
        "t. hamburg": np.nan,
        "no thanks 2spooky4me": np.nan,
        "blank": np.nan,
        "you'll score 100 points in my heart": np.nan,
        "dc": np.nan,
        "e.g": np.nan,
        "mes": np.nan,
        "i ain't that stupid": np.nan,
        "mjtl": np.nan,
        "iap": np.nan,
        "zb": np.nan,
        "kmb": np.nan,
        "dps": np.nan,
        "dwd on behalf of 10k": np.nan,
        "[not answering]": np.nan,
        "jake s": np.nan,
        "no thanks": np.nan,
        "drew millard": np.nan,
        "gokingsgo": np.nan,
        "b.a": np.nan,
        "zzzg": np.nan,
        "soup": np.nan,
        ".svc": np.nan,
        "@natbencol": np.nan,
        "cwz": np.nan,
        "nate the great ( mck not beaulieu)": np.nan,
        "i am a coward": np.nan,
        "abs": np.nan,
        "fs ggmu": np.nan,
        "bdc12": np.nan,
        "alex makhalov": np.nan,
        "trw": np.nan,
        "casto": np.nan,
        "here's my gamble: nobody but mcdavid hits 100": np.nan,
        "signed teh": np.nan,
        "bettman eats boogers!": np.nan,
        "npp": np.nan,
        "nnnope": np.nan,
        "absolutely not!": np.nan,
        "fuck no lol": np.nan,
        "qq": np.nan,
        "js33": np.nan,
        "(jgp)": np.nan,
        "no way i’ll risk it": np.nan,
        "no answer (don’t think anyone will)": np.nan,
    }
    q10 = ['q10a1']
    for question in q10:
        print(f"Standardizing the answers for column {question}")
        # Replace by various names of hart candidates
        df[question].replace(to_replace=bonus_dict, value=None, inplace=True)
        print("Done!")
    print("All standardization operations complete!")
    return df


def reporting_operations(df, minor_surgery_count, major_surgery_count):
    """ Having put together the entire standardized dataframe,
    we're ready to generate data from it! This function uses
    a provided df, minor surgery count, and major surgery count
    to provide some overall statistics, as well as value counts
    for each question. Returns nothing except for printing out
    a lot of data. 
    """
    num_entries = len(df)
    pos_total_answers = num_entries * 46
    nan_count = df.isna().sum()
    pos_answers = num_entries * 5
    num_answers = pos_total_answers - sum(nan_count)
    total_surgeries = major_surgery_count + minor_surgery_count
    print(f"After completing all standardization operations, which included deleting a handful of erroneous/updated entries...")
    print(
        f"There are {num_entries} entries in this year's prediction contest.")
    print(
        f"Of these {num_entries} entries, a possible {pos_total_answers} answers were possible.")
    print(f"Entrants provided {num_answers} answers overall.\n")
    print(f"Of these {num_entries} entries, {major_surgery_count} required major surgery. This is {(major_surgery_count / num_entries) * 100:.2f}% of all entries.")
    print("'Major surgery' means that the submission had to be rewritten in whole or in part, in order to be processed by the automatic scripting. For example, if someone used spaces as separators rather than commas, my script could not account for this, and the entry had to be rewritten entirely.")
    print(f"Of these {num_entries} entries, {minor_surgery_count} required minor surgery. This is {(minor_surgery_count / num_entries) * 100:.2f}% of all entries.")
    print("'Minor surgery' means that individual cells for an entry had to be corrected (some needing a single correction, others needing several), usually because of inconsistencies in the entry.")
    print("For example, if someone listed 'mcdavid, draisaitl. mackinnon,...', the period instead of a comma would lead to a single cell receiving 'draisaitl. mackinnon' as an answer, and these would have to be corrected manually.")
    print("Some of these were more problematic than the 'major' issues, because the diagnosis was usually more involved than the bigger issues which were more obvious.\n")
    print(f"In total, {total_surgeries} of the {num_entries} entries ({(total_surgeries / num_entries) * 100:.2f})% required some significant modification that prevented them from being handled automatically. This was, by far, the most involved and time-intensive part of building this program.")
    q1 = ['q1a1', 'q1a2', 'q1a3', 'q1a4', 'q1a5']
    q2 = ['q2a1', 'q2a2', 'q2a3', 'q2a4', 'q2a5']
    q3 = ['q3a1', 'q3a2', 'q3a3', 'q3a4', 'q3a5']
    q4 = ['q4a1', 'q4a2', 'q4a3', 'q4a4', 'q4a5']
    q5 = ['q5a1', 'q5a2', 'q5a3', 'q5a4', 'q5a5']
    q6 = ['q6a1', 'q6a2', 'q6a3', 'q6a4', 'q6a5']
    q7 = ['q7a1', 'q7a2', 'q7a3', 'q7a4', 'q7a5']
    q8 = ['q8a1', 'q8a2', 'q8a3', 'q8a4', 'q8a5']
    q9 = ['q9a1', 'q9a2', 'q9a3', 'q9a4', 'q9a5']
    a = df['q1a1'].value_counts()
    b = df['q1a2'].value_counts()
    c = df['q1a3'].value_counts()
    d = df['q1a4'].value_counts()
    e = df['q1a5'].value_counts()
    q1_nan_sum = 0
    for question in q1:
        temp_nan = df[question].isna().sum()
        q1_nan_sum += temp_nan
    x = a.add(b, fill_value=0).add(c, fill_value=0).add(
        d, fill_value=0).add(e, fill_value=0)
    x = x.sort_values(ascending=False)
    print("***** ***** QUESTION 1 SUMMARY ***** *****")
    print(f"Here is the data for Question 1 (teams to make the playoffs).")
    print(
        f"Out of a possible {pos_answers} answers, {int(sum(x))} answers were recieved.")
    print(f"{q1_nan_sum} possible answers were not completed.")
    print(f"{len(x)} different answers were provided for this question.")
    print("Here are the various answers people provided for this question, in descending order of frequency:")
    print(x)
    a = df['q2a1'].value_counts()
    b = df['q2a2'].value_counts()
    c = df['q2a3'].value_counts()
    d = df['q2a4'].value_counts()
    e = df['q2a5'].value_counts()
    q2_nan_sum = 0
    for question in q2:
        temp_nan = df[question].isna().sum()
        q2_nan_sum += temp_nan
    x = a.add(b, fill_value=0).add(c, fill_value=0).add(
        d, fill_value=0).add(e, fill_value=0)
    x = x.sort_values(ascending=False)
    print("***** ***** QUESTION 2 SUMMARY ***** *****")
    print(f"Here is the data for Question 2 (teams to miss the playoffs).")
    print(
        f"Out of a possible {pos_answers} answers, {int(sum(x))} answers were recieved.")
    print(f"{q2_nan_sum} possible answers were not completed.")
    print(f"{len(x)} different answers were provided for this question.")
    print("Here are the various answers people provided for this question, in descending order of frequency:")
    print(x)
    a = df['q3a1'].value_counts()
    b = df['q3a2'].value_counts()
    c = df['q3a3'].value_counts()
    d = df['q3a4'].value_counts()
    e = df['q3a5'].value_counts()
    q3_nan_sum = 0
    for question in q3:
        temp_nan = df[question].isna().sum()
        q3_nan_sum += temp_nan
    x = a.add(b, fill_value=0).add(c, fill_value=0).add(
        d, fill_value=0).add(e, fill_value=0)
    x = x.sort_values(ascending=False)
    print("***** ***** QUESTION 3 SUMMARY ***** *****")
    print(f"Here is the data for Question 3 (coaches to not lose their jobs).")
    print(
        f"Out of a possible {pos_answers} answers, {int(sum(x))} answers were recieved.")
    print(f"{q3_nan_sum} possible answers were not completed.")
    print(f"{len(x)} different answers were provided for this question.")
    print("Here are the various answers people provided for this question, in descending order of frequency:")
    print(x)
    a = df['q4a1'].value_counts()
    b = df['q4a2'].value_counts()
    c = df['q4a3'].value_counts()
    d = df['q4a4'].value_counts()
    e = df['q4a5'].value_counts()
    q4_nan_sum = 0
    for question in q4:
        temp_nan = df[question].isna().sum()
        q4_nan_sum += temp_nan
    x = a.add(b, fill_value=0).add(c, fill_value=0).add(
        d, fill_value=0).add(e, fill_value=0)
    x = x.sort_values(ascending=False)
    print("***** ***** QUESTION 4 SUMMARY ***** *****")
    print(f"Here is the data for Question 4 (GMs to not lose their jobs).")
    print(
        f"Out of a possible {pos_answers} answers, {int(sum(x))} answers were recieved.")
    print(f"{q4_nan_sum} possible answers were not completed.")
    print(f"{len(x)} different answers were provided for this question.")
    print("Here are the various answers people provided for this question, in descending order of frequency:")
    print(x)
    a = df['q5a1'].value_counts()
    b = df['q5a2'].value_counts()
    c = df['q5a3'].value_counts()
    d = df['q5a4'].value_counts()
    e = df['q5a5'].value_counts()
    q5_nan_sum = 0
    for question in q5:
        temp_nan = df[question].isna().sum()
        q5_nan_sum += temp_nan
    x = a.add(b, fill_value=0).add(c, fill_value=0).add(
        d, fill_value=0).add(e, fill_value=0)
    x = x.sort_values(ascending=False)
    print("***** ***** QUESTION 5 SUMMARY ***** *****")
    print(f"Here is the data for Question 5 (goalies to start 60% of team's games).")
    print(
        f"Out of a possible {pos_answers} answers, {int(sum(x))} answers were recieved.")
    print(f"{q5_nan_sum} possible answers were not completed.")
    print(f"{len(x)} different answers were provided for this question.")
    print("Here are the various answers people provided for this question, in descending order of frequency:")
    print(x)
    a = df['q6a1'].value_counts()
    b = df['q6a2'].value_counts()
    c = df['q6a3'].value_counts()
    d = df['q6a4'].value_counts()
    e = df['q6a5'].value_counts()
    q6_nan_sum = 0
    for question in q6:
        temp_nan = df[question].isna().sum()
        q6_nan_sum += temp_nan
    x = a.add(b, fill_value=0).add(c, fill_value=0).add(
        d, fill_value=0).add(e, fill_value=0)
    x = x.sort_values(ascending=False)
    print("***** ***** QUESTION 6 SUMMARY ***** *****")
    print(f"Here is the data for Question 6 (Top 10 Calder Voting).")
    print(
        f"Out of a possible {pos_answers} answers, {int(sum(x))} answers were recieved.")
    print(f"{q6_nan_sum} possible answers were not completed.")
    print(f"{len(x)} different answers were provided for this question.")
    print("Here are the various answers people provided for this question, in descending order of frequency:")
    print(x)
    a = df['q7a1'].value_counts()
    b = df['q7a2'].value_counts()
    c = df['q7a3'].value_counts()
    d = df['q7a4'].value_counts()
    e = df['q7a5'].value_counts()
    q7_nan_sum = 0
    for question in q7:
        temp_nan = df[question].isna().sum()
        q7_nan_sum += temp_nan
    x = a.add(b, fill_value=0).add(c, fill_value=0).add(
        d, fill_value=0).add(e, fill_value=0)
    x = x.sort_values(ascending=False)
    print("***** ***** QUESTION 7 SUMMARY ***** *****")
    print(f"Here is the data for Question 7 (Top 10 Norris Voting).")
    print(
        f"Out of a possible {pos_answers} answers, {int(sum(x))} answers were recieved.")
    print(f"{q7_nan_sum} possible answers were not completed.")
    print(f"{len(x)} different answers were provided for this question.")
    print("Here are the various answers people provided for this question, in descending order of frequency:")
    print(x)
    a = df['q8a1'].value_counts()
    b = df['q8a2'].value_counts()
    c = df['q8a3'].value_counts()
    d = df['q8a4'].value_counts()
    e = df['q8a5'].value_counts()
    q8_nan_sum = 0
    for question in q8:
        temp_nan = df[question].isna().sum()
        q8_nan_sum += temp_nan
    x = a.add(b, fill_value=0).add(c, fill_value=0).add(
        d, fill_value=0).add(e, fill_value=0)
    x = x.sort_values(ascending=False)
    print("***** ***** QUESTION 8 SUMMARY ***** *****")
    print(f"Here is the data for Question 8 (Top 15 Hart Voting).")
    print(
        f"Out of a possible {pos_answers} answers, {int(sum(x))} answers were recieved.")
    print(f"{q8_nan_sum} possible answers were not completed.")
    print(f"{len(x)} different answers were provided for this question.")
    print("Here are the various answers people provided for this question, in descending order of frequency:")
    print(x)
    a = df['q9a1'].value_counts()
    b = df['q9a2'].value_counts()
    c = df['q9a3'].value_counts()
    d = df['q9a4'].value_counts()
    e = df['q9a5'].value_counts()
    q9_nan_sum = 0
    for question in q9:
        temp_nan = df[question].isna().sum()
        q9_nan_sum += temp_nan
    x = a.add(b, fill_value=0).add(c, fill_value=0).add(
        d, fill_value=0).add(e, fill_value=0)
    x = x.sort_values(ascending=False)
    print("***** ***** QUESTION 9 SUMMARY ***** *****")
    print(f"Here is the data for Question 9 (NHL roster players to change teams).")
    print(
        f"Out of a possible {pos_answers} answers, {int(sum(x))} answers were recieved.")
    print(f"{q9_nan_sum} possible answers were not completed.")
    print(f"{len(x)} different answers were provided for this question.")
    print("Here are the various answers people provided for this question, in descending order of frequency:")
    print(x)
    x = df['q10a1'].value_counts()
    q10_nan_sum = df.q10a1.isna().sum()
    x = x.sort_values(ascending=False)
    print("***** ***** QUESTION 10 SUMMARY ***** *****")
    print(f"Here is the data for Bonus Question 10 (earn 100+ points, not including McDavid).")
    print(
        f"Out of a possible {num_entries} answers, {int(sum(x))} answers were recieved.")
    print(f"{q10_nan_sum} possible answers were not completed.")
    print(f"{len(x)} different answers were provided for this question.")
    print("Here are the various answers people provided for this question, in descending order of frequency:")
    print(x)


def save_to_csv(df):
    """This function saves the provided cleaned, standardized
    dataframe to a .csv file. 
    """
    # Save the dataframe to a .csv file
    print("********** SAVING DATAFRAME TO SPREADSHEET (.CSV) **********")
    print("The complete standardized dataframe of entries and their answers will be saved to .csv.")
    print("This will allow for exploration in a spreadsheet with Excel, Google Sheets, etc.")
    df.to_csv('contest_entries_clean.csv')
    print("This data has been saved in the file 'contest_entries_clean.csv'.")
    print("Thank you!")


def main():
    print("Please provide the relative path to the html page you wish to scrape.")
    print("This page's comments will be scraped for entries to the 2021-22 Down Goes Brown Prediction Contest.")
    source_html = input("Path to .html: ")
    authors, comments = entry_scraper(source_html)
    major_surgery_count, authors, comments = comment_fixer(authors, comments)
    df = generate_dataframe(authors, comments)
    df, minor_surgery_count = dataframe_fixer(df)
    df = standardization_operations(df, authors)
    reporting_operations(df, minor_surgery_count, major_surgery_count)
    save_to_csv(df)


if __name__ == "__main__":
    main()
