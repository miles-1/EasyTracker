# File paths, given the image sequence file. Hardcoded keys in lots of places
CONFIG = {
    "params": "/params.json",
    "diff1": "/differences1",
    "diff2": "/differences2",
    "contour": "/contour.json",
    "track": "/track.json",
    "csv": "/data.csv",
}

# Possible image extensions
extension = ["jpg", "jpeg", "tif", "png"]

# Button features
args = {
    "font": ('Consolas', 12),
    "width": 40,
    "pady": 10
}
args1 = args.copy()
args1.update(dict(bg="grey", fg="black"))
args2 = args.copy()
args2.update(dict(bg="white", fg="grey"))

# Scale dictionary for scale.json. Hardcoded keys in lots of places
params_dict = {
    "scale": 1,
    "units": "pixel",
    "duration": 1,
    "canny_lower": 100,
    "canny_upper": 200,
    "kernel": 3,
    "dilate_it1": 4,
    "erode_it1": 3,
    "dilate_it2": 5,
    "erode_it2": 5,
    "area_lower": -1,
    "area_upper": -1
}

# TODO: write program help
program_help = "This program ..." \
               "No background movement in video"

# General error message
em = "Please complete past steps (or click the 'Start where you left off' button) " \
     "before attempting to complete this step."

# Error message 1
em1 = "You have not yet completed step 1). " + em

# Error message 2
em2 = "You have not yet completed step 1) or 2). " + em
