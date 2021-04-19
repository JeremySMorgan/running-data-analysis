from typing import List
import os
import datetime
import json
import pandas

session_directory = "Sport-sessions"

def meters_to_miles(meters: float) -> float:
    """ Convert meters to miles
    """
    return 0.000621371 * meters

def directory_filenames(dir_: str, extension: str) -> List[str]:
    """ Return all filenames with a certain extension in a directory
    """
    extension = "." + extension
    filenames = []
    for f in os.listdir(session_directory):
        filename = os.path.join(session_directory, f)
        if not os.path.isfile(filename) or extension not in filename:
            continue
        filenames.append(filename)
    return filenames


class Run:

    def __init__(self, date: datetime.datetime, duration: float, distance: float) -> None:
        """ 
        Args:
            date (datetime.datetime): run date
            duration (float): The duration of the run, in minutes
            distance (float): The distance traveled
        """
        assert isinstance(date, datetime.datetime)
        assert isinstance(duration, float)
        assert isinstance(distance, float)
        self.date = date
        self.duration = duration
        self.distance = distance

    def __str__(self) -> str:
        return f"date: {self.date} duration: {round(self.duration, 2)}\tdistance: {self.distance}"

def main():

    runs: List[Run] = []

    for filename in directory_filenames(session_directory, "json"):
        data = json.load(open(filename))

        run_date = datetime.datetime.fromtimestamp(data["start_time"] / 1000)
        run_duration_mins = data["duration"] / (1000 * 60)
        run_distance_mi = meters_to_miles(data["distance"])
        runs.append(Run(run_date, run_duration_mins, run_distance_mi))

    runs.sort(key=lambda r: r.date)

    for run in runs:
        print(run)

if __name__ == "__main__":
    main()