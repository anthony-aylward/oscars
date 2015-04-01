#==============================================================================#
#          Visualizing results for "Racial bias of the Academy Awards"         #
#==============================================================================#

# Load the data file

breakdown <- read.csv("breakdown.csv", header=TRUE)

#------------------------------------------------------------------------------#
#                        Computing the 95% quantile                            #
#------------------------------------------------------------------------------#

# Initialize a vector to store the 95% quantiles

region95 <- c()

# For each year, compute the 95% quantile for the number of white nominees,
# assuming random selection from the background population

for (i in 1:length(breakdown[[1]])) {
    region95 <- c(
        region95,
        qhyper(
            0.95,
            breakdown[["White.Actors"]][[i]],
            breakdown[["Actors"]][[i]]-breakdown[["White.Actors"]][[i]],
            breakdown[["Nominees"]][[i]]
        )
    )
}

#------------------------------------------------------------------------------#
#                                   Plotting                                   #
#------------------------------------------------------------------------------#

# Initialize the graphics device, in this case a png.

png("plot.png", width = 1200, height = 480)

# Create a plot with enough space to display the data.

plot(breakdown[["Year"]], breakdown[["Nominees"]], type="n", ann=FALSE)
title(
    main="Number of white Oscar nominees in ''actor'' categories, by year", 
    xlab="Year"
)

# Draw the gray region.

polygon(
    c(
        breakdown[["Year"]][[1]],
        breakdown[["Year"]],
        breakdown[["Year"]][[length(breakdown[["Year"]])]]
    ),
    c(
        0,
        breakdown[["Nominees"]],
        0
    ),
    border=NA,
    col="lightgray"
)

# Draw the red region.

polygon(
    c(
        breakdown[["Year"]][[63]],
        breakdown[["Year"]][63:length(breakdown[["Year"]])],
        breakdown[["Year"]][[length(breakdown[["Year"]])]]
    ),
    c(
        0,
        breakdown[["Nominees"]][63:length(breakdown[["Nominees"]])],
        0
    ),
    border=NA,
    col="lightsalmon"
)

# Draw the blue region.

polygon(
    c(
        breakdown[["Year"]][[63]],
        breakdown[["Year"]][63:length(breakdown[["Year"]])],
        breakdown[["Year"]][[length(breakdown[["Year"]])]]
    ),
    c(
        0,
        region95[63:length(region95)],
        0
    ),
    border=NA,
    col="lightblue"
)

# Draw the small gray region.

polygon(
    c(
        breakdown[["Year"]][[65]],
        breakdown[["Year"]][65:66],
        breakdown[["Year"]][[66]]
    ),
    c(
        0,
        breakdown[["Nominees"]][65:66],
        0
    ),
    border=NA,
    col="lightgray"
)

# Plot the points.

points(breakdown[["Year"]], breakdown[["White.Nominees"]], pch=19, col="black")
points(
    breakdown[["Year"]][c(64,67:length(breakdown[["Year"]]))],
    breakdown[["White.Nominees"]][c(64,67:length(breakdown[["Year"]]))],
    pch=19,
    col="blue"
)
points(breakdown[["Year"]][c(68,70,71,87)], breakdown[["White.Nominees"]][c(68,70,71,87)], pch=19, col="red", type="h", lwd="2")
points(breakdown[["Year"]][c(68,70,71,87)], breakdown[["White.Nominees"]][c(68,70,71,87)], pch=19, col="red")

# Turn off the graphics device.

dev.off()

# Create the cropped version of the plot analagously.

png("plot-cropped.png", width = 480, height = 480)
plot(c(breakdown[["Year"]][63:87], 2015), c(breakdown[["White.Nominees"]][63:87], 0), type="n", ann=FALSE)
title(
    main="Number of white Oscar nominees in ''actor'' categories, by year", 
    xlab="Year"
)
polygon(
    c(
        breakdown[["Year"]][[63]],
        breakdown[["Year"]][63:length(breakdown[["Year"]])],
        breakdown[["Year"]][[length(breakdown[["Year"]])]]
    ),
    c(
        0,
        breakdown[["Nominees"]][63:length(breakdown[["Nominees"]])],
        0
    ),
    border=NA,
    col="lightsalmon"
)
polygon(
    c(
        breakdown[["Year"]][[63]],
        breakdown[["Year"]][63:length(breakdown[["Year"]])],
        breakdown[["Year"]][[length(breakdown[["Year"]])]]
    ),
    c(
        0,
        region95[63:length(region95)],
        0
    ),
    border=NA,
    col="lightblue"
)
polygon(
    c(
        breakdown[["Year"]][[65]],
        breakdown[["Year"]][65:66],
        breakdown[["Year"]][[66]]
    ),
    c(
        0,
        breakdown[["Nominees"]][65:66],
        0
    ),
    border=NA,
    col="lightgray"
)
points(
    breakdown[["Year"]][c(64,67:length(breakdown[["Year"]]))],
    breakdown[["White.Nominees"]][c(64,67:length(breakdown[["Year"]]))],
    pch=19,
    col="blue"
)
points(breakdown[["Year"]][c(68,70,71,87)], breakdown[["White.Nominees"]][c(68,70,71,87)], pch=19, col="red", type="h", lwd="2")
points(breakdown[["Year"]][c(68,70,71,87)], breakdown[["White.Nominees"]][c(68,70,71,87)], pch=19, col="red")
dev.off()