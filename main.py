from event_pipeline.session import Session
from event_pipeline.track_options import TrackOptions

def run_analysis():
    try:
        year = input('Enter Year: ').strip()
        track_options, builder = TrackOptions(year).get_track_options()
        track_name = builder.pick_track()
        session_name = input('Enter Session Name: ').strip().lower()
        
        if not (track_name and session_name and year.isdigit()):
            print("Invalid input. Please enter valid track, session and year")
            return
        
        Session(track_name, session_name, year).run()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_analysis()

    
