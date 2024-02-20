# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_list = []
    for d in old_dates:
        new_list.apppend(datetime.strptime(d,"%Y-%m-%d").strftime("%d %b %Y"))
    return new_list


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start,str) or not instance(n,int):
        raise TypeError
    output = []
    for i in range(n):
        output.append(datetime.strptime(start,"%Y-%m-%d") + timedelta(days=i))
    return output
    


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    output = []
    for i,j in enumerate(values):
        telp_list = []
        telp_list.append(datetime.strptime(start_date,"%Y-%m-%d") + timedelta(days=i))
        telp_list.append(j)
        output.append(tuple(telp_list))
    return output
                                           


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile,newline='') as file:
        reader = DictReader(file)
        late_fees = defaultdict(float)
        for row in reader:
            date_due = datetime.strptime(row['date_due'],"%m/%d/%Y")
            date_returned = datetime.strptime(row['date_returned'],"%m/%d/%Y")
            days_late = (date_returned - date_due).days
            if days_late > 0:
                late_fee = days_late * 0.25
            else:
                late_fee = 0
            late_fees[row['patron_id']] += late_fee
    with open(outfile,'w',newline='') as file:
        writer = DictWriter(file,fieldnames=['patron_id','late_fees'])
        writer.writeheader()
        for patron_id,fee in late_fees.items():
            writer.writerow({'patron_id':patron_id,"late_fees":f"{fee:.2f}"})
                            
    


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
