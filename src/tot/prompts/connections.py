# 5 shot
standard_prompt = '''Given 16 words, make 4 groups of exactly 4 words that share some common category. Only produce the Output, no added enumeration or formatting.:

Input: DOG POP BALL SOCK SLUG FROG GLOVE TROT BAT HOUND GLOBE POUND ORB NEWT HOLE SPHERE
Output: BALL GLOBE ORB SPHERE, POP POUND SLUG SOCK, BAT DOG FROG NEWT, GLOVE HOLE HOUND TROT

Input: POUND LOCKER LEVEL CRATER NAIL HILLS CAPE HANGER PULSE HAMMER BEAT GORGE BALL RIDGE PRINT THUMP
Output: BEAT POUND PULSE THUMP, CAPE CRATER GORGE RIDGE, BALL HILLS LOCKER PRINT, HAMMER HANGER LEVEL NAIL

Input: CROSSWORD TIME STAR SIGN RAINBOW MENU CONTRACT BILLBOARD BANNER PEOPLE GRIMACE ENGAGE RETAIN HEADER SEMBLANCE SIDEBAR
Output: BANNER HEADER MENU SIDEBAR, CONTRACT ENGAGE RETAIN SIGN, BILLBOARD PEOPLE STAR TIME, CROSSWORD GRIMACE RAINBOW SEMBLANCE

Input: SPIN ART WAVE FLAG FLOP ANGLE WILT TURN ANON RIVER WHISTLE SLANT HOLE HAIL BIAS THOU
Output: ANON ART THOU WILT, FLOP HOLE RIVER TURN, ANGLE BIAS SLANT SPIN, FLAG HAIL WAVE WHISTLE

Input: HUNT CHECK GAME FORD PRESIDENT PLAY CAR STOP OXEN BLOCK MOVIE ACTOR DAM DYSENTERY DIRECTOR CONCERT
Output: CONCERT GAME MOVIE PLAY, BLOCK CHECK DAM STOP, ACTOR CAR DIRECTOR PRESIDENT, DYSENTERY FORD HUNT OXEN

Input: {input}
Output: 
'''

# 3 shot
cot_prompt = '''Given 16 words, make 4 groups of exactly 4 words that share some common category. Each step, generate thoughts about what the possible groups could be as seen in the examples. End with the Output, no added enumeration or formatting.

Input: DOG POP BALL SOCK SLUG FROG GLOVE TROT BAT HOUND GLOBE POUND ORB NEWT HOLE SPHERE
Thoughts: 
    BALL GLOBE ORB SPHERE round three-dimensional objects (left: DOG POP SOCK SLUG FROG GLOVE TROT BAT HOUND POUND NEWT HOLE)
    BALL GLOBE ORB SPHERE round three-dimensional objects, POP POUND SLUG SOCK describe hitting or punching something (left: DOG FROG GLOVE TROT BAT HOUND NEWT HOLE)
    BALL GLOBE ORB SPHERE round three-dimensional objects, POP POUND SLUG SOCK describe hitting or punching something, BAT DOG FROG NEWT animals used in the Witches Brew in MacBeth (left: GLOVE HOLE HOUND TROT)
    BALL GLOBE ORB SPHERE round three-dimensional objects, POP POUND SLUG SOCK describe hitting or punching something, BAT DOG FROG NEWT animals used in the Witches Brew in MacBeth, GLOVE HOLE HOUND TROT follow the word Fox
Output: BALL GLOBE ORB SPHERE, POP POUND SLUG SOCK, BAT DOG FROG NEWT, GLOVE HOLE HOUND TROT

Input: POUND LOCKER LEVEL CRATER NAIL HILLS CAPE HANGER PULSE HAMMER BEAT GORGE BALL RIDGE PRINT THUMP
Thoughts: 
    BEAT POUND PULSE THUMP synonyms for throb (left: LOCKER LEVEL CRATER NAIL HILLS CAPE HANGER HAMMER GORGE BALL RIDGE PRINT)
    BEAT POUND PULSE THUMP synonyms for throb, CAPE CRATER GORGE RIDGE are all landforms (left: LOCKER LEVEL NAIL HILLS HANGER HAMMER BALL PRINT)
    BEAT POUND PULSE THUMP synonyms for throb, CAPE CRATER GORGE RIDGE are all landforms, BALL HILLS LOCKER PRINT words that follow the word Foot (left: LEVEL NAIL HANGER HAMMER)
    BEAT POUND PULSE THUMP synonyms for throb, CAPE CRATER GORGE RIDGE are all landforms, BALL HILLS LOCKER PRINT words that follow the word Foot, LEVEL NAIL HANGER HAMMER used to hang pictures
Output: BEAT POUND PULSE THUMP, CAPE CRATER GORGE RIDGE, BALL HILLS LOCKER PRINT, HAMMER HANGER LEVEL NAIL

Input: CROSSWORD TIME STAR SIGN RAINBOW MENU CONTRACT BILLBOARD BANNER PEOPLE GRIMACE ENGAGE RETAIN HEADER SEMBLANCE SIDEBAR
Thoughts: 
    BANNER HEADER MENU SIDEBAR are parts of a website (left: CROSSWORD TIME STAR SIGN RAINBOW CONTRACT BILLBOARD PEOPLE GRIMACE ENGAGE RETAIN SEMBLANCE)
    BANNER HEADER MENU SIDEBAR are parts of a website, CONTRACT ENGAGE RETAIN SIGN are synonyms of Employ (left: CROSSWORD TIME STAR RAINBOW BILLBOARD PEOPLE GRIMACE SEMBLANCE)
    BANNER HEADER MENU SIDEBAR are parts of a website, CONTRACT ENGAGE RETAIN SIGN are synonyms of Employ, BILLBOARD PEOPLE STAR TIME are all magazines (left: CROSSWORD RAINBOW GRIMACE SEMBLANCE)
    BANNER HEADER MENU SIDEBAR are parts of a website, CONTRACT ENGAGE RETAIN SIGN are synonyms of Employ, BILLBOARD PEOPLE STAR TIME are all magazines, CROSSWORD RAINBOW GRIMACE SEMBLANCE words that end with medieval weapons in their name
Output: BANNER HEADER MENU SIDEBAR, CONTRACT ENGAGE RETAIN SIGN, BILLBOARD PEOPLE STAR TIME, CROSSWORD GRIMACE RAINBOW SEMBLANCE

Input: {input}
Thoughts:
Output:
'''

