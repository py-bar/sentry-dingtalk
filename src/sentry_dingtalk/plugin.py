# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_DingTalk
from src.sentry_dingtalk.forms import DingTalkOptionsForm

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"


class DingTalkPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingTalk.
    """
    author = 'panda'
    author_url = 'https://github.com/py-bar/sentry-dingtalk'
    version = sentry_DingTalk.VERSION
    description = 'Send error counts to DingTalk.'
    resource_links = [
        ('Source', 'https://github.com/py-bar/sentry-dingtalk'),
        ('Bug Tracker', 'https://github.com/py-bar/sentry-dingtalk/issues'),
        ('README', 'https://github.com/py-bar/sentry-dingtalk/blob/master/README.md'),
    ]

    slug = 'DingTalk'
    title = 'DingTalk'
    conf_key = slug
    conf_title = title
    project_conf_form = DingTalkOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, fail_silently=False):
        self.post_process(group, event, fail_silently=fail_silently)

    def post_process(self, group, event, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        access_token = self.get_option('access_token', group.project)

        send_url = DingTalk_API.format(token=access_token)
        title = "New alert from {}".format(event.project.name)

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": "#### {title} \n > {message} [href]({url})".format(
                    title=title,
                    message=event.message,
                    url="{0}events/{1}/".format(group.get_absolute_url(), event.id)
                )
            }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )



