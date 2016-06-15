require("BB")
setwd('/Users/Dennis/Desktop/Summer_2016')


# full model, structural equations with identities
model <- function(d2) {
# d2: data frame with all values
# returns: data frame with values updated by equatiosn
  
  # Nominal reference price (Deflator)
  d2$prRPCOnom[t] <- 
    d2$prRPCO[t]*d2$DOMDEF[t]/100
  
  # Corn farm price
  d2$prPPCO[t] <- 
    .816*d2$prRPCOnom[t] + 
    d2$e_prPPCO[t]
  
  # Corn expect market price
  d2$prEPCOmkt[t] <- d2$prPPCO[t]

  # Corn expect yield
  d2$crYECOto[t] <- 
    -2.28290274642977 + 
    0.107815751601678*(d2$YEAR[t]-1900)
  
  # Corn expected revenue
  d2$Y262_EMktRct[t] <- 
    d2$prEPCOmkt[t]*d2$crYECOto[t]

  # Corn expect mkt net return
  d2$prENCOmkt[t] <- 
    d2$Y262_EMktRct[t] - d2$prVCCO[t]
  
  # Corn planted area, price component
  d2$crAPCOpri[t] <- 
    10.611101118283*d2$prENCOmkt[t] +
    -0.902382503422328*d2$prENSRmkt[t] +
    -1.47558373064159*d2$prENWHmkt[t] +
    -0.245657668808256*d2$prENCTmkt[t] +
    -6.83910949962186*d2$prENSB[t]
  
  # Behav. corn area planted
  d2$crAPCOto[t] <-
    .5*d2$crAPCOpri[t] +
    .3*d2$crAPCOpri[t-1] +
    .2*d2$crAPCOpri[t-2] +
    ifelse(d2$YEAR[t]>=2017, 1, 0)*40*(1+.15)^(d2$YEAR[t]-2014) +
    d2$e_crAPCOto[t]
  
  # Corn area harvested
  d2$crAHCOto[t] <- 
    0.758855*d2$crAPCOto[t-1] +
    1.499*(d2$YEAR[t-1]-1900)*d2$crAPCOto[t-1]/1000 +
    d2$e_crAHCOto[t]
  
  # Corn yield
  d2$crYLCOto[t] <- 
    0.108737105543302*(d2$YEAR[t-1]-1900) +
    0.0913912636493641*d2$prPPCO[t-1]/d2$Fert_PPI[t-1] +
    d2$e_crYLCOto[t]
  
  # Corn production
    d2$crPRCOto[t] <- d2$crYLCOto[t] * d2$crAHCOto[t]
  
  # Corn imports
  d2$crIMCOto[t] <- 
    d2$crIMCOto[t-1] +
    2*d2$crIMCOto[t-1]*(d2$prPPCO[t]/d2$prPPCO[t-1]-1) +
    d2$e_crIMCOto[t]
  d2$crIMCOto[d2$crIMCOto<0] <- 0 # don't let imports be negative
  
  # Corn supply
  d2$crSYCOto[t] <- d2$crESCOto[t-1] + d2$crPRCOto[t] + d2$crIMCOto[t]
  
  # Behavioral corn exports
  d2$crEXCOto[t] <- 
    2.96502892559359*d2$lsPRHGjpn[t] +
    2.96502892559359*d2$Hog_PrdEU6[t] +
    2.96502892559359*d2$Hog_PrdUK[t] +
    -441.214299056417*d2$prPPCO[t]/d2$SDR_exch[t] +
    d2$e_crEXCOto[t]
  
  # Corn for fuel, just hard coded in
  
  # Corn FSI (food, seed, indust incl alc)
  d2$crDMCOFD[t] <-
    d2$crDMCOOT[t] +
    -99.0995281730836*d2$POP[t] +
    1.50026988753628*d2$POP[t]*(d2$YEAR[t-1]-1900) +
    6.15613730393188*d2$prPPWH[t]/d2$All_CPI[t]*d2$POP[t] +
    -14.8824052828484*d2$prPPCO[t]/d2$All_CPI[t]*d2$POP[t] +
    1649.07060892978*d2$RealDispInc[t] +
    1.13148382687209*d2$crAPCOto[t]*d2$Crn_SeedRate[t+1]/1000 +
    d2$e_crDMCOFD[t] 
  
  # Corn feed & resid (not sure if this is the correct equation to use)
  d2$crDMCOFE[t] <-
    471.267379169762*d2$GCAU[t] +
    0.248861330680676*d2$prCPSM[t]/d2$LivestockP[t]*d2$GCAU[t] +
    1.26455907960682*d2$prPPSR[t]/d2$LivestockP[t]*d2$GCAU[t] +
    0.427654411065806*d2$prPPBA[t]/d2$LivestockP[t]*d2$GCAU[t] +
    0.831092830565033*d2$prPPOC[t]/d2$LivestockP[t]*d2$GCAU[t] +
    -5.18301435157038*d2$prPPCO[t]/d2$LivestockP[t]*d2$GCAU[t] +
    0.624418*d2$crDMCOFE[t-1]*d2$GCAU[t]/d2$GCAU[t-1] +
    d2$e_crDMCOFE[t]

  # Corn dom disapp
  d2$crDMCOto[t] <-
    d2$crDMCOFD[t] +
    d2$crDMCOFE[t] 
  
  # Corn stocks (also not sure if this is the correct one to use)
  d2$crESCOto[t] <-
    -90*d2$prPPCO[t] +
    0.4*d2$crPRCOto[t] +
    d2$e_crESCOto[t] 

  d2 # function result
  
}

