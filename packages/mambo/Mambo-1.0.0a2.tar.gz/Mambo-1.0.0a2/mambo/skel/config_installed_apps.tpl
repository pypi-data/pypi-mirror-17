
# ------------------------------------------------------------------------------
#: INSTALLED_APPS

    #
    INSTALLED_APPS = [
        "mambo.contrib.error_page",

        #
        # "mambo.contrib.maintenance_page", # uncomment to activate the maintenace page


        # { # AUTH
        #     "app": "mambo.contrib.auth",
        #     "modules": {
        #         "login": {
        #             "route": "/account/",
        #         },
        #         "account": {
        #             "route": "/account/",
        #         },
        #         "admin": {
        #             "route": "/admin/users/"
        #         }
        #     },
        #     "options": {
        #         # for login and logout view
        #         "login_view": None,
        #         "logout_view": None,
        #
        #         # permission
        #         "allow_signup": True,
        #         "allow_login": True,
        #         "allow_social_login": False,
        #
        #         # Verification
        #         "verify_email": False,
        #         "verify_email_token_ttl": 60 * 24,
        #         "verify_email_template": "verify-email.txt",
        #         "verify_signup_email_template": "verify-signup-email.txt",
        #
        #         # reset password
        #         "reset_password_method": "token",  # token or password
        #         "reset_password_token_ttl": 60,  # in minutes
        #         "reset_password_email_template": "reset-password.txt",

        #         # When a user is required to change password, list endpoints
        #         # that could still be accessed without requiring password
        #         # change page
        #         "require_password_change_exclude_endpoints": []
        #
        #     }
        # },
        #


        #
        # {  # ADMIN interface
        #     "app": "mambo.contrib.admin",
        #     "decorators": ["mambo.contrib.auth.accepts_manager_roles"], # Force all user to be at least manager
        #     "options": {
        #         "brand": "Admin Zone",
        #         "theme": "yeti"
        #     }
        #
        # },


        # {  # PUBLISHER
        #     "app": "mambo.contrib.publisher",
        #     "modules": {
        #         "admin": {
        #             "route": "/admin/publisher"
        #         }
        #     }
        # },


        # {  # CONTACT_PAGE
        #     "app": "mambo.contrib.contact_page",
        #     "route": "/contact/",
        #     "nav_menu": {
        #         "title": "Contact Us",
        #         "css_class": "Hello World",
        #         "visible": True,
        #         "order": 100
        #     },
        #     "options": {
        #         "title": "Get in touch!",
        #         "return_to": "Index:index",
        #         "send_to": "",
        #         "template": "contact-us.txt",
        #         "success_message": "Thank you soooooo much for sending this message. "
        #                            "We'll contact you within the next 72 hours"
        #     }
        # }
    ]

# ------------------------------------------------------------------------------