import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    # Open a file using Python's CSV reader.
    f = open("zips.csv")
    reader = csv.reader(f)

    headers=next(reader, None)
    print(headers)

    #i = 0
    # Iterate over the rows of the opened CSV file.
    for row in reader:
        #i += 1;
        # Execute database queries, one per row; then print out confirmation.
        db.execute("INSERT INTO location (zipcode, city, state, latitude, longitude, population) VALUES (:zipcode, :city, :state, :latitude, :longitude, :population)",
                    {"zipcode": row[0].zfill(5), "city": row[1], "state": row[2], "latitude": row[3], "longitude": row[4], "population": row[5]})

        #print(f"Added flight from {row[0]} to {row[1]} lasting {row[2]} minutes.")
        #if i==100:
            #break
    # Technically this is when all of the queries we've made happen!
    db.commit()
    n_loc = db.execute("SELECT COUNT(*) FROM location").fetchall()
    print(f"# of Locations: {n_loc}")

if __name__ == "__main__":
    main()
