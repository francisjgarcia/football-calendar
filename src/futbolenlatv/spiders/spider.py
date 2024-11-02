import os
from dotenv import load_dotenv
from datetime import datetime
import scrapy
from scrapy.http import FormRequest
from futbolenlatv.items import FutbolItem
from google_calendar import create_calendar_event

# Load the .env file from the root directory of the project
load_dotenv()

# Get the list of teams and competitions from environment variables
ALLOWED_TEAMS = os.getenv("ALLOWED_TEAMS").split(",")
ALLOWED_COMPETITIONS = os.getenv("ALLOWED_COMPETITIONS").split(",")
SPECIAL_COMPETITIONS = os.getenv("SPECIAL_COMPETITIONS").split(",")
SPECIAL_CHANNELS = os.getenv("SPECIAL_CHANNELS").split(",")


class FutbolSpider(scrapy.Spider):
    name = "FutbolEnLaTV"
    start_urls = ["https://www.futbolenlatv.es"]

    def parse(self, response):
        form = response.css('form[action="/"]')

        if form:
            yield FormRequest.from_response(
                response,
                formdata={'opSearch': '1'},
                formxpath='//form[@action="/"]',
                callback=self.after_form
            )
        else:
            self.logger.error('No form found with action="/"')

    def after_form(self, response):
        for days in response.css('table.tablaPrincipal > tbody'):
            item = FutbolItem()
            # Extract and clean the match date
            raw_date = days.css('tr.cabeceraTabla > td::text').get()

            # Remove text before the date and keep only the relevant part
            item['date'] = self.extract_date(raw_date)

            for day in days.css('tr'):
                hour = day.css('td.hora::text').get()
                if hour is None or hour.strip() in ["PD", "APLAZADO"]:
                    self.logger.warning(
                        "Hour not found for this match, skipping."
                    )
                    continue
                item['hour'] = hour.strip()
                item['datetime'] = self.convert_to_iso8601(
                    item['date'], item['hour']
                )
                item['local'] = day.css('td.local > span::text').get()
                item['visitor'] = day.css('td.visitante > span::text').get()
                item['competition'] = day.css(
                    'td.detalles > ul > li > div.contenedorImgCompeticion > '
                    'span.ajusteDoslineas > label::text'
                ).get()
                item['channels'] = day.css(
                    'td.canales > ul.listaCanales > li::text'
                ).getall()

                # Check if the match is from a team or competition of interest
                if ((item['local'] in ALLOWED_TEAMS or
                     item['visitor'] in ALLOWED_TEAMS) and
                    (item['competition'] in ALLOWED_COMPETITIONS)) or \
                    (item['competition'] in SPECIAL_COMPETITIONS and
                     any(channel in SPECIAL_CHANNELS
                         for channel in item['channels'])):
                    # Add the event to the calendar in each iteration
                    create_calendar_event(item)
                    yield item
                else:
                    self.logger.info(
                        f"Match of {item['local']} vs {item['visitor']} "
                        f"not in filtered teams or competitions."
                    )

    def extract_date(self, raw_date):
        """
        Extract only the date from the given text in the format
        'Matches today Thursday, 01/01/1970'.
        """
        if ',' in raw_date:
            # Take the part after the last comma
            return raw_date.split(',')[-1].strip()  # Return the clean date
        return raw_date.strip()  # Return the clean string if no commas

    def convert_to_iso8601(self, date_str, hour_str):
        """
        Convert the extracted date and time to ISO 8601 format
        (YYYY-MM-DDTHH:MM:SS). We assume that:
        - The date is extracted in DD/MM/YYYY format
        - The time is extracted in HH:MM format
        """
        try:
            # Convert the date and time into a datetime object
            date_format = "%d/%m/%Y"
            datetime_obj = datetime.strptime(date_str, date_format)

            # Extract the time if present
            if hour_str:
                hour_format = "%H:%M"
                time_obj = datetime.strptime(hour_str, hour_format).time()

                # Combine the date and time into a single datetime object
                combined_datetime = datetime.combine(datetime_obj, time_obj)
                # Return date and time in ISO 8601 format
                return combined_datetime.isoformat()
            # Return only the date in ISO 8601 format
            return datetime_obj.isoformat()
        except Exception as e:
            self.logger.error(f"Error converting date and time: {e}")
            return None
