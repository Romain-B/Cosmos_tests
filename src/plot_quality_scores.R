args<-commandArgs(TRUE)

testit <- function(x = sort(runif(20)), ...)
{
    pb <- txtProgressBar(...)
    for(i in c(0, x, 1)) {Sys.sleep(0.5); setTxtProgressBar(pb, i)}
    Sys.sleep(1)
    close(pb)
}
testit(style = 3)


quality_table = read.table(args[1])
colnames(quality_table) = seq(1,dim(quality_table)[2])
means = apply(quality_table, 2, mean)

pdf(args[2])
boxplot(quality_table, xlab = 'Read position (bp)', ylab = 'Quality score', 
    main = '', ylim = c(0,40), pars=list(staplelty=0, whisklty=0), 
    outline = FALSE)
rect(-10,0, dim(quality_table)[2]+10,20, 
    col = rgb(255,0,0,100, maxColorValue = 255), border = NA )
rect(-10,20, dim(quality_table)[2]+10,28, 
    col = rgb(255,150,0,100, maxColorValue = 255), border = NA )
rect(-10,28, dim(quality_table)[2]+10,40, 
    col = rgb(0,255,0,100, maxColorValue = 255), border = NA )
boxplot(quality_table, col = 'white', add = TRUE, 
    pars=list(staplelty=0, whisklty=0), outline = FALSE)

invisible(dev.off());
