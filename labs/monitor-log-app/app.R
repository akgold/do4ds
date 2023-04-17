library(shiny)
library(log4r)

# Create log object
log <- logger("DEBUG")
# Log startup
info(log, paste("App starting"))
n <- reactiveVal(2)

ui <- fluidPage(
  titlePanel(
    "Get some fractions"
  ),
  mainPanel(
    actionButton(
      "button", "Press Me"
    ),
    textOutput("frac")
  )
)

server <- function(input, output) {
  observeEvent(
    input$button, {
      info(log, "Button Pressed")
      # Increment value of count reactive
      n(compute_frac(n()))
    })

  output$frac <- renderText(n())
}

compute_frac <- function(n) {
  # Do some math
  n <- n %% 5 # Do a modulous for no reason
  debug(log, paste("n:", n))
  n <- n + n/n # Add n/n (it's always 1, right?)

  # Error if it's not a number
  if (is.nan(n)) error(log, "n is not a number")

  n
}

# Run the application
shinyApp(ui = ui, server = server)
