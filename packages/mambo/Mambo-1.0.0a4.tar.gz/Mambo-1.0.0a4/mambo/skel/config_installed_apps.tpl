
# ------------------------------------------------------------------------------
#: INSTALLED_APPS
    #
    # Installed apps/extensions to your application
    # The order is important. If an app depends on another app to work
    # that must be placed before the calling app
    #
    INSTALLED_APPS = [
        # Error Page. Create a friendly page when an error occurs
        "mambo.contrib.error_page",

        # # Maintenance page. When uncommented, the whole site will show a maintenance page
        # # "mambo.contrib.maintenance_page",
        #
        # # AUTH: Authentication system to signup, login, manage users,
        # # give access etc
        # # Require to run `mambo syncdb` to setup the db
        # # Also, run once `mambo auth:create-super-admin email@xyz.com` to
        # # create the super admin
        # {
        #     "app": "mambo.contrib.auth",
        #     "modules": {
        #         "login": {
        #             "route": "/account/",
        #             "nav_menu": {
        #                 "title": "Signin",
        #                 "align_right": True
        #             }
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
        #         "login_view": "Index:index",
        #         "logout_view": "Index:index",
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
        #
        #         # # When a user is required to change password, list endpoints
        #         # # that could still be accessed without requiring password
        #         # # change page
        #         # "require_password_change_exclude_endpoints": []
        #     }
        # },
        #
        # # ADMIN: Creates and admin interface for the application.
        # # Use when creating admin site
        # {
        #     "app": "mambo.contrib.admin",
        #     # For additional roles in the whole admin page, uncomment below
        #     #"decorators": ["mambo.contrib.auth.accepts_manager_roles"],
        #     "options": {
        #         "brand": "The Admin",
        #         "theme": "yeti"  # Recommended: yeti, superhero, amelia
        #     }
        #
        # },
        #
        # # PUBLISHER: A pseudo CMS to add content to the site.
        # # Require to run `mambo syncdb` to setup the db
        # {
        #     "app": "mambo.contrib.publisher",
        #     "modules": {
        #         "admin": {
        #             "route": "/admin/publisher"
        #         }
        #     }
        # },
        #
        # # CONTACT PAGE: Creates a page for users to contact admin.
        # # MAIL_* config must be setup
        # {
        #     "app": "mambo.contrib.contact_page",
        #     "route": "/contact/",
        #     "nav_menu": {
        #         "title": "Contact",
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