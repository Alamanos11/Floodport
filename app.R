library(shiny)
library(ggplot2)

# Global constants
n_tide <- 0.4
b <- 0.001  # Set constant value for b
ground_base <- -10  # Starting ground elevation
xmin_struct <- 10
xmax_struct <- 20
x_max <- 20  # Reduced to x = 20

ui <- navbarPage(
  title = "Port Flooding Profile Model",
  
  # New Tab for Introduction Text
  tabPanel("Introduction",
           fluidRow(
             column(width = 12,
                    h3("Welcome to the Floodport App!"),
                    p("This interactive app is designed for educational purposes."),
                    p("You will take on the role of a coastal risk analyst, exploring how different natural hazards can challenge the safety of a port."),
                    br(),
                    p("You will control key variables like:"),
                    tags$ul(
                      tags$li("High tides - natural tidal cycles that elevate water levels"),
                      tags$li("Storm surge - sudden sea-level rises during extreme storms,"),
                      tags$li("Rainfall contribution - added flooding from heavy rainfall, directly running off into the port,"),
                      tags$li("Sea-level rise - gradual changes due to climate change, over the years,"),
                      tags$li("Engineering structures, like the port dock’s height.")
                    ),
                    br(),
                    p("These forces can act alone or together, leading to coastal floods that threaten ports and infrastructure, which we try to design with the most practical and safe way."),
                    br(),
                    h4("Your task: Experiment with different combinations of these factors to see when, why, and how much our port floods."),
                    p("Understand how hazard interactions amplify risk, and gain insights into real-world engineering challenges and adaptation strategies!"),
                    br(),
                    p("Let’s dive in the next tab to find out!")
             )
           )
  ),
  
  # Tab for Select Parameters (Side Panel)
  tabPanel("Select parameters",
           sidebarLayout(
             sidebarPanel(
               selectInput("scenario", "Select Scenario",
                           choices = c("mild", "moderate", "extreme", "custom"),
                           selected = "mild"),
               numericInput("H_construction", "Structure Height H (m) - how tall do you want the port dock? Engineers design this for flood-protection!", value = 12, min = 0, step = 0.1),
               numericInput("t", "Time (t) - select your planning horizon in years.", value = 0, min = 0, step = 1),
               numericInput("b", "b is the conversion factor (m of sea-level rise per mm of rainfall). In impervious surfaces (like concrete) the rainfall becomes water-rise almost immediately (b=0.001), but if engineers design some retention areas (like buffer zones) b can go closer to zero!", value = 0.001, min = 0, step = 0.001),
               
               
               # Custom Scenario Inputs below the predefined ones
               conditionalPanel(
                 condition = "input.scenario == 'custom'",
                 numericInput("n_tide", "Tide height in meters above initial sea-level (n tide). How high tides might occur?", value = 0.5, min = 0, step = 0.1),
                 numericInput("n_surge", "Storm-surge height in meters above initial sea-level (n surge). How much sea-water can be pushed on shore during a strong wind storm?", value = 0.7, min = 0, step = 0.1),
                 numericInput("P", "Precipitation (P) in mm of water. How much do you think it will rain?", value = 80, min = 0, step = 1),
                 numericInput("c", "Annual sea-level rise rate (m/year). How fast do you think climate change might cause rising water elevations?", value = 0.01, min = 0, step = 0.001)
               )
             ),
             mainPanel(
               p("A simple representation of the port flood problem assumes that the effective water level n(t) is the sum of the potential water elevation caused by:"),
               tags$ul(
                 tags$li("a tide: n tide (in meters)"),
                 tags$li("a storm surge: n surge (in meters)"),
                 tags$li("a precipitation event: P (in mm), running off into the port, which is converted into meters of water elevation rise through a conversion factor b (m of water/mm of rainfall)"),
                 tags$li("sea-level rise happening gradually with a pace c over the years (t)")
               ),
               br(),
               h5("At a certain time, this is expressed as:"),
               withMathJax("$$n(t) = n_{tide}(t) + n_{surge}(t) + b \\cdot P(t) + c \\cdot t$$"),
               p("Flooding occurs when this effective water level exceeds the port’s dock elevation."),
               h5("Select from the following three predefined scenarios, which describe different climatic conditions and their effects on the port:"),
               withMathJax(
                 "$$\\text{Mild (e.g. RCP 2.6):}\\quad n_{tide} = 0.5m, \\quad n_{surge} = 0.7m,\\quad P = 80mm,\\quad c = 0.01m/year\\\\ \\\\ \\
                 \\text{Moderate (e.g. RCP 4.5-6.0):}\\quad n_{tide} = 0.5m, \\quad n_{surge} = 1.0m,\\quad P = 110mm,\\quad c = 0.015m/year\\\\ \\\\ \\
                 \\text{Extreme (e.g. RCP 8.5):}\\quad n_{tide} = 0.5m, \\quad n_{surge} = 1.6m,\\quad P = 150mm,\\quad c = 0.018m/year$$"
               ),
               h5("or choose the fully customizable scenario “custom”."),
               
               br(),
               plotOutput("floodPlot"),
               verbatimTextOutput("floodDifference"),
               plotOutput("timeDiffPlot")  # Including the figure for Flooded Difference Over Time here
             )
           )
  ),
  
  # Tab for Sensitivity Analysis
  tabPanel("Flood drivers",
           fluidRow(
             column(width = 12,
                    p("Sensitivity analysis is a technique used to understand how changes in input variables affect the output of a model or system. It helps identify which variables have the most impact, allowing us to see how small adjustments can lead to significant changes in results. This is especially useful in decision-making."),
                    p("We tested the sensitivity of the main model’s parameters based on the three pre-defined scenarios (as % changes from the moderate scenario), and here is what we found:"),
                    
                    img(src = "sen.png", height = "500px", width = "900px"),
                    
                    p("How would you interpret this result? What can engineers do to protect a port from flooding? (Think about how to analyze all parameters used, and which ones can be affected!)")
             )
           )
  )
)

