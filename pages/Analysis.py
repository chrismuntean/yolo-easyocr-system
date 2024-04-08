import os
import pandas as pd

import json
import streamlit as st

def display_dataframe():

    # check if the all_plates.json file exists
    if os.path.exists("logs/perm/all_plates.json"):

        # get the all_plates.json file
        with open("logs/perm/all_plates.json", "r") as file:
            all_plates = json.load(file)

        # Create a list and append the data to it
        data = []

        for plate, detections in all_plates.items():
            data.append({
                "analyze": "/Analysis?plate=" + plate,
                "plate": plate,
                "detection_count": str(len(detections)), # Convert to str to align left
                "first_seen": detections[0]["date"] + " " + detections[0]["time"],
                "last_seen": detections[-1]["date"] + " " + detections[-1]["time"],
                "risk": "High" if len(detections) > 5 else "Low"
            })

        # Create a pandas DataFrame from the list
        df = pd.DataFrame(data)

        # Display the DataFrame using streamlit
        all_plates_dataframe.dataframe(
            df,
            column_config={
                "analyze": st.column_config.LinkColumn("Analyze", display_text = "View media"),
                "plate": "Plate",
                "detection_count": "Sightings",
                "first_seen": "First Seen",
                "last_seen": "Last Seen",
                "risk": "Risk"
            },

            hide_index=True,
            use_container_width=True
        )

    else:
        # if the all_plates.json file does not exist, display an error
        st.error("No plates detected yet")

# Check if a variable was passed in the URL query string
plate = st.query_params.get("plate")

if plate != None:
    st.header(plate, divider = 'gray')

    # Get the list of times the plate was detected from /logs/perm/all_plates.json
    
    # check if the all_plates.json file exists
    if os.path.exists("logs/perm/all_plates.json"):

        # get the all_plates.json file
        with open("logs/perm/all_plates.json", "r") as file:
            all_plates = json.load(file)

        # check if the plate is in the all_plates.json file
        if plate in all_plates:

            # reverse the list so that the latest detection is shown first
            all_plates[plate].reverse()

            for plate in all_plates[plate]:
                
                # for each time the plate was detected create an expander with the date and time
                with st.expander(plate["date"] + " at " + plate["time"]):
                    
                    # create 2 columns for the video and images
                    vid_col, image_col = st.columns([3, 1])

                    # load video bytes
                    vid_file = open('logs' + plate["video_path"], 'rb')
                    vid_bytes = vid_file.read()

                    # display the video
                    vid_col.video(vid_bytes)

                    # display the images vertically
                    image_col.image('logs' + plate["veh_crop_path"], use_column_width=True)
                    image_col.image('logs' + plate["plate_crop_path"], use_column_width=True)

        else:
            st.error("Plate number not found in logs.")


else:
    # No plate specified so display the default dataframe to allow the user to choose one
    st.header("Analysis", divider = 'gray')

    # create an empty dataframe object
    all_plates_dataframe = st.empty()

    display_dataframe()