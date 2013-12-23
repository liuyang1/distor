def transInt(d):
    d["mport"] = int(d["mport"])


def logConf(d):
    import logger
    log = logger.get()
    for k, v in d.iteritems():
        log.info("%s: %s" % (k, v))


def loadLocalConf(filename):
    d = {}
    fp = open(filename)
    for line in fp.readlines():
        line = line.strip()
        if line == "" or line[0] == "#":
            continue
        line = line.split("=")
        k, v = line[0].strip(), line[1].strip()
        d[k] = v
    transInt(d)
    logConf(d)
    fp.close()
    return d

eConf = loadLocalConf("distor.conf")
