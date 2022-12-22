from flask import Blueprint,render_template

errorhandlers=Blueprint('errorhandlers',__name__)

@errorhandlers.app_errorhandler(404)
def error_404(error):
    return render_template('templates_errorhandlers/404.html'),404

@errorhandlers.app_errorhandler(403)
def error_403(error):
    return render_template('templates_errorhandlers/403.html'),403

@errorhandlers.app_errorhandler(500)
def error_500(error):
    return render_template('templates_errorhandlers/500.html'),500
