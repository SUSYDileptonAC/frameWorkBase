from ConfigParser import ConfigParser

#cfg = ConfigParser()
#with open("squarks_xsecs.csv", "r") as fi:
    #for line in fi:
        #mass, xsec, relerr = line.split(",")
        #mass = mass.strip()
        #xsec = xsec.strip()
        #relerr = relerr.strip()
        #cfg.add_section(mass)
        #cfg.set(mass, "crosssection", float(xsec))
        #cfg.set(mass, "crosssectionerror", float(xsec)*float(relerr)/100.0)


#with open('squarks_xsecs.ini', 'w') as configfile:
    #cfg.write(configfile)

cfg = ConfigParser()
with open("sbottom_xsecs.csv", "r") as fi:
    for line in fi:
        mass, xsec, relerr = line.split(",")
        mass = mass.strip()
        xsec = xsec.strip()
        relerr = relerr.strip()
        cfg.add_section(mass)
        cfg.set(mass, "crosssection", float(xsec))
        cfg.set(mass, "crosssectionerror", float(xsec)*float(relerr)/100.0)

with open('sbottom_xsecs.ini', 'w') as configfile:
    cfg.write(configfile)
