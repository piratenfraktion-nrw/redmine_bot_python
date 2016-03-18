from cx_Freeze import setup, Executable

setup(name = 'redmine_bot',
        version = "0.1",
        description = "",
        executables = [Executable("redmine_bot/app.py")] , )
