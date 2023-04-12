library(ggplot2)
library(GGally)
library(stringi)
library(data.table)

# remove goalies
salaries <- rbindlist(lapply(list.files("./data/salaries", full.names = TRUE), fread))[
    POS != "G"
]

# remove whitespace and any punctuation characters
salaries$PLAYER <- trimws(gsub("^[0-9]+\\.", "", salaries$PLAYER))

# two different approaches. Match rate is better with the first,
# so we leave it this way.
clean_name <- function(name) {
    trimws(tolower(gsub("[^A-z]", "", stringi::stri_trans_general(name, "Latin-ASCII"))))
    # trimws(tolower(gsub('[^A-z]', '', iconv(name, "latin1", "ASCII", sub=""))))
}

# clean up the salary dataframe
salaries[, `:=`(
    "SALARY" = as.numeric(gsub("[^0-9]", "", SALARY)),
    "AAV" = as.numeric(gsub("[^0-9]", "", AAV)),
    "BASE SALARY" = as.numeric(gsub("[^0-9]", "", `BASE SALARY`)),
    "S.BONUS" = as.numeric(gsub("[^0-9]", "", `S.BONUS`)),
    "P.BONUS" = as.numeric(gsub("[^0-9]", "", `P.BONUS`)),
    "CAP HIT" = as.numeric(gsub("[^0-9]", "", `CAP HIT`)),
    "CAP HIT %" = as.numeric(gsub("[^0-9]", "", `CAP HIT %`)),
    "SEASON" = as.integer(sapply(strsplit(SEASON, "-"), "[", 1)),
    "SIGNING DATE" = dplyr:::coalesce(
        as.Date(`SIGNING DATE`, format = "%b %d, %Y"),
        as.Date(`SIGNING DATE`, "%b. %d, %Y")
    ),
    "merge_name" = clean_name(PLAYER)
)]
salaries <- salaries[SALARY > 0]
salaries[, CNTRCT_AGE := SEASON - year(`SIGNING DATE`)]

player_stats <- fread("./data/all_player_data.csv")[situation == "all" & position != "G"]
team_metadata <- fread("./data/team_metadata.csv")

core_stats <- player_stats[
    ,
    .(
        playerId, season, name, position, team, games_played, icetime, shifts,
        onIce_xGoalsPercentage, offIce_xGoalsPercentage, penalties, faceoffsWon,
        penalityMinutes, penalityMinutesDrawn, shotsBlockedByPlayer, I_F_goals,
        I_F_primaryAssists, I_F_secondaryAssists, I_F_points, I_F_hits,
        "merge_name" = clean_name(name)
    )
]

# clean some team names
core_stats$team <- sapply(core_stats$team, function(x) {
    team <- switch(x,
        S.J = "SJS",
        T.B = "TBL",
        N.J = "NJD",
        L.A = "LAK"
    )
    ifelse(is.null(team), x, team)
})

# merge the core stats we care about with salary information
all_player_data <- merge(
    core_stats,
    salaries,
    by.x = c("merge_name", "season"),
    by.y = c("merge_name", "SEASON"),
    all = TRUE
)

# now merge in the team metadata
full_df <- merge(
    all_player_data,
    team_metadata,
    by.x = "team",
    by.y = "Abbr",
    all = FALSE
)

# output
write.csv(full_df, "./data/full_data.csv")
