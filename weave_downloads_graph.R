#!/usr/bin/rscript

library(ggplot2)
library(getopt)

spec = matrix(c(
    'githubdownloads', 'd', 1, 'character',
    'releases', 'r', 2, 'character',
    'help', 'h', 0, 'logical'
), byrow=TRUE, ncol = 4)

opt = getopt(spec)

if ( !is.null(opt$help) | is.null(opt$githubdownloads) ) {
    cat(getopt(spec, usage=TRUE))
    q(status=1)
}

if ( is.null(opt$releases) ) { opt$releases = "weave-release-ranges.csv" }

df <- read.csv(opt$githubdownloads)

# releaseRangesis release number, start date, end date

releaseRanges <- read.csv(opt$releases, colClasses = 'character')
releaseRanges$Start_Date <- as.Date(releaseRanges$Start_Date, format='%m/%d/%Y')
releaseRanges$End_Date <- as.Date(releaseRanges$End_Date, format='%m/%d/%Y')
releaseRanges[nrow(releaseRanges),3] <- Sys.Date()

setRelease <- function(date) {
    tidyDate <- as.Date(date, format="%m/%d/%Y")
    ourRelease <- releaseRanges[releaseRanges$Start_Date <= tidyDate 
                  & releaseRanges$End_Date >= tidyDate, ]
    return(ourRelease$Release)
}

releaseDownloadsMax <- function (release) {
    downloads <- max(tidyDf$Download.Total[tidyDf$Release == release])
    return(downloads)
}

# tidy up our data set, if we have no downloads remove
# the data, and then add Release data

tidyDf <- df[,1:4]
tidyDf <- tidyDf[!is.na(tidyDf$Download.Total), ]
tidyDf[, "Release"] <- sapply(tidyDf$Date, setRelease)
tidyDf[, "TotalSum"] <- cumsum(tidyDf$Difference)

graphData <- data.frame(Release = character(),
                        Downloads = numeric())

for (i in 1:length(unique(releaseRanges$Release)) ) {
    thisRelease <- releaseRanges$Release[i]
    thisMax <- releaseDownloadsMax(thisRelease) 
    newRow <- data.frame(Release = thisRelease, Downloads = thisMax)
    graphData <- rbind(graphData, newRow)
} 

g <- ggplot(graphData, aes(1, y=Downloads, fill=Downloads))
g <- g + geom_bar(stat="identity", colour="white", width=0.4)
g <- g + ggtitle("Cumulative Downloads from Github") + labs(x="Weave", y="Downloads")


ggsave(filename = "cumulative-downloads-barchart.png")








