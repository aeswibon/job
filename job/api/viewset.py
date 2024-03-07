import base64
import json

import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django_redis import get_redis_connection
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from job.api.serializer import JobSerializer
from job.constants import AUTH_URL, TOKEN_URL
from job.helper import generate_code_challenge, generate_code_verifier, make_token
from job.models import Job

twitter = make_token()
redis = get_redis_connection("default")


class JobViewset(viewsets.GenericViewSet):
    _code_verifier = generate_code_verifier()
    _code_challenge = generate_code_challenge(_code_verifier)

    queryset = Job.objects.filter(deleted=False).order_by("date")
    serializer_class = JobSerializer

    def __tweet(self, token):
        job = self.queryset.first()
        if not job:
            raise Exception("No job found!")

        payload = f"🌟 Exciting Opportunity Alert! 🌟\n \n🔍 Job: {job.position}\n- Company: {job.company}\n- Location: {job.location}\n- Due Date: {job.date.strftime("%d-%m-%Y") if job.date else "NA"}\n- Salary: {job.salary if job.salary else "NA"}\n- Apply here: {job.url}\n\n#JobAlert #LinkedInJobs 📈👩‍💼👨‍💻"

        res = requests.request(
            "POST",
            "https://api.twitter.com/2/tweets",
            json={"text": payload},
            headers={
                "Authorization": "Bearer {}".format(token.get("access_token")),
                "Content-Type": "application/json",
            },
        )
        if res.status_code != 201:
            raise Exception("Job not tweeted!!")
        job.deleted = True
        job.save(update_fields=["deleted"])

    @action(detail=False, methods=["post"])
    def home(self, request, *args, **kwargs):
        auth_url, state = twitter.authorization_url(
            AUTH_URL,
            code_challenge=self._code_challenge,
            code_challenge_method="S256",
        )
        redis.set("oauth_state", state)
        return HttpResponseRedirect(redirect_to=auth_url)

    @action(detail=False, methods=["get"])
    def callback(self, request, *args, **kwargs):
        code = request.GET.get("code")
        state = request.GET.get("state")
        redis.set("state", state)
        redis.set("code", code)

        token = twitter.fetch_token(
            token_url=TOKEN_URL,
            client_secret=settings.CLIENT_SECRET,
            code_verifier=self._code_verifier,
            code=code,
        )

        st_token = '"{}"'.format(token)
        j_token = json.loads(st_token)
        redis.set("token", j_token)

        self.__tweet(json.loads(j_token.replace("'", '"')))
        return Response({"message": "Job tweeted successfully!"})

    @action(detail=False, methods=["get"])
    def refresh(self, request, *args, **kwargs):
        t = redis.get("token")
        bb_t = t.decode("utf-8").replace("'", '"')
        data = json.loads(bb_t)
        encode_string = base64.b64encode(
            str.encode(f"{settings.CLIENT_ID}:{settings.CLIENT_SECRET}")
        ).decode("ascii")

        refreshed_token = twitter.refresh_token(
            token_url=TOKEN_URL,
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            refresh_token=data["refresh_token"],
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {encode_string}",
            },
        )

        st_refreshed_token = '"{}"'.format(refreshed_token)
        j_refreshed_token = json.loads(st_refreshed_token)
        redis.set("token", j_refreshed_token)

        self.__tweet(json.loads(j_refreshed_token.replace("'", '"')))
        return Response({"message": "Job tweeted successfully!"})
