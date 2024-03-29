#
# This is a Plumber API. You can run the API by clicking
# the 'Run API' button above.
#
# Find out more about building APIs with Plumber here:
#
#    https://www.rplumber.io/
#

library(plumber)
library(dplyr)
library(ggplot2)
library(logger)

#* @apiTitle Palmer Penguins API
#* @apiDescription An API for exploring the Palmer Penguins dataset

# A function to help with arg parsing
parse_args <- function(
    species = c("Adelie", "Chinstrap", "Gentoo", NA),
    sex = c("male", "female", NA)
) {
  # Do argument checking + log
  tryCatch({
    species <- match.arg(species, several.ok = TRUE)
    logger::log_info("species: {paste(species, collapse = ', ')}")
    sex <- match.arg(sex, several.ok = TRUE)
    logger::log_info("sex: {paste(sex, collapse = ', ')}")
  },
  error = function(e) {

    msg <- paste("Bad argument: ", e$message)
    logger::log_error(msg)
    stop(msg)
  }
  )

  # filter data
  palmerpenguins::penguins %>%
    dplyr::filter(
      species %in% !!species,
      sex %in% !!sex
    )
}

#* Get the mean of some fields by species
#* @param species penguin species, one of Adelie, Chinstrap, Gentoo, defaults to all
#* @param sex sex, one of male, female, NA, defaults to all
#* @get /stats
function(species = c("Adelie", "Chinstrap", "Gentoo", NA), sex = c("male", "female", NA)) {
  log_info("Getting stats")

  dat <- parse_args(species, sex)

  list(
    species = species,
    sex = sex,
    stats = dat %>%
      dplyr::summarize(
        across(
          bill_length_mm:body_mass_g,
          mean,
          na.rm = TRUE
        )
      )
  )
}

#* Plot flipper length against body mass
#* @serializer png
#* @param species penguin species, one of Adelie, Chinstrap, Gentoo, defaults to all
#* @param sex sex, one of male, female, NA, defaults to all
#* @get /plot
function(
    species = c("Adelie", "Chinstrap", "Gentoo", NA),
    sex = c("male", "female", NA)
) {
  log_info("Getting plot")
  dat <- parse_args(species, sex)

  tryCatch(
    plot <- dat %>%
      ggplot(
        aes(
          x = flipper_length_mm,
          y = body_mass_g,
          color = species
        )
      ) +
      geom_point() +
      theme_minimal() +
      xlab("Flipper Length (mm)") +
      ylab("Body Mass (g)") +
      ggtitle("Penguin Flipper Length vs Body Mass") +
      labs(color = "Species"),
    warning = function(w) log_warn(w$message)
  )

  print(plot)
}

# Programmatically alter your API
#* @plumber
function(pr) {
  pr %>%
    # Overwrite the default serializer to return unboxed JSON
    pr_set_serializer(serializer_unboxed_json())
}
