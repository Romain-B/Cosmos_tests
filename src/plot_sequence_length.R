args<-commandArgs(TRUE)

data = read.table(args[1], sep = '\t')

pdf(args[2])
hist(data[,2], main="", xlab = "Sequence length", col = "plum3")

testit <- function(x = sort(runif(20)), ...)
{
    pb <- txtProgressBar(...)
    for(i in c(0, x, 1)) {Sys.sleep(0.5); setTxtProgressBar(pb, i)}
    Sys.sleep(1)
    close(pb)
}
testit(style = 3)


invisible(dev.off())