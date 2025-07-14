from event_pipeline.session import Session

def run_analysis():
    try:
        track_name = input('Enter Track Name: ').strip().lower()
        session_name = input('Enter Session Name: ').strip().lower()
        year = input('Enter Year: ').strip()

        if not (track_name and session_name and year.isdigit()):
            print("Invalid input. Please enter valid track, session and year")
            return
        
        Session(track_name, session_name, year).run()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_analysis()

    
