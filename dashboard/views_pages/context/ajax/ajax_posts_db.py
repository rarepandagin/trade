
import os
import dashboard.views_pages.toolkit as tk
from dashboard.models import models_tick
import pandas as pd
from dashboard.modules.indicators.indicators import IndicatorsClass


def handle_ajax_posts_db(req, payload):

    admin_settings = tk.get_admin_settings()
    admin_settings.command_function = req
    admin_settings.command_arguments = payload
    admin_settings.save()
