def generateCallTime(seconds):
    print "%d seconds" % seconds
    hours = minutes =  0
    secondsInHour = 60*60
    while seconds >= secondsInHour:
        print "adding an hour"
        hours += 1
        seconds -= secondsInHour
    while seconds >= 60:
        print "adding a minute"
        minutes += 1
        seconds -= 60
    print "%d seconds left over" % seconds

    return "{0:02d}h:{1:02d}m:{2:02d}s".format(hours, minutes, seconds)




a = [0, 1, 2, 10, 20, 50, 60, 61, 64, ((60 * 60) + 61)]
for i in a:
    print generateCallTime(i)