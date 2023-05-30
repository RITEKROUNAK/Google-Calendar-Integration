from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import json

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = ['https://www.googleapis.com/auth/calendar']
REDIRECT_URL = 'http://localhost:8000/rest/v1/calendar/redirect/'


def home(request):
    login_url = reverse('google_calendar_init')
    return redirect(login_url)


@api_view(['GET'])
def GoogleCalendarInitView(request):
    if 'credentials' in request.session:
        return redirect(REDIRECT_URL)

    try:
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_OAUTH_CLIENT_SECRET,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URL
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline'
        )
        request.session['state'] = state
        return Response({"authorization_url": authorization_url}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    error = request.GET.get('error')
    if error:
        return Response({'error': error}, status=403)

    try:
        if 'credentials' in request.session:
            session_credentials = Credentials(**request.session['credentials'])
            if session_credentials.valid:
                if session_credentials.expired and session_credentials.refresh_token:
                    session_credentials.refresh(Request())
            else:
                state = request.session['state']
                flow = Flow.from_client_secrets_file(
                    settings.GOOGLE_OAUTH_CLIENT_SECRET,
                    scopes=SCOPES,
                    state=state,
                    redirect_uri=REDIRECT_URL
                )
                authorization_response = request.get_full_path()
                flow.fetch_token(authorization_response=authorization_response)
                credentials = flow.credentials
                request.session['credentials'] = credentials_to_dict(credentials)
                session_credentials = Credentials(**request.session['credentials'])

            service = build('calendar', 'v3', credentials=session_credentials)
            calendar_list = service.calendarList().list().execute()
            calendar_id_list = [(item['id'], item['summary']) for item in calendar_list['items']]
            events_list = {}
            for x in calendar_id_list:
                events = service.events().list(calendarId=x[0], maxResults=10).execute()
                events_list[x[1]] = events['items']

            return Response(events_list, status=200)

        else:
            state = request.session['state']
            flow = Flow.from_client_secrets_file(
                settings.GOOGLE_OAUTH_CLIENT_SECRET,
                scopes=SCOPES,
                state=state,
                redirect_uri=REDIRECT_URL
            )
            authorization_response = request.get_full_path()
            flow.fetch_token(authorization_response=authorization_response)
            credentials = flow.credentials
            request.session['credentials'] = credentials_to_dict(credentials)
            session_credentials = Credentials(**request.session['credentials'])

            service = build('calendar', 'v3', credentials=session_credentials)
            calendar_list = service.calendarList().list().execute()
            calendar_id_list = [(item['id'], item['summary']) for item in calendar_list['items']]
            events_list = {}
            for x in calendar_id_list:
                events = service.events().list(calendarId=x[0], maxResults=10).execute()
                events_list[x[1]] = events['items']

            return Response(events_list, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
