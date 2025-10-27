
import dashboard.views_pages.toolkit as tk


def handle_ajax_posts_db(req, payload):

    tk.update_admin_settings("command_function", req)
    tk.update_admin_settings("command_arguments", payload)

