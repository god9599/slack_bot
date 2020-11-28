# -*- coding: utf-8 -*-
import json
import re
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
import secretKey

import def_crawling.corona
import def_crawling.music
import def_crawling.help
import def_crawling.git_user
import def_crawling.boj
import def_crawling.weather
import def_crawling.real_time_search
import def_crawling.restaurant

app = Flask(__name__)

sc = SlackClient(secretKey.slack_token)
ERR_TEXT = "명령어가 잘못됐거나 없는 유저입니다. 도움말은 *help* 를 입력해 주세요."

# define header for urllib request
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/58.0.3029.110 Safari/537.36'
hds = {'User-Agent': user_agent}
hds_json = {'User-Agent': user_agent, 'Content-Type': 'Application/json'}


# 이벤트 핸들하는 함수

# STATUS_CODE = 200
def _event_handler(event_type, slack_event):

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        try:
            text = slack_event["event"]["text"][13:].replace(',', '').split()
            compile_text = re.compile(r'\d\d\d\d-\d\d-\d\d')


            if len(text) >= 3:
                match_text = compile_text.findall(text[2])


            if text[1] == 'music':
                keywords = def_crawling.music._crawl_music_chart(text)

            elif text[1] == 'corona':
                keywords = def_crawling.corona._crawl_corona()

            elif text[1] == 'naver':
                keywords = def_crawling.real_time_search._crawl_naver_search()

            elif text[1] == 'weather' and text[2]:
                keywords = def_crawling.weather.search_weather(text[2])

            elif text[1] == 'restaurant' and text[2]:
                keywords = def_crawling.restaurant.serach_restaurant(text[2])

            elif text[1] == 'help':
                keywords = def_crawling.help._help_desk()

            elif text[1] == 'boj':
                keywords = def_crawling.boj._get_boj(text[2], text[3])

            elif text[2] == '0':
                keywords = def_crawling.git_user._get_user_profile(text[1])

            elif text[2] == '1':
                keywords = def_crawling.git_user._get_contributions_graph(text[1])

            elif len(text) >= 3 and match_text[0] is not None:
                keywords = def_crawling.git_user._get_dd_contribution(text[1], match_text[0])

            # else:
            #     global STATUS_CODE
            #     keywords = ERR_TEXT
            #     STATUS_CODE = 400
            #
            # if STATUS_CODE != 400:
            #     STATUS_CODE = 200

        except Exception as e:
            # STATUS_CODE = 500
            keywords = ERR_TEXT
            print("오류발생", e)

        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, {"X-Slack-No-Retry": 1})


@app.route("/slack", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)
    # print(slack_event)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if secretKey.slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('localhost', port=8080, debug=True)