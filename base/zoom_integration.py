from zoomus import ZoomClient

def create_zoom_meeting(class_request):
    client = ZoomClient('API_KEY', 'API_SECRET')
    meeting = client.meeting.create(
        topic=class_request.topic,
        start_time=class_request.time.isoformat(),
        duration=60  # Duration in minutes
    )
    return meeting['join_url']
