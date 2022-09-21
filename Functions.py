import re
#The only library we are importing is regex

#process_regex()
#Regular expressions part of the code - 2 steps are implemented here.
#British english words that have "ou" are converted to american spelling with just "o"
def process_regex(path_to_text_file):
     print("Processing file...")
     #reading the dante_inf file here and saving all the text as string in new_contents
     with open(path_to_text_file,'r') as f:
          contents=f.read()
          #new contents is the same as contents, just saving in to a different variable to perform some regex functions
          new_contents = contents

          #words is a dictionary containing all the "ou" words. The key is the British word and value is the corresponding American English spelling for the same word
          #substitutes for both lower and upper cases, as well as words with "ou" words as root. for example colourful
          words = {'[Aa]rbour':'arbor', '[Aa]rdour':'ardor', '[Aa]rmour':'armor','[Bb]ehaviour':'behavior','[Cc]andour':'candor', '[Cc]lamour':'clamor','[Cc]olour':	'color', '[Dd]emeanour':	'demeanor', '[Ee]ndeavour':	'endeavor', '[Ff]avour':	'favor', '[Ff]lavour':	'flavor', '[Hh]arbour':	'habor','[Hh]onour' :	'honor','[Hh]umour':	'humor','[Ll]abour':	'labor', '[Nn]eighbour':'neighbor', '[Oo]dour':	'odor', '[Pp]arlour':	'parlor', '[Rr]ancour':	'rancor','[Rr]igour':	'rigor','[Rr]umour':	'rumor', '[Ss]aviour':'savior','[Ss]avour':'savor', '[Ss]plendour':'splendor', '[Tt]umour':'tumor', '[Vv]alour':'valor','[Vv]igour':'vigor'}
          
          #reading the dante_inf file and substituting british words with american counterparts
          for key,value in words.items():
               new_contents = re.sub(key,value,new_contents)
          
          #In this step, the titles like Mr. Dr. etc are substituted with expanded forms of the titles
          #expansions is a dictionary with titles as key and expanded titles as values. Works for both lower and upper cases
          expansions = {"[Mm]rs.": "Misses","[Mm]r.": "Mister", "[Dd]r.": "Doctor","[Mm]s.": "Miss"}
          for key,value in expansions.items():
             new_contents = re.sub(key,value,new_contents)
          
          #After 2 steps of regex, the edited text - new_contents has to be saved into a file called regex.txt 
          return_file_path="regex.txt"
          with open(return_file_path, "w") as new:
             new.write(new_contents)
     print("Output stored to 'regex.txt'")
     #return(return_file_path)

#normalise_text() #This is the normalization part of the code.  
#normalize_text takes the output from regex as input 
# #reading the file content into a variable re_data and saving all the data as a string
def normalize_text(regex_file):
     print("Normalizing text...")
     with open(regex_file) as r:
          re_data = r.read()
     

     #convert to lower case. Using regex lower() #takes re_data i.e., output of regex step as input here
     lower_string = re_data.lower()

     # remove numbers. Removing numbers since we don't need them in a dictionary, using sub and regex pattern
     #lower_string is all the data in lower case and output from previous step
     #\d+ matches any digit character and is replaced with "" 
     no_number_string = re.sub(r'\d+','',lower_string)
     

     #remove special characters other than ' for words like he's we're etc
     #[^A-Za-z\s']+ matches any character that is not in (A-Z range, a-z range, whitespace, ' and -) and substitutes it with "", basically removes it.
     no_punctuation_string = re.sub("[^A-Za-z\s'-]+","",no_number_string)
     #for words like divinely-constituted, removing the hyphen - would turn it into a single word. So, replacing - with a single space
     no_punctuation_string1 = no_punctuation_string.replace("-", " ")
     

     #Since the entire text is a single string right now, using the split() function to split the lines by *space* to get a list of all the words, i.e., list of strings
     list_words = no_punctuation_string1.split()
     #this output is a list
     
     #dante_inf has words in quotations, for example "He is cool". When split, this becomes list of strings "He, is, cool" 
     #So to remove extra quotes like in "happy", using strip which removes the given characters from the beginning and end of the string
     #the apostrophe in the middle of word is not affected, like he's or Bob's
     #each word is then appended into a new list
     listwords1 = []
     for word in list_words:
          new_word = word.strip("\'")
          listwords1.append(new_word)

     #Words shouldn't appear twice in dictionaries. So, we have to remove duplicates
     #So converting this into a set which removes duplicates and then converting it back into a list to sort
     without_duplicates = [*set(listwords1)]
     

     #To sort the words in the list, using sort(). Produces an ordered list of strings
     without_duplicates.sort()
     
     #without_duplicates is a list. We want to save the words in this list into a file as a string
     #with one word in one line, like in an actual dictionary
     #using join method to join all list items into a string and " " space as a seperator
     dictionary_words_txt = ' '.join(without_duplicates)
     
     #the final dictionary is saved in dictionary.txt
     dict_file="dictionary.txt"
     with open(dict_file, 'w') as d:
          #splitting by space to make sure each word goes into a new line later
          a=dictionary_words_txt.split()
          for i in a:
               d.write(i+"\n")
     print("Output stored to 'dictionary.txt'")
     #return(dict_file)


