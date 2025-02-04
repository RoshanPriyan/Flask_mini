new_project/
    |- api/
        |- __init__.py
        |- users/
            |- __init__.py
            |- models.py              # Contains models for 'users'
            |- routers.py             # Handles routing, Blueprints, and API setup
            |- utils.py               # helper methods
            |- views/                 # Contains function-based API logic
                |- __init__.py        # Optional; can be empty
                |- employee_list_api.py  # Function-based logic (e.g., employee list)
    |- sqlenv/                        # Virtual environment (excluded from version control)
    |- .env                           # Environment variables
    |- __init__.py                    # App-level init, can be removed if unused
    |- config.py                      # Database connection and settings
    |- global_utils.py                # Helper functions
    |- main.py                        # Entry point for the Flask app
    |- read_me.txt                    # Documentation
    |- requirement.txt                # library included
