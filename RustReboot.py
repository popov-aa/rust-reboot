import sys, getopt
import subprocess
import sys
import webrcon
import websockets
import asyncio
import time
from datetime import datetime

def printHelpAndExit(result):
  print('RustReboot.py --host <host> --port <port> --password <password>')
  sys.exit(result)


def callbackFunc(someArg):
  print('Wow')


def runCommand(loop, connector, command):
  loop.run_until_complete(connector.command(command, callbackFunc))


def main(argv):
  host = None
  port = None
  password = None

  try:
    opts, args = getopt.getopt(argv, "", ["help", "host=", "port=", "password="])
  except getoptGetoptError:
    printHelpAndExit(1)
  for opt, arg in opts:
    if opt == '--help':
      printHelpAndExit(0)
    if opt == '--host':
      host = arg
    elif opt == '--port':
      port = arg
    elif opt == "--password":
      password = arg

  if host == None or port == None or password == None:
    printHelpAndExit(1)

  loop = asyncio.get_event_loop()
  connector = webrcon.RconConnector(host, port, password, message_callback=None, console_callback=None)
  loop.run_until_complete(connector.start(loop))


  minutesLeft = 60
  while minutesLeft > 10:
    runCommand(loop, connector, 'say Внимание! Перезагрузка сервера состоится через %s минут.' % minutesLeft)
    time.sleep(600)
    minutesLeft -= 10

  while minutesLeft > 1:
    runCommand(loop, connector, 'say Внимание! Перезагрузка сервера состоится через %s минут.' % minutesLeft)
    time.sleep(60)
    minutesLeft -= 1

  secondsLeft = 60
  while secondsLeft > 10:
    runCommand(loop, connector, 'say Внимание! Перезагрузка сервера состоится через %s секунд.' % secondsLeft)
    time.sleep(10)
    secondsLeft -= 10

  while secondsLeft > 0:
    runCommand(loop, connector, 'say Внимание! Перезагрузка сервера состоится через %s секунд.' % secondsLeft)
    time.sleep(1)
    secondsLeft -= 1

  runCommand(loop, connector, 'say Перезагрузка!')
  runCommand(loop, connector, 'server.save')
  loop.run_until_complete(connector.close())
  exit(0)

if __name__ == "__main__":
  main(sys.argv[1:])