server <- function(input, output, session) {
  scenario_defaults <- reactive({
    if (input$scenario == "custom") {
      return(list(n_surge = input$n_surge, P = input$P, c = input$c, n_tide = input$n_tide, b=input$b))
    } else {
      switch(input$scenario,
             mild = list(n_surge = 0.7, P = 80, c = 0.01, n_tide = 0.5, b=0.001),
             moderate = list(n_surge = 1, P = 110, c = 0.015, n_tide = 0.5, b=0.001),
             extreme = list(n_surge = 1.6, P = 150, c = 0.018, n_tide = 0.5, b=0.001))
    }
  })
  
  output$floodPlot <- renderPlot({
    n_surge <- scenario_defaults()$n_surge
    P <- scenario_defaults()$P
    c <- scenario_defaults()$c
    n_tide <- scenario_defaults()$n_tide
    a <- 0  # Always 0 as per your request
    t <- input$t
    H_construction <- input$H_construction + ground_base
    b<- input$b
    
    n_total <- n_tide + n_surge + b * P + c * t
    
    x_vals <- seq(0, x_max, by = 0.5)
    ground_vals <- ground_base + a * x_vals
    df_ground <- data.frame(x = x_vals, ground = ground_vals)
    
    # Structure polygon
    x_struct_vals <- seq(xmin_struct, xmax_struct, by = 0.1)
    ground_struct <- ground_base + a * x_struct_vals
    df_structure <- data.frame(
      x = c(x_struct_vals, rev(x_struct_vals)),
      y = c(rep(H_construction, length(x_struct_vals)), rev(ground_struct))
    )
    
    intersect_sea_ground <- -ground_base / a
    intersect_sea_struct <- xmin_struct
    end_sea_x <- min(intersect_sea_ground, intersect_sea_struct)
    x_sea_vals <- seq(0, end_sea_x, by = 0.5)
    df_sea_fill <- data.frame(
      x = c(x_sea_vals, rev(x_sea_vals)),
      y = c(rep(0, length(x_sea_vals)), rev(ground_base + a * x_sea_vals))
    )
    
    if (n_total > H_construction) {
      end_nsea_x <- min((n_total - ground_base) / a, x_max)
    } else {
      end_nsea_x <- min(xmin_struct, x_max)
    }
    x_nsea_vals <- seq(0, end_nsea_x, by = 0.5)
    df_nsea_fill <- data.frame(
      x = c(x_nsea_vals, rev(x_nsea_vals)),
      y = c(rep(n_total, length(x_nsea_vals)), rev(ground_base + a * x_nsea_vals))
    )
    
    df_sea_line <- data.frame(x = c(0, end_sea_x), y = c(0, 0))
    df_nsea_line <- data.frame(x = c(0, end_nsea_x), y = c(n_total, n_total))
    
    ggplot() +
      geom_polygon(data = df_sea_fill, aes(x = x, y = y), fill = "black", alpha = 0.3) +
      geom_line(data = df_sea_line, aes(x = x, y = y), color = "black", size = 1) +
      geom_polygon(data = df_nsea_fill, aes(x = x, y = y), fill = "blue", alpha = 0.3) +
      geom_line(data = df_nsea_line, aes(x = x, y = y), color = "blue", size = 1) +
      geom_line(data = df_ground, aes(x = x, y = ground), color = "brown", size = 1.5) +
      geom_polygon(data = df_structure, aes(x = x, y = y), fill = "gray50", alpha = 0.7) +
      annotate("text", x = 1, y = 0.3, label = "Initial Sea Level", color = "black", hjust = 0, size = 5, fontface = "bold") +
      annotate("text", x = 1, y = n_total + 0.3, label = "New Sea Level", color = "blue", hjust = 0, size = 5, fontface = "bold") +
      
      labs(title = "Flooding Profile",
           x = "Distance (x) [m]",
           y = "Elevation (z) [m]") +
      xlim(0, x_max) +
      ylim(min(df_ground$ground) - 0.5, max(H_construction, n_total) + 1.5) +
      coord_fixed(ratio = 1) +
      theme_minimal(base_size = 16) +
      theme(
        plot.title = element_text(face = "bold", size = 18, color = "black"),
        axis.title = element_text(face = "bold", size = 16, color = "black"),
        axis.text = element_text(size = 14, color = "black")
      )
  })
  
  output$floodDifference <- renderPrint({
    n_surge <- scenario_defaults()$n_surge
    P <- scenario_defaults()$P
    c <- scenario_defaults()$c
    n_tide <- scenario_defaults()$n_tide
    a <- 0
    t <- input$t
    H_construction <- input$H_construction + ground_base
    b<-input$b
    
    n_total <- n_tide + n_surge + b * P + c * t
    
    # Calculate the difference between New Sea Level and structure height
    difference <- n_total - H_construction
    
    if (difference > 0) {
      cat("Difference:", difference, "m\n")
      cat("The area is flooded.\n")
    } else {
      cat("Difference: 0m\n")
      cat("The area is not flooded.\n")
    }
  })
  
  # For the new tab, plot the difference between sea level and structure over time
  output$timeDiffPlot <- renderPlot({
    time_vals <- 0:100
    diff_vals <- numeric(length(time_vals))
    
    for (i in seq_along(time_vals)) {
      t <- time_vals[i]
      n_surge <- scenario_defaults()$n_surge
      P <- scenario_defaults()$P
      c <- scenario_defaults()$c
      n_tide <- scenario_defaults()$n_tide
      H_construction <- input$H_construction + ground_base
      b<-input$b
      
      n_total <- n_tide + n_surge + b * P + c * t
      diff_vals[i] <- max(n_total - H_construction, 0)  # Set negative differences to 0
    }
    
    df_diff <- data.frame(Time = time_vals, Difference = diff_vals)
    
    ggplot(df_diff, aes(x = Time, y = Difference)) +
      geom_line(color = "blue", size = 1.2) +
      geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
      labs(title = "Flooded Difference Over Time",
           x = "Time (t) [years]",
           y = "Difference [m]") +
      theme_minimal(base_size = 16) +
      theme(
        plot.title = element_text(face = "bold", size = 18, color = "black"),
        axis.title = element_text(face = "bold", size = 16, color = "black"),
        axis.text = element_text(size = 14, color = "black")
      )
  })
}

shinyApp(ui = ui, server = server)
