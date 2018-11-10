# ==={ JUtils 2 by Ryan Jones }=== #
# Release Date: 11/8/2018

import datetime
import time
import traceback
import shlex
import sys

class Compatibility():
    """Provides simple methods to aid with compatibility."""
    def getVersion():
        """Returns a tuple providing the major, minor, patch, and pre-release identifier like so: (Major, Minor, Patch, Identifier)"""
        return (0, 2, 0, "")

    def getVersionString():
        """Returns the version in the following format: Major.Minor.Patch(-Pre-release Indetifier)\nThe identifier may be absent if the release is a full release."""
        versionData = Compatibility.getVersion()
        return ("%s.%s.%s" % versionData[:-1]) + ("" if len(versionData[3]) == 0 else "-%s" % versionData[3])

    def getSimpleVersion():
        """Returns a tuple providing the major, minor, and patch information for easier handing of compatibility."""
        return Compatibility.getVersion()[:-1]

    def getMajorVersion():
        """Returns the major version number."""
        return Compatibility.getVersion()[0]

class AdvancedMap():
    """Provides a simple methods to map and filter objects without having to nest and cast excessively."""
    def __init__(self, results = []):
        self.results = list(results)

    def mapData(self, function, data):
        """Does the same thing as map(), but it casts `data` to a list, the results are stored as a list to be editted or retrieved with other functions.\n'function' - Either a lambda function or a pre-defined function to be used for mapping.\n'data' - Some iterable data structure that can be cast to a list."""
        self.results = list(map(function, list(data)))
        return self
    
    def mapResults(self, function):
        """Does the same thing as map(), but re-maps the stored results with function given.\n'function' - Either a lambda function or a pre-defined function to be used for mapping."""
        return self.mapData(function, self.results)

    def selectivelyMapResults(self, filterFunction, mapFunction):
        """Using 'filterFunction', only the elements filtered for true will be remapped with 'mapFunction'."""
        plist = Utilities.createEmbeddedList(range(0, len(self.results)), self.results)
        AdvancedMap(plist).filterResults(lambda x: filterFunction(x[1])).forEach(lambda x: AdvancedMap.__setElementAt(self.results, x[0], mapFunction(x[1])))
        return self

    def __setElementAt(plist, index, newElement):
        # Internal function so we can do an assignment operator in a lambda, normally not allowed.
        plist[index] = newElement

    def addMapToResults(self, function, data):
        """Maps the data provided using the function, and then adds it to the stored results.\n'function' - Either a lambda function or a pre-defined function to be used for mapping.\n'data' - Some iterable data structure that can be cast to a list."""
        self.results += list(map(function, list(data)))
        return self
    
    def filterResults(self, function):
        """Filters stored results using the function provided, and thus alters the final result.\n'function' - The function used to filter the stored results."""
        self.results = self.getFilteredResults(function)
        return self

    def forEach(self, function):
        """Executes the given function and passes each stored result as a parameter."""
        for x in self.results:
            function(x)
        return self

    def getResults(self):
        """Returns the results of all maps and filters."""
        return self.results
    
    def getFilteredResults(self, function):
        """Returns the results of all maps and filters, and filters them. Stored results are not affected.\n'function' - Lambda expression or function to filter the data with."""
        return list(filter(function, self.results))

    def clearResults(self):
        """Clears stored results."""
        self.results.clear()
        return self