#levenshtein minimum distance
#used an online reference for levenshtein distance
def levenshtein(s, t):
     
        #levenshtein(s, t) -> ldist #ldist is the Levenshtein distance between the strings 
        #where s will be the word from the user input to spell checker and t will be the word from our dictionary made from dante_inf words
        #For all i and j, dist[i,j] will contain the Levenshtein distance between the first i characters of s and the first j characters of t
    
    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]

    # source prefixes can be transformed into empty strings 
    # by deletions:
    for i in range(1, rows):
        dist[i][0] = i

    # target prefixes can be created from an empty source string
    # by inserting the characters
    for i in range(1, cols):
        dist[0][i] = i
        
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = 2
            dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                 dist[row][col-1] + 1,      # insertion
                                 dist[row-1][col-1] + cost) # substitution
 
    return dist[row][col]
# returns levenshtein distance between two strings

#Main spell checker function
def spell_checker():
     #the user input is a string
     input_string=""
     print("----------------------------------------\nWelcome to the spell checker!\nPlease enter a text to check spelling or enter quit to exit the program.")
     while(True):
          print("\n-----------------------------------------\nEnter text to be checked:",end='')
          input_string=input()
          #if the text entered by user is not quit, text goes to the spell checker
          if(input_string!='quit'):
               checker(input_string)
          #if user types "quit", they exit the spell checker
          else:
               print('Goodbye!')
               break

#checker function takes the user input from spell checker if it is not "quit"
def checker(input_string):
     #the string entered by user is split by space and saved as a list of strings
     words=input_string.split()
     #using the dictionary.txt here to see if the words entered by user exist in our dictionary
     f=open('dictionary.txt','r')
     dictionary=f.read()

     #created a list misspelt to save any missplet words
     misspelt=[]

     #words is the list containing the words entered by the user
     for word in words:
          if word not in dictionary:
               #if that word doesn't exist in our dictiuonary, using append to add it to the list misspelt
               misspelt.append(word)
     #if the list is empty, it means no spelling errors
     if(len(misspelt)==0):
          print("No misspellings detected!")
     #if there are misspelt words, we are going to suggesr some words
     else:
          print("Misspelling - Suggestion")
          print("----------------------------------------")
          for misspelt_word in misspelt:
               suggestions={} 
               #suggestions is a dictionary to store a few words that we think the user wanted to spell, in place of the misspelt word as values
               #it will also contain levenshtein distance as key 
               suggested_words=[]
               dictionary_words=dictionary.split()
               #a list of all the words in our dictionary

               for dict_word in dictionary_words:
                    calculated_distance = levenshtein(misspelt_word,dict_word)
                    #calling levenshtein distance fn here to calculate the distance between the misspelt word and each of the words in our dictionary
                    suggestions= add_suggestions(suggestions,calculated_distance,dict_word)
                    #add_suggestions function
               minimum_key=min(sorted(suggestions))
               suggested_words.extend(suggestions[minimum_key])
               suggested_words.extend(suggestions[minimum_key+1])
               for k in suggested_words:
                    if (len(k)!=len(misspelt_word)):
                         suggested_words.remove(k)
               print(misspelt_word+'-',end='')
               print(suggested_words)
     return

#add_suggestions functions takes the dictionary(contains all words in the dictionary.txt as a )
def add_suggestions(dictionary,key,add_values):
     if key not in dictionary:
          dictionary[key] = list()
     dictionary[key].append(add_values)
     return dictionary


#-------------------------
def spell_checker():
     print("----------------------------------------")
     print("Welcome to the spell checker!")
     print("Please enter a text to check spelling or enter quit to exit the program.")
     print("-----------------------------------------")

     misspelt = {}
     suggestions_list = []
     input_string = input("Enter text here:")
     input_words = input_string.split()
     with open("dictionary.txt") as dict:
          dante_dictionary = dict.read()
     dante_words = dante_dictionary.split() 
     
     if(input_string=="quit"):
          print(input_string)
     else:
          for word in input_words:
               if word not in dante_dictionary:
                    for s in dante_words:
                         misspelt[levenshtein(word, s)] = s
                    print(misspelt)
                    for distance, suggestion in misspelt.items():
                         min_distance = min(misspelt.keys())
                         if distance == min_distance:
                              suggestions_list.append(suggestion)
                         print(suggestions_list)


#main
regex_file=process_regex("dante_inf.txt")
dict_file=normalize_text("regex.txt")
spell_checker()