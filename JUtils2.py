# ==={ JUtils 2 by Ryan Jones }=== #
# Release Date: 11/8/2018
# Version: 0.1.0

import datetime
import time
import traceback
import shlex

class Compatibility():
    """Provides simple methods to aid with compatibility."""
    def getVersion():
        """Returns a tuple providing the major, minor, patch, and pre-release identifier like so: (Major, Minor, Patch, Identifier)"""
        return (0, 1, 0, "")

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
        return (data[0].lower(), data[1:] if len(data) >= 2 else [])

    def createEmbeddedList(keys, values):
        """Creates an embedded list, using each key as the first element and each value as the second element in each sub-list."""
        return list(map(lambda x, y: [x, y], keys, values))
    
    def createTupleList(keys, values):
        """Creates a tuple list, using each key as the first element and each value as the second element in each tuple."""
        return list(map(lambda x, y: (x, y), keys, values))
    
    def createDictionary(keys, values):
        """Creates a dictionary given keys and values."""
        return dict(map(lambda x, y: (x, y), keys, values))

def Main():
    value = 250
    for r in range(3, value):
        advancedMap = AdvancedMap(range(0, value)).selectivelyMapResults(lambda x: x % r == 0, lambda x: -x)
        print(sum(range(0, value)) / sum(advancedMap.getResults()))

if __name__ == "__main__":
    Main()
