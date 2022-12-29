import discord
import os
import random
from keep_alive import keep_alive

client = discord.Client()

board = [ [2, 0, 0],
          [2, 0, 0],
          [0, 0, 0]]

#the current state of each square in the board
state = {0 : '       ',
          1 : '  X  ',
          2 : '  O  ',}

#the inputs and which square they change
coordsDict = {'$p tl' : (0, 0), 
              "$p tm" : (0, 1),
              "$p tr" : (0, 2),
              "$p ml" : (1, 0),
              "$p mm" : (1, 1),
              "$p mr" : (1, 2),
              "$p bl" : (2, 0),
              "$p bm" : (2, 1),
              "$p br" : (2, 2)}

turns = [0]
playingBot = [False]
playingBotMedium = [False]

def drawBoard(board, state):
  boardStr = ""
  boardStr += '-----------------\n'

  for line in board:
    lineStr = '|'
    for val in line:
      lineStr += state[val] + '|'
    lineStr += '\n'
    boardStr += lineStr + '-----------------\n'

  return boardStr

#checks for a winner horizontally
def checkRows(board):
  for line in board:
    if line == [1, 1, 1]:
      return "x"
    elif line == [2, 2, 2]:
      return "O"
  return ""

#checks for a winner vertically
def checkColumns(board):
  newBoard = [[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0]]

  for x in range(3):
    for y in range(3):
      newBoard[x][y] = board[y][x]

  return checkRows(newBoard)

#checks for a winner diagonally
def checkDiagonal(board):
  dig1 = [board[0][0], board[1][1], board[2][2]]
  dig2 = [board[0][2], board[1][1], board[2][0]]
  digs = [dig1, dig2]
  return checkRows(digs)

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):

  msg = message.content

  #sends information into a channel on how to play the game
  if msg.startswith("$tiktachow"):
    await message.channel.send("for a new game do $newgame, to play do $p __, to pick a space, the commands are t-top, m-middle, b-bottom, l-left, m-middle, r-right, so if you wanted to top left space it would be $p tl. This only supports two people playing at a time, in future am planning on allowing you to play against the bot")

  def set_to_zero(coords, board):
    board[coords[0]][coords[1]] = 0

  def set_to_one(coords, board):
    board[coords[0]][coords[1]] = 1

  def set_to_two(coords, board):
    board[coords[0]][coords[1]] = 2

  #changes every square state to 0
  def resetBoard(board):
    for x in range(3):
      for y in range(3):
        board[x][y] = 0

    turns[0] = 0

  #checks if a space already has been changed
  def notChosen(coords, board):
    if board[coords[0]][coords[1]] == 0:
      return True
    else:
      return False

  #checks if all places on the board have been taken
  def boardFull(board):
    for x in range(3):
      for y in range(3):
        if board[x][y] == 0: return False
    return True

  def checkWin(coords, board):
    for line in board:
      if line == [1, 1, 0]:
        return line, "2"

  #starts a two person game
  if msg.startswith("$newgame"):
    resetBoard(board)
    await message.channel.send(drawBoard(board, state))

  #starts a bot game with different difficulties
  if msg.startswith("$playbot"):
    if msg.startswith("$playbot m"):
      playingBotMedium[0] = True
    else:
      playingBot[0] = True
    resetBoard(board)
    await message.channel.send("tiktacbot activated, you play first")
    await message.channel.send(drawBoard(board, state))
    
  if msg.lower() in coordsDict.keys():
    if notChosen(coordsDict[msg.lower()], board):
      if turns[0] % 2 == 0: 
        set_to_one(coordsDict[msg.lower()], board)
      else:
        set_to_two(coordsDict[msg.lower()], board)
      turns[0] += 1

      await message.channel.send(drawBoard(board, state))
      winner = checkRows(board)
      if not winner: winner = checkColumns(board)
      if not winner: winner = checkDiagonal(board)

      if winner:
        await message.channel.send(winner + ' wins!')
        resetBoard(board)
        playingBot[0] = False

      if boardFull(board):
        await message.channel.send("draw")
        resetBoard(board)
        playingBot[0] = False
        
      if playingBot[0]:
        botChoice = random.choice(list(coordsDict.keys()))
        while notChosen(coordsDict[botChoice], board) == False:
          botChoice = random.choice(list(coordsDict.keys()))
        set_to_two(coordsDict[botChoice], board)
        await message.channel.send(drawBoard(board, state))
        winner = checkRows(board)
        if not winner: winner = checkColumns(board)
        if not winner: winner = checkDiagonal(board)
        if not winner:
          turns[0] += 1
        else:
          await message.channel.send(winner + ' wins!')
          resetBoard(board)
          playingBot[0] = False

keep_alive()
client.run(os.getenv("TOKEN"))