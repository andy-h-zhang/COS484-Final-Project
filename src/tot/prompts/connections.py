# 5 shot
standard_prompt = ''' Given a collection of 16 randomly sorted words, generate an output of 4 groups of 4 words that share some common category.

Input: Dog Pop Ball Sock Slug Frog Glove Trot Bat Hound Globe Pound Orb Newt Hole Sphere
Output: Ball Globe Orb Sphere (Round Three-Dimensional Objects), Pop Pound Slug Sock (Punch), Bat Dog Frog Newt (Animals in the Witches' Brew in MacBeth), Glove Hole Hound Trot (Fox ___)
Input: Pound Locker Level Crater Nail Hills Cape Hanger Pulse Hammer Beat Gorge Ball Ridge Print Thump
Output: Beat Pound Pulse Thump (Throb), Cape Crater Gorge Ridge (Landforms), Ball Hills Locker Print (Foot ___), Hammer Hanger Level Nail (Picture Hanging Needs)
Input: Crossword Time Star Sign Rainbow Menu Contract Billboard Banner People Grimace Engage Retain Header Semblance Sidebar
Output: Banner Header Menu Sidebar (Parts of a Website), Contract Engage Retain Sign (Employ), Billboard People Star Time (Magazines), Crossword Grimace Rainbow Semblance (Ending with Medieval Weapons)
Input: Spin Art Wave Flag Flop Angle Wilt Turn Anon River Whistle Slant Hole Hail Bias Thou
Output: Anon Art Thou Wilt (Shakespearean Words), Flop Hole River Turn (Cards in Texas Hold Em), Angle Bias Slant Spin (Partiality), Flag Hail Wave Whistle (Signal Down, as a Taxi)
Input: Spin Shadow Excellent Juke
Output:

'''


cot_prompt = ''' Given a collection of 16 randomly sorted words, generate thoughts about which 4 words might share some common category, and then generate an output of 4 groups of 4 words that share some common category.

'''