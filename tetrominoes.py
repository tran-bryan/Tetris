#Filler Arrays of Tetris pieces
#I piece
Ione = [
[0,0,0,0],
[0,0,0,0],
[1,1,1,1],
[0,0,0,0]
]
Itwo= [
[0,0,1,0],
[0,0,1,0],
[0,0,1,0],
[0,0,1,0]
]
Ipiece=[Ione, Itwo, Ione, Itwo]


#T piece
Tone=[
[0,0,0,0],
[0,0,1,0],
[0,1,1,1],
[0,0,0,0]
]
Ttwo=[
[0,0,0,0],
[0,0,1,0],
[0,0,1,1],
[0,0,1,0]
]
Tthree=[
[0,0,0,0],
[0,0,0,0],
[0,1,1,1],
[0,0,1,0]
]
Tfour=[
[0,0,0,0],
[0,0,1,0],
[0,1,1,0],
[0,0,1,0]
]
Tpiece=[Tone, Ttwo, Tthree, Tfour]


#Square Piece
Square=[
[0,0,0,0],
[0,1,1,0],
[0,1,1,0],
[0,0,0,0]
]
Squarepeice=[Square, Square, Square, Square]


#L piece
Lone=[
[0,0,0,0],
[0,0,0,1],
[0,1,1,1],
[0,0,0,0]
]
Ltwo=[
[0,0,0,0],
[0,0,1,0],
[0,0,1,0],
[0,0,1,1]
]
Lthree=[
[0,0,0,0],
[0,0,0,0],
[0,1,1,1],
[0,1,0,0]
]
Lfour=[
[0,0,0,0],
[0,1,1,0],
[0,0,1,0],
[0,0,1,0]
]
Lpeice=[Lone, Ltwo, Lthree, Lfour]


#Reverse L piece
reverseLone=[
[0,0,0,0],
[0,1,0,0],
[0,1,1,1],
[0,0,0,0]
]
reverseLtwo=[
[0,0,0,0],
[0,0,1,1],
[0,0,1,0],
[0,0,1,0]
]
reverseLthree=[
[0,0,0,0],
[0,0,0,0],
[0,1,1,1],
[0,0,0,1]
]
reverseLfour=[
[0,0,0,0],
[0,0,1,0],
[0,0,1,0],
[0,1,1,0]
]
reverseLpeice=[reverseLone, reverseLtwo, reverseLthree, reverseLfour]


#S piece
Sone=[
[0,0,0,0],
[0,0,1,1],
[0,1,1,0],
[0,0,0,0]
]
Stwo=[
[0,0,0,0],
[0,1,0,0],
[0,1,1,0],
[0,0,1,0]
]
Speice=[Sone, Stwo, Sone, Stwo]


#Reverse S or the Z piece
reverseSone=[
[0,0,0,0],
[0,1,1,0],
[0,0,1,1],
[0,0,0,0]
]
reverseStwo=[
[0,0,0,0],
[0,0,1,0],
[0,1,1,0],
[0,1,0,0]
]
reverseSpeice=[reverseSone, reverseStwo, reverseSone, reverseStwo]

#Set of all the peices
setofRandompieces=[Ipiece, Tpiece, Lpeice, reverseLpeice, Speice, reverseSpeice, Squarepeice]