class Utilities():
    """Provides an assortment of functions and tools used frequently."""
    def tryParse(value, otherwise = 0):
        """Parses value to an integer, otherwise it returns the 0 or the second parameter."""
        try:
            return int(value)
        except:
            return otherwise
    
    def logTracebackToFile(filename):
        """Logs the most recent traceback to a file named 'filename'."""
        with open(filename, "a") as fileWrite:
            fileWrite.write(Utilities.getSystemTimeString() + "\n" + traceback.format_exc())

    def getSystemTime():
        """Returns the system time in milliseconds."""
        return int(round(time.time() * 1000))

    def getSystemTimeString():
        """Returns a string based on the current system time."""
        return Utilities.getStringFromTimestamp(Utilities.getSystemTime())

    def getStringFromTimestamp(time):
        """Converts a timestamp in milliseconds to a string."""
        return str(datetime.datetime.fromtimestamp(time / 1000))
    
    def stringToIntList(string):
        """Converts a string to an integer list. The elements correspond to the character code in the original string."""
        return AdvancedMapMap().mapData(lambda x: ord(x), string).getResults()

    def intListToString(intList):
        """Converts an integer list into a string."""
        return "".join(AdvancedMap().mapData(lambda x: chr(x), intList).getResults())

    def xorCrypto(key, data):
        """Encrypts 'data' with 'key' using symmetric XOR encryption."""
        if type(data) is str:
            data = Utilities.stringToIntList(data)

        if type(key) is str:
            key = Utilities.stringToIntList(key)
    
        if type(data) is list:
            offset = 0
            for x in range(0, len(data)):
                data[x] ^= key[offset]
                offset = offset + 1 if offset + 1 < len(key) else 0
            
            return data

    def parseCommand(string):
        """Splits and parses a string into a useable command format in tuple form, with the first element being the main command, and the second being a list of arguments. "command test" would return ("command", ["test"])"""
        data = shlex.split(string)
        return ("", []) if len(data) == 0 else (data[0].lower(), data[1:] if len(data) >= 2 else [])

    def getParsedInput(dialog):
        """Returns a tuple with the primary command as the first element and the arguments (list form) as the second element."""
        while True:
            commandInput = input(dialog)
            if len(commandInput.replace(" ", "")) == 0:
                continue
            return Utilities.parseCommand(commandInput)

    def createEmbeddedList(keys, values):
        """Creates an embedded list, using each key as the first element and each value as the second element in each sub-list."""
        return list(map(lambda x, y: [x, y], keys, values))
    
    def createTupleList(keys, values):
        """Creates a tuple list, using each key as the first element and each value as the second element in each tuple."""
        return list(map(lambda x, y: (x, y), keys, values))
    
    def createDictionary(keys, values):
        """Creates a dictionary given keys and values."""
        return dict(map(lambda x, y: (x, y), keys, values))

class CommandProcessor2():
    """Functions similarly to JUtils' CommandProcessor class, but it builds upon it and improves."""
    def __init__(self, commands = {}):
        self.commands = commands
        self.queue = []

    def queueCommands(self, commands):
        """Input a list of commands, either parsed or non-parsed, to be queue and executed later."""
        self.queue += AdvancedMap(commands).selectivelyMapResults(lambda x: type(x) is str, lambda x: Utilities.parseCommand(x)).getResults()

    def executeQueue(self):
        """Execute stored commands."""
        queue = self.queue.copy()
        self.queue.clear()
        self.executeCommands(queue)

    def isQueueClear(self):
        return len(self.queue) == 0

    def executeCommands(self, commands):
        """Input a list of commands, either parsed or non-parsed, to be executed."""
        AdvancedMap(commands).selectivelyMapResults(lambda x: type(x) is str, lambda x: Utilities.parseCommand(x)).forEach(lambda x: self.executeCommand(x[0], x[1]))

    def executeCommand(self, command, args = []):
        """Input a command and its arguments to execute the command."""
        try:
            if type(command) is str:
                command = self.commands[command]
        except:
            print("Unknown command. Try the 'help' command for a detailed list of commands.")
            return

        if len(args) < command.getMinimumArguments():
            print("Usage: () indicates an optional argument, [] indicates a required argument:\n" + command.getUsage())
        else:
            if command.isEnabled():
                command.execute(args)
            else:
                reason = command.getDisabledReason()
                print(f"This command has been disabled! [{reason}]")
        return self

    def registerCommands(self, commands):
        """Input a list of commands to be registered."""
        self.commands.update(Utilities.createDictionary(AdvancedMap(commands).mapResults(lambda x: x.getName().lower()).getResults(), commands))
        return self

    def deregisterCommand(self, command):
        """Input a command to be deregistered."""
        self.commands.pop(command)
        return self

    def getExactCommandByName(self, name):
        """Returns an exact command by name."""
        try:
            return self.commands[name.lower()]
        except:
            return None
    
    def getCommandsByName(self, name):
        """Returns a list of commands that contain 'name' in their name."""
        return AdvancedMap(Utilities.createEmbeddedList(self.commands)).filterResults(lambda x: name.lower() in x[0]).mapResults(lambda x: x[1]).getResults()

    def getRegisteredCommands(self):
        """Returns a list of all registered commands."""
        return list(self.commands.values())

# === Standalone Script === #
class HelpCommand():
    def __init__(self, processor):
        self.processor = processor

    def getName(self):
        return "help"

    def execute(self, args):
        if len(args) == 0:
            print("\n===[Commands Help]===")
            for command in self.processor.getRegisteredCommands():
                name = command.getName().lower()
                desc = command.getShortDescription()
                print(f"{name}: {desc}")
            print()
        else:
            search = args[0]
            results = self.processor.getCommandsByName(search)
            print("\n===[Commands Help]===")
            print(str(len(results)) + f" results were found with the search term \'{search}\'.\n")
            for command in results:
                name = command.getName().lower()
                usage = command.getUsage()
                arguments = str(command.getMinimumArguments())
                desc = "\n".join(command.getLongDescription())
                print(f"{name} Command:\nUsage: {usage}\nMinimum arguments: {arguments}\n{desc}\n")

    def getMinimumArguments(self):
        return 0
    
    def getUsage(self):
        return "help (search)"
    
    def getShortDescription(self):
        return "Lists all commands in detail."
    
    def getLongDescription(self):
        return ["Lists all commands in detail.", "Specific commands can be searched as an optional argument."]

    def isEnabled(self):
        return True

