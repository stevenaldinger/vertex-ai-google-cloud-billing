from datetime import date

def get_todays_date():
    """
    Returns today's date.

    Returns:
        str: today's date in the format dd/mm/YYYY
    """

    return date.today().strftime("%d/%m/%Y")