closing.eqs <- function(x, d1) {
# x: array of values to try as solution
# d1: data frame with all variables
# returns: array of closing equation values
  
  d1[t, vars] <- matrix(x, nrow=length(t), ncol=length(vars), byrow=FALSE) # insert variables to solve into dataset
  d1 <- model(d1) # call model
    
  eqs <- list()
  
  # Corn closing equation
  eqs$prRPCO <- d1$crSYCOto[t] - (d1$crEXCOto[t] + d1$crDMCOto[t] + d1$crESCOto[t])
  
  unlist(eqs) # equations to solve
  
}


# get data
base.data <- read.csv('data.csv', header=TRUE) # import data from CSV file


# run model
solve.years <- 2014:2023 # solve years
vars <- c('prRPCO') # variables that are used for model closure
t <- match(solve.years, base.data$YEAR) # index of solve years (global variable that is needed for functions)

solve.vars <- unlist(base.data[t, vars]) # get starting values for solution
ans <- BBsolve(par=solve.vars, d1=base.data, fn=closing.eqs, control=list(tol=1e-3, trace=FALSE, noimp=100)) # solve model


# get output
out.data <- base.data # create output data set
out.data[t, vars] <- matrix(ans$par, nrow=length(t), ncol=length(vars), byrow=FALSE) # get prices
out.data <- model(out.data) # get all other equation results


# output results to csv file
write.csv(out.data, file = 'Out.csv', row.names=FALSE, na='')


#graph all variables
graph.vars <- c('prRPCOnom', 'prPPCO', 'prEPCOmkt', 'crYECOto', 'Y262_EMktRct', 'prENCOmkt', 'crAPCOpri', 'crAPCOto', 'crAHCOto', 'crYLCOto', 
     'crPRCOto', 'crIMCOto', 'crSYCOto', 'crEXCOto', 'crDMCOto', 'crDMCOFD', 'crDMCOFE', 'crESCOto', 'prRPCO')
graph.vars <- c(vars, graph.vars)
graphs <- function(var) {
  par(mar=c(8, 4, 4, 2)+.1, xpd=TRUE) # allow things to be drawn outside plot region
  
  y.max <- max(base.data[t, var], out.data[t, var])*1.01
  y.min <- min(base.data[t, var], out.data[t, var])*.99

  
  plot(solve.years, base.data[t, var], main=var, ylim=c(y.min, y.max), type='l', lwd=2, xlab='Year', ylab='Value')
  lines(solve.years, out.data[t, var], col='blue')
  legend("bottom", inset=c(0, -.33),c("Baseline","Result"),lwd=c(2,1),col=c("black","blue"),lty=c(1,1), horiz=TRUE, bty='n')
}
for (i in 1:length(graph.vars)) graphs(graph.vars[i])