class DefineCommand():
    def getName(self):
        return "define"

    def execute(self, args):
        global storedVariables
        default = "" if len(args) == 1 and (args[0] not in storedVariables.keys()) else storedVariables[args[0]]
        storedVariables.update({args[0]: default if len(args) < 2 else args[1]})

    def getMinimumArguments(self):
        return 1
    
    def getUsage(self):
        return "define [variable] [value]"
    
    def getShortDescription(self):
        return "Defines a string variable to store in memory."
    
    def getLongDescription(self):
        return ["Defines a string variable to store in memory."]

    def isEnabled(self):
        return True

class DefineIntCommand():
    def getName(self):
        return "defint"

    def execute(self, args):
        global storedVariables
        default = 0 if len(args) == 1 and (args[0] not in storedVariables.keys()) else storedVariables[args[0]]
        storedVariables.update({args[0]: default if len(args) < 2 else Utilities.tryParse(args[1], args[1])})

    def getMinimumArguments(self):
        return 1
    
    def getUsage(self):
        return "defint [variable] (value)"
    
    def getShortDescription(self):
        return "Defines an integer variable to store in memory."
    
    def getLongDescription(self):
        return ["Defines a integer variable to store in memory.", "The value is optional, you can simply declare"]

    def isEnabled(self):
        return True

class AddCommand():
    def getName(self):
        return "add"

    def execute(self, args):
        global storedVariables
        try:
            if type(storedVariables[args[0]]) is int:
                storedVariables[args[0]] += Utilities.tryParse(args[1], args[1])
            else:
                storedVariables[args[0]] += args[1]
        except:
            pass

    def getMinimumArguments(self):
        return 2
    
    def getUsage(self):
        return "add [variable] [value]"
    
    def getShortDescription(self):
        return "Adds 'value' to 'variable'."
    
    def getLongDescription(self):
        return ["Adds 'value' to 'variable'."]

    def isEnabled(self):
        return True

class ConditionalCommand():
    def __init__(self, processor):
        self.processor = processor
    
    def getName(self):
        return "conditional"

    def execute(self, args):
        global storedVariables
        if str(storedVariables[args[0]]) == args[1]:
            self.processor.queueCommands(AdvancedMap(args[2:]).mapResults(lambda x: ConditionalCommand.__replaceAll(x, storedVariables)).getResults())

    def __replaceAll(string, data):
        for x in data.keys():
            string = string.replace(f"%{x}%", str(data[x]))
        return string

    def getMinimumArguments(self):
        return 3
    
    def getUsage(self):
        return "conditional [variable] [value] [commands...]"
    
    def getShortDescription(self):
        return "Executes the commands if variable equals value."
    
    def getLongDescription(self):
        return ["Executes the commands if variable equals value."]

    def isEnabled(self):
        return True

class CompareCommand():
    def getName(self):
        return "compare"

    def execute(self, args):
        global storedVariables
        try:
            if args[1] == ">":
                if type(storedVariables[args[0]]) is int:
                    storedVariables.update({"results": "true" if storedVariables[args[0]] > Utilities.tryParse(args[2]) else "false"})
                    return
            if args[1] == ">=":
                if type(storedVariables[args[0]]) is int:
                    storedVariables.update({"results": "true" if storedVariables[args[0]] >= Utilities.tryParse(args[2]) else "false"})
                    return
            if args[1] == "=":
                if type(storedVariables[args[0]]) is int:
                    storedVariables.update({"results": "true" if storedVariables[args[0]] == Utilities.tryParse(args[2]) else "false"})
                    return
            if args[1] == "<":
                if type(storedVariables[args[0]]) is int:
                    storedVariables.update({"results": "true" if storedVariables[args[0]] < Utilities.tryParse(args[2]) else "false"})
                    return
            if args[1] == "<=":
                if type(storedVariables[args[0]]) is int:
                    storedVariables.update({"results": "true" if storedVariables[args[0]] <= Utilities.tryParse(args[2]) else "false"})
                    return 
        except:
            pass
        storedVariables.update({"results": "false"})

    def getMinimumArguments(self):
        return 3
    
    def getUsage(self):
        return "compare [variable] [comparison operator] [value]"
    
    def getShortDescription(self):
        return "Stores the result of variable the command in the results variable."
    
    def getLongDescription(self):
        return ["Stores the result of variable being greater than value in the results variable."]

    def isEnabled(self):
        return True