# 1 shot
propose_prompt = '''Form groups of four words that share some common category. End with the Input and Possible groups, no added enumeration, commentary, self analysis, or formatting. Put **all** unused words in parantheses as seen below.

Input: PUMP FOOT TIME SEA LEAGUE LOAFER WHY US BOOT YARD PEOPLE ARE MILE SNEAKER QUEUE ESSENCE

Possible next steps:
PUMP BOOT LOAFER SNEAKER types of footwear (left: FOOT TIME SEA LEAGUE WHY US YARD PEOPLE ARE MILE QUEUE ESSENCE)
MILE YARD FOOT LEAGUE units of measurement for distance (left: PUMP TIME SEA LOAFER WHY US BOOT PEOPLE ARE SNEAKER QUEUE ESSENCE)
TIME QUEUE WHY ARE abstract or philosophical concepts (left: PUMP FOOT SEA LEAGUE LOAFER US BOOT YARD PEOPLE MILE SNEAKER ESSENCE)
PEOPLE US ESSENCE SEA relate to identity or being (left: PUMP FOOT TIME LEAGUE LOAFER WHY BOOT YARD ARE MILE SNEAKER QUEUE)
PEOPLE US ARE WHY relate to humans/social concepts (left: PUMP FOOT TIME SEA LEAGUE LOAFER WHY US BOOT YARD PEOPLE ARE MILE SNEAKER QUEUE ESSENCE)
SEA LEAGUE YARD QUEUE naval or maritime terms (left: PUMP FOOT TIME LOAFER WHY US BOOT PEOPLE ARE MILE SNEAKER ESSENCE)
TIME US PEOPLE ESSENCE names of magazines (left: PUMP FOOT SEA LEAGUE LOAFER WHY BOOT YARD ARE MILE SNEAKER QUEUE)
SEA WHY ARE QUEUE letter homophones (left: PUMP FOOT TIME LEAGUE LOAFER US BOOT YARD PEOPLE MILE SNEAKER ESSENCE)

Input: {input}
Possible next steps:
'''

# 5 shot
value_prompt =  '''Given some words along with a category that might relate them, evaluate how confident you feel in the combinations are on a scale from 0-1 using 1 decimal point. Put **all** unused words in parantheses as seen below.


Input: BALL GLOBE ORB SPHERE round three-dimensional objects (left: DOG POP SOCK SLUG FROG GLOVE TROT BAT HOUND POUND NEWT HOLE)
Value: 0.6

Input: BALL GLOBE ORB SPHERE round three-dimensional objects, POP POUND SLUG SOCK describe hitting or punching something (left: DOG FROG GLOVE TROT BAT HOUND NEWT HOLE)
Value: 0.8

Input: BALL GLOBE ORB SPHERE round three-dimensional objects, POP POUND SLUG SOCK describe hitting or punching something, BAT DOG FROG NEWT animals used in the Witches Brew in MacBeth (left: GLOVE HOLE HOUND TROT)
Value: 0.7

Input: BALL GLOBE ORB SPHERE round three-dimensional objects, POP POUND SLUG SOCK describe hitting or punching something, BAT DOG FROG NEWT animals used in the Witches Brew in MacBeth, GLOVE HOLE HOUND TROT follow the word Fox
Value: 0.8

Reply with whatever reasoning you like, **then** END your answer on a single line containing your confidence rating on a scale from 0-1 using 1 decimal point.
Input: {input}
Value: '''

value_last_step_prompt = '''Given an input of 16 words and a proposed answer consisting of 4 groups of 4, evaluate whether all four groups have exactly four distinct words in meaningful groupings, and that no word is repeated. End with the final answer Output, no added enumeration or formatting.

Input: DOG POP BALL SOCK SLUG FROG GLOVE TROT BAT HOUND GLOBE POUND ORB NEWT HOLE SPHERE
Thoughts: BALL GLOBE ORB SPHERE round three-dimensional objects, POP POUND SLUG SOCK describe hitting or punching something, BAT DOG FROG NEWT animals used in the Witches Brew in MacBeth, GLOVE HOLE HOUND TROT follow the word Fox
Output: BALL GLOBE ORB SPHERE, POP POUND SLUG SOCK, BAT DOG FROG NEWT, GLOVE HOLE HOUND TROT

Input: {input}  
Thoughts:
Output: {output}'''