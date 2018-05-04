from app import app
from app.services import quandle_codes_helper

__author__ = 'mukundmk'


if __name__ == '__main__':
    created = quandle_codes_helper()
    if not created:
        print('Error fetching ticker symbols. Retry again later.')
        exit()

    app.run(port=7777)