class PrintCommand():
    def getName(self):
        return "print"

    def execute(self, args):
        global storedVariables
        message = PrintCommand.__replaceAll(args[0], storedVariables)
        print(message)

    def __replaceAll(string, data):
        for x in data.keys():
            string = string.replace(f"%{x}%", str(data[x]))
        return string

    def getMinimumArguments(self):
        return 1
    
    def getUsage(self):
        return "print [message]"
    
    def getShortDescription(self):
        return "Prints a message on screen."
    
    def getLongDescription(self):
        return ["Prints a message on screen.", "Use %VariableName% to insert stored variable values."]

    def isEnabled(self):
        return True

class ExecuteCommand():
    def __init__(self, processor):
        self.processor = processor
    
    def getName(self):
        return "execute"

    def execute(self, args):
        global storedVariables
        self.processor.queueCommands(AdvancedMap(args).mapResults(lambda x: ExecuteCommand.__replaceAll(x, storedVariables)).getResults())

    def __replaceAll(string, data):
        for x in data.keys():
            string = string.replace(f"%{x}%", str(data[x]))
        return string

    def getMinimumArguments(self):
        return 1
    
    def getUsage(self):
        return "print [message]"
    
    def getShortDescription(self):
        return "Prints a message on screen."
    
    def getLongDescription(self):
        return ["Prints a message on screen.", "Use %VariableName% to insert stored variable values."]

    def isEnabled(self):
        return True

class RunScriptCommand():
    def __init__(self, processor):
        self.processor = processor
    
    def getName(self):
        return "run"

    def execute(self, args):
        if True:
            commands = []
            with open(args[0], "r") as fileRead:
                commands = AdvancedMap(fileRead).mapResults(lambda x: x.strip()).filterResults(lambda x: len(x) > 0).getResults()
            global storedVariables
            self.processor.queueCommands(AdvancedMap(commands).mapResults(lambda x: RunScriptCommand.__replaceAll(x, storedVariables)).getResults())
        else:
            print("An error occurred while executing the script.")

    def __replaceAll(string, data):
        for x in data.keys():
            string = string.replace(f"%{x}%", str(data[x]))
        return string

    def getMinimumArguments(self):
        return 1
    
    def getUsage(self):
        return "run [file/script]"
    
    def getShortDescription(self):
        return "Executes the commands in the given script."
    
    def getLongDescription(self):
        return ["Executes the commands in the given script."]

    def isEnabled(self):
        return True

class WaitCommand():
    def getName(self):
        return "wait"

    def execute(self, args):
        start = Utilities.getSystemTime()
        time = 1000 if len(args) == 0 else Utilities.tryParse(args[0], 1000)
        while start + time > Utilities.getSystemTime():
            pass

    def getMinimumArguments(self):
        return 0
    
    def getUsage(self):
        return "wait"
    
    def getShortDescription(self):
        return "Waits the specified milliseconds."
    
    def getLongDescription(self):
        return ["Waits the specified milliseconds."]

    def isEnabled(self):
        return True

class ExitCommand():
    def getName(self):
        return "exit"

    def execute(self, args):
        sys.exit()

    def getMinimumArguments(self):
        return 0
    
    def getUsage(self):
        return "exit"
    
    def getShortDescription(self):
        return "Closes the terminal."
    
    def getLongDescription(self):
        return ["Closes the terminal."]

    def isEnabled(self):
        return True

def runTerminal(header = "", commands = []):
    global storedVariables
    storedVariables = {}
    processor = CommandProcessor2()
    print(header)
    processor.registerCommands([HelpCommand(processor), RunScriptCommand(processor), DefineCommand(), DefineIntCommand(), CompareCommand(), AddCommand(), PrintCommand(), ExecuteCommand(processor), ConditionalCommand(processor), WaitCommand(), ExitCommand()] + commands)
    while True:
        parsedCommand = Utilities.getParsedInput("> ")
        processor.executeCommand(parsedCommand[0], parsedCommand[1])
        while not processor.isQueueClear():
            processor.executeQueue()

if __name__ == "__main__":
    runTerminal("[JUtils2 v" + Compatibility.getVersionString() + "]\nCreated by Ryan Jones @ 2018\n\nUse the 'help' command for a detailed list of commands.\n")
