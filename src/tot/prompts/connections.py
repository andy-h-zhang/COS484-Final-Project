# 5 shot
standard_prompt = '''Given a collection of 16 randomly sorted words, generate an output of 4 groups separated by commas of exactly 4 words that share some common category. Please use the format of the examples given and add nothing more:

Input: Dog Pop Ball Sock Slug Frog Glove Trot Bat Hound Globe Pound Orb Newt Hole Sphere
Output: Ball Globe Orb Sphere, Pop Pound Slug Sock, Bat Dog Frog Newt, Glove Hole Hound Trot
Input: Pound Locker Level Crater Nail Hills Cape Hanger Pulse Hammer Beat Gorge Ball Ridge Print Thump
Output: Beat Pound Pulse Thump, Cape Crater Gorge Ridge, Ball Hills Locker Print, Hammer Hanger Level Nail
Input: Crossword Time Star Sign Rainbow Menu Contract Billboard Banner People Grimace Engage Retain Header Semblance Sidebar
Output: Banner Header Menu Sidebar, Contract Engage Retain Sign, Billboard People Star Time, Crossword Grimace Rainbow Semblance
Input: Spin Art Wave Flag Flop Angle Wilt Turn Anon River Whistle Slant Hole Hail Bias Thou
Output: Anon Art Thou Wilt, Flop Hole River Turn, Angle Bias Slant Spin, Flag Hail Wave Whistle
Input: Hunt Check Game Ford President Play Car Stop Oxen Block Movie Actor Dam Dysentery Director Concert
Output: Concert Game Movie Play, Block Check Dam Stop, Actor Car Director President, Dysentery Ford Hunt Oxen
Input: {}
Output: 
'''

# 5 shot
cot_prompt = '''Given a collection of 16 randomly sorted words, generate thoughts in parantheses about which 4 words might share some common category, and then generate an output of exactly 4 groups separated by commas of exactly 4 words that share some common category. Please use the format of the following examples and add nothing else. You cannot write anything after Output:

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

Input: {}
'''

# 1 shot
propose_prompt = '''Given the words below, try to guess the most likely {} different categories that exactly four of the words have in common. Note, that whatever words you don't choose must also form groups of four that share a category in common. Please stick to the following format example (which in this case picks the three mostly likely categories out of eight words) and nothing more - providing the thoughts in alphabetical order with the category in parentheses:

Input: Movie Check Block Game Concert Play Dam Stop
Thoughts: Block Check Dam Stop (Restrict), Concert Game Movie Play (Ticketed Events), Check Game Play Stop (Games)

Input: {}
Thoughts:
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

Input: {}
Output:
'''