import datetime
import re


def format_srt_time(timedelta_obj):
    # Format the time in HH:MM:SS,mmm format
    hours, remainder = divmod(timedelta_obj.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    # Ensure milliseconds has 3 digits
    milliseconds = f"{int(timedelta_obj.microseconds / 1000):03d}"
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds}"


def text_to_srt(text, wps=3.2):
    # Split the text into chunks
    chunks = re.split(r"\n\s*\n", text.strip())

    # Initialize the start time as 00:00:00,000
    start_time = datetime.timedelta(hours=0, minutes=0, seconds=0)

    srt_text = ""

    for i, chunk in enumerate(chunks, start=1):
        # Calculate the end time
        word_count = len(chunk.split())
        end_time = start_time + datetime.timedelta(seconds=word_count / wps)

        # Format the times in HH:MM:SS,mmm format
        start_time_str = format_srt_time(start_time)
        end_time_str = format_srt_time(end_time)

        # Create the SRT string
        srt_text += f"{i}\n"
        srt_text += f"{start_time_str} --> {end_time_str}\n"
        srt_text += chunk + "\n\n"

        # Update the start time for the next chunk
        start_time = end_time

    return srt_text


# Testing the function
text = """
This is a test.
This is only a test.

If this was a real situation, you would be directed to more information.
"""

print(text_to_srt(text))
