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

# 5 shot
cot_prompt = '''Given 16 words, make 4 groups of exactly 4 words that share some common category. Each step, generate thoguhts about what the possible groups could be as seen in the examples. End with the Output, no added enumeration or formatting.:

Input: Dog Pop Ball Sock Slug Frog Glove Trot Bat Hound Globe Pound Orb Newt Hole Sphere
Thoughts: 
    Ball Globe Orb and Sphere resemble round, three-dimensional objects.
    Pop Pound Slug and Sock are words used to describe hitting or punching something.
    Bat Dog Frog and Newt are all animals used in the Witches Brew in MacBeth.
    Glove Hole Hound and Trot are words that follow the word Fox.
Output: Ball Globe Orb Sphere, Pop Pound Slug Sock, Bat Dog Frog Newt, Glove Hole Hound Trot

Input: Pound Locker Level Crater Nail Hills Cape Hanger Pulse Hammer Beat Gorge Ball Ridge Print Thump
Thoughts: 
    Beat Pound Pulse and Thump are synonyms for Throb.
    Cape Crater Gorge Ridge are all landforms.
    Ball Hills Locker Print are words that follow the word Foot.
    Hammer Hanger Level Nail are objects needed for hanging pictures.
Output: Beat Pound Pulse Thump, Cape Crater Gorge Ridge, Ball Hills Locker Print, Hammer Hanger Level Nail

Input: Crossword Time Star Sign Rainbow Menu Contract Billboard Banner People Grimace Engage Retain Header Semblance Sidebar
Thoughts: 
    Banner Header Menu Sidebar are parts of a website.
    Contract Engage Retain Sign are synonyms of Employ.
    Billboard People Star Time are all magazines.
    Crossword Grimace Rainbow Semblance are words that end with medieval weapons in their name.
Output: Banner Header Menu Sidebar, Contract Engage Retain Sign, Billboard People Star Time, Crossword Grimace Rainbow Semblance

Input: Spin Art Wave Flag Flop Angle Wilt Turn Anon River Whistle Slant Hole Hail Bias Thou
Thoughts: 
    Anon Art Thou Wilt are Shakespearean words.
    Flop Hole River Turn are cards used in Texas Hold Em.
    Angle Bias Slant Spin are words that represent partiality.
    Flag Hail Wave Whistle are different ways to signal down a taxi.
Output: Anon Art Thou Wilt, Flop Hole River Turn, Angle Bias Slant Spin, Flag Hail Wave Whistle

Input: Hunt Check Game Ford President Play Car Stop Oxen Block Movie Actor Dam Dysentery Director Concert
Thoughts: 
    Concert Game Movie Play are all ticketed events.
    Block Check Dam Stop are words that represent restricting.
    Actor Car Director President could represent a historical figure named Ford.
    Dysentery Ford Hunt Oxen are associated with the game, The Oregon Trail.
Output: Concert Game Movie Play, Block Check Dam Stop, Actor Car Director President, Dysentery Ford Hunt Oxen

Input: {input}
Output:
'''

# 1 shot
propose_prompt = '''Form groups of four words that share some common category. End with the Input and Possible groups, no added enumeration or formatting.
Input: Pump Foot Time Sea League Loafer Why Us Boot Yard People Are Mile Sneaker Queue Essence 

Possible groups:
Pump Boot Loafer Sneaker: types of footwear.
Mile Yard Foot League: units of measurement for distance.
Time Queue Why Are: abstract or philosophical concepts.
People Us Essence Sea: might relate to identity or being (though a bit abstract).
People Us Are Why: might be pronouns or relate to humans/social concepts.
Sea League Yard Queue: naval or maritime terms? Might be a stretch
Time Us People Essence: names of magazines
Sea Why Are Queue: letter homophones

Input: {input}
Possible groups:
'''

# 5 shot
value_prompt =  '''Given some words along with a category that might relate them in parentheses, evaluate how confident you feel in the combinations are on a scale from 0-1 using 1 decimal point. Note that a word cannot appear twice. Use the following examples and format exactly like them, adding nothing more:
Input: Block Check Dam Stop (Restrict), Concert Game Movie Play (Ticketed Events)
Output: 0.9

Input: Block Check Dam Stop (Restrict), Concert Check Movie Play (Ticketed Events)
Output: 0

Input: Ball Banana Showcase Period (Punctuation Marks)
Output: 0.1

Input: Anon Art Thou Wilt (Shakespearean Words), Flop Hole River Turn (Cards in Texas Hold Em), Angle Bias Slant Spin (Partiality)
Output: 0.8

Input: Anon Art Thou Wilt (Shakespearean Words)
Output: 0.9

Input: {input}
Output:
'''

value_last_step_prompt = '''Given an input of 16 words and a proposed answer consisting of 4 groups of 4, evaluate how confident you are that all four groups represent meaningful and distinct categories using only the provided words, and that no word is repeated. Output a score from 0.0 to 1.0 in increments of 0.1. Use the examples for reference.

Input: DOG POP BALL SOCK SLUG FROG GLOVE TROT BAT HOUND GLOBE POUND ORB NEWT HOLE SPHERE  
Answer: BALL GLOBE ORB SPHERE, POP POUND SLUG SOCK, BAT DOG FROG NEWT, GLOVE HOLE HOUND TROT  
Output: 1.0

Input: PUMP FOOT TIME SEA LEAGUE LOAFER WHY US BOOT YARD PEOPLE ARE MILE SNEAKER QUEUE ESSENCE  
Answer: FOOT SEA PEOPLE WHY, MILE YARD SNEAKER ESSENCE, TIME ARE US PUMP, BOOT LEAGUE LOAFER QUEUE  
Output: 0.3

Input: SPIN ART WAVE FLAG FLOP ANGLE WILT TURN ANON RIVER WHISTLE SLANT HOLE HAIL BIAS THOU  
Answer: ANON ART THOU WILT, FLOP HOLE RIVER TURN, ANGLE BIAS SLANT SPIN, FLAG HAIL WAVE WHISTLE  
Output: 1.0

Input: HUNT CHECK GAME FORD PRESIDENT PLAY CAR STOP OXEN BLOCK MOVIE ACTOR DAM DYSENTERY DIRECTOR CONCERT  
Answer: CONCERT GAME MOVIE PLAY, BLOCK CHECK DAM STOP, ACTOR CAR DIRECTOR PRESIDENT, DYSENTERY FORD HUNT OXEN  
Output: 1.0

Input: {input}  
Output: {output}  
Output:'''